FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/pyproject.toml ./
RUN pip install --no-cache-dir setuptools wheel && \
    pip install --no-cache-dir -e .

# Copy application code
COPY backend/trade_safety ./trade_safety

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/healthz')"

CMD ["uvicorn", "trade_safety.main:app", "--host", "0.0.0.0", "--port", "8000"]
