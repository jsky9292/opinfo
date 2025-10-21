#!/bin/bash

echo "=========================================="
echo "dkxm8.com 크롤러 실행"
echo "=========================================="
echo ""

# 패키지 설치 확인
echo "[1단계] 패키지 설치 확인 중..."
if ! python3 -c "import selenium" &> /dev/null; then
    echo "Selenium이 설치되지 않았습니다. 설치 중..."
    pip3 install -r requirements.txt
else
    echo "이미 설치되어 있습니다."
fi

echo ""
echo "[2단계] 크롤러 실행 중..."
echo ""

# 크롤러 실행
python3 dkxm8_crawler.py

echo ""
echo "=========================================="
echo "실행 완료! 생성된 파일을 확인하세요."
echo "=========================================="
