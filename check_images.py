#!/usr/bin/env python3
import json

data = json.load(open('details_fixed_complete_20251012_134600.json', encoding='utf-8'))
sample = data[0]

print('=== 샘플 데이터 ===')
print(f'제목: {sample.get("title")}')
print(f'지역: {sample.get("area")}')
print(f'썸네일: {sample.get("thumbnail", "없음")[:50]}')
detail_images = sample.get("detail_images", [])
print(f'상세이미지: {len(detail_images)}개')
if detail_images:
    print(f'첫번째: {detail_images[0][:60]}')

print('\n=== 전체 통계 ===')
total = len(data)
with_details = sum(1 for x in data if x.get('detail_images'))
print(f'총 업소: {total}개')
print(f'상세이미지 있음: {with_details}개')
print(f'비율: {with_details/total*100:.1f}%')
