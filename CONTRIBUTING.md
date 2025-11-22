# 기여 가이드

## 개발 환경 설정

```bash
git clone https://github.com/algorima/trade-safety.git
cd trade-safety

# Backend
cd backend
pip install -e ".[dev]"
pytest

# Frontend
cd frontend
npm install
npm run build
```

## PR 제출

1. Feature 브랜치 생성
2. 코드 작성 + 테스트
3. Conventional Commits 형식
4. PR 생성 (CLA 서명 필요)

## 코드 품질

### Backend
```bash
black trade_safety      # 포맷팅
isort trade_safety      # import 정렬
mypy trade_safety       # 타입 체크
pytest                  # 테스트
```

### Frontend
```bash
npm run build           # 타입 체크 포함
```

## CLA 서명

첫 PR 시 CLA Assistant 봇이 안내합니다.
댓글로 "I have read the CLA and I agree." 작성하면 서명 완료.

## 주의사항

- `_vendor/` 코드는 수정 최소화 (Buppy와 동기화)
- LLM 프롬프트 변경 시 A/B 테스트 필수
- CLAUDE.md의 철학 원칙 준수
