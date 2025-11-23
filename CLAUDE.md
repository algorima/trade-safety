# Trade Safety 개발 가이드

## 아키텍처

### Backend

```
trade_safety/
├── schemas.py          # Pydantic 스키마
├── prompts.py          # 시스템 프롬프트
├── service.py          # 비즈니스 로직
├── models.py           # SQLAlchemy 모델
├── repositories/       # Repository 패턴
├── api/                # FastAPI 엔드포인트
└── config.py           # 설정
```

### Frontend

```
src/
├── components/         # UI 컴포넌트
├── repositories/       # API 접근
├── types.ts            # TypeScript 타입
└── i18n/               # 다국어
```

## 코드 품질

- DRY: 중복 금지, aioia-core 재사용
- Opportunistic Refactoring: 변경 쉽게 → 변경
- 오류 처리: 예상 오류 catch, 예상 외 throw

## 보안

- SQL Injection: SQLAlchemy ORM
- XSS: React 자동 이스케이핑
- LLM Prompt Injection 방지
- API 키 환경 변수 관리

## 테스트

- TDD: Red → Green → Refactor
- LLM 테스트: 범위 검증, Golden Dataset

## 네이밍

- Python: `snake_case.py`, `PascalCase`, `snake_case()`
- TypeScript: `PascalCase.tsx`, `camelCase()`, `index.ts`

## 다국어

- 모든 언어 동시 추가 (en, ko, ja, zh, es, id)
- 기계 번역 금지

## LLM 프롬프트

- 변경 시 A/B 테스트 필수
- Golden Dataset 회귀 테스트

## 외부 기여

- CLA 서명 필수
- CLAUDE.md, CONTRIBUTING.md 숙지
