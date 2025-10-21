#!/usr/bin/env python3
"""
dkxm8.com 전용 크롤러
로그인 정보: mdmix / 1234
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
import csv
from datetime import datetime

# 로그인 정보
USERNAME = "mix1220"
PASSWORD = "1234"

class DKXM8Crawler:
    def __init__(self, headless=False):
        """크롤러 초기화"""
        self.headless = headless
        self.driver = None
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'login_success': False,
            'categories': [],
            'items': []
        }
    
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        print("🔧 브라우저 드라이버 설정 중...")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        # 기본 옵션
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # 자동화 감지 우회
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent 설정
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            
            # 자동화 감지 추가 우회
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
    
    def access_site(self):
        """사이트 접근"""
        print("\n🌐 로그인 페이지 접근 중...")

        try:
            # 로그인 페이지로 직접 이동
            self.driver.get("https://dkxm8.com/bbs/login.php")
            time.sleep(5)  # 페이지 로딩 대기
            
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            print(f"✅ 페이지 로드 완료")
            print(f"   URL: {current_url}")
            print(f"   제목: {page_title}")
            
            # 스크린샷 저장
            self.driver.save_screenshot('screenshot_main.png')
            print("   📸 스크린샷 저장: screenshot_main.png")
            
            # HTML 저장
            with open('page_main.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print("   💾 HTML 저장: page_main.html")
            
            return True
            
        except Exception as e:
            print(f"❌ 사이트 접근 실패: {e}")
            return False
    
    def find_login_form(self):
        """로그인 폼 찾기"""
        print("\n🔍 로그인 폼 검색 중...")
        
        # 다양한 셀렉터 시도
        selectors = {
            'username': [
                "input[name='mb_id']",
                "input[name='userid']",
                "input[name='user_id']",
                "input[name='id']",
                "input[name='username']",
                "input[id='mb_id']",
                "input[id='userid']",
                "input[type='text'][placeholder*='아이디']",
                "input[type='text']:first-of-type"
            ],
            'password': [
                "input[name='mb_password']",
                "input[name='password']",
                "input[name='passwd']",
                "input[id='mb_password']",
                "input[id='password']",
                "input[type='password']"
            ],
            'submit': [
                "button[type='submit']",
                "input[type='submit']",
                "button.btn-login",
                "button#login",
                "a.login-btn"
            ]
        }
        
        login_elements = {}
        
        # Username 필드
        for selector in selectors['username']:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                if elem.is_displayed():
                    login_elements['username'] = (selector, elem)
                    print(f"   ✓ Username 필드: {selector}")
                    break
            except:
                continue
        
        # Password 필드
        for selector in selectors['password']:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                if elem.is_displayed():
                    login_elements['password'] = (selector, elem)
                    print(f"   ✓ Password 필드: {selector}")
                    break
            except:
                continue
        
        # Submit 버튼
        for selector in selectors['submit']:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                if elem.is_displayed():
                    login_elements['submit'] = (selector, elem)
                    print(f"   ✓ Submit 버튼: {selector}")
                    break
            except:
                continue
        
        if 'username' in login_elements and 'password' in login_elements:
            print("✅ 로그인 폼 발견!")
            return login_elements
        else:
            print("⚠️  로그인 폼을 찾지 못했습니다.")
            print("   페이지를 확인해보세요: screenshot_main.png")
            return None
    
    def login(self, login_elements):
        """로그인 수행"""
        print(f"\n🔑 로그인 시도 중... (ID: {USERNAME})")
        
        try:
            # Username 입력
            username_elem = login_elements['username'][1]
            username_elem.clear()
            username_elem.send_keys(USERNAME)
            print("   ✓ 아이디 입력 완료")
            time.sleep(0.5)
            
            # Password 입력
            password_elem = login_elements['password'][1]
            password_elem.clear()
            password_elem.send_keys(PASSWORD)
            print("   ✓ 비밀번호 입력 완료")
            time.sleep(0.5)
            
            # Submit
            if 'submit' in login_elements:
                login_elements['submit'][1].click()
                print("   ✓ 로그인 버튼 클릭")
            else:
                password_elem.send_keys('\n')
                print("   ✓ Enter 키 입력")
            
            # 로그인 처리 대기
            time.sleep(5)
            
            # 로그인 성공 확인
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            # 스크린샷 저장
            self.driver.save_screenshot('screenshot_after_login.png')
            
            # 성공 여부 판단
            if 'logout' in page_source or '로그아웃' in page_source:
                print("✅ 로그인 성공!")
                self.results['login_success'] = True
                return True
            elif 'login' in current_url or '로그인' in page_source:
                print("❌ 로그인 실패 (로그인 페이지에 머물러 있음)")
                print("   아이디/비밀번호를 확인해주세요.")
                return False
            else:
                print("⚠️  로그인 성공 여부 불명확")
                print(f"   현재 URL: {current_url}")
                print("   스크린샷을 확인해주세요: screenshot_after_login.png")
                return None
            
        except Exception as e:
            print(f"❌ 로그인 중 오류: {e}")
            return False
    
    def extract_categories(self):
        """카테고리 구조 추출"""
        print("\n📋 카테고리 구조 추출 중...")
        
        categories = []
        
        # 다양한 네비게이션 영역 시도
        nav_selectors = [
            "nav a",
            "ul.menu a", "ul.nav a",
            ".category a", ".menu a", ".gnb a",
            "header a", ".navigation a",
            "#menu a", "#nav a",
            ".sidebar a", ".left-menu a"
        ]
        
        try:
            for selector in nav_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        if elem.is_displayed():
                            text = elem.text.strip()
                            href = elem.get_attribute('href')
                            
                            if text and href and len(text) > 0:
                                categories.append({
                                    'text': text,
                                    'url': href,
                                    'selector': selector
                                })
                except:
                    continue
            
            # 중복 제거
            seen = set()
            unique_categories = []
            for cat in categories:
                key = (cat['text'], cat['url'])
                if key not in seen:
                    seen.add(key)
                    unique_categories.append(cat)
            
            self.results['categories'] = unique_categories
            
            if unique_categories:
                print(f"✅ {len(unique_categories)}개 카테고리 발견:")
                for i, cat in enumerate(unique_categories[:20], 1):
                    print(f"   {i}. {cat['text'][:40]}: {cat['url']}")
                
                if len(unique_categories) > 20:
                    print(f"   ... 외 {len(unique_categories) - 20}개")
            else:
                print("⚠️  카테고리를 찾지 못했습니다.")
            
            return unique_categories
            
        except Exception as e:
            print(f"❌ 카테고리 추출 중 오류: {e}")
            return []
    
    def crawl_main_page(self):
        """메인 페이지의 업체 정보 크롤링"""
        print("\n📄 메인 페이지 업체 크롤링 중...")

        items = []

        try:
            # 업체 카드 찾기
            card_selectors = [
                "div.gal_top",  # 실제 업체 카드 클래스
                "div.gal_list",
                "div[class*='gal']"
            ]

            cards = []
            for selector in card_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        cards = elements
                        print(f"   ✓ 셀렉터 발견: {selector} ({len(cards)}개)")
                        break
                except:
                    continue

            if not cards:
                print("   ⚠️  업체 카드를 찾을 수 없습니다. 페이지 구조 확인 필요")
                return items

            # 각 카드에서 정보 추출
            for idx, card in enumerate(cards[:50], 1):  # 최대 50개
                try:
                    # 업체명 (h4 태그)
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

                    # 설명 (strong 태그)
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
                        kakao_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'카톡') or contains(text(),'kakao')]]/span")
                        kakao_id = kakao_elem.text.strip()
                    except:
                        pass

                    # 텔레그램 ID
                    telegram_id = ""
                    try:
                        telegram_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'텔레') or contains(text(),'telegram')]]/span")
                        telegram_id = telegram_elem.text.strip()
                    except:
                        pass

                    # 썸네일 이미지 URL
                    image_url = ""
                    try:
                        img = card.find_element(By.CSS_SELECTOR, ".imgwrap img")
                        image_url = img.get_attribute('src')
                        if image_url and not image_url.startswith('http'):
                            image_url = 'https://dkxm8.com' + image_url
                    except:
                        pass

                    # 프로필 상세 이미지 가져오기 (옵션)
                    detail_images = []
                    if url and idx <= 3:  # 처음 3개만 상세 이미지 수집
                        print(f"      📸 프로필 상세 이미지 수집 중...")
                        detail_images = self.get_profile_details(url)
                        if detail_images:
                            print(f"      ✓ {len(detail_images)}개 상세 이미지 발견")

                    if title or url:
                        item = {
                            'number': idx,
                            'title': title,
                            'url': url,
                            'description': description[:100] if description else "",
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': image_url,
                            'detail_images': detail_images,
                            'category': '메인페이지'
                        }
                        items.append(item)

                        if idx <= 5:  # 처음 5개만 출력
                            print(f"   {idx}. {title[:30]}")

                except Exception as e:
                    continue

            print(f"   ✓ 총 {len(items)}개 업체 수집 완료")
            return items

        except Exception as e:
            print(f"   ❌ 크롤링 실패: {e}")
            import traceback
            traceback.print_exc()
            return items

    def get_profile_details(self, profile_url):
        """프로필 팝업에서 상세 이미지 가져오기"""
        detail_images = []
        original_window = self.driver.current_window_handle

        try:
            # 새 창으로 프로필 열기
            self.driver.execute_script(f"window.open('{profile_url}', '_blank');")
            time.sleep(3)

            # 새 창으로 전환
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            time.sleep(3)

            # iframe이 있는지 확인
            try:
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                if iframes:
                    self.driver.switch_to.frame(iframes[0])
                    time.sleep(2)
            except:
                pass

            # 페이지 소스 저장 (디버깅용)
            # with open('profile_popup_debug.html', 'w', encoding='utf-8') as f:
            #     f.write(self.driver.page_source)

            # 모든 이미지 찾기
            try:
                imgs = self.driver.find_elements(By.TAG_NAME, "img")
                for img in imgs:
                    try:
                        src = img.get_attribute('src')
                        if src:
                            # data/file 경로를 포함한 이미지만
                            if '/data/file/' in src or '/data/editor/' in src:
                                if not src.startswith('http'):
                                    src = 'https://dkxm8.com' + src
                                if src not in detail_images:
                                    detail_images.append(src)
                    except:
                        continue
            except:
                pass

            # iframe에서 빠져나오기
            try:
                self.driver.switch_to.default_content()
            except:
                pass

            # 원래 창으로 돌아가기
            self.driver.close()
            self.driver.switch_to.window(original_window)
            time.sleep(1)

        except Exception as e:
            print(f"      ⚠️  오류: {str(e)[:50]}")
            # 에러 발생 시 원래 창으로 복귀
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

    def crawl_category(self, category_url, category_name):
        """특정 카테고리 페이지 크롤링"""
        print(f"\n📄 카테고리 크롤링: {category_name}")
        print(f"   URL: {category_url}")

        items = []

        try:
            self.driver.get(category_url)
            time.sleep(3)

            # 스크린샷 저장
            screenshot_name = f"screenshot_{category_name.replace('/', '_')}.png"
            self.driver.save_screenshot(screenshot_name)

            # HTML 저장 (디버깅용)
            html_name = f"page_{category_name.replace('/', '_')}.html"
            with open(html_name, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)

            # 업체 카드 찾기
            card_selectors = [
                "div.gal_top",  # 실제 업체 카드 클래스
                "div.gal_list",
                "div[class*='gal']"
            ]

            cards = []
            for selector in card_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        cards = elements
                        break
                except:
                    continue

            if not cards:
                print(f"   ⚠️  업체 카드를 찾을 수 없습니다")
                return items

            # 각 카드에서 정보 추출
            for idx, card in enumerate(cards[:30], 1):  # 최대 30개
                try:
                    # 업체명 (h4 태그)
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

                    # 설명 (strong 태그)
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
                        kakao_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'카톡') or contains(text(),'kakao')]]/span")
                        kakao_id = kakao_elem.text.strip()
                    except:
                        pass

                    # 텔레그램 ID
                    telegram_id = ""
                    try:
                        telegram_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'텔레') or contains(text(),'telegram')]]/span")
                        telegram_id = telegram_elem.text.strip()
                    except:
                        pass

                    # 썸네일 이미지 URL
                    image_url = ""
                    try:
                        img = card.find_element(By.CSS_SELECTOR, ".imgwrap img")
                        image_url = img.get_attribute('src')
                        if image_url and not image_url.startswith('http'):
                            image_url = 'https://dkxm8.com' + image_url
                    except:
                        pass

                    # 프로필 상세 이미지 가져오기 (옵션)
                    detail_images = []
                    if url and idx <= 5:  # 처음 5개만 상세 이미지 수집 (시간 절약)
                        print(f"      📸 프로필 상세 이미지 수집 중...")
                        detail_images = self.get_profile_details(url)
                        if detail_images:
                            print(f"      ✓ {len(detail_images)}개 상세 이미지 발견")

                    if title or url:
                        item = {
                            'number': idx,
                            'title': title,
                            'url': url,
                            'description': description[:100] if description else "",
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': image_url,
                            'detail_images': detail_images,
                            'category': category_name
                        }
                        items.append(item)

                except Exception as e:
                    continue

            print(f"   ✓ {len(items)}개 업체 수집")
            return items

        except Exception as e:
            print(f"   ❌ 크롤링 실패: {e}")
            return items
    
    def save_results(self):
        """결과 저장"""
        print("\n💾 결과 저장 중...")
        
        # JSON 저장
        json_file = f'crawl_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"   ✓ JSON: {json_file}")
        
        # CSV 저장 (카테고리)
        if self.results['categories']:
            csv_file = f'categories_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['text', 'url'])
                writer.writeheader()
                for cat in self.results['categories']:
                    writer.writerow({'text': cat['text'], 'url': cat['url']})
            print(f"   ✓ CSV: {csv_file}")
    
    def run(self):
        """크롤러 실행"""
        print("=" * 70)
        print("🚀 dkxm8.com 크롤러 시작")
        print("=" * 70)

        try:
            # 1. 드라이버 설정
            if not self.setup_driver():
                return False

            # 2. 사이트 접근
            if not self.access_site():
                return False

            # 3. 자동 로그인 시도
            print("\n🔑 자동 로그인 시도 중...")

            # 로그인 페이지로 이동
            if 'login.php' in self.driver.current_url:
                try:
                    # 아이디 입력
                    username_field = self.driver.find_element(By.NAME, "mb_id")
                    username_field.clear()
                    username_field.send_keys(USERNAME)

                    # 비밀번호 입력
                    password_field = self.driver.find_element(By.NAME, "mb_password")
                    password_field.clear()
                    password_field.send_keys(PASSWORD)

                    # 로그인 버튼 클릭
                    submit_btn = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                    submit_btn.click()

                    print("✅ 로그인 버튼 클릭 완료")
                    time.sleep(8)

                    # 로그인 성공 여부 확인
                    if 'login.php' in self.driver.current_url:
                        print("⚠️  로그인 실패 - 로그인 페이지에 머물러 있음")
                        print("   아이디/비밀번호를 확인하세요")
                        # 스크린샷 저장
                        self.driver.save_screenshot('login_failed.png')
                        print("\n브라우저를 열어둡니다. 수동으로 로그인 후 아무 키나 누르세요...")
                        try:
                            input()
                        except EOFError:
                            time.sleep(60)
                    else:
                        print("✅ 로그인 성공!")

                    # 메인 페이지로 이동
                    self.driver.get("https://dkxm8.com/")
                    print("✅ 메인 페이지로 이동")
                    time.sleep(5)

                except Exception as e:
                    print(f"⚠️  자동 로그인 실패: {e}")
                    print("60초 대기 중... 수동으로 로그인해주세요")
                    time.sleep(60)
            else:
                print("⚠️  로그인 페이지가 아닙니다. 60초 대기")
                time.sleep(60)

            # 로그인 성공 확인
            current_url = self.driver.current_url
            print(f"\n현재 URL: {current_url}")

            # 스크린샷 저장
            self.driver.save_screenshot('screenshot_after_login.png')
            print("📸 로그인 후 스크린샷 저장: screenshot_after_login.png")

            page_source = self.driver.page_source.lower()
            if 'logout' in page_source or '로그아웃' in page_source:
                print("✅ 로그인 확인됨!")
                self.results['login_success'] = True
            else:
                print("⚠️  로그인 여부 확인 불가 - 크롤링 계속 진행")

            # 4. 메인 페이지 업체 크롤링
            main_items = self.crawl_main_page()
            self.results['items'].extend(main_items)

            # 5. 카테고리 추출
            categories = self.extract_categories()

            # 6. 지역 카테고리만 크롤링 (대전/충청, 부산/경남 등)
            region_categories = [cat for cat in categories if '/' in cat['text'] and 'bbs' not in cat['url']]

            print(f"\n🗂️  {len(region_categories)}개 지역 카테고리 크롤링 시작...")
            for cat in region_categories[:3]:  # 처음 3개 지역만 테스트
                items = self.crawl_category(cat['url'], cat['text'])
                self.results['items'].extend(items)
                time.sleep(2)  # 요청 간격

            # 7. 결과 저장
            self.save_results()

            print("\n" + "=" * 70)
            print("✅ 크롤링 완료!")
            print("=" * 70)
            print(f"로그인: {'성공' if self.results['login_success'] else '확인불가'}")
            print(f"카테고리 수: {len(self.results['categories'])}")
            print("\n생성된 파일:")
            print("  - screenshot_main.png")
            print("  - screenshot_after_login.png")
            print("  - page_main.html")
            print("  - crawl_results_*.json")
            if self.results['categories']:
                print("  - categories_*.csv")

            print("\n브라우저를 닫으려면 아무 키나 누르세요...")
            try:
                input()
            except EOFError:
                print("10초 후 자동 종료...")
                time.sleep(10)

            return True

        except Exception as e:
            print(f"\n❌ 크롤러 실행 중 오류: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            if self.driver:
                self.driver.quit()
                print("\n🔚 브라우저 종료")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("dkxm8.com 크롤러")
    print("로그인 정보: mdmix / ****")
    print("=" * 70)
    
    import sys
    
    headless = '--headless' in sys.argv or '-h' in sys.argv
    
    if headless:
        print("ℹ️  헤드리스 모드로 실행합니다 (UI 없음)")
    else:
        print("ℹ️  일반 모드로 실행합니다 (브라우저 보임)")
        print("   헤드리스 모드: python dkxm8_crawler.py --headless")
    
    crawler = DKXM8Crawler(headless=headless)
    success = crawler.run()
    
    sys.exit(0 if success else 1)
