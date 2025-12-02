"""Repository factory for Trade Safety."""

from __future__ import annotations

from sqlalchemy.orm import sessionmaker

from aioia_core.factories import BaseRepositoryFactory

from trade_safety.repositories.trade_safety_repository import (
    DatabaseTradeSafetyCheckManager,
)


class TradeSafetyCheckManagerFactory(BaseRepositoryFactory[DatabaseTradeSafetyCheckManager]):
    """Factory for creating TradeSafetyCheckManager instances.

    Inherits from BaseRepositoryFactory which provides:
    - create_repository(db_session=None): Create repository instance
    - create_manager(db_session=None): Deprecated alias for backward compatibility
    """

    def __init__(self, db_session_factory: sessionmaker):
        """Initialize factory with session factory.

        Args:
            db_session_factory: SQLAlchemy session factory
        """
        super().__init__(db_session_factory, DatabaseTradeSafetyCheckManager)
