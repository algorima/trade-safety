# 기여 가이드

## 개발 환경

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety

# Backend
cd backend
poetry install
make unit-test

# Frontend
cd frontend
npm install
npm run build
```

## PR 제출

1. Feature 브랜치 생성
2. 코드 작성 + 테스트
3. Conventional Commits 형식 (제목은 한국어)
4. PR 생성 (CLA 서명 필요)

## PR 제목

Conventional Commits 형식: `<type>(<scope>): <한국어 제목>`

### Type
- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서만 변경
- **refactor**: 코드 리팩토링 (기능 변경 없음)
- **test**: 테스트 추가/수정
- **perf**: 성능 개선
- **style**: 코드 포맷, 스타일 변경 (로직 변경 없음)
- **ci**: CI/CD 설정 변경
- **chore**: 빌드 프로세스, 도구 설정 등

### Scope
변경 영역을 나타냅니다:
- 플랫폼: `frontend`, `backend`
- 비즈니스: `analysis`, `detection`, `translation`
- 데이터: `db`, `models`, `api`
- UI: `ui`, `theme`, `i18n`
- 연동: `openai`, `sentry`
- 배포: `docker`, `deploy`, `config`, `workflow`
- 기타: `deps`, `service`

예시: `feat(frontend): 결과 페이지 헤더 구현`

## 브랜치 네이밍

형식: `주작업/작업-내용`

주 작업 유형:
- feat: 신기능 개발
- refactor: 코드 품질 개선
- fix: 기능 수정

작업 내용:
- 영어로 작성
- 간략하게 표현 (예: URL 패치 → URL-fetch)
- 최대한 명사 사용
- 단어 구분: - 로 가독성 향상

예시: feat/URL-fetch, refactor/output-language, fix/i18n-config



## 코드 품질

### Backend
```bash
make format
make lint
make type-check
make unit-test
```

### Frontend
```bash
npm run lint
npm run type-check
npm test
```

## CLA 서명

첫 PR 시 CLA Assistant 봇이 안내합니다.
