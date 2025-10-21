#!/usr/bin/env python3
import json
import re

def extract_category(title):
    """제목에서 카테고리 추출"""
    match = re.search(r'\[(.*?)\]', title)
    if match:
        cat = match.group(1)
        cat_map = {
            '건마': '건마',
            '휴게텔': '휴게텔',
            '오피스텔': '오피스텔',
            '오피': '오피스텔',
            '안마': '안마',
            '룸/풀사롱': '룸/풀사롱',
            '주점': '룸/풀사롱',
            '키스방': '키스방',
            '립카페': '키스방',
            '유흥주점': '룸/풀사롱',
            '트젠/리얼': '기타'
        }
        return cat_map.get(cat, '기타')
    return '기타'

def clean_name(title):
    """제목에서 [카테고리] 제거"""
    return re.sub(r'\[.*?\]\s*', '', title).strip()

def convert_to_react_format(crawled_data):
    """크롤링 데이터를 React 형식으로 변환"""
    result = []

    for idx, item in enumerate(crawled_data, 1):
        category = extract_category(item['title'])
        name = clean_name(item['title'])

        shop = {
            'id': idx,
            'name': name,
            'location': item.get('area', ''),
            'district': item.get('area', ''),
            'rating': round(4.0 + (idx % 10) * 0.1, 1),
            'price': '문의',
            'services': [],
            'image': item.get('thumbnail', 'https://dkxm8.com/img/temp_thum.jpg'),
            'description': item.get('description', ''),
            'phone': item.get('phone', ''),
            'address': f"{item.get('area', '')}시",
            'hours': item.get('hours', ''),
            'featured': idx <= 20,
            'category': category,
            'url': item.get('url', ''),
            'kakao_id': item.get('kakao_id', ''),
            'telegram_id': item.get('telegram_id', '')
        }
        result.append(shop)

    return result

if __name__ == '__main__':
    # 크롤링된 데이터 읽기
    with open('details_fixed_temp_20251012_131036.json', 'r', encoding='utf-8') as f:
        crawled = json.load(f)

    print(f'크롤링 데이터: {len(crawled)}개')

    # React 형식으로 변환
    react_data = convert_to_react_format(crawled)

    # 저장
    output_file = 'shops_data_240.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(react_data, f, ensure_ascii=False, indent=2)

    print(f'✅ 변환 완료: {len(react_data)}개 → {output_file}')

    # 샘플 출력
    print(f'\n샘플 데이터:')
    print(json.dumps(react_data[0], ensure_ascii=False, indent=2))
