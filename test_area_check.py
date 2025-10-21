#!/usr/bin/env python3
"""
한 지역의 실제 업소 수 확인 (대전)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = 'mix1220'
PASSWORD = '1234'

opts = Options()
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

try:
    print('로그인...')
    driver.get('https://dkxm8.com/bbs/login.php')
    time.sleep(2)
    driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
    driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
    time.sleep(3)

    print('\n대전 지역 접속...')
    driver.get('https://dkxm8.com/?area=대전')
    time.sleep(5)

    # 페이지 소스 확인
    print('\n=== 페이지 구조 분석 ===')

    # 1. 모든 가능한 셀렉터로 카드 찾기
    selectors = [
        "div.gal_top",
        "div.gal_list",
        "div[class*='gal']",
        "div.item",
        "div.shop",
        "article",
        "li.item"
    ]

    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elements) > 0:
                print(f'  ✓ {selector}: {len(elements)}개 발견')
        except:
            pass

    # 2. 페이지네이션 확인
    print('\n=== 페이지네이션 확인 ===')
    pagination_selectors = [
        "div.pagination",
        "div.paging",
        "nav.pagination",
        "ul.pagination",
        "div[class*='page']",
        "a[href*='page']"
    ]

    for selector in pagination_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elements) > 0:
                print(f'  ✓ {selector}: {len(elements)}개 발견')
                for elem in elements[:3]:
                    print(f'     텍스트: {elem.text[:100]}')
        except:
            pass

    # 3. 스크롤 테스트 (무한 스크롤 확인)
    print('\n=== 스크롤 테스트 ===')
    initial_count = len(driver.find_elements(By.CSS_SELECTOR, "div.gal_top"))
    print(f'  초기 카드 수: {initial_count}개')

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    after_scroll_count = len(driver.find_elements(By.CSS_SELECTOR, "div.gal_top"))
    print(f'  스크롤 후 카드 수: {after_scroll_count}개')

    if after_scroll_count > initial_count:
        print('  → 무한 스크롤 감지!')
    else:
        print('  → 무한 스크롤 없음')

    # 4. 첫 번째 카드의 HTML 구조 출력
    print('\n=== 첫 번째 카드 HTML ===')
    cards = driver.find_elements(By.CSS_SELECTOR, "div.gal_top")
    if cards:
        print(cards[0].get_attribute('outerHTML')[:500])

    input('\n엔터를 누르면 종료합니다...')

finally:
    driver.quit()
