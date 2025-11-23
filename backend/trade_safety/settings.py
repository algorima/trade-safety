"""Settings for Trade Safety service."""

from pydantic_settings import BaseSettings


class TradeSafetyModelSettings(BaseSettings):
    """
    Trade Safety LLM model settings.

    Environment variables:
        TRADE_SAFETY_MODEL: OpenAI model name (default: gpt-4o-2024-11-20)
    """

    model: str = "gpt-4o-2024-11-20"

    class Config:
        env_prefix = "TRADE_SAFETY_"
