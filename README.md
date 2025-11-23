# Trade Safety

K-pop 굿즈 거래 안전성 AI 분석 서비스

## 주요 기능

- LLM 기반 거래글 분석
- 6개 언어 지원
- 위험 신호 탐지
- 가격 분석
- Freemium 모델

## 빠른 시작

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety/backend

poetry install
export OPENAI_API_KEY=sk-...
poetry run uvicorn trade_safety.main:app --reload
```

접속: http://localhost:8000/docs

## 문서

- [통합 가이드](docs/integration-guide.md) - FastAPI/React 프로젝트 통합
- [기여 가이드](CONTRIBUTING.md) - 개발 환경 및 PR
- [개발 원칙](CLAUDE.md) - 아키텍처 및 코드 품질

## 라이선스

Apache 2.0
