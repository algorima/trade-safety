"""Tests for TradeSafetyCheckManagerFactory."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aioia_core.factories import BaseRepositoryFactory
from aioia_core.models import Base

from trade_safety.factories import TradeSafetyCheckManagerFactory
from trade_safety.repositories.trade_safety_repository import (
    DatabaseTradeSafetyCheckManager,
)


@pytest.fixture
def db_session_factory():
    """Create in-memory SQLite database session factory."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


class TestTradeSafetyCheckManagerFactory:
    """Tests for TradeSafetyCheckManagerFactory."""

    def test_inherits_from_base_repository_factory(self, db_session_factory):
        """Factory should inherit from BaseRepositoryFactory."""
        factory = TradeSafetyCheckManagerFactory(db_session_factory)

        assert isinstance(factory, BaseRepositoryFactory)

    def test_has_create_repository_method(self, db_session_factory):
        """Factory should have create_repository method from BaseRepositoryFactory."""
        factory = TradeSafetyCheckManagerFactory(db_session_factory)

        assert hasattr(factory, "create_repository")
        assert callable(factory.create_repository)

    def test_create_repository_returns_manager_instance(self, db_session_factory):
        """create_repository should return DatabaseTradeSafetyCheckManager instance."""
        factory = TradeSafetyCheckManagerFactory(db_session_factory)

        repository = factory.create_repository()

        assert isinstance(repository, DatabaseTradeSafetyCheckManager)

    def test_create_repository_with_session(self, db_session_factory):
        """create_repository should accept optional db_session parameter."""
        factory = TradeSafetyCheckManagerFactory(db_session_factory)
        session = db_session_factory()

        repository = factory.create_repository(session)

        assert isinstance(repository, DatabaseTradeSafetyCheckManager)
        assert repository.db_session is session

    def test_deprecated_create_manager_still_works(self, db_session_factory):
        """create_manager should still work for backward compatibility."""
        factory = TradeSafetyCheckManagerFactory(db_session_factory)

        with pytest.warns(DeprecationWarning):
            repository = factory.create_manager()

        assert isinstance(repository, DatabaseTradeSafetyCheckManager)
