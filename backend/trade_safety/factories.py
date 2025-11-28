"""Manager factory for Trade Safety."""

from __future__ import annotations

from sqlalchemy.orm import Session

from trade_safety.repositories.trade_safety_repository import (
    DatabaseTradeSafetyCheckManager,
)


class TradeSafetyCheckManagerFactory:
    """Factory for creating TradeSafetyCheckManager instances."""

    def create_manager(self, db_session: Session) -> DatabaseTradeSafetyCheckManager:
        """
        Create a manager instance with the given session.

        Args:
            db_session: Database session

        Returns:
            DatabaseTradeSafetyCheckManager instance
        """
        return DatabaseTradeSafetyCheckManager(db_session)
