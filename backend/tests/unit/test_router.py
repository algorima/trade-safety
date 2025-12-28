"""Tests for trade safety router with UserInfoProvider."""

from unittest.mock import MagicMock

import pytest
from aioia_core.auth import UserInfo, UserInfoProvider, UserRole
from aioia_core.settings import JWTSettings, OpenAIAPISettings
from sqlalchemy.orm import Session, sessionmaker

from trade_safety.api.router import create_trade_safety_router
from trade_safety.factories import TradeSafetyCheckManagerFactory
from trade_safety.settings import TradeSafetyModelSettings


class MockUserInfoProvider:
    """Mock implementation of UserInfoProvider protocol."""

    def get_user_info(self, user_id: str, db: Session) -> UserInfo | None:
        """Return mock user info."""
        return UserInfo(
            user_id=user_id,
            username="test_user",
            nickname="Test User",
            email="test@example.com",
            role=UserRole.USER,
        )


@pytest.fixture
def openai_api() -> OpenAIAPISettings:
    """Create OpenAI API settings for testing."""
    return OpenAIAPISettings(api_key="test-key")


@pytest.fixture
def model_settings() -> TradeSafetyModelSettings:
    """Create model settings for testing."""
    return TradeSafetyModelSettings()


@pytest.fixture
def jwt_settings() -> JWTSettings:
    """Create JWT settings for testing."""
    return JWTSettings(secret_key="test-secret-key")


@pytest.fixture
def mock_session_factory() -> sessionmaker:
    """Create mock session factory."""
    return MagicMock(spec=sessionmaker)


@pytest.fixture
def mock_manager_factory() -> TradeSafetyCheckManagerFactory:
    """Create mock manager factory."""
    return MagicMock(spec=TradeSafetyCheckManagerFactory)


@pytest.fixture
def user_info_provider() -> UserInfoProvider:
    """Create mock UserInfoProvider."""
    return MockUserInfoProvider()


def test_create_trade_safety_router_with_user_info_provider(
    openai_api: OpenAIAPISettings,
    model_settings: TradeSafetyModelSettings,
    jwt_settings: JWTSettings,
    mock_session_factory: sessionmaker,
    mock_manager_factory: TradeSafetyCheckManagerFactory,
    user_info_provider: UserInfoProvider,
) -> None:
    """Test that router accepts UserInfoProvider."""
    router = create_trade_safety_router(
        openai_api=openai_api,
        model_settings=model_settings,
        jwt_settings=jwt_settings,
        db_session_factory=mock_session_factory,
        manager_factory=mock_manager_factory,
        user_info_provider=user_info_provider,
    )

    assert router is not None


def test_create_trade_safety_router_with_none_user_info_provider(
    openai_api: OpenAIAPISettings,
    model_settings: TradeSafetyModelSettings,
    jwt_settings: JWTSettings,
    mock_session_factory: sessionmaker,
    mock_manager_factory: TradeSafetyCheckManagerFactory,
) -> None:
    """Test that router works with None UserInfoProvider."""
    router = create_trade_safety_router(
        openai_api=openai_api,
        model_settings=model_settings,
        jwt_settings=jwt_settings,
        db_session_factory=mock_session_factory,
        manager_factory=mock_manager_factory,
        user_info_provider=None,
    )

    assert router is not None
