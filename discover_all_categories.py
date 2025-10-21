#!/usr/bin/env python3
"""
사이트에서 모든 지역 카테고리 추출 (서울, 경기, 부산 등)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json, re
from urllib.parse import unquote

USERNAME = 'mix1220'
PASSWORD = '1234'

class CategoryDiscovery:
    def __init__(self):
        self.driver = None

    def setup(self):
        print('브라우저 설정...')
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument('--window-size=1920,1080')
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
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

    def discover_all_areas(self):
        """페이지 소스에서 모든 ?area= 링크 추출"""
        print('\n메인 페이지 접속...')
        self.driver.get('https://dkxm8.com/')
        time.sleep(3)

        print('페이지 소스 분석 중...\n')
        page_source = self.driver.page_source

        # area= 패턴 찾기
        matches = re.findall(r'\?area=([^&"\s\'<>]+)', page_source)

        # URL 디코딩
        decoded = []
        for match in matches:
            try:
                decoded_area = unquote(match)
                if decoded_area and decoded_area not in decoded:
                    decoded.append(decoded_area)
                    print(f'  {len(decoded)}. {decoded_area}')
            except:
                pass

        print(f'\n✓ 총 {len(decoded)}개 지역 발견')

        # 저장
        output = 'all_areas.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(decoded, f, ensure_ascii=False, indent=2)
        print(f'💾 저장: {output}')

        return decoded

    def run(self):
        print('='*60)
        print('사이트에서 모든 지역 카테고리 추출')
        print('='*60)

        self.setup()
        self.login()
        areas = self.discover_all_areas()

        print(f'\n{'='*60}')
        print(f'완료: {len(areas)}개 지역')
        print(f'{'='*60}')

        self.driver.quit()

if __name__ == '__main__':
    discovery = CategoryDiscovery()
    discovery.run()
