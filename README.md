# Trade Safety

[![Status](https://img.shields.io/website?url=https%3A%2F%2Faioia.ai%2Ftrade-safety&label=Status)](https://aioia.ai/trade-safety)

K-pop 굿즈 거래글 AI 분석 서비스

---

## 주요 기능

- LLM 기반 거래글 분석 (한국어 슬랭 이해)
- 사기 신호 탐지 (Risk Signals, Cautions, Safe Indicators)
- 가격 분석 (시세 비교)
- 안전 체크리스트
- 감정 지원 (FOMO 완화)
- 6개 언어 지원
- Freemium 모델

---

## 빠른 시작

### Backend

```bash
cd backend
poetry install
export OPENAI_API_KEY=sk-...
poetry run uvicorn main:app --reload
```

접속: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

접속: http://localhost:3000

---

## 라이브러리 사용

기존 프로젝트에 통합하려면 [통합 가이드](docs/integration-guide.md)를 참조하세요.

---

## 프로젝트 구조

```
backend/
├── trade_safety/  # 라이브러리
└── main.py        # Standalone 앱

frontend/
├── src/app/       # Next.js
└── src/components/ # 라이브러리
```

---

## 문서

- [통합 가이드](docs/integration-guide.md)
- [기여 가이드](CONTRIBUTING.md)
- [개발 원칙](CLAUDE.md)

---

## 라이선스

Apache 2.0
