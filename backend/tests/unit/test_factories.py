"""Tests for TradeSafetyCheckManagerFactory."""

import warnings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aioia_core.factories import BaseRepositoryFactory
from aioia_core.models import Base

from trade_safety.factories import TradeSafetyCheckManagerFactory
from trade_safety.repositories.trade_safety_repository import (
    DatabaseTradeSafetyCheckManager,
)


def _create_db_session_factory() -> sessionmaker:
    """Create in-memory SQLite database session factory."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


class TestTradeSafetyCheckManagerFactory:
    """Tests for TradeSafetyCheckManagerFactory."""

    def test_inherits_from_base_repository_factory(self):
        """Factory should inherit from BaseRepositoryFactory."""
        factory = TradeSafetyCheckManagerFactory(_create_db_session_factory())

        assert isinstance(factory, BaseRepositoryFactory)

    def test_has_create_repository_method(self):
        """Factory should have create_repository method from BaseRepositoryFactory."""
        factory = TradeSafetyCheckManagerFactory(_create_db_session_factory())

        assert hasattr(factory, "create_repository")
        assert callable(factory.create_repository)

    def test_create_repository_returns_manager_instance(self):
        """create_repository should return DatabaseTradeSafetyCheckManager instance."""
        factory = TradeSafetyCheckManagerFactory(_create_db_session_factory())

        repository = factory.create_repository()

        assert repository is not None
        assert isinstance(repository, DatabaseTradeSafetyCheckManager)

    def test_create_repository_with_session(self):
        """create_repository should accept optional db_session parameter."""
        db_session_factory = _create_db_session_factory()
        factory = TradeSafetyCheckManagerFactory(db_session_factory)
        session = db_session_factory()

        repository = factory.create_repository(session)

        assert repository is not None
        assert isinstance(repository, DatabaseTradeSafetyCheckManager)
        assert repository.db_session is session

    def test_deprecated_create_manager_still_works(self):
        """create_manager should still work for backward compatibility."""
        factory = TradeSafetyCheckManagerFactory(_create_db_session_factory())

        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("always")
            repository = factory.create_manager()

        assert repository is not None
        assert isinstance(repository, DatabaseTradeSafetyCheckManager)
        assert any(issubclass(w.category, DeprecationWarning) for w in caught_warnings)
