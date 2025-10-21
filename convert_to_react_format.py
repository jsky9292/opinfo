#!/usr/bin/env python3
"""
크롤링 데이터를 React 앱 형식으로 변환
"""
import json
from datetime import datetime

def convert_to_react_format(input_file, output_file):
    """크롤링 데이터를 React 앱 형식으로 변환"""

    # 입력 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        crawled_data = json.load(f)

    print(f'총 {len(crawled_data)}개 업소 변환 시작...\n')

    react_data = []

    for idx, shop in enumerate(crawled_data, 1):
        # 카테고리 추출 (제목에서 [카테고리] 부분)
        title = shop.get('title', '')
        category = '기타'
        name = title

        if title.startswith('[') and ']' in title:
            end_bracket = title.index(']')
            category = title[1:end_bracket]
            name = title[end_bracket+1:].strip()

        # React 앱 형식으로 변환
        # location은 큰 지역 (대전, 서울 등), district는 세부 지역 (봉명동, 탄방동 등)
        react_shop = {
            'id': idx,
            'name': name,
            'location': shop.get('area', ''),  # 큰 지역
            'district': shop.get('district', shop.get('area', '')),  # 세부 지역 (동 이름)
            'rating': 4.5,  # 기본값
            'price': '가격 문의',
            'services': ['마사지', '힐링'],  # 기본값
            'image': shop.get('thumbnail', 'https://dkxm8.com/img/temp_thum.jpg'),
            'description': shop.get('description', ''),
            'phone': shop.get('phone', ''),
            'address': shop.get('district', shop.get('area', '')),  # 세부 지역을 주소로
            'hours': shop.get('hours', ''),
            'featured': False,
            'category': category,
            'gallery': shop.get('detail_images', [shop.get('thumbnail', '')]),
            'kakao_id': shop.get('kakao_id', ''),
            'telegram_id': shop.get('telegram_id', ''),
            'url': shop.get('url', '')
        }

        # gallery가 비어있으면 thumbnail로 채우기
        if not react_shop['gallery'] or len(react_shop['gallery']) == 0:
            react_shop['gallery'] = [react_shop['image']]

        react_data.append(react_shop)

        if idx % 50 == 0:
            print(f'  [{idx}/{len(crawled_data)}] 변환 중...')

    # 출력 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(react_data, f, ensure_ascii=False, indent=2)

    print(f'\n✅ 완료: {len(react_data)}개 업소 → {output_file}')

    # 통계 출력
    print('\n📊 통계:')
    print(f'  총 업소: {len(react_data)}개')

    # 이미지 통계
    with_images = sum(1 for s in react_data if len(s['gallery']) > 1)
    print(f'  상세 이미지 있음: {with_images}개 ({with_images/len(react_data)*100:.1f}%)')

    # 카테고리별 통계
    categories = {}
    for shop in react_data:
        cat = shop['category']
        categories[cat] = categories.get(cat, 0) + 1

    print('\n📊 카테고리별:')
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f'  {cat}: {count}개')

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # 기본값: 가장 최근 완료 파일 찾기
        import glob
        files = glob.glob('details_fixed_complete_*.json')
        if files:
            input_file = max(files, key=lambda x: x.split('_')[-1])
            print(f'📁 입력 파일: {input_file}\n')
        else:
            print('❌ 크롤링 완료 파일을 찾을 수 없습니다.')
            sys.exit(1)

    output_file = f'shops_data_react_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    convert_to_react_format(input_file, output_file)
