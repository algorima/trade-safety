"""
Database infrastructure for Trade Safety.

This module provides base database models and CRUD manager patterns.

TODO: 이 코드는 Buppy에서 복사됨. 추후 buppy-common 라이브러리로 추출 예정
Copied from Buppy for independence. Will be extracted to buppy-common later.
"""

from __future__ import annotations

import uuid
from abc import ABC
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import DateTime, MetaData, String, and_, desc, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# ==============================================================================
# SQLAlchemy Base Models
# ==============================================================================

# Define naming convention for database constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)


class Base(DeclarativeBase):
    """The base class for all SQLAlchemy declarative models."""

    metadata = metadata


class BaseModel(Base):
    """Base model with id, created_at, and updated_at fields."""

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# ==============================================================================
# Base Manager (CRUD Operations)
# ==============================================================================

ModelType = TypeVar("ModelType", bound=PydanticBaseModel)
DBModelType = TypeVar("DBModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class BaseManager(
    ABC,
    Generic[ModelType, DBModelType, CreateSchemaType, UpdateSchemaType],
):
    """
    Base manager class for basic database CRUD operations.

    Args:
        db_session: SQLAlchemy session.
        db_model: SQLAlchemy model class.
        convert_to_model: Function to convert DB model to Pydantic model.
        convert_to_db_model: Function to convert Pydantic model to DB model data dict.
        default_load_options: Default SQLAlchemy loader options to apply to queries.
    """

    def __init__(
        self,
        db_session: Session,
        db_model: type[DBModelType],
        convert_to_model: Callable[[DBModelType], ModelType],
        convert_to_db_model: Callable[[CreateSchemaType], dict],
        default_load_options: list[Any] | None = None,
    ):
        self.db_session = db_session
        self.db_model = db_model
        self.convert_to_model = convert_to_model
        self.convert_to_db_model = convert_to_db_model
        self.default_load_options = (
            default_load_options if default_load_options is not None else []
        )

    def get_by_id(
        self, item_id: str, load_options: list[Any] | None = None
    ) -> ModelType | None:
        """Retrieves an item by its ID, with optional eager loading."""
        query = self.db_session.query(self.db_model)

        options_to_apply = self.default_load_options
        if load_options is not None:
            options_to_apply = load_options

        if options_to_apply:
            query = query.options(*options_to_apply)

        db_item = query.filter(self.db_model.id == item_id).first()
        return self.convert_to_model(db_item) if db_item else None

    def get_all(
        self,
        current: int = 1,
        page_size: int = 10,
        sort: list[tuple[str, str]] | None = None,
        filters: list[dict[str, Any]] | None = None,
        load_options: list[Any] | None = None,
    ) -> tuple[list[ModelType], int]:
        """
        Retrieves all items with pagination, sorting, filtering, and optional eager loading.

        Args:
            current: Current page number (starts from 1).
            page_size: Number of items per page.
            sort: Sort criteria [(field_name, 'asc'|'desc'), ...].
            filters: Filter criteria [{'field': field_name, 'operator': operator, 'value': value}, ...].
            load_options: SQLAlchemy loader options to apply to the query.

        Returns:
            A tuple containing the list of items and the total number of items.
        """
        # Start with base query
        query = self.db_session.query(self.db_model)

        # Apply loading options
        options_to_apply = self.default_load_options
        if load_options is not None:
            options_to_apply = load_options

        if options_to_apply:
            query = query.options(*options_to_apply)

        # Apply filters
        if filters:
            filter_conditions = self._build_filter_conditions(filters)
            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

        # Apply sorting
        if sort:
            for field, order in sort:
                column = getattr(self.db_model, field, None)
                if column is None:
                    continue
                if order.lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(column)
        elif hasattr(self.db_model, "created_at"):
            query = query.order_by(desc(self.db_model.created_at))

        # Get total count
        total = query.count()

        # Apply pagination
        if page_size >= 0:
            offset = (current - 1) * page_size
            query = query.offset(offset).limit(page_size)

        db_items = query.all()

        return [self.convert_to_model(item) for item in db_items], total

    def _build_filter_conditions(self, filters: list[dict[str, Any]]) -> list[Any]:
        """Recursively builds SQLAlchemy filter conditions from filter criteria."""
        conditions = []
        for filter_item in filters:
            operator = filter_item.get("operator")

            # Conditional Filter (or/and)
            if (
                operator in {"or", "and"}
                and "value" in filter_item
                and isinstance(filter_item["value"], list)
            ):
                nested_conditions = self._build_filter_conditions(filter_item["value"])
                if nested_conditions:
                    if operator == "or":
                        conditions.append(or_(*nested_conditions))
                    else:
                        conditions.append(and_(*nested_conditions))
                continue

            # Logical Filter
            field = filter_item.get("field")
            if not field:
                continue

            column = getattr(self.db_model, field, None)
            if column is None:
                continue

            # Handle value-less operators first
            if operator == "null":
                conditions.append(column.is_(None))
                continue
            if operator == "nnull":
                conditions.append(column.isnot(None))
                continue

            value = filter_item.get("value")
            if value is None:  # Skip operators that require a value
                continue

            if operator == "eq":
                conditions.append(column == value)
            elif operator == "ne":
                conditions.append(column != value)
            elif operator == "contains":
                conditions.append(column.ilike(f"%{value}%"))
            elif operator == "startswith":
                conditions.append(column.ilike(f"{value}%"))
            elif operator == "endswith":
                conditions.append(column.ilike(f"%{value}"))
            elif operator == "gt":
                conditions.append(column > value)
            elif operator == "gte":
                conditions.append(column >= value)
            elif operator == "lt":
                conditions.append(column < value)
            elif operator == "lte":
                conditions.append(column <= value)
            elif operator == "in":
                conditions.append(column.in_(value))

        return conditions

    def create(self, schema: CreateSchemaType) -> ModelType:
        """Creates a new item."""
        create_data = self.convert_to_db_model(schema)

        if "id" not in create_data or create_data.get("id") is None:
            create_data["id"] = str(uuid.uuid4())

        if hasattr(self.db_model, "created_at") and (
            "created_at" not in create_data or create_data.get("created_at") is None
        ):
            create_data["created_at"] = datetime.now(timezone.utc)
        if hasattr(self.db_model, "updated_at") and (
            "updated_at" not in create_data or create_data.get("updated_at") is None
        ):
            create_data["updated_at"] = datetime.now(timezone.utc)

        db_item = self.db_model(**create_data)
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)
        return self.convert_to_model(db_item)

    def update(self, item_id: str, schema: UpdateSchemaType) -> ModelType | None:
        """Updates an existing item."""
        db_item = (
            self.db_session.query(self.db_model)
            .filter(self.db_model.id == item_id)
            .first()
        )
        if not db_item:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_item, field):
                setattr(db_item, field, value)

        if hasattr(db_item, "updated_at"):
            db_item.updated_at = datetime.now(timezone.utc)

        self.db_session.commit()
        self.db_session.refresh(db_item)
        return self.convert_to_model(db_item)

    def delete(self, item_id: str) -> bool:
        """
        Deletes an item by its ID.
        Any database exceptions (e.g., IntegrityError for foreign key constraints)
        are intentionally not caught here and will be propagated.

        Args:
            item_id: The unique identifier of the item to delete.

        Returns:
            True if the item was found and deleted successfully.
            False if the item was not found.
        """
        db_item = (
            self.db_session.query(self.db_model)
            .filter(self.db_model.id == item_id)
            .first()
        )
        if not db_item:
            return False

        self.db_session.delete(db_item)
        self.db_session.commit()
        return True
