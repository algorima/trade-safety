"""Settings for Trade Safety service."""

from pathlib import Path

from pydantic_settings import BaseSettings

ALLOWED_LANGUAGES = {"EN", "KO", "ES", "ID", "JA", "ZH", "TH", "VI", "TL"}


class TwitterAPISettings(BaseSettings):
    """
    Twitter API authentication settings.

    Environment variables:
        TWITTER_BEARER_TOKEN: Twitter API Bearer Token
    """

    bearer_token: str | None = None

    class Config:
        env_prefix = "TWITTER_"


class TradeSafetyModelSettings(BaseSettings):
    """
    Trade Safety LLM and ML model settings.

    Environment variables:
        TRADE_SAFETY_MODEL: OpenAI model name (default: gpt-5.2)
        TRADE_SAFETY_ML_ENABLED: Enable ML classifier (default: False)
        TRADE_SAFETY_ML_MODEL_DIR: ML model directory path
        TRADE_SAFETY_ML_THRESHOLD_HIGH: ML high confidence threshold (default: 0.85)
        TRADE_SAFETY_ML_THRESHOLD_LOW: ML low confidence threshold (default: 0.20)
    """

    # LLM settings
    model: str = "gpt-5.2"

    # ML settings
    ml_enabled: bool = False
    ml_model_dir: Path | None = None
    ml_threshold_high: float = 0.85
    ml_threshold_low: float = 0.20

    class Config:
        env_prefix = "TRADE_SAFETY_"
