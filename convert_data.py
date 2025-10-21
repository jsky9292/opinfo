"""
크롤링 데이터를 React 앱에서 사용할 형식으로 변환하는 스크립트
"""
import json
from datetime import datetime

def convert_crawled_to_react_format(input_file, output_file):
    """크롤링된 JSON을 React MassageShop 형식으로 변환"""

    # 크롤링 데이터 로드
    with open(input_file, 'r', encoding='utf-8') as f:
        crawled_data = json.load(f)

    # items 배열 추출
    items = crawled_data.get('items', [])

    # React 형식으로 변환
    react_shops = []

    for idx, item in enumerate(items, 1):
        # 카테고리는 업종으로 매핑 (오피스텔, 건마 등)
        # 제목이나 설명에서 업종 추출
        service_type = '오피스텔'  # 기본값
        title_lower = item.get('title', '').lower()
        if '건마' in title_lower or '건전' in title_lower:
            service_type = '건마'
        elif '핸플' in title_lower or '립' in title_lower:
            service_type = '핸플/립'
        elif '유흥' in title_lower or '밤' in title_lower:
            service_type = '유흥/밤'
        elif '주점' in title_lower:
            service_type = '유흥주점'
        elif '안마' in title_lower:
            service_type = '안마'
        elif '휴게텔' in title_lower:
            service_type = '휴게텔'
        elif '키스방' in title_lower:
            service_type = '키스방'
        elif '토핑' in title_lower or '리얼' in title_lower:
            service_type = '토핑/리얼'

        # 지역 파싱 (카테고리에서 지역 추출)
        location_map = {
            '대전/충청': ('대전', '유성구'),
            '부산/경남': ('부산', '해운대구'),
            '서울/강남': ('서울', '강남구'),
            '인천/경기': ('인천', '연수구'),
            '대구/경북': ('대구', '중구'),
            '강원/제주/전라': ('강원', '춘천시'),
            '메인페이지': ('서울', '강남구')
        }

        category = item.get('category', '메인페이지')
        location, district = location_map.get(category, ('서울', '강남구'))

        # 서비스 목록 생성 (description이나 title에서 추출 가능)
        services = []
        if '스웨디시' in item.get('title', ''):
            services.append('스웨디시')
        if '아로마' in item.get('title', ''):
            services.append('아로마')
        if '타이' in item.get('title', ''):
            services.append('타이마사지')
        if not services:
            services = ['전신마사지', '힐링케어']

        # React Shop 객체 생성
        react_shop = {
            'id': idx,
            'name': item.get('title', f'업소 {idx}').replace('[오피스텔]', '').replace('[건마]', '').strip(),
            'location': location,
            'district': district,
            'rating': round(4.3 + (idx % 7) * 0.1, 1),  # 4.3-4.9 사이 랜덤
            'price': '60,000원~',  # 기본값 (추후 수정 가능)
            'services': services,
            'image': item.get('thumbnail', 'https://via.placeholder.com/400x300'),
            'description': item.get('description', '')[:100] or '편안한 힐링 공간에서 최고의 마사지 서비스를 제공합니다.',
            'phone': item.get('phone', ''),
            'address': f'{location}시 {district}',
            'hours': item.get('hours', '09:00 - 22:00'),
            'featured': idx <= 6,  # 처음 6개는 추천
            'category': service_type,
            'gallery': item.get('detail_images', []),  # 모든 이미지
            'detailDescription': item.get('description', '') or '프리미엄 마사지 서비스를 제공하는 전문 업소입니다.',
            'kakao_id': item.get('kakao_id', ''),
            'telegram_id': item.get('telegram_id', ''),
            'url': item.get('url', ''),
            'amenities': ['무료 주차', '샤워시설', '개인 락커', 'WiFi', '수건 제공'],
            'businessHours': {
                '월요일': item.get('hours', '09:00 - 22:00'),
                '화요일': item.get('hours', '09:00 - 22:00'),
                '수요일': item.get('hours', '09:00 - 22:00'),
                '목요일': item.get('hours', '09:00 - 22:00'),
                '금요일': item.get('hours', '09:00 - 23:00'),
                '토요일': item.get('hours', '09:00 - 23:00'),
                '일요일': '10:00 - 21:00'
            },
            'priceList': [
                {
                    'service': '전신 마사지',
                    'duration': '60분',
                    'price': '60,000원',
                    'description': '전신 마사지로 근육 이완과 혈액순환 개선'
                },
                {
                    'service': '프리미엄 마사지',
                    'duration': '90분',
                    'price': '90,000원',
                    'description': '프리미엄 오일을 사용한 특별 케어'
                }
            ],
            'reviews': [
                {
                    'id': 1,
                    'userName': '만족한 고객',
                    'rating': 5,
                    'comment': '정말 만족스러운 서비스였습니다!',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'service': '전신 마사지'
                }
            ]
        }

        react_shops.append(react_shop)

    # JSON 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(react_shops, f, ensure_ascii=False, indent=2)

    print(f"✅ 변환 완료!")
    print(f"   입력: {input_file}")
    print(f"   출력: {output_file}")
    print(f"   변환된 업소 수: {len(react_shops)}개")

    # 통계 출력
    print(f"\n📊 변환 통계:")
    print(f"   - 카카오톡 ID 있는 업소: {sum(1 for s in react_shops if s['kakao_id'])}개")
    print(f"   - 텔레그램 ID 있는 업소: {sum(1 for s in react_shops if s['telegram_id'])}개")
    print(f"   - 갤러리 이미지 있는 업소: {sum(1 for s in react_shops if s['gallery'])}개")
    print(f"   - 평균 갤러리 이미지 수: {sum(len(s['gallery']) for s in react_shops) / len(react_shops):.1f}개")

if __name__ == '__main__':
    # 가장 최신 크롤링 파일 찾기
    import glob
    import os

    crawl_files = glob.glob('crawl_results_*.json')
    if not crawl_files:
        print("❌ 크롤링 결과 파일을 찾을 수 없습니다.")
        exit(1)

    # 최신 파일 선택
    latest_file = max(crawl_files, key=os.path.getctime)
    output_file = 'shops_data.json'

    print(f"🔄 데이터 변환 시작...")
    print(f"   소스: {latest_file}")

    convert_crawled_to_react_format(latest_file, output_file)
