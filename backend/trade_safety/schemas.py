from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class RiskSeverity(str, Enum):
    """Severity level of a risk signal"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskCategory(str, Enum):
    """Category of risk signal"""

    PAYMENT = "payment"
    SELLER = "seller"
    PLATFORM = "platform"
    PRICE = "price"
    CONTENT = "content"


class RiskSignal(BaseModel):
    """Individual risk signal detected in the trade"""

    category: RiskCategory
    severity: RiskSeverity
    title: str
    description: str
    what_to_do: str = Field(description="Recommended action for user")

    model_config = ConfigDict(from_attributes=True)


class PriceAnalysis(BaseModel):
    """Analysis of trade price"""

    market_price_range: str | None = Field(
        None, description="Typical market price range"
    )
    offered_price: Decimal | None = Field(None, description="Price offered in trade")
    currency: str | None = Field(
        None, max_length=3, description="ISO 4217 currency code (e.g., USD, KRW, JPY)"
    )
    price_assessment: str = Field(description="Assessment of price fairness")
    warnings: list[str] = Field(
        default_factory=list, description="Price-related warnings"
    )

    @field_validator("offered_price", mode="before")
    @classmethod
    def parse_offered_price(cls, v: Any) -> Any:
        """
        Convert 'N/A' or empty string to None for Decimal parsing.

        This is a pre-validator that normalizes input before Pydantic's
        automatic type conversion to Decimal.
        """
        if v is None:
            return None
        if isinstance(v, str) and v.strip().upper() in {"N/A", ""}:
            return None
        return v  # type: ignore[return-value]  # Pydantic handles type conversion after validation

    @field_serializer("offered_price")
    def serialize_offered_price(self, value: Decimal | None) -> float | None:
        """
        Convert Decimal to float for JSON serialization.

        Decimal is not JSON serializable by default, so we convert to float
        for API responses while maintaining Decimal internally for accuracy.
        """
        if value is None:
            return None
        return float(value)

    model_config = ConfigDict(from_attributes=True)


class TradeSafetyAnalysis(BaseModel):
    """Complete LLM analysis of a trade"""

    ai_summary: list[str] = Field(
        default_factory=list, description="AI-generated 3-line summary of the trade analysis"
    )
    translation: str | None = Field(
        None, description="Translation of trade post if not in English"
    )
    nuance_explanation: str | None = Field(
        None, description="Explanation of Korean slang/nuances"
    )
    risk_signals: list[RiskSignal] = Field(
        default_factory=list, description="Identified risk signals"
    )
    cautions: list[RiskSignal] = Field(
        default_factory=list, description="Points requiring caution"
    )
    safe_indicators: list[RiskSignal] = Field(
        default_factory=list, description="Positive safety indicators"
    )
    price_analysis: PriceAnalysis = Field(description="Price analysis")
    safety_checklist: list[str] = Field(
        default_factory=list, description="Safety checklist items"
    )
    safe_score: int = Field(
        ge=0, le=100, description="Overall safety score 0-100 (higher is safer)"
    )
    recommendation: str = Field(description="Final recommendation")
    emotional_support: str = Field(description="Empathetic message to reduce anxiety")

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# Domain Models (following Shipment pattern)
# ==============================================================================


class TradeSafetyCheckBase(BaseModel):
    """Base model with common fields (excluding llm_analysis which differs by use case)"""

    model_config = ConfigDict(from_attributes=True)

    # User input fields
    input_text: str = Field(description="Trade post URL or text")

    # System-generated fields
    user_id: str | None = Field(None, description="User ID (None for guest)")
    safe_score: int = Field(
        ge=0, le=100, description="Overall safety score (higher is safer)"
    )

    # Expert review fields
    expert_advice: str | None = Field(None, description="Expert advice text")
    expert_reviewed: bool = Field(default=False, description="Whether expert reviewed")
    expert_reviewed_at: datetime | None = Field(
        None, description="Expert review timestamp"
    )
    expert_reviewed_by: str | None = Field(None, description="Expert reviewer ID")


class TradeSafetyCheckCreate(TradeSafetyCheckBase):
    """Internal creation schema with all required fields (DB storage)"""

    llm_analysis: dict[str, Any] = Field(
        description="LLM analysis result serialized to dict for DB storage"
    )


class TradeSafetyCheck(TradeSafetyCheckBase):
    """Complete model with system fields (API response with type-safe analysis)"""

    id: str
    llm_analysis: TradeSafetyAnalysis = Field(
        description="LLM analysis result with structured type"
    )
    created_at: datetime
    updated_at: datetime


class TradeSafetyCheckUpdate(BaseModel):
    """Update schema for safety check (primarily for internal use)"""

    user_id: str | None = Field(
        default=None, description="User ID for claiming guest checks"
    )
    expert_advice: str | None = Field(default=None, description="Expert advice text")
    expert_reviewed: bool | None = Field(
        default=None, description="Whether expert reviewed"
    )
    expert_reviewed_at: datetime | None = Field(
        default=None, description="Expert review timestamp"
    )
    expert_reviewed_by: str | None = Field(
        default=None, description="Expert reviewer ID"
    )

    model_config = ConfigDict(from_attributes=True)
