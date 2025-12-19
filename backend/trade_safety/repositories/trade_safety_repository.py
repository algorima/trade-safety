"""Trade Safety Check Repository implementation."""

from __future__ import annotations

from aioia_core.managers import BaseManager
from sqlalchemy.orm import Session

from trade_safety.managers import TradeSafetyCheckManager
from trade_safety.models import DBTradeSafetyCheck
from trade_safety.schemas import (
    TradeSafetyAnalysis,
    TradeSafetyCheck,
    TradeSafetyCheckCreate,
    TradeSafetyCheckUpdate,
)


def _convert_db_to_model(db_check: DBTradeSafetyCheck) -> TradeSafetyCheck:
    """Convert DBTradeSafetyCheck to TradeSafetyCheck with type-safe llm_analysis."""
    return TradeSafetyCheck(
        id=db_check.id,
        user_id=db_check.user_id,
        input_text=db_check.input_text,
        llm_analysis=TradeSafetyAnalysis(**db_check.llm_analysis),
        safe_score=db_check.safe_score,
        expert_advice=db_check.expert_advice,
        expert_reviewed=db_check.expert_reviewed,
        expert_reviewed_at=db_check.expert_reviewed_at,
        expert_reviewed_by=db_check.expert_reviewed_by,
        created_at=db_check.created_at,
        updated_at=db_check.updated_at,
    )


def _convert_to_db_model(schema: TradeSafetyCheckCreate) -> dict:
    """Convert TradeSafetyCheckCreate to database dict."""
    return schema.model_dump(exclude_unset=True)


class DatabaseTradeSafetyCheckManager(
    BaseManager[
        TradeSafetyCheck,
        DBTradeSafetyCheck,
        TradeSafetyCheckCreate,
        TradeSafetyCheckUpdate,
    ],
    TradeSafetyCheckManager,
):
    """Database implementation of TradeSafetyCheckManager."""

    def __init__(self, db_session: Session):
        """
        Initialize DatabaseTradeSafetyCheckManager.

        Args:
            db_session: SQLAlchemy session
        """
        super().__init__(
            db_session=db_session,
            db_model=DBTradeSafetyCheck,
            convert_to_model=_convert_db_to_model,
            convert_to_db_model=_convert_to_db_model,
        )
