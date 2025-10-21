#!/usr/bin/env python3
"""
발견된 모든 지역(106개)을 순차 크롤링
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

class CompleteCrawler:
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
        print('로그인 완료\n')

    def crawl_area(self, area_name):
        """특정 지역의 모든 업소 크롤링 (대전 방식)"""
        try:
            from urllib.parse import quote
            encoded_area = quote(area_name)
            url = f"https://dkxm8.com/?area={encoded_area}"
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
                return []

            items = []
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
                    shop_url = ""
                    try:
                        profile_link = card.find_element(By.CSS_SELECTOR, "a[href*='profile_popup']")
                        shop_url = profile_link.get_attribute('href')
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

                    # 썸네일
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

                    if title or shop_url:
                        item = {
                            'title': title,
                            'url': shop_url,
                            'description': description,
                            'hours': hours,
                            'phone': phone,
                            'kakao_id': kakao_id,
                            'telegram_id': telegram_id,
                            'thumbnail': thumbnail,
                            'area': area_name  # 지역 정보 추가
                        }
                        items.append(item)

                except Exception as e:
                    continue

            return items

        except Exception as e:
            print(f'  ✗ 오류: {e}')
            return []

    def run(self):
        print('='*60)
        print('전국 106개 지역 순차 크롤링')
        print('='*60)

        # 발견된 지역 목록 로드
        with open('all_areas.json', 'r', encoding='utf-8') as f:
            areas = json.load(f)

        print(f'\n총 {len(areas)}개 지역 크롤링 시작\n')

        self.setup()
        self.login()

        for idx, area in enumerate(areas, 1):
            print(f'[{idx}/{len(areas)}] {area:20s}', end=' ')

            items = self.crawl_area(area)

            if items:
                self.results.extend(items)
                # 썸네일 체크
                real_thumbs = len([x for x in items if 'data/file/main' in x.get('thumbnail', '')])
                print(f'✓ {len(items):3d}개 (썸네일 {real_thumbs:3d}개)')
            else:
                print('○ 없음')

            # 10개 지역마다 중간 저장
            if idx % 10 == 0:
                temp_file = f'complete_crawl_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                print(f'  → 중간 저장: {temp_file} (누적 {len(self.results):,}개)\n')

            time.sleep(2)

        # 최종 저장
        output = f'complete_crawl_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f'\n{"="*60}')
        print(f'✅ 완료: {len(self.results):,}개 업소 → {output}')
        print(f'{"="*60}')

        # 통계
        real_thumbs = len([x for x in self.results if 'data/file/main' in x.get('thumbnail', '')])
        with_phone = len([x for x in self.results if x.get('phone')])

        print(f'\n📊 통계:')
        print(f'  총 업소: {len(self.results):,}개')
        print(f'  실제 썸네일: {real_thumbs:,}개 ({real_thumbs/len(self.results)*100:.1f}%)')
        print(f'  전화번호: {with_phone:,}개 ({with_phone/len(self.results)*100:.1f}%)')

        self.driver.quit()

if __name__ == '__main__':
    crawler = CompleteCrawler()
    crawler.run()
