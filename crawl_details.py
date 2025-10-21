#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json
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
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print('준비 완료')

    def login(self):
        print('로그인...')
        self.driver.get('https://dkxm8.com/bbs/login.php')
        time.sleep(3)
        self.driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
        time.sleep(5)
        print('로그인 완료')

    def get_shop_detail(self, url, title, area, region):
        """각 업소의 상세 페이지에서 정보 추출"""
        try:
            self.driver.get(url)
            time.sleep(2)

            detail = {
                'title': title,
                'url': url,
                'area': area,
                'region': region,
                'images': [],
                'description': '',
                'phone': '',
                'address': '',
                'hours': '',
                'services': [],
                'price': '문의',
                'kakao_id': '',
                'telegram_id': ''
            }

            # 이미지 추출 (썸네일 + 갤러리) - GIF 배너 제외
            try:
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, 'img[src*="data/profile"], img[src*="data/file"]')
                for img in img_elements[:10]:  # 최대 10장
                    src = img.get_attribute('src')
                    if src and ('profile' in src or 'file' in src):
                        # GIF 배너 제외 (배너는 보통 gif 확장자 사용)
                        if not src.lower().endswith('.gif'):
                            detail['images'].append(src)
            except:
                pass

            # 설명/소개글 추출
            try:
                desc_selectors = [
                    'div.profile_content',
                    'div.content',
                    'div.wr_content',
                    'div[class*="intro"]',
                    'div[class*="desc"]',
                    'td[class*="content"]'
                ]
                for selector in desc_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        text = elements[0].text.strip()
                        if len(text) > 20:  # 의미있는 내용만
                            detail['description'] = text[:500]  # 최대 500자
                            break
            except:
                pass

            # 전화번호 추출
            try:
                phone_patterns = [
                    'a[href^="tel:"]',
                    'span[class*="phone"]',
                    'div[class*="phone"]',
                    'td[class*="phone"]'
                ]
                for pattern in phone_patterns:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                    if elements:
                        if pattern.startswith('a[href'):
                            phone = elements[0].get_attribute('href').replace('tel:', '')
                        else:
                            phone = elements[0].text.strip()

                        # 전화번호 형식 확인 (숫자와 하이픈만)
                        import re
                        phone_clean = re.sub(r'[^0-9-]', '', phone)
                        if len(phone_clean) >= 9:  # 최소 9자리
                            detail['phone'] = phone_clean
                            break
            except:
                pass

            # 주소 추출
            try:
                addr_selectors = [
                    'div[class*="addr"]',
                    'span[class*="addr"]',
                    'td[class*="addr"]',
                    'div[class*="location"]'
                ]
                for selector in addr_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        addr = elements[0].text.strip()
                        if '시' in addr or '구' in addr or '동' in addr:
                            detail['address'] = addr[:100]
                            break
            except:
                pass

            # 영업시간 추출
            try:
                time_selectors = [
                    'div[class*="time"]',
                    'span[class*="time"]',
                    'td[class*="time"]',
                    'div[class*="hour"]'
                ]
                for selector in time_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        hours = elements[0].text.strip()
                        if ':' in hours or '시' in hours:
                            detail['hours'] = hours[:50]
                            break
            except:
                pass

            # 카카오톡/텔레그램 ID 추출
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

            # 가격 정보 추출
            try:
                price_selectors = [
                    'span[class*="price"]',
                    'div[class*="price"]',
                    'td[class*="price"]'
                ]
                for selector in price_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        price = elements[0].text.strip()
                        if '원' in price or '만' in price or price.replace(',', '').isdigit():
                            detail['price'] = price
                            break
            except:
                pass

            # 서비스 메뉴 추출
            try:
                service_selectors = [
                    'ul[class*="service"] li',
                    'div[class*="menu"] span',
                    'div[class*="service"] span'
                ]
                for selector in service_selectors:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        services = [elem.text.strip() for elem in elements[:10] if elem.text.strip()]
                        if services:
                            detail['services'] = services
                            break
            except:
                pass

            return detail

        except Exception as e:
            print(f'  → 오류: {e}')
            return None

    def run(self, input_file):
        print('='*60)
        print(f'상세 정보 크롤링 시작: {input_file}')
        print('='*60)

        # 입력 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            shops = json.load(f)

        print(f'\n총 {len(shops)}개 업소 크롤링 시작...\n')

        self.setup()
        self.login()

        for idx, shop in enumerate(shops, 1):
            print(f'[{idx}/{len(shops)}] {shop["title"]} ({shop["area"]})', end=' ')

            detail = self.get_shop_detail(
                shop['url'],
                shop['title'],
                shop['area'],
                shop['region']
            )

            if detail:
                self.results.append(detail)
                img_count = len(detail['images'])
                print(f'✓ (이미지: {img_count}개)')
            else:
                print('✗')

            # 5개마다 저장 (중간 저장)
            if idx % 5 == 0:
                temp_file = f'details_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                print(f'  → 중간 저장: {temp_file}')

            time.sleep(1.5)  # 서버 부하 방지

        # 최종 저장
        output = f'details_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f'\n✅ 완료: {len(self.results)}개 → {output}')
        self.driver.quit()

if __name__ == '__main__':
    crawler = DetailCrawler()
    crawler.run('final_all_20251011_125541.json')
