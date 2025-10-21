#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json, re
from datetime import datetime

USERNAME = 'mix1220'
PASSWORD = '1234'

class NationalCrawler:
    def __init__(self):
        self.driver = None
        self.results = []

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

    def get_shop_detail(self, url, title):
        """대전 데이터 구조와 동일하게 크롤링"""
        try:
            self.driver.get(url)
            time.sleep(1.5)

            detail = {
                'title': title,
                'url': url,
                'description': '',
                'hours': '',
                'phone': '',
                'thumbnail': '',
                'kakao_id': '',
                'telegram_id': ''
            }

            # 페이지 전체 텍스트
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text

            # 썸네일 이미지 (GIF 제외, data/file/main만)
            try:
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, 'img[src*="data/file/main"]')
                for img in img_elements:
                    src = img.get_attribute('src')
                    if src and 'data/file/main' in src and not src.lower().endswith('.gif'):
                        detail['thumbnail'] = src
                        break

                if not detail['thumbnail']:
                    detail['thumbnail'] = 'https://dkxm8.com/img/temp_thum.jpg'
            except:
                detail['thumbnail'] = 'https://dkxm8.com/img/temp_thum.jpg'

            # 설명 (15~80자, 이모지/키워드)
            try:
                lines = page_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if 15 <= len(line) <= 80:
                        if any(k in line for k in ['❤', '✨', '⭐', '✅', '♥', '신규', '이벤트', '할인', 'NF', '한국', '실사', '100%', '20대']):
                            detail['description'] = line
                            break
            except:
                pass

            # 영업시간
            try:
                for line in lines:
                    line = line.strip()
                    if re.search(r'(AM|PM|\d{1,2}:\d{2}|\d{1,2}시|오전|오후|새벽)', line, re.IGNORECASE):
                        if 10 <= len(line) <= 60:
                            detail['hours'] = line
                            break
            except:
                pass

            # 전화번호 (010)
            try:
                phone_pattern = r'(010[-\s]?\d{4}[-\s]?\d{4})'
                phones = re.findall(phone_pattern, page_text)
                if phones:
                    # 특수문자 제거하고 첫 번째 번호 사용
                    detail['phone'] = re.sub(r'[^\d\-]', '', phones[0])
            except:
                pass

            # 카카오톡/텔레그램
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href]')
                for link in links:
                    href = link.get_attribute('href')
                    if href:
                        if 'kakao' in href.lower():
                            detail['kakao_id'] = href
                        elif 't.me' in href or 'telegram' in href.lower():
                            detail['telegram_id'] = href
            except:
                pass

            return detail

        except Exception as e:
            print(f'→ 오류: {e}')
            return None

    def run(self, input_file, start_idx=0):
        print('='*60)
        print(f'대전 형식으로 전국 크롤링 시작: {input_file}')
        print(f'시작 인덱스: {start_idx}')
        print('='*60)

        # 입력 파일 읽기 (final_all_20251011_125541.json)
        with open(input_file, 'r', encoding='utf-8') as f:
            shops = json.load(f)

        total = len(shops)
        shops_to_crawl = shops[start_idx:]

        print(f'\n총 {len(shops_to_crawl)}개 업소 크롤링 ({start_idx+1}~{total})...\n')

        self.setup()
        self.login()

        for idx, shop in enumerate(shops_to_crawl, start_idx+1):
            print(f'[{idx}/{total}] {shop["title"]}', end=' ')

            detail = self.get_shop_detail(shop['url'], shop['title'])

            if detail:
                self.results.append(detail)
                has_thumb = '✓' if detail['thumbnail'] != 'https://dkxm8.com/img/temp_thum.jpg' else '○'
                print(f'{has_thumb}')
            else:
                print('✗')

            # 10개마다 중간 저장
            if idx % 10 == 0:
                temp_file = f'national_like_daejeon_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                print(f'  → 중간 저장: {temp_file} ({len(self.results)}개)')

            time.sleep(1)

        # 최종 저장
        output = f'national_like_daejeon_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f'\n✅ 완료: {len(self.results)}개 → {output}')
        self.driver.quit()

if __name__ == '__main__':
    crawler = NationalCrawler()
    crawler.run('final_all_20251011_125541.json', start_idx=0)
