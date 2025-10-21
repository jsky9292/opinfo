#!/usr/bin/env python3
"""
사이트에서 실제 지역 목록을 추출
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json

USERNAME = 'mix1220'
PASSWORD = '1234'

class AreaDiscovery:
    def __init__(self):
        self.driver = None

    def setup(self):
        print('브라우저 설정...')
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-blink-features=AutomationControlled')
        # opts.add_argument('--headless')  # 일단 헤드리스 모드 해제
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

    def discover_areas(self):
        """메인 페이지에서 지역 목록 추출"""
        print('\n사이트 메인 페이지 접속...')
        self.driver.get('https://dkxm8.com/')
        time.sleep(3)

        print('\n페이지 HTML 구조 확인 중...')

        # 여러 가능한 셀렉터 시도
        selectors = [
            "select[name='area']",
            "select#area",
            "select.area",
            "ul.area-list",
            "div.area-menu",
            ".area-select",
            "a[href*='?area=']"
        ]

        areas = []

        for selector in selectors:
            try:
                print(f'\n시도 중: {selector}')
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                if elements:
                    print(f'  → 발견: {len(elements)}개 요소')

                    # select 박스인 경우
                    if 'select' in selector:
                        for elem in elements:
                            options = elem.find_elements(By.TAG_NAME, 'option')
                            for opt in options:
                                value = opt.get_attribute('value')
                                text = opt.text.strip()
                                if value and value != '':
                                    areas.append({'value': value, 'text': text})
                                    print(f'    - {value}: {text}')

                    # 링크인 경우
                    elif 'href' in selector:
                        for elem in elements[:20]:  # 처음 20개만
                            href = elem.get_attribute('href')
                            if href and '?area=' in href:
                                area = href.split('?area=')[-1].split('&')[0]
                                text = elem.text.strip()
                                areas.append({'value': area, 'text': text})
                                print(f'    - {area}: {text}')

                    if areas:
                        print(f'\n✓ 총 {len(areas)}개 지역 발견!')
                        break

            except Exception as e:
                print(f'  → 실패: {e}')
                continue

        if not areas:
            print('\n셀렉터로 찾지 못함. 페이지 소스에서 수동 검색 중...')
            page_source = self.driver.page_source

            # area= 패턴 찾기
            import re
            matches = re.findall(r'\?area=([^&"\s]+)', page_source)
            unique_areas = list(set(matches))

            print(f'\n페이지 소스에서 발견된 지역: {len(unique_areas)}개')
            for area in unique_areas[:50]:  # 처음 50개만 출력
                print(f'  - {area}')
                areas.append({'value': area, 'text': area})

        # 저장
        if areas:
            output = 'discovered_areas.json'
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(areas, f, ensure_ascii=False, indent=2)
            print(f'\n💾 저장: {output}')

        return areas

    def run(self):
        print('='*60)
        print('사이트에서 지역 목록 추출')
        print('='*60)

        self.setup()
        self.login()
        areas = self.discover_areas()

        print(f'\n{'='*60}')
        print(f'완료: {len(areas)}개 지역 발견')
        print(f'{'='*60}')

        input('\n계속하려면 Enter를 누르세요...')
        self.driver.quit()

if __name__ == '__main__':
    discovery = AreaDiscovery()
    discovery.run()
