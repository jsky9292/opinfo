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
    # 첫 번째 크롤링 데이터 (0~240)
    print('첫 번째 크롤링 데이터 읽기...')
    with open('details_fixed_temp_20251012_131036.json', 'r', encoding='utf-8') as f:
        part1 = json.load(f)

    # 두 번째 크롤링 완료 파일 찾기
    import glob
    complete_files = glob.glob('details_fixed_complete_*.json')

    if complete_files:
        complete_file = sorted(complete_files)[-1]
        print(f'두 번째 크롤링 데이터 읽기: {complete_file}')
        with open(complete_file, 'r', encoding='utf-8') as f:
            part2 = json.load(f)
    else:
        # 완료 파일이 없으면 최신 임시 파일 사용
        temp_files = sorted(glob.glob('details_fixed_temp_202510*.json'))
        if len(temp_files) > 1:
            temp_file = temp_files[-1]
            print(f'임시 파일 사용: {temp_file}')
            with open(temp_file, 'r', encoding='utf-8') as f:
                part2 = json.load(f)
        else:
            part2 = []

    # 병합
    all_data = part1 + part2
    print(f'\n총 데이터: {len(part1)} + {len(part2)} = {len(all_data)}개')

    # React 형식으로 변환
    react_data = convert_to_react_format(all_data)

    # 저장
    output_file = 'shops_data_all.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(react_data, f, ensure_ascii=False, indent=2)

    print(f'✅ 변환 완료: {len(react_data)}개 → {output_file}')

    # 통계
    categories = {}
    locations = {}
    with_thumbnail = 0
    with_phone = 0
    with_hours = 0

    for shop in react_data:
        cat = shop['category']
        categories[cat] = categories.get(cat, 0) + 1

        loc = shop['location']
        locations[loc] = locations.get(loc, 0) + 1

        if shop['image'] != 'https://dkxm8.com/img/temp_thum.jpg':
            with_thumbnail += 1
        if shop['phone']:
            with_phone += 1
        if shop['hours']:
            with_hours += 1

    print(f'\n📊 통계:')
    print(f'  카테고리별:')
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f'    {cat}: {count}개')

    print(f'\n  지역별:')
    for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
        print(f'    {loc}: {count}개')

    print(f'\n  상세정보:')
    print(f'    썸네일 있음: {with_thumbnail}개 ({with_thumbnail/len(react_data)*100:.1f}%)')
    print(f'    전화번호 있음: {with_phone}개 ({with_phone/len(react_data)*100:.1f}%)')
    print(f'    영업시간 있음: {with_hours}개 ({with_hours/len(react_data)*100:.1f}%)')
