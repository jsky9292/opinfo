#!/usr/bin/env python3
"""
dkxm8.com 전체 지역 크롤러
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

# 전체 지역 리스트 (원본 사이트 구조)
ALL_REGIONS = {
    "대전/충청": ["대전", "천안", "청주", "세종", "서산", "당진", "보령", "진천", "아산", "충주", "제천", "홍성", "논산", "오창", "음성", "옥천", "공주", "증평", "계룡", "부여", "태안", "예산", "오송"],
    "부산/경남": ["부산", "울산", "양산", "마산", "창원", "진해", "김해", "거제", "진주", "통영", "사천", "밀양", "함안", "창녕", "고성", "남해", "하동", "산청", "함양", "거창", "합천"],
    "서울/강남": ["강남구", "서초구", "송파구", "강동구", "광진구", "성동구", "중구", "종로구", "용산구", "마포구", "서대문구", "은평구", "강서구", "양천구", "구로구", "금천구", "영등포구", "동작구", "관악구", "강북구", "노원구"],
    "인천/경기": ["인천", "송도", "부평", "계양", "수원", "성남", "고양", "용인", "부천", "안산", "안양", "남양주", "화성", "평택", "의정부", "시흥", "파주", "김포", "광명", "광주", "군포", "하남"],
    "대구/경북": ["대구", "중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "포항", "경주", "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산", "군위", "의성", "청송", "영양", "영덕", "청도", "고령", "성주", "칠곡", "예천", "봉화", "울진", "울릉도"],
    "광주/전라": ["광주", "전주", "군산", "익산", "정읍", "남원", "김제", "목포", "여수", "순천", "나주", "광양"],
    "강원/제주/전라": ["춘천", "원주", "강릉", "동해", "태백", "속초", "삼척", "제주", "서귀포"]
}

class AllRegionsCrawler:
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

    def crawl_area(self, area_name, region_name):
        """특정 지역 크롤링"""
        print(f"   📄 {area_name} 크롤링 중...", end=" ")

        items = []

        try:
            url = f"https://dkxm8.com/?area={area_name}"
            self.driver.get(url)
            time.sleep(3)

            # 업체 카드 찾기
            cards = []
            selectors = ["div.gal_top", "div.gal_list", "div[class*='gal']"]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        cards = elements
                        break
                except:
                    continue

            if not cards:
                print(f"⚠️  업체 없음")
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
                    profile_url = ""
                    try:
                        profile_link = card.find_element(By.CSS_SELECTOR, "a[href*='profile_popup']")
                        profile_url = profile_link.get_attribute('href')
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

                    # 상세 이미지 수집 (처음 5개 업소만)
                    detail_images = []
                    if profile_url and idx <= 5:
                        detail_images = self.get_profile_details(profile_url)

                    if title or profile_url:
                        item = {
                            'number': idx,
                            'title': title,
                            'url': profile_url,
                            'description': description,
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': image_url,
                            'detail_images': detail_images,
                            'area': area_name,
                            'region': region_name
                        }
                        items.append(item)

                except Exception as e:
                    continue

            print(f"✓ {len(items)}개")
            return items

        except Exception as e:
            print(f"❌ 오류: {str(e)[:30]}")
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
        print("🚀 전국 전체 지역 크롤러 시작")
        print("=" * 70)

        try:
            if not self.setup_driver():
                return False

            if not self.login():
                return False

            total_cities = sum(len(cities) for cities in ALL_REGIONS.values())
            print(f"\n전체 지역: {len(ALL_REGIONS)}개 권역, {total_cities}개 도시")

            current = 0
            for region_name, cities in ALL_REGIONS.items():
                print(f"\n{'='*70}")
                print(f"🗺️  {region_name} ({len(cities)}개 도시)")
                print(f"{'='*70}")

                for city in cities:
                    current += 1
                    print(f"[{current}/{total_cities}] ", end="")
                    items = self.crawl_area(city, region_name)
                    self.results.extend(items)
                    time.sleep(1.5)  # 서버 부하 방지

            # 결과 저장
            output_file = f'all_regions_crawl_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)

            print("\n" + "=" * 70)
            print(f"✅ 크롤링 완료! 총 {len(self.results)}개 업체 수집")
            print(f"💾 파일 저장: {output_file}")
            print("=" * 70)

            # 통계 출력
            print("\n📊 권역별 통계:")
            region_stats = {}
            for item in self.results:
                region = item.get('region', '미분류')
                region_stats[region] = region_stats.get(region, 0) + 1

            for region, count in sorted(region_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {region}: {count}개")

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
        print("ℹ️  일반 모드로 실행합니다 (크롤링 시간: 약 10-15분)")

    crawler = AllRegionsCrawler(headless=headless)
    success = crawler.run()

    sys.exit(0 if success else 1)
