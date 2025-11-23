# 통합 가이드

Trade Safety는 **독립 실행(Standalone)** 및 **라이브러리 통합** 두 가지 방식으로 사용 가능합니다.

## 구조

**Backend**: `trade_safety/` (라이브러리) + `main.py` (standalone)
**Frontend**: `src/components/` (라이브러리) + `src/app/` (standalone)

---

## Standalone 실행

### Backend
```bash
cd backend
poetry install
export OPENAI_API_KEY=sk-...
export JWT_SECRET_KEY=your-secret
poetry run uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 라이브러리로 통합

## FastAPI 프로젝트

### 설치

```bash
pip install git+https://github.com/algorima/trade-safety.git#subdirectory=backend
```

### 사용

```python
from trade_safety import TradeSafetyService
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
npm install @trade-safety/react @aioia/core
```

### 컴포넌트

```tsx
import { DetailedResult } from "@trade-safety/react";

<DetailedResult analysis={analysis} />
```

### Repository

```tsx
import { TradeSafetyRepository } from "@trade-safety/react";

const repository = new TradeSafetyRepository(apiService);
await repository.create({ input_text: "..." });
```

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
