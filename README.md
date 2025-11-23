# Trade Safety

K-pop 굿즈 거래 안전성 AI 분석 서비스

## 주요 기능

- 🤖 LLM 기반 거래글 분석
- 🌍 6개 언어 지원
- ⚠️ 위험 신호 탐지
- 💰 시장가 대비 가격 분석
- 📝 안전 체크리스트
- 🔓 Freemium 모델

## 빠른 시작

### Docker

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety
OPENAI_API_KEY=sk-... docker-compose up
```

http://localhost:8000/docs 접속

### Python

```python
from trade_safety import TradeSafetyService
from trade_safety.settings import TradeSafetyModelSettings

settings = TradeSafetyModelSettings()
service = TradeSafetyService(settings)

analysis = await service.analyze_trade("급처분 양도해요")
print(f"위험도: {analysis.risk_score}/100")
```

### API

```bash
curl -X POST http://localhost:8000/trade-safety \
  -H "Content-Type: application/json" \
  -d '{"input_text": "급처분 양도해요"}'
```

## 개발

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
