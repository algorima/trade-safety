# Trade Safety Backend

Python package for AI-powered safety analysis of K-pop merchandise trades.

## Features

- **LLM-based Analysis**: Uses GPT-4/Claude to analyze trade posts
- **Multi-language Support**: Translates Korean slang and nuances
- **Risk Detection**: Identifies payment, seller, platform, price, and content risks
- **Price Analysis**: Compares offered prices with market values
- **Freemium Model**: Quick summary for guests, full analysis for authenticated users

## Installation

### From Buppy (as submodule)

```bash
# Already included as submodule in Buppy
poetry install
```

### Standalone

```bash
cd backend
pip install -e .
```

## Usage

### As Library

```python
from trade_safety import TradeSafetyService
from config.app_config import BaseAppConfig

# Initialize service with Buppy's config
service = TradeSafetyService(app_config=buppy_app_config)

# Analyze a trade
analysis = await service.analyze_trade(
    input_text="급처분 ㅠㅠ 공구 실패해서 양도해요"
)

print(f"Risk Score: {analysis.risk_score}/100")
print(f"Risk Signals: {len(analysis.risk_signals)}")
```

### As FastAPI Router

```python
from trade_safety.api.router import create_trade_safety_router

# Create router with Buppy's config
router = create_trade_safety_router(app_config=buppy_app_config)

# Include in your FastAPI app
app.include_router(router, prefix="/api/v2")
```

## Dependencies

- **Buppy Infrastructure**: Requires Buppy's BaseAppConfig, BaseManager, and LLM providers
- **LangChain**: LLM integration
- **SQLAlchemy**: Database models
- **FastAPI**: API endpoints
- **Pydantic**: Data validation

## Project Structure

```
backend/
├── trade_safety/
│   ├── __init__.py          # Package exports
│   ├── models.py             # Pydantic models
│   ├── service.py            # TradeSafetyService
│   ├── database/
│   │   ├── models.py         # SQLAlchemy models
│   │   └── manager.py        # CRUD manager
│   ├── api/
│   │   └── router.py         # FastAPI router
│   └── config/
│       └── prompts.py        # System prompts
├── tests/
├── pyproject.toml
└── README.md
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black trade_safety
isort trade_safety

# Type check
mypy trade_safety
```

## License

Apache 2.0
