#!/usr/bin/env python3
"""
dkxm8.com 전체 업체 완전 크롤링 - 모든 페이지 수집
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime

# 로그인 정보
USERNAME = "mix1220"
PASSWORD = "1234"

# 테스트용 - 대전만 크롤링
TEST_CITY = "대전"

class CompleteCrawler:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.results = []

    def setup_driver(self):
        """Chrome 드라이버 설정"""
        print("🔧 브라우저 드라이버 설정 중...")

        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless=new')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

        print("✅ 브라우저 준비 완료\n")

    def login(self):
        """로그인"""
        try:
            print("🔑 로그인 중...")
            self.driver.get("https://dkxm8.com/bbs/login.php")
            time.sleep(3)

            username_field = self.driver.find_element(By.NAME, "mb_id")
            password_field = self.driver.find_element(By.NAME, "mb_password")

            username_field.clear()
            username_field.send_keys(USERNAME)

            password_field.clear()
            password_field.send_keys(PASSWORD)

            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_btn.click()

            time.sleep(5)

            if 'login.php' in self.driver.current_url:
                print("❌ 로그인 실패")
                return False

            print("✅ 로그인 성공!\n")
            return True

        except Exception as e:
            print(f"❌ 로그인 오류: {e}")
            return False

    def get_total_pages(self):
        """전체 페이지 수 확인"""
        try:
            # 페이지네이션 요소 찾기
            pagination_selectors = [
                "div.pg_wrap",
                "div.pagination",
                "div[class*='paging']",
                "div[class*='page']",
            ]

            for selector in pagination_selectors:
                try:
                    pagination = self.driver.find_element(By.CSS_SELECTOR, selector)
                    # 페이지 번호 링크 찾기
                    page_links = pagination.find_elements(By.TAG_NAME, "a")

                    max_page = 1
                    for link in page_links:
                        try:
                            page_num = int(link.text.strip())
                            max_page = max(max_page, page_num)
                        except:
                            continue

                    if max_page > 1:
                        return max_page
                except:
                    continue

            # 페이지네이션을 찾지 못하면 1페이지로 간주
            return 1

        except Exception as e:
            print(f"   ⚠️ 페이지 수 확인 오류: {e}")
            return 1

    def extract_shop_data(self, card):
        """업체 카드에서 데이터 추출"""
        try:
            data = {}

            # 제목
            try:
                h4 = card.find_element(By.TAG_NAME, "h4")
                data['title'] = h4.text.strip()
            except:
                return None

            # URL
            try:
                link = card.find_element(By.CSS_SELECTOR, "a[href*='profile']")
                data['url'] = link.get_attribute('href')
            except:
                data['url'] = ""

            # 설명
            try:
                desc = card.find_element(By.CSS_SELECTOR, ".galInfo strong, .description")
                data['description'] = desc.text.strip()
            except:
                data['description'] = ""

            # 영업시간
            try:
                hours = card.find_element(By.XPATH, ".//p[contains(., '영업시간')]//span | .//span[contains(@class, 'hours')]")
                data['hours'] = hours.text.strip()
            except:
                data['hours'] = ""

            # 전화번호
            try:
                phone = card.find_element(By.XPATH, ".//a[contains(@href, 'tel:')] | .//p[contains(., '전화')]//span")
                data['phone'] = phone.text.strip().replace('tel:', '')
            except:
                data['phone'] = ""

            # 썸네일 이미지
            try:
                img = card.find_element(By.TAG_NAME, "img")
                data['thumbnail'] = img.get_attribute('src')
            except:
                data['thumbnail'] = ""

            # 카카오톡 ID
            try:
                kakao = card.find_element(By.XPATH, ".//a[contains(@href, 'kakao') or contains(., '카톡')]")
                data['kakao_id'] = kakao.text.strip()
            except:
                data['kakao_id'] = ""

            # 텔레그램 ID
            try:
                telegram = card.find_element(By.XPATH, ".//a[contains(@href, 't.me') or contains(., '텔레')]")
                data['telegram_id'] = telegram.text.strip()
            except:
                data['telegram_id'] = ""

            return data

        except Exception as e:
            return None

    def crawl_page(self, url, page_num=1):
        """특정 페이지 크롤링"""
        print(f"      페이지 {page_num} 크롤링 중...", end=" ")

        items = []

        try:
            self.driver.get(url)
            time.sleep(3)

            # 페이지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # 업체 카드 찾기
            cards = []
            selectors = ["div.gal_top", "div.gal_list", "div[class*='gal']"]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for elem in elements:
                            if elem not in cards:
                                cards.append(elem)
                except:
                    pass

            if not cards:
                print("⚠️ 업체 없음")
                return items

            # 각 카드 처리
            for card in cards:
                data = self.extract_shop_data(card)
                if data and data.get('title'):
                    items.append(data)

            print(f"✓ {len(items)}개")

        except Exception as e:
            print(f"❌ 오류: {e}")

        return items

    def crawl_city(self, city_name):
        """특정 도시 전체 크롤링"""
        print(f"\n{'='*70}")
        print(f"📍 {city_name} 크롤링 시작")
        print(f"{'='*70}")

        all_items = []

        try:
            # 첫 페이지 접속
            base_url = f"https://dkxm8.com/?area={city_name}"
            self.driver.get(base_url)
            time.sleep(3)

            # 전체 페이지 수 확인
            total_pages = self.get_total_pages()
            print(f"   ✓ 전체 페이지 수: {total_pages}\n")

            # 각 페이지 크롤링
            for page in range(1, total_pages + 1):
                if page == 1:
                    page_url = base_url
                else:
                    page_url = f"{base_url}&page={page}"

                items = self.crawl_page(page_url, page)
                all_items.extend(items)

                # 페이지 간 딜레이
                if page < total_pages:
                    time.sleep(2)

            print(f"\n   ✅ {city_name}: 총 {len(all_items)}개 업체 수집 완료")

        except Exception as e:
            print(f"   ❌ 크롤링 오류: {e}")

        return all_items

    def run(self):
        """크롤러 실행"""
        try:
            self.setup_driver()

            if not self.login():
                return

            print("\n" + "="*70)
            print("🚀 완전 크롤러 시작 (대전 테스트)")
            print("="*70)

            # 대전 크롤링
            items = self.crawl_city(TEST_CITY)

            # 결과 저장
            if items:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"complete_crawl_{TEST_CITY}_{timestamp}.json"

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(items, f, ensure_ascii=False, indent=2)

                print("\n" + "="*70)
                print(f"✅ 크롤링 완료! 총 {len(items)}개 업체 수집")
                print(f"💾 파일 저장: {filename}")
                print("="*70)
            else:
                print("\n⚠️ 수집된 데이터가 없습니다")

        except KeyboardInterrupt:
            print("\n⚠️ 사용자가 중단했습니다")
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()

        finally:
            if self.driver:
                print("\n🔚 브라우저 종료")
                self.driver.quit()

if __name__ == "__main__":
    print("ℹ️  완전 크롤러 - 대전 전체 업체 수집")
    print("ℹ️  헤드리스 모드로 실행\n")

    crawler = CompleteCrawler(headless=True)
    crawler.run()
