from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class SeoulCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        print("로그인...")
        self.driver.get('https://dkxm8.com/theme/dkxm8_2024/login.html')
        time.sleep(2)

        id_input = self.wait.until(EC.presence_of_element_located((By.ID, 'login_id')))
        pw_input = self.driver.find_element(By.ID, 'login_pw')

        id_input.send_keys('opinfo')
        pw_input.send_keys('opinfo123')

        login_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_btn.click()
        time.sleep(3)
        print("로그인 완료")

    def scroll_down(self):
        last = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1.5)
            new = self.driver.execute_script('return document.body.scrollHeight')
            if new == last:
                break
            last = new

    def crawl_city(self, city_name):
        print(f"\n[서울/{city_name}] 크롤링 중...")

        # 서울/강남 지역의 실제 URL 구조 확인 필요
        url = f'https://dkxm8.com/theme/dkxm8_2024/region_shop.html?region=서울/강남&area={city_name}'

        self.driver.get(url)
        time.sleep(2)

        # 스크롤
        self.scroll_down()
        time.sleep(1)

        # 업체 수집
        try:
            cards = self.driver.find_elements(By.CSS_SELECTOR, '.shop_card, .card, [class*="shop"]')
            print(f"  찾은 카드 수: {len(cards)}개")

            shops = []
            for card in cards:
                try:
                    shop = {}

                    # 제목
                    title_elem = card.find_element(By.CSS_SELECTOR, 'h3, .title, [class*="title"]')
                    shop['title'] = title_elem.text.strip() if title_elem else ''

                    # 설명
                    try:
                        desc_elem = card.find_element(By.CSS_SELECTOR, '.description, p, [class*="desc"]')
                        shop['description'] = desc_elem.text.strip()
                    except:
                        shop['description'] = ''

                    # 이미지
                    try:
                        img_elem = card.find_element(By.CSS_SELECTOR, 'img')
                        shop['thumbnail'] = img_elem.get_attribute('src')
                    except:
                        shop['thumbnail'] = ''

                    shop['region'] = '서울/강남'
                    shop['area'] = city_name

                    if shop['title']:
                        shops.append(shop)

                except Exception as e:
                    continue

            print(f"  수집된 업체: {len(shops)}개")
            return shops

        except Exception as e:
            print(f"  에러: {e}")
            return []

    def crawl_seoul(self):
        seoul_areas = ['강남구', '서초구', '송파구', '강동구', '광진구',
                       '성동구', '중구', '종로구', '용산구', '마포구']

        all_shops = []

        for city in seoul_areas:
            shops = self.crawl_city(city)
            all_shops.extend(shops)
            time.sleep(1)

        return all_shops

    def save(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n저장 완료: {filename}")
        print(f"총 {len(data)}개 업체")

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    print("=" * 50)
    print("서울 지역 크롤링 시작")
    print("=" * 50)

    crawler = SeoulCrawler()

    try:
        print("브라우저 설정...")
        print("준비 완료")

        crawler.login()

        shops = crawler.crawl_seoul()

        if shops:
            filename = f'seoul_shops_{time.strftime("%Y%m%d_%H%M%S")}.json'
            crawler.save(shops, filename)
        else:
            print("\n서울 지역에 업체가 없거나 크롤링 실패")

    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        crawler.close()
