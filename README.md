# Trade Safety

K-pop 굿즈 거래 안전성 AI 분석 서비스

## 주요 기능

- 🤖 **LLM 기반 분석**: GPT-4/Claude로 거래글 종합 분석
- 🌍 **다국어 지원**: 6개 언어 (한국어, 영어, 일본어, 중국어, 스페인어, 인도네시아어)
- ⚠️ **위험 신호 탐지**: 결제, 판매자, 플랫폼, 가격, 콘텐츠 카테고리별 분류
- 💰 **가격 분석**: 시장가 대비 적정성 평가
- 📝 **안전 체크리스트**: 실천 가능한 검증 단계 제공
- 🔓 **Freemium 모델**: 비로그인 사용자 요약, 로그인 사용자 상세 분석

## 빠른 시작

### 독립 실행 (Docker)

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety

# 환경 변수 설정 후 실행
OPENAI_API_KEY=sk-... docker-compose up
```

**접속**: http://localhost:8000/docs

환경 변수 목록은 `.env.example` 참조

### Buppy 통합

```bash
cd /path/to/buppy
git submodule add https://github.com/algorima/trade-safety.git trade-safety
git submodule update --init
```

상세 가이드: [docs/integration-guide.md](docs/integration-guide.md)

## 프로젝트 구조

```
trade-safety/
├── backend/trade_safety/
│   ├── schemas.py                      # Pydantic 도메인 스키마
│   ├── prompts.py                      # 시스템 프롬프트
│   ├── service.py                      # LLM 분석 비즈니스 로직
│   ├── models.py                       # SQLAlchemy DB 모델
│   ├── repositories/                   # Repository 패턴 (데이터 접근)
│   │   └── trade_safety_repository.py
│   ├── api/                            # FastAPI 엔드포인트
│   │   └── router.py
│   ├── _vendor/                        # Buppy 복사 코드 (임시)
│   │   ├── config.py
│   │   ├── database.py
│   │   └── errors.py
│   └── main.py                         # Standalone 진입점
│
├── frontend/src/
│   ├── components/                     # UI 컴포넌트
│   ├── repositories/                   # Repository 패턴 (API 접근)
│   │   └── TradeSafetyRepository.ts
│   ├── types.ts                        # TypeScript 타입
│   └── i18n/                           # 다국어 번역
│
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## 사용 방법

### Python 라이브러리

```python
from trade_safety import TradeSafetyService
from trade_safety._vendor.config import TradeSafetyConfig

config = TradeSafetyConfig.from_env()
service = TradeSafetyService(config)

analysis = await service.analyze_trade("급처분 양도해요")
print(f"위험도: {analysis.risk_score}/100")
```

### REST API

```bash
curl -X POST http://localhost:8000/trade-safety \
  -H "Content-Type: application/json" \
  -d '{"input_text": "급처분 양도해요"}'
```

### React 컴포넌트

```tsx
import { DetailedResult } from "@trade-safety/react";

<DetailedResult analysis={analysis} />
```

## 개발 환경

### Backend

```bash
cd backend
pip install -e ".[dev]"
pytest
black trade_safety
mypy trade_safety
```

### Frontend

```bash
cd frontend
npm install
npm run build
```

## 요구사항

- Python 3.10-3.12
- PostgreSQL
- OpenAI 또는 Anthropic API 키

## 문서

- [Buppy 통합 가이드](docs/integration-guide.md)
- [기여 가이드](CONTRIBUTING.md)
- [개발 원칙](CLAUDE.md)

## 라이선스

Apache 2.0

## 문의

이슈: https://github.com/algorima/trade-safety/issues
