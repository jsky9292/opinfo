from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 간단한 테스트 - 서울/강남 지역에 실제 데이터가 있는지 확인
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

try:
    print("로그인...")
    driver.get('https://dkxm8.com/theme/dkxm8_2024/login.html')
    time.sleep(2)

    id_input = wait.until(EC.presence_of_element_located((By.ID, 'login_id')))
    pw_input = driver.find_element(By.ID, 'login_pw')

    id_input.send_keys('opinfo')
    pw_input.send_keys('opinfo123')

    login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_btn.click()
    time.sleep(3)
    print("로그인 완료")

    # 서울 강남구 테스트
    print("\n서울 강남구 페이지 접속 중...")
    driver.get('https://dkxm8.com/theme/dkxm8_2024/region_shop.html?region=서울/강남&area=강남구')
    time.sleep(3)

    # 페이지 소스 확인
    page_source = driver.page_source

    # 업체 카드 찾기
    cards = driver.find_elements(By.CSS_SELECTOR, '.shop_card, .card, [class*="shop"], [class*="item"]')
    print(f"찾은 요소 수: {len(cards)}개")

    # 텍스트 내용 확인
    if "업체가 없습니다" in page_source or "검색 결과가 없습니다" in page_source:
        print("→ 서울/강남구에 등록된 업체가 없습니다.")
    elif len(cards) == 0:
        print("→ 카드 요소를 찾을 수 없습니다. CSS 선택자를 다시 확인해야 합니다.")
        # body 내용 일부 출력
        body = driver.find_element(By.TAG_NAME, 'body')
        print(f"\nBody 텍스트 샘플 (처음 500자):\n{body.text[:500]}")
    else:
        print(f"→ {len(cards)}개의 카드 요소를 찾았습니다!")
        for i, card in enumerate(cards[:3]):
            print(f"카드 {i+1}: {card.text[:100]}")

except Exception as e:
    print(f"에러: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
