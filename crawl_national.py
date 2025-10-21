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

ALL_REGIONS = {
    '대전/충청': ['대전', '천안', '청주', '세종', '서산', '당진', '보령', '진천', '아산', '충주', '제천', '홍성', '논산', '오창', '음성'],
    '부산/경남': ['부산', '울산', '양산', '마산', '창원', '진해', '김해', '거제', '진주'],
    '서울/강남': ['강남구', '서초구', '송파구', '강동구', '광진구', '성동구', '중구', '종로구', '용산구', '마포구'],
    '인천/경기': ['인천', '송도', '부평', '수원', '성남', '고양', '용인', '부천', '안산'],
    '대구/경북': ['대구', '포항', '경주', '구미'],
    '광주/전라': ['광주', '전주', '군산', '익산'],
    '강원/제주': ['춘천', '원주', '강릉', '제주', '서귀포']
}

class NationalCrawler:
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
    
    def crawl_city(self, city, region, idx, total):
        print(f'[{idx}/{total}] {city} ({region})', end=' ')
        try:
            self.driver.get(f'https://dkxm8.com/?area={city}')
            time.sleep(2)
            self.scroll()
            cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.gal_top, div[class*=gal]')
            
            count = 0
            for card in cards:
                try:
                    title = card.find_element(By.TAG_NAME, 'h4').text.strip() if card.find_elements(By.TAG_NAME, 'h4') else ''
                    url = card.find_element(By.CSS_SELECTOR, 'a[href*=profile]').get_attribute('href') if card.find_elements(By.CSS_SELECTOR, 'a[href*=profile]') else ''
                    if title or url:
                        self.results.append({'title': title, 'url': url, 'area': city, 'region': region})
                        count += 1
                except: pass
            print(f'-> {count}개')
        except Exception as e:
            print(f'-> 오류')
    
    def run(self):
        print('='*50)
        print('전국 크롤링 시작')
        print('='*50)
        self.setup()
        self.login()
        
        total = sum(len(cities) for cities in ALL_REGIONS.values())
        current = 0
        
        for region, cities in ALL_REGIONS.items():
            print(f'\n{region} ({len(cities)}개):')
            for city in cities:
                current += 1
                self.crawl_city(city, region, current, total)
                time.sleep(1.5)
        
        output = f'national_all_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f'\n완료: {len(self.results)}개 → {output}')
        self.driver.quit()

crawler = NationalCrawler()
crawler.run()
