"""
Standalone FastAPI application for Trade Safety.

This module provides the entry point for running Trade Safety as an independent service.

Usage:
    uvicorn trade_safety.main:app --reload
"""

import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from trade_safety.infrastructure.config import (
    TradeSafetyConfig,
    create_db_session_factory,
    init_database,
)
from trade_safety.infrastructure.database import BaseModel
from trade_safety.infrastructure.errors import (
    INTERNAL_SERVER_ERROR,
    VALIDATION_ERROR,
    ErrorResponse,
)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize configuration from environment
config = TradeSafetyConfig.from_env()

# Initialize database
logger.info("Initializing database: %s", config.database_url.split("@")[-1])  # Hide password
init_database(config.database_url)

# Create FastAPI app
app = FastAPI(
    title="Trade Safety API",
    version="0.1.0",
    description="AI-powered safety analysis for K-pop merchandise trading",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# Error Handlers
# ==============================================================================


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTPException with consistent error response format."""
    from trade_safety.infrastructure.errors import (
        extract_error_code_from_exception,
        get_error_detail_from_exception,
    )

    error_code = extract_error_code_from_exception(exc)
    detail = get_error_detail_from_exception(exc)

    logger.warning(
        "HTTPException: %s %s | status=%d | code=%s",
        request.method,
        request.url,
        exc.status_code,
        error_code,
    )

    error_data = ErrorResponse(status=exc.status_code, detail=detail, code=error_code)
    return JSONResponse(status_code=exc.status_code, content=error_data.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    first_error = exc.errors()[0] if exc.errors() else {}
    field = (
        first_error.get("loc", ["unknown"])[-1]
        if first_error.get("loc")
        else "unknown"
    )

    detail = f"Validation error in field '{field}': {first_error.get('msg', 'Invalid value')}"

    logger.warning(
        "ValidationError: %s %s | errors=%s",
        request.method,
        request.url,
        exc.errors(),
    )

    error_data = ErrorResponse(status=422, detail=detail, code=VALIDATION_ERROR)
    return JSONResponse(status_code=422, content=error_data.model_dump())


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(
        "Unexpected error: %s %s | exc=%r",
        request.method,
        request.url,
        exc,
        exc_info=True,
    )

    error_data = ErrorResponse(
        status=500,
        detail="Internal Server Error",
        code=INTERNAL_SERVER_ERROR,
    )
    return JSONResponse(status_code=500, content=error_data.model_dump())


# ==============================================================================
# Routes
# ==============================================================================


# TODO: Refactor router to standalone mode (remove BaseCrudRouter dependency)
# For now, this is a placeholder for standalone execution
# The actual router uses BaseCrudRouter which requires Buppy infrastructure


@app.get("/healthz", tags=["management"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status message
    """
    return {"status": "healthy", "service": "trade-safety"}


@app.get("/", tags=["management"])
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message with documentation link
    """
    return {
        "message": "Trade Safety API",
        "description": "AI-powered safety analysis for K-pop merchandise trading",
        "docs": "/docs",
    }


# Note: Trade Safety router requires BaseCrudRouter refactoring for standalone mode
# Current router implementation at trade_safety/api/router.py is designed for Buppy integration
# TODO: Create standalone router that doesn't depend on BaseCrudRouter
