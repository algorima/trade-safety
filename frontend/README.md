# Trade Safety React Components

React components for K-pop merchandise trade safety analysis.

## Features

- **DetailedResult**: Full analysis display with risk score, signals, and recommendations
- **QuickResultTeaser**: Freemium teaser for non-authenticated users
- **RiskSignalCard**: Reusable risk signal display component
- **TradeSafetyRepository**: API client for backend integration
- **Multi-language Support**: 6 languages (en, ko, ja, zh, es, id)

## Installation

### From Buppy (as local package)

```bash
# In Buppy's package.json
{
  "dependencies": {
    "@trade-safety/react": "file:../trade-safety/frontend"
  }
}

npm install
```

### Standalone

```bash
cd frontend
npm install
npm run build
```

## Usage

### Import Components

```tsx
import { DetailedResult, QuickResultTeaser } from "@trade-safety/react";
import type { TradeSafetyAnalysis } from "@trade-safety/react";

function TradeSafetyPage() {
  return (
    <DetailedResult
      analysis={analysis}
      expertAdvice={expertAdvice}
    />
  );
}
```

### Use Repository

```tsx
import { TradeSafetyRepository } from "@trade-safety/react";

const repository = new TradeSafetyRepository(apiService);
const response = await repository.create({ input_text: "..." });
```

### Integrate i18n

```tsx
import { enTranslations, koTranslations } from "@trade-safety/react";

i18n.init({
  resources: {
    en: {
      translation: {
        ...yourTranslations,
        page: {
          tradeSafety: enTranslations,
        },
      },
    },
    ko: {
      translation: {
        ...yourTranslations,
        page: {
          tradeSafety: koTranslations,
        },
      },
    },
  },
});
```

## Peer Dependencies

These must be installed in your project:

- React ^18.0.0
- React DOM ^18.0.0
- Next.js ^13.0.0 or ^14.0.0
- Tailwind CSS (with DaisyUI theme)

## Development

```bash
# Watch mode
npm run dev

# Build
npm run build

# Clean
npm run clean
```

## License

Apache 2.0
