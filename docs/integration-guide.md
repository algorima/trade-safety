# 통합 가이드

기존 프로젝트에 Trade Safety 라이브러리를 통합하는 방법

> Standalone 실행: [README.md](../README.md) 참조

## 라이브러리로 통합

## FastAPI 프로젝트

### 설치

```bash
pip install git+https://github.com/algorima/trade-safety.git#subdirectory=backend
```

### 사용

```python
from trade_safety.service import TradeSafetyService
from trade_safety.settings import TradeSafetyModelSettings

settings = TradeSafetyModelSettings()
service = TradeSafetyService(settings)

analysis = await service.analyze_trade("거래글 내용")
```

### FastAPI 라우터

```python
from trade_safety.api.router import create_trade_safety_router

router = create_trade_safety_router(app_config)
app.include_router(router, prefix="/api")
```

### 환경 변수

```bash
export DATABASE_URL=postgresql://...
export OPENAI_API_KEY=sk-...
```

---

## React/Next.js 프로젝트

### 설치

```bash
npm install trade-safety @aioia/core
```

### Tailwind 설정 (필수)

```ts
// tailwind.config.ts
content: [
  "./src/**/*.{js,ts,jsx,tsx}",
  "./node_modules/trade-safety/dist/**/*.{js,jsx,ts,tsx}",
  "./node_modules/@aioia/core/dist/**/*.{js,jsx,ts,tsx}",
]
```

### 컴포넌트

```tsx
import { DetailedResult } from "trade-safety";

<DetailedResult analysis={analysis} />
```

### Repository

```tsx
import { TradeSafetyRepository } from "trade-safety";

const repository = new TradeSafetyRepository(apiService);
await repository.create({ input_text: "..." });
```

### i18n 통합

```tsx
import { tradeSafetyTranslations, TRADE_SAFETY_NS } from "trade-safety/locale";

// 호스트 앱의 i18n 인스턴스에 번역 리소스 추가
Object.entries(tradeSafetyTranslations).forEach(([lang, resources]) => {
  i18n.addResourceBundle(lang, TRADE_SAFETY_NS, resources);
});
```

지원 언어: `en`, `ko`, `ja`, `zh`, `es`, `id`

---

## 데이터베이스

### Migration

```bash
cd trade-safety/backend
alembic upgrade head
```

### 테이블

`trade_safety_checks`: 분석 결과 (user_id: nullable, FK 없음)

## 개발

```bash
# Backend
make format lint type-check

# Frontend
npm run lint type-check
npm run build:lib  # 라이브러리만 빌드
```
