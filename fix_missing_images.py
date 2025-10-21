#!/usr/bin/env python3
"""
기본 이미지를 사용하는 업소와 구인 광고 이미지를 썸네일로 사용하는 업소의 이미지를 수정하는 스크립트
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json, re
from datetime import datetime

USERNAME = 'mix1220'
PASSWORD = '1234'

class ImageFixer:
    def __init__(self):
        self.driver = None

    def setup(self):
        print('브라우저 설정...')
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print('준비 완료')

    def login(self):
        print('로그인...')
        self.driver.get('https://dkxm8.com/bbs/login.php')
        time.sleep(2)
        self.driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
        time.sleep(3)
        print('로그인 완료')

    def is_recruitment_image(self, img_url, img_element=None):
        """구인 광고 이미지인지 판별"""
        # 1. 파일명 기반 판별
        recruitment_keywords = ['구인', '채용', '모집', 'recruit', 'hiring']
        url_lower = img_url.lower()

        for keyword in recruitment_keywords:
            if keyword in url_lower:
                return True

        # 2. 이미지 크기 기반 판별 (구인 광고는 보통 세로로 긴 이미지)
        if img_element:
            try:
                width = img_element.size['width']
                height = img_element.size['height']

                # 세로가 가로보다 1.5배 이상 긴 경우 (포스터 형태)
                if height > width * 1.5:
                    return True

                # 너무 큰 이미지 (1000px 초과)도 구인 광고일 가능성
                if height > 1000 or width > 1000:
                    return True
            except:
                pass

        # 3. 파일명 패턴 분석 (숫자만 있거나 특정 패턴)
        # 예: _1797.png (마지막 4자리가 숫자)
        filename_pattern = re.search(r'_(\d{4})\.(png|jpg|gif)$', url_lower)
        if filename_pattern:
            # 1700-1800 범위는 구인 광고일 가능성 (타임스탬프)
            number = int(filename_pattern.group(1))
            if 1700 <= number <= 1900:
                return True

        return False

    def get_best_thumbnail(self, url):
        """업소의 가장 적합한 썸네일 이미지 선택"""
        try:
            self.driver.get(url)
            time.sleep(1.5)

            # 모든 이미지 수집 (element와 함께)
            img_elements = self.driver.find_elements(By.CSS_SELECTOR, '.imgWrap img[src*="data/editor"]')
            images_data = []

            for img in img_elements:
                src = img.get_attribute('src')
                if src:
                    # 중복 제거
                    if not any(d['url'] == src for d in images_data):
                        images_data.append({
                            'url': src,
                            'element': img
                        })

            if not images_data:
                return None

            all_image_urls = [img['url'] for img in images_data]

            # 구인 광고가 아닌 이미지 찾기
            good_images = []
            for img_data in images_data:
                is_recruit = self.is_recruitment_image(img_data['url'], img_data['element'])
                if not is_recruit:
                    good_images.append(img_data['url'])

            # 좋은 이미지가 있으면 첫 번째 사용
            if good_images:
                return good_images[0], all_image_urls

            # 모두 구인 광고면 중간 이미지 사용 (실제 업소 사진일 가능성)
            middle_idx = len(all_image_urls) // 2
            return all_image_urls[middle_idx], all_image_urls

        except Exception as e:
            print(f'  오류: {e}')
            return None

    def run(self, input_file):
        print('='*60)
        print(f'이미지 수정 시작: {input_file}')
        print('='*60)

        # 데이터 로드
        with open(input_file, 'r', encoding='utf-8') as f:
            shops = json.load(f)

        # 수정이 필요한 업소 찾기
        needs_fix = []
        for shop in shops:
            # 1. 기본 이미지 사용
            if 'temp_thum.jpg' in shop.get('image', ''):
                # URL에 idx가 있는 경우만
                if 'idx=' in shop.get('url', '') and '&gubun=' in shop.get('url', ''):
                    url = shop.get('url', '')
                    idx = re.search(r'idx=(\d+)', url)
                    if idx and idx.group(1):  # idx 값이 비어있지 않은 경우
                        needs_fix.append(shop)
            # 2. 구인 광고 이미지 사용 (파일명에 구인 관련 키워드)
            elif self.is_recruitment_image(shop.get('image', '')):
                needs_fix.append(shop)

        print(f'\n수정 필요: {len(needs_fix)}개 / 전체: {len(shops)}개\n')

        if not needs_fix:
            print('수정할 업소가 없습니다.')
            return

        self.setup()
        self.login()

        fixed_count = 0
        for idx, shop in enumerate(needs_fix, 1):
            print(f'[{idx}/{len(needs_fix)}] {shop["name"]}...', end=' ')

            result = self.get_best_thumbnail(shop['url'])
            if result:
                new_thumbnail, all_images = result

                # 원본 데이터에서 해당 업소 찾아서 업데이트
                for original_shop in shops:
                    if original_shop['name'] == shop['name'] and original_shop['url'] == shop['url']:
                        old_image = original_shop.get('image', '')
                        original_shop['image'] = new_thumbnail
                        original_shop['gallery'] = all_images

                        if old_image != new_thumbnail:
                            print(f'✓ 수정됨')
                            fixed_count += 1
                        else:
                            print(f'○ 동일')
                        break
            else:
                print('✗ 실패')

            time.sleep(1)

        # 저장
        output_file = f'shops_data_fixed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(shops, f, ensure_ascii=False, indent=2)

        print(f'\n✅ 완료: {fixed_count}개 수정 → {output_file}')
        self.driver.quit()

if __name__ == '__main__':
    fixer = ImageFixer()
    fixer.run('shops_data_react_20251014_120943.json')
