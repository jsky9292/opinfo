#!/usr/bin/env python3
"""
수정된 크롤러 테스트 - 단일 업소
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

USERNAME = 'mix1220'
PASSWORD = '1234'

def test_single_shop():
    # Chrome 설정
    opts = Options()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    try:
        # 로그인
        print('로그인 중...')
        driver.get('https://dkxm8.com/bbs/login.php')
        time.sleep(2)
        driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
        driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
        time.sleep(3)

        # 테스트 URL
        test_url = "https://dkxm8.com/profile_popup.php?idx=648513&gubun=1"
        print(f'\n테스트 URL: {test_url}\n')

        driver.get(test_url)
        time.sleep(2)

        # 수정된 셀렉터로 이미지 추출
        print('='*60)
        print('수정된 셀렉터 테스트: .imgWrap img[src*="data/editor"]')
        print('='*60)

        img_elements = driver.find_elements(By.CSS_SELECTOR, '.imgWrap img[src*="data/editor"]')
        image_urls = []

        for img in img_elements:
            src = img.get_attribute('src')
            if src and src not in image_urls:
                image_urls.append(src)

        print(f'\n✅ 발견된 이미지: {len(image_urls)}개\n')

        for idx, url in enumerate(image_urls, 1):
            print(f'[{idx}] {url}')

        if image_urls:
            print(f'\n✅ 성공! 썸네일: {image_urls[0]}')
            print(f'✅ 상세 이미지 {len(image_urls)}개 수집됨')
        else:
            print('\n❌ 실패! 이미지를 찾을 수 없습니다.')

    except Exception as e:
        print(f'\n❌ 오류: {e}')
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == '__main__':
    test_single_shop()
