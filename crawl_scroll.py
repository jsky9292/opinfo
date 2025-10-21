#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json
from datetime import datetime

USERNAME = "mix1220"
PASSWORD = "1234"
TEST_AREA = "대전"

class ScrollCrawler:
    def __init__(self):
        self.driver = None
        self.results = []
    
    def setup_driver(self):
        print("브라우저 설정 중...")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("준비 완료")
        return True
    
    def login(self):
        print("로그인 중...")
        self.driver.get("https://dkxm8.com/bbs/login.php")
        time.sleep(3)
        self.driver.find_element(By.NAME, "mb_id").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "mb_password").send_keys(PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, "input[type=submit]").click()
        time.sleep(5)
        print("로그인 성공")
        return True
    
    def scroll_down(self):
        print("스크롤 중...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("스크롤 완료")
    
    def run(self):
        self.setup_driver()
        self.login()
        
        url = f"https://dkxm8.com/?area={TEST_AREA}"
        print(f"접속: {url}")
        self.driver.get(url)
        time.sleep(3)
        
        self.scroll_down()
        
        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.gal_top, div[class*=gal]")
        print(f"{len(cards)}개 카드 발견")
        
        output = f"crawl_scroll_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output, "w", encoding="utf-8") as f:
            json.dump([{"count": len(cards), "area": TEST_AREA}], f, ensure_ascii=False, indent=2)
        
        print(f"완료: {len(cards)}개, 저장: {output}")
        self.driver.quit()
        return True

if __name__ == "__main__":
    crawler = ScrollCrawler()
    crawler.run()
