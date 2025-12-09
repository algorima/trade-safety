# Trade Safety Frontend

K-pop 굿즈 거래 안전성 분석 React 컴포넌트

## 주요 컴포넌트

- **DetailedResult**: 상세 분석 결과 (위험도, 신호, 추천)
- **QuickResultTeaser**: Freemium 티저 (비로그인 사용자용)
- **RiskSignalCard**: 위험 신호 카드
- **TradeSafetyRepository**: API 클라이언트

## 설치

```bash
npm install trade-safety @aioia/core
```

## 사용법

### 컴포넌트

```tsx
import { DetailedResult } from "trade-safety";

<DetailedResult analysis={analysis} expertAdvice={expertAdvice} />
```

### Repository

```tsx
import { TradeSafetyRepository } from "trade-safety";

const repository = new TradeSafetyRepository(apiService);
const response = await repository.create({ input_text: "..." });
```

### i18n 통합

```tsx
import { tradeSafetyTranslations, TRADE_SAFETY_NS } from "trade-safety";

// 호스트 앱의 i18n 인스턴스에 번역 리소스 추가
Object.entries(tradeSafetyTranslations).forEach(([lang, resources]) => {
  i18n.addResourceBundle(lang, TRADE_SAFETY_NS, resources);
});
```

## Peer Dependencies

- React 18+
- Next.js 13 또는 14
- Tailwind CSS with DaisyUI
- @aioia/core

## 라이선스

Apache 2.0
