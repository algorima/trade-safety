# Trade Safety 개발 가이드

## 프로젝트 구조

- `frontend/`: NPM 라이브러리 + Next.js 애플리케이션 (데모/개발용)
  - `package.json`, `package-lock.json` 모두 git에 커밋 (dual-purpose 프로젝트)
  - dependencies 변경 시 `npm install` 실행하여 `package-lock.json` 업데이트 필요

## 코드 품질

- DRY: 중복 금지, aioia-core 재사용
- Opportunistic Refactoring: 변경 쉽게 → 변경 (make the change easy, then make the easy change)
- Guard Clause: 함수 초반에 전제조건 검사, 실패 시 즉시 반환
- 오류 처리: 예상 오류 catch, 예상 외 throw
- 불변 조건(DB에서 조회한 데이터의 필수 필드 등)은 `assert`로 검증

## 아키텍처 원칙

- **Presentational** (`/components/**`): UI만 담당. API/전역상태/라우팅 금지. i18n(useTranslation)은 허용.
- **Container** (`/page.tsx`): 데이터 페칭, 전역 상태, 비즈니스 로직 담당.

## 문제 해결 (5 Whys)

- 새로운 문제가 발생하면, "왜?"를 충분히 반복하여 근본 원인을 먼저 파악하세요.
- 표면적 증상이 아닌 시스템적 원인을 찾아 해결하세요.

## 보안

- LLM Prompt Injection 방지

## 테스트

- TDD: Red → Green → Refactor
- 테스트 삭제는 코드 품질 포기입니다.
- 테스트 격리: `setUp` 변경 전 다른 테스트에 미치는 side effect를 확인하세요.

## 코드 수정 후 필수 실행

프론트엔드 코드를 수정한 후에는 **반드시** 다음 명령을 `frontend/`에서 실행하세요:
1. `npm run format` - Prettier 코드 포맷팅
2. `npm run lint:fix` - ESLint 자동 수정
3. `npm run type-check` - TypeScript 타입 검사
4. `npm test` - Jest 단위 테스트 실행

백엔드 코드를 수정한 후에는 **반드시** 다음 명령을 프로젝트 루트에서 실행하세요:
1. `make -C backend format` - isort, black 코드 포맷팅
2. `make -C backend lint` - Pylint 검사
3. `make -C backend type-check` - mypy, pyright 타입 검사
4. `make -C backend unit-test` - 단위 테스트 실행

## Python

- Tests: `assert <var> is not None` 로 타입 안정성 유지

## 네이밍

- Python: `snake_case.py`, `PascalCase`, `snake_case()`
- TypeScript: `PascalCase.tsx`, `camelCase()`, `index.ts`

## 스타일링

- 조건부 클래스 관리: `clsx` 사용
- CSS 프레임워크: Tailwind CSS + DaisyUI
- 아이콘: Heroicons v2 (`@heroicons/react`)

## 컴포넌트 정의

- 컴포넌트는 Named Exports 사용, 함수 선언 방식으로 정의
- **예외**: Next.js App Router의 페이지 컴포넌트(`page.tsx`, `layout.tsx`, `error.tsx` 등)는 default export 사용
- 컴포넌트 외 일반 함수는 화살표 함수로 정의

## 다국어

- 모든 언어 동시 추가 (en, ko, ja, zh, es, id)

## Pull Request 작성 가이드

### 제목
- Conventional Commits 형식으로 72자 이내 한국어 작성: `<type>(<scope>): <한국어 제목>`

### 설명 구조
1. **요약 (한글, 1-2문장)** - 사용자 관점에서 무엇이 달라지는지 요약, 중요한 키워드 **볼드** 처리
2. **목적** - 이 변경이 왜 필요한지, 어떤 문제를 해결하는지 쉬운 단어로 구체적이고 명확하게 설명
3. **주요 변경 사항** - 사용자 경험과 기능 관점에서 무엇이 개선되는지 설명. 유사한 내용 묶어 하위 섹션 구성, 삭제된 기능도 모두 설명
4. **구조 변경 (선택)** - 주요 모듈 및 클래스를 tree로 구조화. 핵심 구조는 Mermaid로 시각화 (괄호와 같은 특수 문자는 인용 부호로 감싸기)
5. **테스트 체크리스트** - 사용자 관점에서 실제로 동작을 확인할 수 있는 시나리오를 체크박스 스타일로 작성 (기술적 테스트 항목이 아닌, 기능과 사용자 경험 중심으로)
6. **개선 효과 (선택)** - 개발자가 아니어도 이해하기 쉽게 케이스별로 설명

상세 템플릿: `.github/PULL_REQUEST_TEMPLATE.md` 참고

## 외부 기여

- Atomic PR: 하나의 PR은 하나의 논리적 변경만 포함
- CLA 서명 필수
- CLAUDE.md, CONTRIBUTING.md 숙지
- PR 템플릿: `.github/PULL_REQUEST_TEMPLATE.md` 참고
