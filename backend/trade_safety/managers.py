"""Trade Safety Check Manager Protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod

from trade_safety.schemas import (
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
