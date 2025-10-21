#!/usr/bin/env python3
"""
전체 지역 크롤링 데이터를 React 앱 형식으로 변환
"""

import json

# 크롤링 데이터 로드
with open('all_regions_crawl_20251009_192537.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 지역 매핑 (region → location)
REGION_TO_LOCATION = {
    "대전/충청": "대전",
    "부산/경남": "부산",
    "서울/강남": "서울",
    "인천/경기": "인천",
    "대구/경북": "대구",
    "광주/전라": "광주",
    "강원/제주/전라": "강원"
}

# 카테고리 매핑 (이름에서 추출)
def extract_category(title):
    if '[오피스텔]' in title:
        return '오피스텔'
    elif '[건마]' in title:
        return '건마'
    elif '[휴게텔]' in title:
        return '휴게텔'
    elif '[안마]' in title:
        return '안마'
    elif '[유흥주점]' in title or '[룸/풀사롱]' in title:
        return '유흥/밤'
    elif '[핸플/립]' in title:
        return '핸플/립'
    elif '[키스방]' in title:
        return '키스방'
    elif '[토핑/리얼]' in title:
        return '토핑/리얼'
    else:
        return '오피스텔'

# React 앱 형식으로 변환
converted_data = []
for idx, item in enumerate(raw_data, 1):
    title = item.get('title', '').replace('[오피스텔]', '').replace('[건마]', '').replace('[휴게텔]', '').replace('[안마]', '').replace('[유흥주점]', '').replace('[룸/풀사롱]', '').replace('[핸플/립]', '').replace('[키스방]', '').replace('[토핑/리얼]', '').strip()

    region_name = item.get('region', '대전/충청')
    location = REGION_TO_LOCATION.get(region_name, '대전')

    shop = {
        'id': idx,
        'name': title,
        'location': location,
        'district': item.get('area', '유성구'),
        'rating': 4.5,
        'price': '60,000원~',
        'services': ['전신마사지', '힐링케어'],
        'image': item.get('thumbnail', ''),
        'description': item.get('description', ''),
        'phone': item.get('phone', ''),
        'address': f"{location}시 {item.get('area', '유성구')}",
        'hours': item.get('hours', '09:00 - 24:00'),
        'featured': idx <= 10,
        'category': extract_category(item.get('title', '')),
        'gallery': item.get('detail_images', []),
        'kakao_id': item.get('kakao_id', ''),
        'telegram_id': item.get('telegram_id', ''),
        'url': item.get('url', '')
    }
    converted_data.append(shop)

# 저장
output_file = 'all_shops_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=2)

print(f"✅ 변환 완료! {len(converted_data)}개 업체")
print(f"💾 파일 저장: {output_file}")

# 통계 출력
print("\n📊 카테고리별 통계:")
categories = {}
for shop in converted_data:
    cat = shop['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"   {cat}: {count}개")

print(f"\n📍 지역별 통계:")
locations = {}
for shop in converted_data:
    loc = shop['location']
    locations[loc] = locations.get(loc, 0) + 1

for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
    print(f"   {loc}: {count}개")

print(f"\n🏙️  도시별 통계 (상위 10개):")
districts = {}
for shop in converted_data:
    dist = shop['district']
    districts[dist] = districts.get(dist, 0) + 1

for dist, count in sorted(districts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"   {dist}: {count}개")
