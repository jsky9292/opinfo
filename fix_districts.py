#!/usr/bin/env python3
"""
이미 크롤링된 데이터에 원본 description에서 district를 추출하여 추가
"""
import json
import re

# 1. 원본 입력 파일 읽기 (description 있음)
with open('daejeon_chungcheong_all_20251009_220324.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

# 2. 크롤링 완료 파일 읽기 (이미지 있음)
with open('details_fixed_complete_20251013_231951.json', 'r', encoding='utf-8') as f:
    crawled_data = json.load(f)

print(f'원본 데이터: {len(original_data)}개')
print(f'크롤링 데이터: {len(crawled_data)}개')

# 3. URL을 key로 하는 dict 생성
original_dict = {item['url']: item for item in original_data}

# 4. 크롤링 데이터에 세부 지역 추가
fixed_count = 0
for shop in crawled_data:
    url = shop['url']

    # 원본 데이터에서 description 찾기
    if url in original_dict:
        original_desc = original_dict[url].get('description', '')

        # description에서 "동" 추출
        if original_desc:
            district_match = re.search(r'([가-힣]+동)', original_desc)
            if district_match:
                extracted_district = district_match.group(1)
                shop['district'] = extracted_district
                fixed_count += 1

print(f'\n✅ 세부 지역 추출 성공: {fixed_count}개 ({fixed_count/len(crawled_data)*100:.1f}%)')

# 5. 저장
output_file = 'details_fixed_with_districts.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(crawled_data, f, ensure_ascii=False, indent=2)

print(f'💾 저장 완료: {output_file}')

# 6. 샘플 출력
print('\n📝 샘플 (세부 지역 추출됨):')
samples = [x for x in crawled_data if x['district'] != x['area']][:10]
for s in samples:
    print(f'  {s["title"]:30s} → {s["area"]:8s} / {s["district"]}')
