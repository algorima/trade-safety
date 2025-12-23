# Trade Safety Backend

K-pop 굿즈 거래 안전성 AI 분석 Python 패키지

## 주요 기능

- LLM 기반 거래글 분석
- 다국어 지원 (한국어 번역 및 뉘앙스 설명)
- 위험 신호 탐지 (결제, 판매자, 플랫폼, 가격, 콘텐츠)
- 시장가 대비 가격 분석
- Freemium 모델

## 설치

```bash
cd backend
poetry install
```

## 사용법

### 서비스 사용

```python
from aioia_core.settings import OpenAIAPISettings
from trade_safety.service import TradeSafetyService
from trade_safety.settings import TradeSafetyModelSettings

openai_api = OpenAIAPISettings(api_key="sk-...")
model_settings = TradeSafetyModelSettings()
service = TradeSafetyService(
    openai_api=openai_api,
    model_settings=model_settings,
)

analysis = await service.analyze_trade("급처분 양도해요")
print(f"위험도: {analysis.risk_score}/100")
```

### FastAPI 통합

```python
from trade_safety.api.router import create_trade_safety_router

router = create_trade_safety_router(app_config)
app.include_router(router, prefix="/api/v2")
```

## 개발

```bash
poetry install
poetry run make test
poetry run make lint
poetry run make type-check
poetry run make format
```

## 환경 변수

| 변수명 | 필수 | 설명 |
|--------|------|------|
| `OPENAI_API_KEY` | O | OpenAI API 키 |
| `TWITTER_BEARER_TOKEN` | X | Twitter/X URL 분석용 (미설정 시 URL 분석 불가) |

## 의존성

- aioia-core (공통 인프라)
- FastAPI, SQLAlchemy, Pydantic
- OpenAI API 키 필요

## 라이선스

Apache 2.0
