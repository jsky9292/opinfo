#!/usr/bin/env python3
"""
모든 지역 카테고리를 순회하면서 업소 크롤링
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

class AllAreasCrawler:
    def __init__(self):
        self.driver = None
        self.results = []
        # 전국 모든 지역 목록 (사이트에서 사용하는 지역명)
        self.areas = [
            # 서울
            '강남', '강동', '강북', '강서', '관악', '광진', '구로', '금천',
            '노원', '도봉', '동대문', '동작', '마포', '서대문', '서초', '성동',
            '성북', '송파', '양천', '영등포', '용산', '은평', '종로', '중구',
            '중랑',
            # 경기
            '고양', '과천', '광명', '광주', '구리', '군포', '김포', '남양주',
            '동두천', '부천', '성남', '수원', '시흥', '안산', '안성', '안양',
            '양주', '여주', '오산', '용인', '의왕', '의정부', '이천', '파주',
            '평택', '포천', '하남', '화성',
            # 인천
            '인천',
            # 강원
            '강릉', '동해', '삼척', '속초', '원주', '춘천', '태백', '홍천',
            # 충북
            '제천', '청주', '충주', '진천', '음성', '오창',
            # 충남
            '계룡', '공주', '논산', '당진', '보령', '서산', '아산', '천안',
            '홍성',
            # 대전/세종
            '대전', '세종',
            # 전북
            '군산', '김제', '남원', '익산', '전주', '정읍',
            # 전남
            '광양', '나주', '목포', '순천', '여수',
            # 광주
            '광주',
            # 경북
            '경산', '경주', '구미', '김천', '문경', '상주', '안동', '영주',
            '영천', '포항',
            # 경남
            '거제', '김해', '밀양', '사천', '양산', '진주', '창원', '통영',
            # 대구
            '대구',
            # 부산
            '부산',
            # 울산
            '울산',
            # 제주
            '제주'
        ]

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
        """특정 지역의 모든 업소 크롤링"""
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
                            'thumbnail': thumbnail
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
        print('전국 모든 지역 순차 크롤링')
        print('='*60)

        self.setup()
        self.login()

        total_areas = len(self.areas)

        for idx, area in enumerate(self.areas, 1):
            print(f'[{idx}/{total_areas}] {area} 크롤링 중...', end=' ')

            items = self.crawl_area(area)

            if items:
                self.results.extend(items)
                print(f'✓ {len(items)}개 수집')
            else:
                print('○ 업소 없음')

            # 10개 지역마다 중간 저장
            if idx % 10 == 0:
                temp_file = f'all_areas_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                print(f'  → 중간 저장: {temp_file} (누적 {len(self.results)}개)\n')

            time.sleep(2)

        # 최종 저장
        output = f'all_areas_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f'\n{"="*60}')
        print(f'✅ 완료: {len(self.results)}개 업소 → {output}')
        print(f'{"="*60}')

        # 통계
        real_thumbs = len([x for x in self.results if x.get('thumbnail', '').startswith('https://dkxm8.com/data/file/main')])
        print(f'\n📊 통계:')
        print(f'  총 업소: {len(self.results)}개')
        print(f'  실제 썸네일: {real_thumbs}개 ({real_thumbs/len(self.results)*100:.1f}%)')

        self.driver.quit()

if __name__ == '__main__':
    crawler = AllAreasCrawler()
    crawler.run()
