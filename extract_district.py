#!/usr/bin/env python3
"""
크롤링 데이터에서 상세 동네 정보 추출
"""

import json
import re
from datetime import datetime

# 동네 키워드 패턴 (구, 동, 읍, 면)
DISTRICT_PATTERNS = [
    r'([가-힣]+구)',  # ~구 (예: 유성구, 서구, 중구)
    r'([가-힣]+동)',  # ~동 (예: 탄방동, 관저동, 둔산동)
    r'([가-힣]+읍)',  # ~읍
    r'([가-힣]+면)',  # ~면
]

def extract_district_from_description(description):
    """설명에서 동네 정보 추출"""
    if not description:
        return None

    # 이모지와 특수문자 제거
    cleaned = re.sub(r'[✨❤️💕💎✅🔥💯👑⭐🎁🎉🌸🌹💐]', '', description)
    cleaned = re.sub(r'[▶◀♥★☆]', '', cleaned)

    # 패턴 매칭
    for pattern in DISTRICT_PATTERNS:
        matches = re.findall(pattern, cleaned)
        if matches:
            # 첫 번째 매칭된 동네 반환
            return matches[0]

    return None

def main():
    # 크롤링 데이터 로드
    input_file = "all_regions_crawl_20251009_192537.json"

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📂 파일 로드: {input_file}")
    print(f"📊 총 {len(data)}개 업체\n")

    # 통계
    stats = {
        'total': len(data),
        'extracted': 0,
        'not_found': 0,
        'by_region': {}
    }

    # 각 업체 처리
    for idx, item in enumerate(data, 1):
        area = item.get('area', '')
        description = item.get('description', '')

        # 동네 정보 추출
        district = extract_district_from_description(description)

        if district:
            item['district'] = district
            stats['extracted'] += 1

            # 지역별 통계
            if area not in stats['by_region']:
                stats['by_region'][area] = {'total': 0, 'extracted': 0}
            stats['by_region'][area]['total'] += 1
            stats['by_region'][area]['extracted'] += 1

            print(f"[{idx}/{len(data)}] {item['title'][:20]:20s} | {area:6s} → {district}")
        else:
            item['district'] = area  # 추출 실패 시 area 사용
            stats['not_found'] += 1

            if area not in stats['by_region']:
                stats['by_region'][area] = {'total': 0, 'extracted': 0}
            stats['by_region'][area]['total'] += 1

            print(f"[{idx}/{len(data)}] {item['title'][:20]:20s} | {area:6s} → (없음, area 사용)")

    # 저장
    output_file = f"districts_extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print(f"✅ 완료! 파일 저장: {output_file}")
    print(f"{'='*70}\n")

    # 통계 출력
    print("📊 통계:")
    print(f"   전체: {stats['total']}개")
    print(f"   동네 추출 성공: {stats['extracted']}개 ({stats['extracted']/stats['total']*100:.1f}%)")
    print(f"   동네 추출 실패: {stats['not_found']}개\n")

    print("📍 지역별 통계:")
    for region, count in stats['by_region'].items():
        success_rate = count['extracted'] / count['total'] * 100 if count['total'] > 0 else 0
        print(f"   {region}: {count['extracted']}/{count['total']} ({success_rate:.1f}%)")

if __name__ == "__main__":
    main()
