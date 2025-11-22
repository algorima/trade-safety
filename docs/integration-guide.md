# 통합 가이드

Trade Safety를 기존 프로젝트에 통합하는 방법

## FastAPI 프로젝트 통합

### 1. 패키지 설치

**pip:**
```bash
pip install git+https://github.com/algorima/trade-safety.git#subdirectory=backend
```

**로컬 개발 (Git 서브모듈):**
```bash
git submodule add https://github.com/algorima/trade-safety.git
pip install -e ./trade-safety/backend
```

### 2. 서비스 초기화

```python
from trade_safety import TradeSafetyService
from trade_safety._vendor.config import TradeSafetyConfig

# 환경 변수에서 설정 로드
config = TradeSafetyConfig.from_env()
service = TradeSafetyService(config)

# 분석 실행
analysis = await service.analyze_trade("거래글 내용")
```

### 3. FastAPI 라우터 등록

```python
from fastapi import FastAPI
from trade_safety.api.router import create_trade_safety_router

app = FastAPI()

# Router 등록
router = create_trade_safety_router(config)
app.include_router(router, prefix="/api")
```

### 4. 환경 변수 설정

```bash
export DATABASE_URL=postgresql://...
export OPENAI_API_KEY=sk-...
```

---

## React/Next.js 프로젝트 통합

### 1. 패키지 설치

**로컬 개발 (Git 서브모듈):**
```bash
git submodule add https://github.com/algorima/trade-safety.git
```

**package.json:**
```json
{
  "dependencies": {
    "@trade-safety/react": "file:./trade-safety/frontend"
  }
}
```

```bash
npm install
```

### 2. 컴포넌트 사용

```tsx
import { DetailedResult, TradeSafetyRepository } from "@trade-safety/react";

function ResultPage() {
  return <DetailedResult analysis={analysis} />;
}
```

### 3. API Repository 사용

```tsx
import { TradeSafetyRepository } from "@trade-safety/react";

const repository = new TradeSafetyRepository(apiService);
const response = await repository.create({ input_text: "..." });
```

---

## 데이터베이스 설정

### Migration 실행

```bash
cd trade-safety/backend
alembic upgrade head
```

### 테이블 구조

- `trade_safety_checks`: 분석 결과 저장
- 외래키: `user_id` (선택, nullable)

---

## Git 서브모듈 관리

### 업데이트
```bash
git submodule update --remote trade-safety
```

### Clone
```bash
git clone --recurse-submodules <your-repo>
```

### 초기화
```bash
git submodule update --init
```
