"""Settings for Trade Safety service."""

from pathlib import Path

from pydantic import field_validator, model_validator
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

    @field_validator("ml_threshold_high", "ml_threshold_low")
    @classmethod
    def validate_threshold_range(cls, v: float) -> float:
        """Validate threshold values are in valid range (0.0~1.0)."""
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Threshold must be between 0.0 and 1.0, got {v}")
        return v

    @model_validator(mode="after")
    def validate_threshold_order(self) -> "TradeSafetyModelSettings":
        """Validate that ml_threshold_low < ml_threshold_high."""
        if self.ml_threshold_low >= self.ml_threshold_high:
            raise ValueError(
                f"ml_threshold_low ({self.ml_threshold_low}) must be less than "
                f"ml_threshold_high ({self.ml_threshold_high})"
            )
        return self

    @model_validator(mode="after")
    def validate_ml_config(self) -> "TradeSafetyModelSettings":
        """Validate ML configuration consistency."""
        if self.ml_enabled and self.ml_model_dir is None:
            raise ValueError(
                "ml_model_dir is required when ml_enabled is True. "
                "Set TRADE_SAFETY_ML_MODEL_DIR environment variable."
            )
        return self

    class Config:
        env_prefix = "TRADE_SAFETY_"
