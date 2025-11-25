# Trade Safety 개발 가이드

## 코드 품질

- DRY: 중복 금지, aioia-core 재사용
- Opportunistic Refactoring: 변경 쉽게 → 변경
- Guard Clause: 함수 초반에 전제조건 검사, 실패 시 즉시 반환
- 오류 처리: 예상 오류 catch, 예상 외 throw

## 보안

- SQL Injection: SQLAlchemy ORM
- XSS: React 자동 이스케이핑
- LLM Prompt Injection 방지
- API 키 환경 변수 관리

## 테스트

- TDD: Red → Green → Refactor
- LLM 테스트: 범위 검증, Golden Dataset

## Python

- Tests: `assert <var> is not None` 로 타입 안정성 유지

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

- Atomic PR: 하나의 PR은 하나의 논리적 변경만 포함
- CLA 서명 필수
- CLAUDE.md, CONTRIBUTING.md 숙지
- PR 템플릿: `.github/PULL_REQUEST_TEMPLATE.md` 참고
