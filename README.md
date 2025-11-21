# Trade Safety

AI-powered safety analysis for K-pop merchandise trading. Helps international fans overcome language barriers and detect scam signals.

## Features

- 🤖 **LLM-based Analysis**: GPT-4/Claude powered trade post analysis
- 🌍 **Multi-language**: Translates Korean slang and nuances
- ⚠️ **Risk Detection**: Identifies payment, seller, platform, price, and content risks
- 💰 **Price Analysis**: Compares offered prices with market values
- 📝 **Safety Checklist**: Actionable steps to verify trades
- 🎨 **React Components**: Pre-built UI components with Tailwind/DaisyUI
- 🔓 **Freemium Model**: Quick summary for guests, full analysis for authenticated users

## Quick Start

### For Buppy Integration (Submodule)

```bash
# Add as submodule
cd /path/to/buppy
git submodule add https://github.com/algorima/trade-safety.git modules/trade-safety
git submodule update --init --recursive

# Install backend
cd modules/trade-safety/backend
poetry install

# Install frontend
cd ../frontend
npm install
```

### Standalone Deployment (Docker)

```bash
# Clone repository
git clone https://github.com/algorima/trade-safety.git
cd trade-safety

# Set up environment
cp docker/.env.example docker/.env
# Edit docker/.env with your API keys

# Run with Docker Compose
cd docker
docker-compose up
```

Visit http://localhost:3000

## Project Structure

```
trade-safety/
├── backend/               # Python package
│   ├── trade_safety/
│   │   ├── models.py      # Pydantic models
│   │   ├── service.py     # TradeSafetyService
│   │   ├── database/      # SQLAlchemy models & managers
│   │   ├── api/           # FastAPI router
│   │   └── config/        # System prompts
│   ├── tests/
│   └── pyproject.toml
│
├── frontend/              # React components
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── api/           # Repository & types
│   │   └── i18n/          # Translations (6 languages)
│   ├── package.json
│   └── tsconfig.json
│
├── docker/                # Standalone deployment
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── docs/                  # Documentation
├── examples/              # Integration examples
└── LICENSE                # Apache 2.0
```

## Usage

### Backend (Python)

```python
from trade_safety import TradeSafetyService

# Initialize service
service = TradeSafetyService(app_config=your_config)

# Analyze a trade
analysis = await service.analyze_trade(
    input_text="급처분 ㅠㅠ 공구 실패해서 양도해요"
)

print(f"Risk Score: {analysis.risk_score}/100")
print(f"Recommendation: {analysis.recommendation}")
```

### Frontend (React)

```tsx
import { DetailedResult } from "@trade-safety/react";

function TradeSafetyPage() {
  return (
    <DetailedResult
      analysis={analysis}
      expertAdvice={expertAdvice}
    />
  );
}
```

## Documentation

- [Backend README](backend/README.md) - Python package details
- [Frontend README](frontend/README.md) - React components guide
- [Integration Guide](docs/integration-guide.md) - How to integrate with your project
- [Deployment Guide](docs/deployment-guide.md) - Production deployment

## Development

### Backend

```bash
cd backend
pip install -e ".[dev]"
pytest
black trade_safety
mypy trade_safety
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Requirements

### Backend
- Python 3.12+
- PostgreSQL
- OpenAI or Anthropic API key

### Frontend
- React 18+
- Next.js 13 or 14
- Tailwind CSS with DaisyUI

## License

Apache 2.0 - see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

- 🐛 [Report issues](https://github.com/algorima/trade-safety/issues)
- 📖 [Documentation](https://github.com/algorima/trade-safety#readme)
- 💬 [Discussions](https://github.com/algorima/trade-safety/discussions)
