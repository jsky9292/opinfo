#!/usr/bin/env python3
"""
dkxm8.com 페이지네이션 포함 완전 크롤러
- 모든 페이지를 순회하여 전체 업체 수집
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime
import re

# 로그인 정보
USERNAME = "mix1220"
PASSWORD = "1234"

# 테스트용 지역 (대전만 먼저)
TEST_REGIONS = {
    "대전/충청": ["대전"]
}

# 전체 지역 리스트
ALL_REGIONS = {
    "대전/충청": ["대전", "천안", "청주", "세종", "서산", "당진", "보령", "진천", "아산", "충주", "제천", "홍성", "논산", "오창", "음성", "옥천", "공주", "증평", "계룡", "부여", "태안", "예산", "오송"],
    "부산/경남": ["부산", "울산", "양산", "마산", "창원", "진해", "김해", "거제", "진주", "통영", "사천", "밀양", "함안", "창녕", "고성", "남해", "하동", "산청", "함양", "거창", "합천"],
    "서울/강남": ["강남구", "서초구", "송파구", "강동구", "광진구", "성동구", "중구", "종로구", "용산구", "마포구", "서대문구", "은평구", "강서구", "양천구", "구로구", "금천구", "영등포구", "동작구", "관악구", "강북구", "노원구"],
    "인천/경기": ["인천", "송도", "부평", "계양", "수원", "성남", "고양", "용인", "부천", "안산", "안양", "남양주", "화성", "평택", "의정부", "시흥", "파주", "김포", "광명", "광주", "군포", "하남"],
    "대구/경북": ["대구", "중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "포항", "경주", "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산", "군위", "의성", "청송", "영양", "영덕", "청도", "고령", "성주", "칠곡", "예천", "봉화", "울진", "울릉도"],
    "광주/전라": ["광주", "전주", "군산", "익산", "정읍", "남원", "김제", "목포", "여수", "순천", "나주", "광양"],
    "강원/제주/전라": ["춘천", "원주", "강릉", "동해", "태백", "속초", "삼척", "제주", "서귀포"]
}


class PaginationCrawler:
    def __init__(self, headless=True, test_mode=True):
        self.headless = headless
        self.test_mode = test_mode
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

    def get_total_pages(self, area_name):
        """해당 지역의 전체 페이지 수 확인"""
        try:
            # 페이지네이션 찾기 (여러 가능한 셀렉터 시도)
            pagination_selectors = [
                "div.pg_wrap",
                "div.pagination",
                "div[class*='paging']",
                "div[class*='page']",
                ".pg",
                "#pagination"
            ]

            max_page = 1

            for selector in pagination_selectors:
                try:
                    pagination = self.driver.find_element(By.CSS_SELECTOR, selector)

                    # 페이지 링크에서 숫자 추출
                    page_links = pagination.find_elements(By.TAG_NAME, "a")

                    for link in page_links:
                        try:
                            # href에서 페이지 번호 추출
                            href = link.get_attribute('href')
                            if href and 'page=' in href:
                                page_match = re.search(r'page=(\d+)', href)
                                if page_match:
                                    page_num = int(page_match.group(1))
                                    max_page = max(max_page, page_num)

                            # 링크 텍스트에서 숫자 추출
                            text = link.text.strip()
                            if text.isdigit():
                                page_num = int(text)
                                max_page = max(max_page, page_num)
                        except:
                            continue

                    if max_page > 1:
                        break

                except:
                    continue

            return max_page

        except Exception as e:
            print(f"   ⚠️ 페이지 수 확인 오류: {e}")
            return 1

    def crawl_page(self, area_name, region_name, page_num):
        """특정 지역의 특정 페이지 크롤링"""
        items = []

        try:
            # URL 구성 (페이지 파라미터 추가)
            if page_num == 1:
                url = f"https://dkxm8.com/?area={area_name}"
            else:
                url = f"https://dkxm8.com/?area={area_name}&page={page_num}"

            self.driver.get(url)
            time.sleep(2)

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

                    if title or profile_url:
                        item = {
                            'title': title,
                            'url': profile_url,
                            'description': description,
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': image_url,
                            'area': area_name,
                            'region': region_name,
                            'page': page_num
                        }
                        items.append(item)

                except Exception as e:
                    continue

            return items

        except Exception as e:
            print(f"      ❌ 페이지 {page_num} 오류: {str(e)[:30]}")
            return items

    def crawl_area_all_pages(self, area_name, region_name):
        """특정 지역의 모든 페이지 크롤링"""
        print(f"\n   📄 {area_name} 크롤링 중...")

        all_items = []

        try:
            # 첫 페이지로 이동하여 전체 페이지 수 확인
            url = f"https://dkxm8.com/?area={area_name}"
            self.driver.get(url)
            time.sleep(2)

            total_pages = self.get_total_pages(area_name)
            print(f"      총 {total_pages}개 페이지 발견")

            # 각 페이지 크롤링
            for page_num in range(1, total_pages + 1):
                print(f"      페이지 {page_num}/{total_pages}...", end=" ")

                items = self.crawl_page(area_name, region_name, page_num)
                all_items.extend(items)

                print(f"{len(items)}개")
                time.sleep(1)  # 서버 부하 방지

            print(f"   ✅ {area_name}: 총 {len(all_items)}개 업체 수집")
            return all_items

        except Exception as e:
            print(f"   ❌ {area_name} 오류: {str(e)[:50]}")
            return all_items

    def run(self):
        """크롤러 실행"""
        print("=" * 70)
        if self.test_mode:
            print("🧪 테스트 모드: 대전만 크롤링")
        else:
            print("🚀 전체 지역 크롤러 시작")
        print("=" * 70)

        try:
            if not self.setup_driver():
                return False

            if not self.login():
                return False

            regions = TEST_REGIONS if self.test_mode else ALL_REGIONS
            total_cities = sum(len(cities) for cities in regions.values())
            print(f"\n전체 지역: {len(regions)}개 권역, {total_cities}개 도시")

            current = 0
            for region_name, cities in regions.items():
                print(f"\n{'='*70}")
                print(f"🗺️  {region_name} ({len(cities)}개 도시)")
                print(f"{'='*70}")

                for city in cities:
                    current += 1
                    print(f"[{current}/{total_cities}]", end="")
                    items = self.crawl_area_all_pages(city, region_name)
                    self.results.extend(items)
                    time.sleep(2)  # 도시 간 대기

            # 결과 저장
            mode_suffix = "test" if self.test_mode else "full"
            output_file = f'crawl_pagination_{mode_suffix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

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

            # 도시별 통계
            print("\n📊 도시별 통계:")
            area_stats = {}
            for item in self.results:
                area = item.get('area', '미분류')
                area_stats[area] = area_stats.get(area, 0) + 1

            for area, count in sorted(area_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {area}: {count}개")

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
    full_mode = '--full' in sys.argv
    test_mode = not full_mode

    if headless:
        print("ℹ️  헤드리스 모드로 실행합니다")
    else:
        print("ℹ️  일반 모드로 실행합니다")

    if test_mode:
        print("ℹ️  테스트 모드: 대전만 크롤링 (약 5분)")
    else:
        print("ℹ️  전체 모드: 전국 크롤링 (약 1-2시간)")

    crawler = PaginationCrawler(headless=headless, test_mode=test_mode)
    success = crawler.run()

    sys.exit(0 if success else 1)
