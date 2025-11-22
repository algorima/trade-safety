"""
Vendored code from Buppy for standalone execution.

TODO: 이 코드는 Buppy에서 복사됨. 추후 buppy-common 라이브러리로 추출 예정
Copied from Buppy for independence. Will be extracted to buppy-common later.
"""

from trade_safety._vendor.config import (
    ModelSettings,
    TradeSafetyConfig,
    create_db_session_factory,
    init_database,
)
from trade_safety._vendor.database import Base, BaseManager, BaseModel
from trade_safety._vendor.errors import (
    RESOURCE_NOT_FOUND,
    UNAUTHORIZED,
    VALIDATION_ERROR,
    ErrorResponse,
    extract_error_code_from_exception,
    get_error_detail_from_exception,
)

__all__ = [
    # Config
    "TradeSafetyConfig",
    "ModelSettings",
    "create_db_session_factory",
    "init_database",
    # Database
    "Base",
    "BaseModel",
    "BaseManager",
    # Errors
    "ErrorResponse",
    "UNAUTHORIZED",
    "VALIDATION_ERROR",
    "RESOURCE_NOT_FOUND",
    "extract_error_code_from_exception",
    "get_error_detail_from_exception",
]
