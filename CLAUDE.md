# Trade Safety 개발 가이드

## 프로젝트 철학

Buppy의 핵심 원칙을 따릅니다:

1. **공감 > 정답**: 사용자가 공감받았다고 느끼게 만듭니다
2. **맥락 > 일반화**: 각 팬덤의 언어와 감정을 세밀하게 반영합니다
3. **자율 > 개입**: 감정을 조작하지 않고 스스로 판단할 여지를 남깁니다
4. **경험 > 기능**: 감정적으로 만족스러운 경험을 출시 기준으로 삼습니다

## 아키텍처 원칙

### Backend 구조

```
trade_safety/
├── schemas.py          # Pydantic 도메인 스키마 (API 계약)
├── prompts.py          # 시스템 프롬프트 (도메인 지식)
├── service.py          # 비즈니스 로직
├── models.py           # SQLAlchemy DB 모델 (데이터 구조)
├── repositories/       # Repository 패턴 (데이터 접근)
├── api/                # FastAPI 엔드포인트
└── _vendor/            # Buppy 복사 코드 (임시, 추후 추출 예정)
```

**책임 분리:**
- **Schemas**: API 입출력 검증, 도메인 모델 정의
- **Models**: DB 테이블 구조, 관계 정의
- **Repositories**: CRUD 작업, 쿼리 로직
- **Service**: 비즈니스 로직, LLM 통합
- **API**: HTTP 엔드포인트, 인증, 에러 처리

### Frontend 구조

```
src/
├── components/         # Presentational UI (상태/API 금지)
├── repositories/       # Repository 패턴 (API 접근)
├── types.ts            # TypeScript 타입 정의
└── i18n/               # 다국어 번역
```

**Container/Presentational 패턴:**
- Buppy 페이지가 Container 역할 (데이터 페칭, 상태 관리)
- Trade Safety 컴포넌트는 Presentational (props만 받아 렌더링)

## 코드 품질

### DRY (Don't Repeat Yourself)
- 동일한 로직이나 패턴 반복 금지
- 기존 컴포넌트/함수를 먼저 확인하고 재사용

### Opportunistic Refactoring
- 변경 전 코드를 먼저 변경하기 쉽게 만듭니다
- "_vendor/ 코드는 추후 buppy-common으로 추출" (make the change easy, then make the easy change)

### 오류 처리
- **예상된 오류** (API 실패, 검증 오류): catch하여 사용자 피드백
- **예상 못한 오류** (버그): Sentry 자동 보고되도록 다시 throw
- **불변 조건**: assert로 검증

## 보안

### OWASP Top 10 준수
- SQL Injection: SQLAlchemy ORM 사용 (raw query 금지)
- XSS: React 자동 이스케이핑 신뢰
- Command Injection: 사용자 입력으로 subprocess 호출 금지

### LLM 보안
- **Prompt Injection 방지**: 사용자 입력을 HumanMessage로 분리
- **출력 검증**: Pydantic으로 LLM 응답 구조 강제
- **API 키 보호**: 환경 변수만 사용, 로그에 출력 금지

## 테스트

### TDD 권장
1. Red: 실패하는 테스트 작성
2. Green: 최소한의 코드로 통과
3. Refactor: 중복 제거, 구조 개선

### LLM 테스트 전략
- 정확한 값 비교 불가 (비결정적 출력)
- 범위 검증: `assert 0 <= risk_score <= 100`
- 구조 검증: `assert "risk_signals" in analysis`
- Golden Dataset: 표준 테스트 케이스 유지

## 네이밍 규칙

### Python
- 파일: `snake_case.py`
- 클래스: `PascalCase`
- 함수/변수: `snake_case`
- 상수: `UPPER_SNAKE_CASE`

### TypeScript
- 파일: `PascalCase.ts` (컴포넌트), `camelCase.ts` (유틸)
- 컴포넌트: `PascalCase`
- 함수/변수: `camelCase`
- 타입/인터페이스: `PascalCase`
- Export: `index.ts` (Python의 `__init__.py`처럼)

## Vendored Code (_vendor/)

`_vendor/` 디렉토리의 코드는 Buppy에서 복사한 임시 코드입니다:

```python
# TODO: 이 코드는 Buppy에서 복사됨. 추후 buppy-common 라이브러리로 추출 예정
```

**원칙:**
- 수정 최소화 (Buppy와 동기화 유지)
- 추후 buppy-common 라이브러리로 추출 예정
- 중복 코드지만 독립성을 위해 허용 (Opportunistic Refactoring)

## 다국어 (i18n)

### 키 추가 시
- **모든** 언어 파일에 함께 추가: `en`, `ko`, `ja`, `zh`, `es`, `id`
- 기존 용어 먼저 확인하여 일관성 유지

### 번역 품질
- 기계 번역 금지
- 팬덤 맥락을 이해하는 네이티브 검수 필수
- "급처", "공구" 같은 은어는 맥락 설명 추가

## LLM 프롬프트

### prompts.py 수정 시
- **프롬프트 변경은 제품 핵심 차별화 요소**
- A/B 테스트 없이 수정 금지
- 변경 시 Golden Dataset으로 회귀 테스트 필수

### 프롬프트 원칙
- 공감적이되 객관적
- 명확한 출력 구조 정의 (JSON schema)
- Few-shot 예시 포함 (향후 추가 예정)

## Git 사용

### 커밋 메시지
- Conventional Commits: `<type>(<scope>): <subject>`
- 한국어 본문: 변경 이유와 영향 명시

### 브랜치 전략
- `feature/` - 새 기능
- `fix/` - 버그 수정
- `refactor/` - 리팩토링
- `docs/` - 문서만 수정

## 외부 기여

### CLA 서명 필수
- 첫 PR 시 CLA Assistant 봇이 자동 안내
- "I have read the CLA and I agree." 댓글로 서명

### 철학 이해 필수
- CLAUDE.md, CONTRIBUTING.md 필독
- "공감 > 정답" 원칙을 위반하는 PR은 기술적으로 완벽해도 거부 가능
