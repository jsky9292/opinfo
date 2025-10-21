#!/usr/bin/env python3
import json

# Load data
with open('details_fixed_complete_20251013_231951.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'총 업소: {len(data)}개')

# Check district extraction
districts = [x for x in data if x.get('district') != x.get('area')]
no_districts = [x for x in data if x.get('district') == x.get('area')]

print(f'\n세부 지역 추출 성공: {len(districts)}개 ({len(districts)/len(data)*100:.1f}%)')
print(f'세부 지역 없음: {len(no_districts)}개 ({len(no_districts)/len(data)*100:.1f}%)')

# Show samples with districts
if districts:
    print('\n=== 세부 지역 추출 성공 샘플 (10개) ===')
    import random
    samples = random.sample(districts, min(10, len(districts)))
    for x in samples:
        print(f'  {x["title"]:30s} → {x["area"]:8s} / {x["district"]}')

# Show samples without districts (to see why they failed)
if no_districts:
    print('\n=== 세부 지역 없음 샘플 (5개 - description 확인) ===')
    samples = random.sample(no_districts, min(5, len(no_districts)))
    for x in samples:
        desc = x.get('description', '')[:50]
        print(f'  {x["title"]:30s} → {x["area"]:8s} | desc: {desc}')

# Area breakdown
areas = {}
for shop in data:
    area = shop.get('area', 'Unknown')
    areas[area] = areas.get(area, 0) + 1

print('\n=== 지역별 분포 ===')
for area, count in sorted(areas.items(), key=lambda x: x[1], reverse=True):
    print(f'  {area:12s}: {count:3d}개')
