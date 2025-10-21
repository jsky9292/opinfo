#!/usr/bin/env python3
"""
리스트 페이지에서 직접 크롤링 (대전 방식)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json
from datetime import datetime

USERNAME = 'mix1220'
PASSWORD = '1234'

class ListCrawler:
    def __init__(self):
        self.driver = None
        self.results = []

    def setup(self):
        print('브라우저 설정...')
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument('--headless')
        opts.add_argument('--window-size=1920,1080')
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print('준비 완료')

    def login(self):
        print('로그인...')
        self.driver.get('https://dkxm8.com/bbs/login.php')
        time.sleep(2)
        self.driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
        time.sleep(3)
        print('로그인 완료')

    def crawl_list_page(self, area_name):
        """리스트 페이지에서 직접 크롤링"""
        print(f'\\n{area_name} 크롤링 중...')
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
                        print(f'  {len(cards)}개 발견')
                        break
                except:
                    continue

            if not cards:
                print(f'  업체 없음')
                return items

            for idx, card in enumerate(cards, 1):
                try:
                    # 업체명
                    title = ""
                    try:
                        h4 = card.find_element(By.TAG_NAME, "h4")
                        title = h4.text.strip()
                    except:
                        pass

                    # URL
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

                    # 카카오톡
                    kakao_id = ""
                    try:
                        kakao_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'카톡')]]/span")
                        kakao_id = kakao_elem.text.strip()
                    except:
                        pass

                    # 텔레그램
                    telegram_id = ""
                    try:
                        telegram_elem = card.find_element(By.XPATH, ".//p[b[contains(text(),'텔레')]]/span")
                        telegram_id = telegram_elem.text.strip()
                    except:
                        pass

                    # 썸네일 (여기가 핵심!)
                    thumbnail = ""
                    try:
                        img = card.find_element(By.CSS_SELECTOR, ".imgwrap img")
                        thumbnail = img.get_attribute('src')
                        if thumbnail and not thumbnail.startswith('http'):
                            thumbnail = 'https://dkxm8.com' + thumbnail
                        if not thumbnail:
                            thumbnail = 'https://dkxm8.com/img/temp_thum.jpg'
                    except:
                        thumbnail = 'https://dkxm8.com/img/temp_thum.jpg'

                    if title or url:
                        item = {
                            'title': title,
                            'url': url,
                            'description': description,
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': thumbnail
                        }
                        items.append(item)

                except Exception as e:
                    continue

            print(f'  ✓ {len(items)}개 수집')
            return items

        except Exception as e:
            print(f'  ✗ 오류: {e}')
            return items

    def run(self, input_file):
        print('='*60)
        print('리스트 페이지에서 직접 크롤링 (대전 방식)')
        print('='*60)

        # 입력 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            shops = json.load(f)

        # 지역별로 그룹화
        from collections import defaultdict
        by_area = defaultdict(list)
        for shop in shops:
            area = shop.get('area', '대전')
            by_area[area].append(shop)

        print(f'\\n총 {len(by_area)}개 지역, {len(shops)}개 업소')

        self.setup()
        self.login()

        # 지역별로 크롤링
        for area_name in sorted(by_area.keys()):
            items = self.crawl_list_page(area_name)
            self.results.extend(items)
            time.sleep(2)

        # 최종 저장
        output = f'list_crawl_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f'\\n✅ 완료: {len(self.results)}개 → {output}')
        self.driver.quit()

if __name__ == '__main__':
    crawler = ListCrawler()
    crawler.run('final_all_20251011_125541.json')
