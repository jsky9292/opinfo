# OpInfo - 업소 정보 플랫폼

대전/충청권 업소 정보를 제공하는 웹 애플리케이션입니다.

## 기술 스택

### Frontend
- React 18
- TypeScript
- Vite
- React Router
- Lucide Icons

### Backend
- Node.js + Express
- MongoDB + Mongoose
- JWT 인증
- CORS

## 프로젝트 구조

```
opinfo2/
├── src/                    # React 프론트엔드
│   ├── components/         # 재사용 컴포넌트
│   ├── pages/              # 페이지 컴포넌트
│   │   ├── admin/          # 관리자 페이지
│   │   └── auth/           # 인증 페이지
│   ├── data/               # 정적 데이터 (shops_data.json)
│   └── App.tsx             # 메인 앱
│
├── server/                 # Express 백엔드
│   ├── routes/             # API 라우트
│   ├── models/             # MongoDB 모델
│   ├── middleware/         # 인증 미들웨어
│   ├── config/             # 데이터베이스 설정
│   └── index.js            # 서버 엔트리포인트
│
└── package.json            # 프로젝트 의존성
```

## 설치 및 실행

### 1. 의존성 설치
```bash
npm install
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```env
MONGODB_URI=mongodb://localhost:27017/opinfo
JWT_SECRET=your_jwt_secret_key
PORT=5000
```

### 3. 개발 서버 실행
```bash
npm run dev
```

- Frontend: http://localhost:3004
- Backend: http://localhost:5000

## 주요 기능

### 사용자 기능
- 업소 목록 조회 (지역, 카테고리 필터)
- 업소 상세 정보 보기
- 검색 기능

### 관리자 기능 (예정)
- 업소 관리 (생성, 수정, 삭제)
- 회원 관리

## 데이터

### shops_data.json
461개 대전/충청권 업소 정보:
- 업소명, 위치, 세부 지역
- 썸네일 및 상세 이미지
- 연락처, 영업시간, 설명
- 카카오톡, 텔레그램 링크

## API 엔드포인트

### 인증
- `POST /api/auth/signup` - 회원가입
- `POST /api/auth/login` - 로그인

### 업소 (예정)
- `GET /api/shops` - 업소 목록
- `GET /api/shops/:id` - 업소 상세
- `POST /api/shops` - 업소 생성 (관리자)
- `PUT /api/shops/:id` - 업소 수정 (소유자/관리자)
- `DELETE /api/shops/:id` - 업소 삭제 (소유자/관리자)

## 배포

추후 Vercel/Netlify (프론트엔드) + Railway/Render (백엔드) 배포 예정

## 라이선스

MIT
