"""
Configuration infrastructure for Trade Safety.

This module provides simplified configuration for standalone execution.

TODO: 이 코드는 Buppy에서 간소화하여 복사됨. 추후 buppy-common 라이브러리로 추출 예정
Simplified from Buppy for independence. Will be extracted to buppy-common later.
"""

from __future__ import annotations

import os
from typing import Any, Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from litellm import completion
from pydantic import BaseModel, Field

# ==============================================================================
# Model Settings
# ==============================================================================


class ModelSettings(BaseModel):
    """Settings required for initializing a chat model, including the model name."""

    chat_model: str = Field(description="The chat model used by the companion.")
    temperature: float = Field(
        default=0.0, description="The temperature for the chat model."
    )
    seed: Optional[int] = Field(
        default=None, description="The random seed for the chat model."
    )


# ==============================================================================
# LLM Provider System (Simplified)
# ==============================================================================


class BaseProvider:
    """Base class for LLM providers."""

    def init_chat_model(
        self,
        model_settings: ModelSettings,
        api_key: str,
        response_format: dict[str, Any] | None = None,
    ) -> BaseChatModel:
        """Initialize chat model with settings."""
        raise NotImplementedError


class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation."""

    def init_chat_model(
        self,
        model_settings: ModelSettings,
        api_key: str,
        response_format: dict[str, Any] | None = None,
    ) -> BaseChatModel:
        """Initialize OpenAI chat model."""
        kwargs: dict[str, Any] = {
            "model": model_settings.chat_model,
            "temperature": model_settings.temperature,
            "api_key": api_key,
        }

        if model_settings.seed is not None:
            kwargs["seed"] = model_settings.seed

        if response_format:
            kwargs["model_kwargs"] = {"response_format": response_format}

        return ChatOpenAI(**kwargs)


class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation."""

    def init_chat_model(
        self,
        model_settings: ModelSettings,
        api_key: str,
        response_format: dict[str, Any] | None = None,
    ) -> BaseChatModel:
        """Initialize Anthropic chat model."""
        # Note: Anthropic doesn't support JSON mode via response_format
        # Use prompt engineering instead
        return ChatAnthropic(
            model=model_settings.chat_model,
            temperature=model_settings.temperature,
            api_key=api_key,
        )


class LiteLLMProvider(BaseProvider):
    """LiteLLM provider implementation."""

    def init_chat_model(
        self,
        model_settings: ModelSettings,
        api_key: str,
        response_format: dict[str, Any] | None = None,
    ) -> BaseChatModel:
        """Initialize LiteLLM model."""
        # LiteLLM uses completion API, wrap in LangChain compatible class
        # This is a simplified implementation
        raise NotImplementedError("LiteLLM provider not yet implemented for standalone")


# ==============================================================================
# Provider Registry
# ==============================================================================


class ProviderRegistry:
    """Registry for LLM providers."""

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
        }

    def get_provider(self, provider_name: str) -> BaseProvider:
        """Get provider by name."""
        if provider_name not in self._providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        return self._providers[provider_name]


# ==============================================================================
# Standalone Configuration
# ==============================================================================


class TradeSafetyConfig:
    """
    Simplified configuration for Trade Safety standalone execution.

    This is a minimal version of Buppy's BaseAppConfig, containing only
    what TradeSafetyService needs to function.
    """

    def __init__(
        self,
        database_url: str,
        openai_api_key: str | None = None,
        anthropic_api_key: str | None = None,
        default_provider: str = "openai",
        default_model: str = "gpt-4o-2024-11-20",
        sentry_dsn: str | None = None,
    ):
        """
        Initialize Trade Safety configuration.

        Args:
            database_url: PostgreSQL connection URL
            openai_api_key: OpenAI API key
            anthropic_api_key: Anthropic API key
            default_provider: Default LLM provider ('openai' or 'anthropic')
            default_model: Default model name
            sentry_dsn: Sentry DSN for error tracking
        """
        self.database_url = database_url
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        self.default_provider = default_provider
        self.default_model = default_model
        self.sentry_dsn = sentry_dsn

        # Initialize provider registry
        self.provider_registry = ProviderRegistry()

        # Create settings object for compatibility with TradeSafetyService
        self.config_settings = self._create_config_settings()

    @classmethod
    def from_env(cls) -> TradeSafetyConfig:
        """
        Create configuration from environment variables.

        Required:
            DATABASE_URL: PostgreSQL connection URL
            OPENAI_API_KEY or ANTHROPIC_API_KEY: At least one LLM provider

        Optional:
            DEFAULT_LLM_PROVIDER: openai (default) or anthropic
            DEFAULT_LLM_MODEL: Model name (default: gpt-4o-2024-11-20)
            SENTRY_DSN: Sentry error tracking
        """
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if not openai_key and not anthropic_key:
            raise ValueError("At least one of OPENAI_API_KEY or ANTHROPIC_API_KEY is required")

        default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
        default_model = os.getenv(
            "DEFAULT_LLM_MODEL", "gpt-4o-2024-11-20"
        )

        return cls(
            database_url=database_url,
            openai_api_key=openai_key,
            anthropic_api_key=anthropic_key,
            default_provider=default_provider,
            default_model=default_model,
            sentry_dsn=os.getenv("SENTRY_DSN"),
        )

    def _create_config_settings(self):
        """Create minimal config_settings object for compatibility with TradeSafetyService."""
        from trade_safety.config.prompts import TRADE_SAFETY_SYSTEM_PROMPT

        class SystemPromptSettings:
            trade_safety_system_prompt = TRADE_SAFETY_SYSTEM_PROMPT
            default_api_provider = self.default_provider
            default_chat_model = self.default_model

        class APISettings:
            openai_api_key = self.openai_api_key
            anthropic_api_key = self.anthropic_api_key

        class ConfigSettings:
            system_prompt_settings = SystemPromptSettings()
            api_settings = APISettings()

        return ConfigSettings()

    def get_api_key(self, provider_name: str) -> str:
        """Get API key for specified provider."""
        if provider_name == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY not configured")
            return self.openai_api_key
        elif provider_name == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            return self.anthropic_api_key
        else:
            raise ValueError(f"Unknown provider: {provider_name}")


# ==============================================================================
# Database Session Management
# ==============================================================================


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_db_session_factory(database_url: str):
    """Create SQLAlchemy session factory."""
    engine = create_engine(database_url, echo=False)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_database(database_url: str):
    """Initialize database (create tables if not exist)."""
    from trade_safety.infrastructure.database import Base

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
