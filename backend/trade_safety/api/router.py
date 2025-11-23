"""
Trade Safety Router for K-pop Merchandise Trading Safety Checks.

This module provides public API endpoints for trade safety analysis:
- POST /trade-safety: Create a new safety check (public, freemium model)
- GET /trade-safety/{check_id}: Get detailed results (requires authentication)
"""

import logging

from aioia_core import errors as error_codes
from aioia_core.auth import UserRoleProvider
from aioia_core.errors import ErrorResponse
from aioia_core.fastapi import BaseCrudRouter
from aioia_core.settings import JWTSettings, OpenAIAPISettings
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import sessionmaker

from trade_safety.factories import TradeSafetyCheckManagerFactory
from trade_safety.repositories.trade_safety_repository import (
    DatabaseTradeSafetyCheckManager,
)
from trade_safety.schemas import (
    QuickCheckResponse,
    QuickCheckSummary,
    TradeSafetyCheck,
    TradeSafetyCheckCreate,
    TradeSafetyCheckUpdate,
)
from trade_safety.service import TradeSafetyService
from trade_safety.settings import TradeSafetyModelSettings

logger = logging.getLogger(__name__)


# ==============================================================================
# API Request/Response Schemas (Router-level, not in domain models)
# ==============================================================================


class TradeSafetyCheckRequest(BaseModel):
    """Public API request for creating a trade safety check (user input only)"""

    input_text: str = Field(description="Trade post URL or text")


class SingleItemResponseModel(BaseModel):
    """Standard CRUD response wrapping single item in data field"""

    data: TradeSafetyCheck


class QuickCheckResponseModel(BaseModel):
    """Standard CRUD response wrapping QuickCheckResponse in data field"""

    data: QuickCheckResponse


# ==============================================================================
# Router Implementation
# ==============================================================================


