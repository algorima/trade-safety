# Trade Safety 개발 가이드

## 프로젝트 철학

1. **공감 > 정답**: 사용자가 공감받았다고 느끼게 만듭니다
2. **맥락 > 일반화**: 각 팬덤의 언어와 감정을 세밀하게 반영합니다
3. **자율 > 개입**: 감정을 조작하지 않고 스스로 판단할 여지를 남깁니다
4. **경험 > 기능**: 감정적으로 만족스러운 경험을 출시 기준으로 삼습니다

## 아키텍처

### Backend

```
trade_safety/
├── schemas.py          # Pydantic 도메인 스키마
├── prompts.py          # 시스템 프롬프트
├── service.py          # 비즈니스 로직
├── models.py           # SQLAlchemy DB 모델
├── repositories/       # Repository 패턴
├── api/                # FastAPI 엔드포인트
└── config.py           # 설정
```

### Frontend

```
src/
├── components/         # UI 컴포넌트
├── repositories/       # Repository 패턴 (API 접근)
├── types.ts            # TypeScript 타입
└── i18n/               # 다국어 번역
```

## 코드 품질

### DRY
- 중복 코드 금지
- aioia-core 재사용

### Opportunistic Refactoring
- 변경 전 코드를 먼저 변경하기 쉽게 만듭니다

### 오류 처리
- 예상된 오류: catch하여 사용자 피드백
- 예상 못한 오류: Sentry 보고
- 불변 조건: assert

## 보안

### OWASP Top 10
- SQL Injection: SQLAlchemy ORM
- XSS: React 자동 이스케이핑
- Command Injection 금지

### LLM 보안
- Prompt Injection 방지
- Pydantic 출력 검증
- API 키 보호

## 테스트

### TDD
1. Red: 실패하는 테스트
2. Green: 통과
3. Refactor: 개선

### LLM 테스트
- 범위 검증 (정확한 값 불가)
- 구조 검증
- Golden Dataset

## 네이밍

### Python
- 파일: `snake_case.py`
- 클래스: `PascalCase`
- 함수: `snake_case`

### TypeScript
- 컴포넌트: `PascalCase.tsx`
- 함수: `camelCase`
- Export: `index.ts`

## 다국어

- 모든 언어 동시 추가: en, ko, ja, zh, es, id
- 기계 번역 금지
- 팬덤 맥락 이해 필수

## LLM 프롬프트

- 프롬프트 변경은 핵심 차별화 요소
- A/B 테스트 필수
- Golden Dataset 회귀 테스트

## 외부 기여

### CLA 서명
- 첫 PR 시 봇이 안내
- "I have read the CLA and I agree."

### 철학 이해
- "공감 > 정답" 위반 시 PR 거부 가능
