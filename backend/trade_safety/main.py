"""
Standalone FastAPI application for Trade Safety.

This module provides the entry point for running Trade Safety as an independent service.

Usage:
    uvicorn trade_safety.main:app --reload

Environment Variables:
    DATABASE_URL: PostgreSQL database URL
    OPENAI_API_KEY: OpenAI API key
    TRADE_SAFETY_MODEL: OpenAI model name (default: gpt-4o-2024-11-20)
    JWT_SECRET_KEY: JWT secret key (default: dev-secret for development)
    LOG_LEVEL: Logging level (default: INFO)
"""

import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aioia_core.database import Base
from aioia_core.errors import (
    INTERNAL_SERVER_ERROR,
    VALIDATION_ERROR,
    ErrorResponse,
    extract_error_code_from_exception,
    get_error_detail_from_exception,
)
from aioia_core.settings import JWTSettings, OpenAIAPISettings

from trade_safety.api.router import create_trade_safety_router
from trade_safety.repositories.trade_safety_repository import (
    DatabaseTradeSafetyCheckManager,
)
from trade_safety.settings import TradeSafetyModelSettings

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ==============================================================================
# Database Settings
# ==============================================================================


class DatabaseSettings(BaseSettings):
    """Database settings (environment variable: DATABASE_URL)"""

    url: str

    class Config:
        env_prefix = "DATABASE_"


# ==============================================================================
# Initialize Settings from Environment Variables
# ==============================================================================

# BaseSettings automatically reads from environment variables
openai_api = OpenAIAPISettings()  # OPENAI_API_KEY
model_settings = TradeSafetyModelSettings()  # TRADE_SAFETY_MODEL
jwt_settings = JWTSettings()  # JWT_SECRET_KEY
db_settings = DatabaseSettings()  # DATABASE_URL

logger.info("Loaded settings from environment variables")
logger.info("Model: %s", model_settings.model)
logger.info("Database: %s", db_settings.url.split("@")[-1])  # Hide credentials


# ==============================================================================
# Initialize Database
# ==============================================================================

engine = create_engine(db_settings.url, echo=False)
Base.metadata.create_all(engine)
db_session_factory = sessionmaker(bind=engine)

logger.info("Database initialized")


# ==============================================================================
# Manager Factories
# ==============================================================================


def trade_safety_check_manager_factory(session):
    """Factory for creating TradeSafetyCheckManager"""
    return DatabaseTradeSafetyCheckManager(session)


# Standalone mode doesn't support user authentication
user_profile_manager_factory = None

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

# Create and include Trade Safety router
trade_safety_router = create_trade_safety_router(
    openai_api=openai_api,
    model_settings=model_settings,
    jwt_settings=jwt_settings,
    db_session_factory=db_session_factory,
    manager_factory=trade_safety_check_manager_factory,
    user_profile_manager_factory=user_profile_manager_factory,
)
app.include_router(trade_safety_router)

logger.info("Trade Safety router registered")


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