class TradeSafetyRouter(
    BaseCrudRouter[
        TradeSafetyCheck,
        TradeSafetyCheckCreate,
        TradeSafetyCheckUpdate,
        DatabaseTradeSafetyCheckManager,
    ]
):
    """
    Trade Safety router with public POST and authenticated GET.

    Unlike standard CRUD routers, this provides:
    - Public POST endpoint (freemium model: quick summary for guests, full for auth users)
    - Authenticated GET endpoint with ownership verification
    - No List, Update, or Delete operations
    """

    def __init__(
        self,
        openai_api: OpenAIAPISettings,
        model_settings: TradeSafetyModelSettings,
        **kwargs,
    ):
        """
        Initialize with Settings objects for LLM service.

        Args:
            openai_api: OpenAI API settings
            model_settings: Model settings
            **kwargs: BaseCrudRouter arguments
        """
        self.openai_api = openai_api
        self.model_settings = model_settings
        super().__init__(**kwargs)

    def _register_routes(self) -> None:
        """Register custom routes instead of standard CRUD"""
        self._register_public_create_route()
        self._register_authenticated_get_route()
        # Admin routes
        self._register_list_route()  # GET /trade-safety (Admin only)
        self._register_update_route()  # PATCH /trade-safety/{id} (Admin only)

    def _register_public_create_route(self) -> None:
        """POST /trade-safety - Public endpoint with freemium model"""

        @self.router.post(
            f"/{self.resource_name}",
            response_model=QuickCheckResponseModel | SingleItemResponseModel,
            summary="Create Trade Safety Check",
            description="""
            Analyze a K-pop merchandise trade for safety issues.

            **Freemium Model**:
            - Non-authenticated users: Get quick summary (risk signal count only)
            - Authenticated users: Get full analysis with detailed recommendations

            The service helps international fans overcome:
            - Language barriers (Korean slang translation)
            - Trust issues (scam signal detection)
            - Information gaps (price analysis)
            - Lack of protection (safety checklist)
            """,
            responses={
                200: {
                    "description": "Safety check completed successfully",
                },
                401: {
                    "model": ErrorResponse,
                    "description": "Invalid authentication token",
                },
                422: {"model": ErrorResponse, "description": "Validation error"},
                500: {"model": ErrorResponse, "description": "Internal server error"},
            },
        )
        async def create_check(
            request: TradeSafetyCheckRequest,
            user_id: str | None = Depends(self.get_current_user_id_dep),
            manager: DatabaseTradeSafetyCheckManager = Depends(self.get_manager_dep),
        ):
            """
            Create a new trade safety check.

            Flow:
            1. Analyze trade using LLM (TradeSafetyService)
            2. Convert Request + Analysis → Domain Create schema
            3. Save to database via manager.create() (BaseManager)
            4. Return quick summary for non-auth or full analysis for auth users
            """
            logger.info(
                "Creating trade safety check: user_id=%s, authenticated=%s",
                user_id or "guest",
                user_id is not None,
            )

            try:
                # Step 1: Analyze trade using LLM
                service = TradeSafetyService(self.openai_api, self.model_settings)
                analysis = await service.analyze_trade(
                    input_text=request.input_text,
                )

                # Step 2: Convert API Request → Domain Create schema (type-safe!)
                create_data = TradeSafetyCheckCreate(
                    # User input fields
                    input_text=request.input_text,
                    # System-generated fields
                    user_id=user_id,
                    llm_analysis=analysis.model_dump(),
                    risk_score=analysis.risk_score,
                    expert_advice=None,
                    expert_reviewed=False,
                    expert_reviewed_at=None,
                    expert_reviewed_by=None,
                )

                # Step 3: Save via BaseManager.create()
                check = manager.create(create_data)

                logger.info(
                    "Trade safety check created: id=%s, risk_score=%d, authenticated=%s",
                    check.id,
                    check.risk_score,
                    user_id is not None,
                )

                # Step 4: Return appropriate response based on auth status
                if not user_id:
                    # Non-authenticated: Quick summary wrapped in data field
                    return QuickCheckResponseModel(
                        data=QuickCheckResponse(
                            id=check.id,
                            quick_summary=QuickCheckSummary(
                                risk_signals_count=len(analysis.risk_signals),
                                cautions_count=len(analysis.cautions),
                                safe_indicators_count=len(analysis.safe_indicators),
                            ),
                            signup_required=True,
                        )
                    )

                # Authenticated: Full analysis wrapped in data field
                return SingleItemResponseModel(data=check)

            except ValueError as e:
                # Input validation errors from service
                logger.warning("Validation error in trade safety check: %s", e)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "detail": str(e),
                        "code": error_codes.VALIDATION_ERROR,
                    },
                ) from e

    def _register_authenticated_get_route(self) -> None:
        """GET /trade-safety/{check_id} - Public endpoint with freemium model"""

        @self.router.get(
            f"/{self.resource_name}/{{check_id}}",
            response_model=QuickCheckResponseModel | SingleItemResponseModel,
            summary="Get Trade Safety Check Details",
            description="""
            Retrieve results of a previously created safety check.

            **Freemium Model**:
            - Non-authenticated users: Get quick summary (risk signal count only)
            - Authenticated users: Get full analysis with detailed recommendations

            **Access**: Anyone with the check_id URL can view the analysis.
            The check_id acts as a secure access token (UUID).
            """,
            responses={
                200: {"description": "Safety check details retrieved successfully"},
                404: {"model": ErrorResponse, "description": "Check not found"},
            },
        )
        async def get_check(
            check_id: str,
            user_id: str | None = Depends(self.get_current_user_id_dep),
            manager: DatabaseTradeSafetyCheckManager = Depends(self.get_manager_dep),
        ):
            """
            Get results of a safety check.

            Access: Anyone with the check_id URL can view.
            The check_id serves as the access control mechanism.
            """
            # Retrieve check via manager
            check = manager.get_by_id(check_id)

            if not check:
                logger.warning(
                    "Check not found: check_id=%s, user_id=%s",
                    check_id,
                    user_id or "guest",
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "detail": "Trade safety check not found",
                        "code": error_codes.RESOURCE_NOT_FOUND,
                    },
                )

            logger.info(
                "Retrieved trade safety check: check_id=%s, user_id=%s, owner_id=%s, authenticated=%s",
                check_id,
                user_id or "guest",
                check.user_id or "guest",
                user_id is not None,
            )

            # Return appropriate response based on auth status
            if not user_id:
                # Non-authenticated: Quick summary
                return QuickCheckResponseModel(
                    data=QuickCheckResponse(
                        id=check.id,
                        quick_summary=QuickCheckSummary(
                            risk_signals_count=len(check.llm_analysis.risk_signals),
                            cautions_count=len(check.llm_analysis.cautions),
                            safe_indicators_count=len(
                                check.llm_analysis.safe_indicators
                            ),
                        ),
                        signup_required=True,
                    )
                )

            # Authenticated: Full analysis
            return SingleItemResponseModel(data=check)


def create_trade_safety_router(
    openai_api: OpenAIAPISettings,
    model_settings: TradeSafetyModelSettings,
    jwt_settings: JWTSettings,
    db_session_factory: sessionmaker,
    manager_factory: TradeSafetyCheckManagerFactory,
    role_provider: UserRoleProvider | None,
) -> APIRouter:
    """
    Create trade safety router with public POST and authenticated GET.

    Args:
        openai_api (OpenAIAPISettings): OpenAI API settings
        model_settings (TradeSafetyModelSettings): Model settings
        jwt_settings (JWTSettings): JWT authentication settings
        db_session_factory (sessionmaker): SQLAlchemy session factory
        manager_factory (TradeSafetyCheckManagerFactory): Factory for creating manager
        role_provider (UserRoleProvider | None): UserRoleProvider for authentication

    Returns:
        APIRouter: Configured FastAPI router
    """
    router = TradeSafetyRouter(
        openai_api=openai_api,
        model_settings=model_settings,
        model_class=TradeSafetyCheck,
        create_schema=TradeSafetyCheckCreate,
        update_schema=TradeSafetyCheckUpdate,
        db_session_factory=db_session_factory,
        manager_factory=manager_factory,
        role_provider=role_provider,
        jwt_secret_key=jwt_settings.secret_key,
        resource_name="trade-safety",
        tags=["Trade Safety"],
    )
    return router.get_router()
