"""Settings for Trade Safety service."""

from pydantic_settings import BaseSettings

ALLOWED_LANGUAGES = {"EN", "KO", "ES", "ID", "JA", "ZH", "TH", "VI", "TL"}

class TradeSafetyModelSettings(BaseSettings):
    """
    Trade Safety LLM model settings.

    Environment variables:
        TRADE_SAFETY_MODEL: OpenAI model name (default: gpt-5.2)
    """

    model: str = "gpt-5.2"

    class Config:
        env_prefix = "TRADE_SAFETY_"
