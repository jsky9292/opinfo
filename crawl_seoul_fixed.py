#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json
from datetime import datetime

USERNAME = 'mix1220'
PASSWORD = '1234'

# 구 이름이 아니라 지역명으로!
SEOUL_AREAS = ['강남', '서초', '송파', '강동', '광진', '성동', '중구', '종로', '용산', '마포']

class SeoulCrawler:
    def __init__(self):
        self.driver = None
        self.results = []

    def setup(self):
        print('브라우저 설정...')
        opts = Options()
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print('준비 완료')

    def login(self):
        print('로그인...')
        self.driver.get('https://dkxm8.com/bbs/login.php')
        time.sleep(3)
        self.driver.find_element(By.NAME, 'mb_id').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'mb_password').send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type=submit]').click()
        time.sleep(5)
        print('로그인 완료')

    def scroll(self):
        last = self.driver.execute_script('return document.body.scrollHeight')
        for _ in range(20):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            new = self.driver.execute_script('return document.body.scrollHeight')
            if new == last: break
            last = new

    def crawl_area(self, area, idx, total):
        print(f'[{idx}/{total}] {area} (서울)', end=' ')
        try:
            self.driver.get(f'https://dkxm8.com/?area={area}')
            time.sleep(2)
            self.scroll()
            cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.gal_top, div[class*=gal]')

            count = 0
            for card in cards:
                try:
                    title = card.find_element(By.TAG_NAME, 'h4').text.strip() if card.find_elements(By.TAG_NAME, 'h4') else ''
                    url = card.find_element(By.CSS_SELECTOR, 'a[href*=profile]').get_attribute('href') if card.find_elements(By.CSS_SELECTOR, 'a[href*=profile]') else ''
                    if title or url:
                        self.results.append({'title': title, 'url': url, 'area': area, 'region': '서울'})
                        count += 1
                except: pass
            print(f'-> {count}개')
        except Exception as e:
            print(f'-> 오류: {e}')

    def run(self):
        print('='*50)
        print('서울 지역 크롤링 시작 (수정버전)')
        print('='*50)
        self.setup()
        self.login()

        for idx, area in enumerate(SEOUL_AREAS, 1):
            self.crawl_area(area, idx, len(SEOUL_AREAS))
            time.sleep(1.5)

        output = f'seoul_fixed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f'\n완료: {len(self.results)}개 → {output}')
        self.driver.quit()

crawler = SeoulCrawler()
crawler.run()
