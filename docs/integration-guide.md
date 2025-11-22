# Buppy 통합 가이드

## 서브모듈 추가

```bash
cd /path/to/buppy
git submodule add https://github.com/algorima/trade-safety.git trade-safety
git submodule update --init
```

## Backend 통합

### 1. 패키지 설치

**pyproject.toml:**
```toml
[tool.poetry.dependencies]
trade-safety = {path = "../trade-safety/backend", develop = true}
```

```bash
poetry install
```

### 2. Router 등록

**backend/fastapi_app/__init__.py:**
```python
from trade_safety.api.router import create_trade_safety_router

router = create_trade_safety_router(app_config)
app.include_router(router)
```

## Frontend 통합

### 1. 패키지 설치

**package.json:**
```json
{
  "dependencies": {
    "@trade-safety/react": "file:../trade-safety/frontend"
  }
}
```

```bash
npm install
```

### 2. 컴포넌트 사용

```tsx
import { DetailedResult, TradeSafetyRepository } from "@trade-safety/react";

<DetailedResult analysis={analysis} />
```

## 주의사항

- **서브모듈 업데이트**: `git submodule update --remote`
- **Clone 시**: `git clone --recurse-submodules`
- **i18n**: trade-safety 번역은 Buppy i18n에 통합 필요
