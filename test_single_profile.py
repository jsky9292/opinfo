#!/usr/bin/env python3
"""
단일 프로필 페이지 테스트 - 상세 이미지 추출 방법 확인
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_profile_page():
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 테스트할 URL (461개 데이터 중 첫 번째)
        test_url = "https://dkxm8.com/profile_popup.php?idx=648513&gubun=1"
        print(f"\n🔍 테스트 URL: {test_url}")

        driver.get(test_url)
        time.sleep(3)

        print("\n" + "="*80)
        print("1️⃣ 모든 img 태그 찾기")
        print("="*80)

        all_imgs = driver.find_elements(By.TAG_NAME, 'img')
        print(f"\n총 {len(all_imgs)}개의 img 태그 발견\n")

        for idx, img in enumerate(all_imgs, 1):
            src = img.get_attribute('src')
            alt = img.get_attribute('alt')
            width = img.get_attribute('width')
            height = img.get_attribute('height')
            parent = img.find_element(By.XPATH, '..')
            parent_class = parent.get_attribute('class')

            print(f"[{idx}]")
            print(f"  src: {src}")
            print(f"  alt: {alt}")
            print(f"  size: {width}x{height}")
            print(f"  parent class: {parent_class}")
            print()

        print("\n" + "="*80)
        print("2️⃣ data/file/main 포함 이미지만 찾기")
        print("="*80)

        main_imgs = [img for img in all_imgs if img.get_attribute('src') and 'data/file/main' in img.get_attribute('src')]
        print(f"\n총 {len(main_imgs)}개의 main 이미지 발견\n")

        for idx, img in enumerate(main_imgs, 1):
            src = img.get_attribute('src')
            print(f"[{idx}] {src}")

        print("\n" + "="*80)
        print("3️⃣ GIF 제외한 main 이미지")
        print("="*80)

        non_gif_imgs = [img for img in main_imgs if not img.get_attribute('src').lower().endswith('.gif')]
        print(f"\n총 {len(non_gif_imgs)}개의 non-GIF main 이미지 발견\n")

        for idx, img in enumerate(non_gif_imgs, 1):
            src = img.get_attribute('src')
            print(f"[{idx}] {src}")

        print("\n" + "="*80)
        print("4️⃣ 페이지 HTML 구조 확인")
        print("="*80)

        # 전체 body의 HTML 일부 출력
        body = driver.find_element(By.TAG_NAME, 'body')
        html_content = body.get_attribute('innerHTML')[:2000]  # 첫 2000자만
        print(f"\nBody HTML (첫 2000자):\n{html_content}\n")

        print("\n" + "="*80)
        print("5️⃣ CSS 셀렉터 테스트")
        print("="*80)

        selectors = [
            'img[src*="data/file/main"]',
            'img[src*="/main/"]',
            'div img[src*="data/file"]',
            '.profile img',
            '#profile img'
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"\n{selector}: {len(elements)}개")
                for idx, elem in enumerate(elements[:3], 1):  # 처음 3개만
                    print(f"  [{idx}] {elem.get_attribute('src')[:80]}...")
            except Exception as e:
                print(f"\n{selector}: 에러 - {e}")

    except Exception as e:
        print(f"\n❌ 오류: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == '__main__':
    test_profile_page()
