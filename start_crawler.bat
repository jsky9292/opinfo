@echo off
chcp 65001 > nul
echo ==========================================
echo dkxm8.com 크롤러 실행
echo ==========================================
echo.

REM 패키지 설치 확인
echo [1단계] 패키지 설치 확인 중...
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo Selenium이 설치되지 않았습니다. 설치 중...
    pip install -r requirements.txt
) else (
    echo 이미 설치되어 있습니다.
)

echo.
echo [2단계] 크롤러 실행 중...
echo.

REM 크롤러 실행
python dkxm8_crawler.py

echo.
echo ==========================================
echo 실행 완료! 생성된 파일을 확인하세요.
echo ==========================================
pause
