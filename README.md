# Trade Safety

K-pop 굿즈 거래 안전성 AI 분석 서비스

## 주요 기능

- LLM 기반 거래글 분석
- 6개 언어 지원
- 위험 신호 탐지
- 가격 분석
- Freemium 모델

## 프로젝트 구조

```
trade-safety/
├── backend/          # FastAPI 앱 + 라이브러리
│   ├── trade_safety/ # 라이브러리 모듈 (다른 프로젝트에서 import 가능)
│   └── main.py       # Standalone 앱 entry point
└── frontend/         # Next.js 앱 + React 컴포넌트 라이브러리
    ├── src/app/      # Next.js App Router (standalone)
    ├── src/components/ # React 컴포넌트 (라이브러리로 export)
    └── package.json
```

## 빠른 시작

### Backend (FastAPI)

```bash
cd trade-safety/backend
poetry install
export OPENAI_API_KEY=sk-...
export JWT_SECRET_KEY=your-secret-key
poetry run uvicorn main:app --reload
```

접속: http://localhost:8000/docs

### Frontend (Next.js)

```bash
cd trade-safety/frontend
npm install
npm run dev
```

접속: http://localhost:3000

## 문서

- [통합 가이드](docs/integration-guide.md) - FastAPI/React 프로젝트 통합
- [기여 가이드](CONTRIBUTING.md) - 개발 환경 및 PR
- [개발 원칙](CLAUDE.md) - 아키텍처 및 코드 품질

## 라이선스

Apache 2.0
