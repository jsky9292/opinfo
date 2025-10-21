#!/usr/bin/env python3
"""
대전 크롤러 방식을 적용한 전국 상세 정보 크롤러
- 대전 크롤러와 동일한 이미지 수집 로직 사용
- 팝업/iframe 내부까지 탐색하여 모든 상세 이미지 수집
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

class DetailCrawler:
    def __init__(self):
        self.driver = None
        self.results = []

    def setup(self):
        print('브라우저 설정...')
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument('--headless')  # 백그라운드 실행
        opts.add_argument('--window-size=1920,1080')
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        opts.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        self.driver.set_page_load_timeout(30)

        # 자동화 감지 방지
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

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

    def get_profile_details(self, profile_url):
        """프로필 팝업에서 상세 이미지 가져오기 (대전 크롤러 방식)"""
        detail_images = []
        original_window = self.driver.current_window_handle

        try:
            # 새 창에서 프로필 열기
            self.driver.execute_script(f"window.open('{profile_url}', '_blank');")
            time.sleep(2)

            # 새 창으로 전환
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            time.sleep(2)

            # iframe이 있다면 전환
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                if iframes:
                    self.driver.switch_to.frame(iframes[0])
                    time.sleep(1)
            except:
                pass

            # 모든 이미지 수집
            try:
                imgs = self.driver.find_elements(By.TAG_NAME, "img")
                for img in imgs:
                    try:
                        src = img.get_attribute('src')
                        # /data/file/ 또는 /data/editor/ 경로 이미지만
                        if src and ('/data/file/' in src or '/data/editor/' in src):
                            if not src.startswith('http'):
                                src = 'https://dkxm8.com' + src
                            if src not in detail_images:
                                detail_images.append(src)
                    except:
                        continue
            except:
                pass

            # iframe에서 빠져나오기
            try:
                self.driver.switch_to.default_content()
            except:
                pass

            # 팝업 닫고 원래 창으로 돌아가기
            self.driver.close()
            self.driver.switch_to.window(original_window)
            time.sleep(0.5)

        except Exception as e:
            print(f'   ⚠️  팝업 처리 오류: {e}')
            # 오류 발생 시 복구
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            try:
                windows = self.driver.window_handles
                if len(windows) > 1:
                    self.driver.close()
                if windows:
                    self.driver.switch_to.window(original_window)
            except:
                pass

        return detail_images

    def get_shop_detail(self, url, title, area, original_description=''):
        """각 업소의 상세 페이지에서 정보 추출"""
        try:
            self.driver.get(url)
            time.sleep(1.5)

            detail = {
                'title': title,
                'url': url,
                'area': area,
                'district': area,  # 세부 지역 (동 이름), 기본값은 큰 지역
                'thumbnail': '',
                'detail_images': [],  # 상세 이미지들
                'description': '',
                'phone': '',
                'hours': '',
                'kakao_id': '',
                'telegram_id': ''
            }

            # 원본 description에서 세부 지역 추출 (우선순위)
            if original_description:
                district_match = re.search(r'([가-힣]+동)', original_description)
                if district_match:
                    detail['district'] = district_match.group(1)

            # 🔥 대전 크롤러 방식으로 상세 이미지 수집
            detail_images = self.get_profile_details(url)

            if detail_images:
                detail['thumbnail'] = detail_images[0]
                detail['detail_images'] = detail_images
            else:
                # fallback: 기존 방식
                try:
                    img_elements = self.driver.find_elements(By.CSS_SELECTOR, '.imgWrap img[src*="data/editor"]')
                    image_urls = []

                    for img in img_elements:
                        src = img.get_attribute('src')
                        if src and src not in image_urls:
                            image_urls.append(src)

                    if image_urls:
                        detail['thumbnail'] = image_urls[0]
                        detail['detail_images'] = image_urls
                    else:
                        detail['thumbnail'] = 'https://dkxm8.com/img/temp_thum.jpg'
                except:
                    detail['thumbnail'] = 'https://dkxm8.com/img/temp_thum.jpg'

            # 페이지 전체 HTML 가져오기
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text

            # 설명/소개글 추출 및 세부 지역 추출
            try:
                lines = page_text.split('\n')
                district = None

                for line in lines:
                    line = line.strip()

                    # 세부 지역 추출 (동 이름이 있는 경우)
                    if '동' in line and not district:
                        district_match = re.search(r'([가-힣]+동)', line)
                        if district_match:
                            district = district_match.group(1)

                    # 15~80자 사이의 홍보성 문구
                    if 15 <= len(line) <= 80:
                        if any(k in line for k in ['❤', '✨', '⭐', '✅', '♥', '신규', '이벤트', '할인', 'NF', '한국', '실사']):
                            detail['description'] = line

                # 세부 지역이 있으면 업데이트
                if district:
                    detail['district'] = district
            except:
                pass

            # 영업시간 추출
            try:
                for line in lines:
                    line = line.strip()
                    if re.search(r'(AM|PM|\d{1,2}:\d{2}|\d{1,2}시)', line, re.IGNORECASE):
                        if 10 <= len(line) <= 60:
                            detail['hours'] = line
                            break
            except:
                pass

            # 전화번호 추출
            try:
                phone_pattern = r'(010[-\s]?\d{4}[-\s]?\d{4})'
                phones = re.findall(phone_pattern, page_text)
                if phones:
                    detail['phone'] = phones[0]
            except:
                pass

            # 카카오톡/텔레그램 링크
            try:
                links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href]')
                for link in links:
                    href = link.get_attribute('href')
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
        print(f'상세 정보 크롤링 시작: {input_file}')
        print(f'시작 인덱스: {start_idx}')
        print('대전 크롤러 방식 적용 - 팝업/iframe 탐색')
        print('='*60)

        # 입력 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            shops = json.load(f)

        total = len(shops)
        shops_to_crawl = shops[start_idx:]

        print(f'\n총 {len(shops_to_crawl)}개 업소 크롤링 시작 ({start_idx+1}~{total})...\n')

        self.setup()
        self.login()

        for idx, shop in enumerate(shops_to_crawl, start_idx+1):
            print(f'[{idx}/{total}] {shop["title"]} ({shop["area"]})', end=' ')

            original_desc = shop.get('description', '')

            detail = self.get_shop_detail(
                shop['url'],
                shop['title'],
                shop['area'],
                original_desc
            )

            if detail:
                self.results.append(detail)
                img_count = len(detail.get('detail_images', []))
                has_thumb = '✓' if detail['thumbnail'] != 'https://dkxm8.com/img/temp_thum.jpg' else '○'
                print(f'{has_thumb} ({img_count}장)')
            else:
                print('✗')

            # 10개마다 중간 저장
            if idx % 10 == 0:
                temp_file = f'details_daejeon_style_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                print(f'  → 중간 저장: {temp_file} ({len(self.results)}개)')

            time.sleep(1)  # 서버 부하 방지

        # 최종 저장
        output = f'details_daejeon_style_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        # 통계
        total_images = sum(len(r.get('detail_images', [])) for r in self.results)
        avg_images = total_images / len(self.results) if self.results else 0

        print(f'\n✅ 완료: {len(self.results)}개 → {output}')
        print(f'📊 통계:')
        print(f'   - 총 이미지 수: {total_images}장')
        print(f'   - 평균 이미지 수: {avg_images:.1f}장/업소')

        self.driver.quit()

if __name__ == '__main__':
    crawler = DetailCrawler()
    # 전국 461개 업소 크롤링 (처음부터)
    crawler.run('daejeon_chungcheong_all_20251009_220324.json', start_idx=0)
