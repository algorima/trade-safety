"""Trade Safety Check Manager implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from trade_safety.database.models import DBTradeSafetyCheck
from trade_safety.infrastructure.database import BaseManager
from trade_safety.models import (
    TradeSafetyAnalysis,
    TradeSafetyCheck,
    TradeSafetyCheckCreate,
    TradeSafetyCheckUpdate,
)


class TradeSafetyCheckManager(ABC):
    """
    Abstract base class for Trade Safety Check management.

    Provides interface for creating, retrieving, and updating trade safety checks.
    """

    @abstractmethod
    def create(self, schema: TradeSafetyCheckCreate) -> TradeSafetyCheck:
        """
        Create a new trade safety check.

        Args:
            schema: Trade safety check creation data with all required fields

        Returns:
            Created trade safety check
        """

    @abstractmethod
    def get_by_id(self, item_id: str) -> TradeSafetyCheck | None:
        """
        Retrieve a trade safety check by ID.

        Args:
            item_id: Unique identifier of the check

        Returns:
            Trade safety check if found, None otherwise
        """

    @abstractmethod
    def update(
        self, item_id: str, schema: TradeSafetyCheckUpdate
    ) -> TradeSafetyCheck | None:
        """
        Update an existing trade safety check.

        Args:
            item_id: Unique identifier of the check
            schema: Update data

        Returns:
            Updated trade safety check if found, None otherwise
        """


def _convert_db_to_model(db_check: DBTradeSafetyCheck) -> TradeSafetyCheck:
    """Convert DBTradeSafetyCheck to TradeSafetyCheck with type-safe llm_analysis."""
    return TradeSafetyCheck(
        id=db_check.id,
        user_id=db_check.user_id,
        input_text=db_check.input_text,
        llm_analysis=TradeSafetyAnalysis(**db_check.llm_analysis),
        risk_score=db_check.risk_score,
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
