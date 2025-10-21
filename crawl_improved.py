#!/usr/bin/env python3
"""
dkxm8.com 개선된 크롤러 - 모든 업체 수집
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

# 테스트할 지역들 (대전만 우선 테스트)
TEST_AREAS = ["대전"]

class ImprovedCrawler:
    def __init__(self, headless=False):
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

    def scroll_to_load_all(self):
        """페이지 스크롤해서 모든 컨텐츠 로드"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(5):  # 최대 5번 스크롤
            # 페이지 끝까지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # 새 높이 확인
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def find_all_shop_cards(self):
        """모든 업체 카드 찾기 - 다양한 셀렉터 시도"""
        all_cards = []

        # 시도할 셀렉터 리스트
        selectors = [
            "div.gal_top",           # 추천 업체
            "div.gal_list",          # 일반 업체 리스트
            "div[class*='gal']",     # gal로 시작하는 모든 div
            "div.shop-card",         # 업체 카드
            "div.shop-item",         # 업체 아이템
            "article",               # article 태그
            "div[onclick*='profile']", # 프로필 클릭 이벤트 있는 div
        ]

        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"   ✓ '{selector}' 발견: {len(elements)}개")
                    all_cards.extend(elements)
            except Exception as e:
                continue

        # 중복 제거 (같은 요소가 여러 셀렉터에 걸릴 수 있음)
        unique_cards = list(set(all_cards))
        return unique_cards

    def extract_shop_info(self, card):
        """카드에서 업체 정보 추출"""
        info = {}

        try:
            # 업체명 추출 - 여러 방법 시도
            title = ""
            try:
                h4 = card.find_element(By.TAG_NAME, "h4")
                title = h4.text.strip()
            except:
                try:
                    h3 = card.find_element(By.TAG_NAME, "h3")
                    title = h3.text.strip()
                except:
                    try:
                        title_elem = card.find_element(By.CSS_SELECTOR, ".shop-title, .title, .name")
                        title = title_elem.text.strip()
                    except:
                        pass

            if not title:
                return None

            info['title'] = title

            # 프로필 URL
            try:
                profile_link = card.find_element(By.CSS_SELECTOR, "a[href*='profile']")
                info['profile_url'] = profile_link.get_attribute('href')
            except:
                info['profile_url'] = ""

            # 설명
            try:
                desc_elem = card.find_element(By.CSS_SELECTOR, ".galInfo strong, .description, .desc")
                info['description'] = desc_elem.text.strip()
            except:
                info['description'] = ""

            # 영업시간
            try:
                hours_elem = card.find_element(By.XPATH, ".//p[contains(., '영업시간')]//span | .//span[contains(@class, 'hours')]")
                info['hours'] = hours_elem.text.strip()
            except:
                info['hours'] = ""

            # 이미지
            try:
                img = card.find_element(By.TAG_NAME, "img")
                info['image'] = img.get_attribute('src')
            except:
                info['image'] = ""

            # 카카오톡 ID
            try:
                kakao_elem = card.find_element(By.XPATH, ".//a[contains(@href, 'kakao') or contains(., '카톡')]")
                info['kakao_id'] = kakao_elem.text.strip()
            except:
                info['kakao_id'] = ""

            # 텔레그램 ID
            try:
                tg_elem = card.find_element(By.XPATH, ".//a[contains(@href, 'telegram') or contains(., '텔레')]")
                info['telegram_id'] = tg_elem.text.strip()
            except:
                info['telegram_id'] = ""

            return info

        except Exception as e:
            print(f"      ⚠️ 정보 추출 오류: {e}")
            return None

    def crawl_area(self, area_name):
        """특정 지역 크롤링"""
        print(f"\n📍 {area_name} 크롤링 시작...")

        items = []

        try:
            url = f"https://dkxm8.com/?area={area_name}"
            self.driver.get(url)
            print(f"   ✓ 페이지 로드: {url}")
            time.sleep(3)

            # 페이지 전체 스크롤
            print(f"   ⏬ 페이지 스크롤 중...")
            self.scroll_to_load_all()

            # 모든 업체 카드 찾기
            print(f"   🔍 업체 카드 검색 중...")
            cards = self.find_all_shop_cards()

            if not cards:
                print(f"   ⚠️ 업체를 찾을 수 없습니다")
                return items

            print(f"   ✓ 총 {len(cards)}개 카드 발견")

            # 각 카드에서 정보 추출
            print(f"   📝 정보 추출 중...")
            for idx, card in enumerate(cards, 1):
                info = self.extract_shop_info(card)
                if info and info.get('title'):
                    info['area'] = area_name
                    info['crawled_at'] = datetime.now().isoformat()
                    items.append(info)
                    print(f"      [{idx}/{len(cards)}] ✓ {info['title']}")

            print(f"   ✅ {area_name}: {len(items)}개 업체 수집 완료")

        except Exception as e:
            print(f"   ❌ 크롤링 오류: {e}")

        return items

    def run(self):
        """크롤러 실행"""
        try:
            self.setup_driver()

            if not self.login():
                return

            print("\n" + "="*70)
            print("🚀 개선된 크롤러 시작 (테스트 모드)")
            print("="*70)

            all_results = []

            for area in TEST_AREAS:
                items = self.crawl_area(area)
                all_results.extend(items)
                time.sleep(2)

            # 결과 저장
            if all_results:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"improved_crawl_{timestamp}.json"

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(all_results, f, ensure_ascii=False, indent=2)

                print("\n" + "="*70)
                print(f"✅ 크롤링 완료! 총 {len(all_results)}개 업체 수집")
                print(f"💾 파일 저장: {filename}")
                print("="*70)
            else:
                print("\n⚠️ 수집된 데이터가 없습니다")

        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")

        finally:
            if self.driver:
                print("\n🔚 브라우저 종료")
                self.driver.quit()

if __name__ == "__main__":
    print("ℹ️  개선된 크롤러 - 대전 지역 테스트")
    crawler = ImprovedCrawler(headless=False)  # 헤드리스 모드 OFF
    crawler.run()
