# Trade Safety 개발 가이드

## 프로젝트 구조

- `frontend/`: NPM 라이브러리 + Next.js 애플리케이션 (데모/개발용)
  - `package.json`, `package-lock.json` 모두 git에 커밋 (dual-purpose 프로젝트)
  - dependencies 변경 시 `npm install` 실행하여 `package-lock.json` 업데이트 필요

## 코드 품질

- DRY: 중복 금지, aioia-core 재사용
- Opportunistic Refactoring: 변경 쉽게 → 변경
- Guard Clause: 함수 초반에 전제조건 검사, 실패 시 즉시 반환
- 오류 처리: 예상 오류 catch, 예상 외 throw

## 보안

- LLM Prompt Injection 방지

## 테스트

- TDD: Red → Green → Refactor

## Python

- Tests: `assert <var> is not None` 로 타입 안정성 유지

## 네이밍

- Python: `snake_case.py`, `PascalCase`, `snake_case()`
- TypeScript: `PascalCase.tsx`, `camelCase()`, `index.ts`

## 다국어

- 모든 언어 동시 추가 (en, ko, ja, zh, es, id)

## Pull Request 작성 가이드

### 제목
- Conventional Commits 형식으로 72자 이내 영문 작성: `<type>(<scope>): <subject>`

### 설명 구조
1. **요약 (한글, 1-2문장)** - 사용자 관점에서 무엇이 달라지는지 요약
2. **목적** - 이 변경이 왜 필요한지, 어떤 문제를 해결하는지 설명
3. **주요 변경 사항** - 변경된 내용을 목록으로 정리
4. **테스트 체크리스트** - 확인해야 할 항목을 체크박스로 작성

상세 템플릿: `.github/PULL_REQUEST_TEMPLATE.md` 참고

## 외부 기여

- Atomic PR: 하나의 PR은 하나의 논리적 변경만 포함
- CLA 서명 필수
- CLAUDE.md, CONTRIBUTING.md 숙지
- PR 템플릿: `.github/PULL_REQUEST_TEMPLATE.md` 참고
