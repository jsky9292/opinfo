#!/usr/bin/env python3
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
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

try:
    print('로그인...')
    driver.get('https://dkxm8.com/bbs/login.php')
    time.sleep(3)
    driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
    driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
    time.sleep(5)
    print('로그인 완료')

    # 여러 URL 패턴 테스트
    test_urls = [
        'https://dkxm8.com/?area=강남구',
        'https://dkxm8.com/?area=강남',
        'https://dkxm8.com/theme/dkxm8_2024/region_shop.html?region=서울/강남&area=강남구',
        'https://dkxm8.com/theme/dkxm8_2024/region_shop.html?area=강남구',
    ]

    for url in test_urls:
        print(f'\n테스트 URL: {url}')
        driver.get(url)
        time.sleep(3)

        # 스크롤
        last = driver.execute_script('return document.body.scrollHeight')
        for _ in range(10):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            new = driver.execute_script('return document.body.scrollHeight')
            if new == last: break
            last = new

        # 여러 CSS 선택자 시도
        selectors = [
            'div.gal_top',
            'div[class*=gal]',
            '.shop_card',
            '.item',
            'div.list-item',
            'div[class*=shop]',
            'div[class*=item]',
        ]

        for selector in selectors:
            cards = driver.find_elements(By.CSS_SELECTOR, selector)
            if cards:
                print(f'  ✓ {selector}: {len(cards)}개 발견')
                # 첫 번째 카드 내용 샘플 출력
                if len(cards) > 0:
                    print(f'    샘플: {cards[0].text[:100]}...')
                break
        else:
            print(f'  ✗ 카드를 찾을 수 없음')
            # body 텍스트 일부 출력
            body = driver.find_element(By.TAG_NAME, 'body')
            print(f'    Body 샘플: {body.text[:200]}...')

except Exception as e:
    print(f'에러: {e}')
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
