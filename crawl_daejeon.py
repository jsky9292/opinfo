#!/usr/bin/env python3
"""
dkxm8.com 대전/충청 지역 크롤러
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime

# 로그인 정보
USERNAME = "mix1220"
PASSWORD = "1234"

# 대전/충청 세부 지역 리스트
DAEJEON_CITIES = [
    "대전", "천안", "청주", "세종", "서산", "당진", "보령", "진천",
    "아산", "충주", "제천", "홍성", "논산", "오창", "음성", "옥천",
    "공주", "증평", "계룡", "부여", "태안", "예산", "오송"
]

class DaejeonCrawler:
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
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)

            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            print("✅ 브라우저 준비 완료")
            return True

        except Exception as e:
            print(f"❌ 드라이버 설정 실패: {e}")
            return False

    def login(self):
        """로그인 수행"""
        print("\n🔑 로그인 중...")

        try:
            self.driver.get("https://dkxm8.com/bbs/login.php")
            time.sleep(3)

            username_field = self.driver.find_element(By.NAME, "mb_id")
            username_field.clear()
            username_field.send_keys(USERNAME)

            password_field = self.driver.find_element(By.NAME, "mb_password")
            password_field.clear()
            password_field.send_keys(PASSWORD)

            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_btn.click()

            time.sleep(5)

            if 'login.php' in self.driver.current_url:
                print("❌ 로그인 실패")
                return False

            print("✅ 로그인 성공!")
            return True

        except Exception as e:
            print(f"❌ 로그인 오류: {e}")
            return False

    def crawl_area(self, area_name):
        """특정 지역 크롤링"""
        print(f"\n📄 {area_name} 크롤링 중...")

        items = []

        try:
            # URL 인코딩 없이 직접 이동
            url = f"https://dkxm8.com/?area={area_name}"
            self.driver.get(url)
            time.sleep(4)

            # 업체 카드 찾기
            cards = []
            selectors = ["div.gal_top", "div.gal_list", "div[class*='gal']"]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        cards = elements
                        print(f"   ✓ {len(cards)}개 업체 발견")
                        break
                except:
                    continue

            if not cards:
                print(f"   ⚠️  업체를 찾을 수 없습니다")
                return items

            # 각 카드에서 정보 추출
            for idx, card in enumerate(cards, 1):
                try:
                    # 업체명
                    title = ""
                    try:
                        h4 = card.find_element(By.TAG_NAME, "h4")
                        title = h4.text.strip()
                    except:
                        pass

                    # 프로필 URL
                    url = ""
                    try:
                        profile_link = card.find_element(By.CSS_SELECTOR, "a[href*='profile_popup']")
                        url = profile_link.get_attribute('href')
                    except:
                        pass

                    # 설명
                    description = ""
                    try:
                        strong = card.find_element(By.CSS_SELECTOR, ".galInfo strong")
                        description = strong.text.strip()
                    except:
                        pass

                    # 영업시간
                    hours = ""
                    try:
                        hour_elem = card.find_element(By.XPATH, ".//p[b[text()='영업시간']]/span")
                        hours = hour_elem.text.strip()
                    except:
                        pass

                    # 전화번호
                    phone = ""
                    try:
                        phone_elem = card.find_element(By.XPATH, ".//p[b[text()='전화번호']]/span")
                        phone = phone_elem.text.strip()
                    except:
                        pass

                    # 카톡 ID
                    kakao_id = ""
                    try:
                        kakao_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'카톡')]]/span")
                        kakao_id = kakao_elem.text.strip()
                    except:
                        pass

                    # 텔레그램 ID
                    telegram_id = ""
                    try:
                        telegram_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'텔레')]]/span")
                        telegram_id = telegram_elem.text.strip()
                    except:
                        pass

                    # 썸네일 이미지
                    image_url = ""
                    try:
                        img = card.find_element(By.CSS_SELECTOR, ".imgwrap img")
                        image_url = img.get_attribute('src')
                        if image_url and not image_url.startswith('http'):
                            image_url = 'https://dkxm8.com' + image_url
                    except:
                        pass

                    # 상세 이미지 수집
                    detail_images = []
                    if url and idx <= 10:  # 처음 10개만 상세 이미지 수집
                        detail_images = self.get_profile_details(url)

                    if title or url:
                        item = {
                            'number': idx,
                            'title': title,
                            'url': url,
                            'description': description,
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': image_url,
                            'detail_images': detail_images,
                            'area': area_name,
                            'location': '대전',
                            'district': area_name
                        }
                        items.append(item)

                        if idx <= 5:
                            print(f"   {idx}. {title[:30]}")

                except Exception as e:
                    continue

            print(f"   ✓ 총 {len(items)}개 수집 완료")
            return items

        except Exception as e:
            print(f"   ❌ 크롤링 실패: {e}")
            return items

    def get_profile_details(self, profile_url):
        """프로필 팝업에서 상세 이미지 가져오기"""
        detail_images = []
        original_window = self.driver.current_window_handle

        try:
            self.driver.execute_script(f"window.open('{profile_url}', '_blank');")
            time.sleep(2)

            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            time.sleep(2)

            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                if iframes:
                    self.driver.switch_to.frame(iframes[0])
                    time.sleep(1)
            except:
                pass

            try:
                imgs = self.driver.find_elements(By.TAG_NAME, "img")
                for img in imgs:
                    try:
                        src = img.get_attribute('src')
                        if src and ('/data/file/' in src or '/data/editor/' in src):
                            if not src.startswith('http'):
                                src = 'https://dkxm8.com' + src
                            if src not in detail_images:
                                detail_images.append(src)
                    except:
                        continue
            except:
                pass

            try:
                self.driver.switch_to.default_content()
            except:
                pass

            self.driver.close()
            self.driver.switch_to.window(original_window)
            time.sleep(0.5)

        except Exception as e:
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            try:
                windows = self.driver.window_handles
                if len(windows) > 1:
                    self.driver.close()
                if windows:
                    self.driver.switch_to.window(original_window)
            except:
                pass

        return detail_images

    def run(self):
        """크롤러 실행"""
        print("=" * 70)
        print("🚀 대전/충청 지역 크롤러 시작")
        print("=" * 70)

        try:
            if not self.setup_driver():
                return False

            if not self.login():
                return False

            # 대전/충청 전체 지역 크롤링
            print(f"\n크롤링할 지역: {len(DAEJEON_CITIES)}개")
            for i, city in enumerate(DAEJEON_CITIES, 1):
                print(f"[{i}/{len(DAEJEON_CITIES)}] {city}")

            for area in DAEJEON_CITIES:
                items = self.crawl_area(area)
                self.results.extend(items)
                time.sleep(2)

            # 결과 저장
            output_file = f'daejeon_crawl_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)

            print("\n" + "=" * 70)
            print(f"✅ 크롤링 완료! 총 {len(self.results)}개 업체 수집")
            print(f"💾 파일 저장: {output_file}")
            print("=" * 70)

            return True

        except Exception as e:
            print(f"\n❌ 오류: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔚 브라우저 종료")


if __name__ == "__main__":
    import sys

    headless = '--headless' in sys.argv

    if headless:
        print("ℹ️  헤드리스 모드로 실행합니다")
    else:
        print("ℹ️  일반 모드로 실행합니다")

    crawler = DaejeonCrawler(headless=headless)
    success = crawler.run()

    sys.exit(0 if success else 1)
