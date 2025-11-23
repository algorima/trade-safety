FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY backend/pyproject.toml backend/poetry.lock ./

# Install dependencies (no dev, no root package yet)
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root

# Copy application code
COPY backend/trade_safety ./trade_safety

# Install root package
RUN poetry install --only-root

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/healthz')"

CMD ["uvicorn", "trade_safety.main:app", "--host", "0.0.0.0", "--port", "8000"]
