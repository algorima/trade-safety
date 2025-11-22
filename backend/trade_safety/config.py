"""Trade Safety specific configuration."""

import os

from aioia_core.llm import ProviderRegistry


class TradeSafetyConfig:
    """Configuration for Trade Safety standalone execution."""

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
    def from_env(cls):
        """Create configuration from environment variables."""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if not openai_key and not anthropic_key:
            raise ValueError(
                "At least one of OPENAI_API_KEY or ANTHROPIC_API_KEY is required"
            )

        return cls(
            database_url=database_url,
            openai_api_key=openai_key,
            anthropic_api_key=anthropic_key,
            default_provider=os.getenv("DEFAULT_LLM_PROVIDER", "openai"),
            default_model=os.getenv("DEFAULT_LLM_MODEL", "gpt-4o-2024-11-20"),
            sentry_dsn=os.getenv("SENTRY_DSN"),
        )

    def _create_config_settings(self):
        """Create minimal config_settings object for compatibility with TradeSafetyService."""
        from trade_safety.prompts import TRADE_SAFETY_SYSTEM_PROMPT

        class SystemPromptSettings:
            trade_safety_system_prompt = TRADE_SAFETY_SYSTEM_PROMPT
            default_api_provider = self.default_provider
            default_chat_model = self.default_model

        class ConfigSettings:
            system_prompt_settings = SystemPromptSettings()

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
