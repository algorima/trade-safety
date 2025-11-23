from datetime import datetime

from aioia_core.database import BaseModel
from sqlalchemy import JSON, Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class DBTradeSafetyCheck(BaseModel):
    """
    Represents a trade safety check request and its analysis results.

    Attributes:
        id (str): Primary key, unique identifier (inherited from BaseModel)
        user_id (str | None): Foreign key to user_profiles, None for guest users
        input_text (str): The trade post text or URL provided by user
        llm_analysis (dict): LLM analysis result in JSON format
        risk_score (int): Risk score from 0-100
        expert_advice (str | None): Additional advice added by expert
        expert_reviewed (bool): Whether expert has reviewed this check
        expert_reviewed_at (datetime | None): When expert reviewed
        expert_reviewed_by (str | None): ID of expert who reviewed
        created_at (datetime): When the check was created (inherited)
        updated_at (datetime): When the check was last updated (inherited)
    """

    __tablename__ = "trade_safety_checks"

    user_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="External user ID from parent application (no FK for open-source portability)",
    )
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    llm_analysis: Mapped[dict] = mapped_column(JSON, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)

    # Expert review fields
    expert_advice: Mapped[str | None] = mapped_column(Text, nullable=True)
    expert_reviewed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false", index=True
    )
    expert_reviewed_at: Mapped[datetime | None] = mapped_column(
        nullable=True, default=None
    )
    expert_reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
