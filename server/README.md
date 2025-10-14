# Opinfo Backend Server

## MongoDB 설치 방법

### Windows
1. MongoDB Community Edition 다운로드: https://www.mongodb.com/try/download/community
2. 설치 프로그램 실행
3. "Complete" 설치 선택
4. MongoDB Compass 설치 옵션 선택 (GUI 도구)
5. 서비스로 설치 옵션 선택

### MongoDB 서비스 시작
```bash
# Windows Services에서 MongoDB 시작
net start MongoDB

# 또는 MongoDB Compass를 사용하여 GUI로 관리
```

## 서버 실행 방법

### 1. 의존성 설치
```bash
cd server
npm install
```

### 2. 환경 변수 설정
`.env` 파일이 이미 생성되어 있습니다. 필요시 수정하세요.

### 3. MongoDB 연결 확인
MongoDB가 실행 중인지 확인:
```bash
# MongoDB 연결 테스트
mongosh
```

### 4. 관리자 계정 생성
```bash
npm run create-admin
```

생성되는 관리자 계정:
- **Username**: `admin`
- **Password**: `admin12345`
- **Email**: `admin@opinfo.com`
- **Role**: `admin`

### 5. 서버 시작
```bash
# 개발 모드 (자동 재시작)
npm run dev

# 프로덕션 모드
npm start
```

## API 엔드포인트

### 인증 API
- `POST /api/auth/signup` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 사용자 정보 조회 (인증 필요)

### 요청 예시

#### 회원가입
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "phone": "010-1234-5678"
  }'
```

#### 로그인
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin12345"
  }'
```

#### 사용자 정보 조회
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 보안 주의사항

1. **비밀번호 변경**: 관리자 계정 생성 후 반드시 비밀번호를 변경하세요
2. **JWT_SECRET 변경**: 프로덕션 환경에서는 `.env` 파일의 JWT_SECRET을 강력한 값으로 변경하세요
3. **HTTPS 사용**: 프로덕션 환경에서는 반드시 HTTPS를 사용하세요

## 프론트엔드 연동

프론트엔드에서 API 호출 시:
```typescript
const API_URL = 'http://localhost:5000/api';

// 로그인
const response = await fetch(`${API_URL}/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

const data = await response.json();
// data.data.token을 localStorage에 저장
```
