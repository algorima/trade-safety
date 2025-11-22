# Trade Safety

K-pop 굿즈 거래 안전성 AI 분석 서비스

## 주요 기능

- 🤖 LLM 기반 거래글 분석
- 🌍 6개 언어 지원 (한국어, 영어, 일본어, 중국어, 스페인어, 인도네시아어)
- ⚠️ 위험 신호 탐지 (결제, 판매자, 플랫폼, 가격, 콘텐츠)
- 💰 시장가 대비 가격 분석
- 📝 안전 체크리스트 제공
- 🔓 Freemium 모델

## 빠른 시작

### Docker 실행

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety

# 환경 변수 설정 후 실행
OPENAI_API_KEY=sk-... docker-compose up
```

http://localhost:8000/docs 접속

환경 변수 목록: `.env.example` 참조

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

## 개발 환경

```bash
# Backend
cd backend
pip install -e ".[dev]"
pytest

# Frontend
cd frontend
npm install
npm run build
```

## 요구사항

- Python 3.10-3.12
- PostgreSQL
- OpenAI API 키

## 문서

- [통합 가이드](docs/integration-guide.md)
- [기여 가이드](CONTRIBUTING.md)
- [개발 원칙](CLAUDE.md)

## 라이선스

Apache 2.0
