# 기여 가이드

## 개발 환경

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety

# Backend
cd backend
poetry install
make unit-test

# Frontend
cd frontend
npm install
npm run build
```

## PR 제출

1. Feature 브랜치 생성
2. 코드 작성 + 테스트
3. Conventional Commits 형식 (제목은 한국어)
4. PR 생성 (CLA 서명 필요)

## 코드 품질

### Backend
```bash
make format
make lint
make type-check
make unit-test
```

### Frontend
```bash
npm run lint
npm run type-check
npm test
```

## CLA 서명

첫 PR 시 CLA Assistant 봇이 안내합니다.
