"""Display order schema definitions for item and category ordering.

This module provides strict Pydantic models for display-order intent and
request/response contracts used by business management resources.
"""

from enum import Enum
from typing import Literal, Optional

from pydantic import Field, UUID4, model_validator

from wiil.models.base import BaseModel


class DisplayOrderPositionMode(str, Enum):
    """Display order position mode enumeration."""

    BEGINNING = "BEGINNING"
    END = "END"
    KEEP_CURRENT = "KEEP_CURRENT"
    BEFORE_ITEM = "BEFORE_ITEM"
    AFTER_ITEM = "AFTER_ITEM"
    ABSOLUTE_INDEX = "ABSOLUTE_INDEX"


class DisplayOrderPositionIntent(BaseModel):
    """How to place an entity in an ordered list."""

    mode: DisplayOrderPositionMode = Field(
        ...,
        description="Positioning mode for the item",
    )


class DisplayOrderRequest(BaseModel):
    """Configuration for display order of items in listings."""

    item_id: Optional[str] = Field(
        ...,
        description="Target item identifier. Null when creating a new item",
        alias="itemId",
    )
    target_category_id: str = Field(
        ...,
        min_length=1,
        description="Category where ordering applies",
        alias="targetCategoryId",
    )
    position_intent: DisplayOrderPositionIntent = Field(
        ...,
        description="How to place an entity in an ordered list",
        alias="positionIntent",
    )
    anchor_item_id: Optional[str] = Field(
        ...,
        description="Required for BEFORE_ITEM and AFTER_ITEM",
        alias="anchorItemId",
    )
    absolute_index: Optional[int] = Field(
        ...,
        ge=0,
        description="Required for ABSOLUTE_INDEX (0-based)",
        alias="absoluteIndex",
    )
    idempotency_key: UUID4 = Field(
        ...,
        description="Client-provided idempotency key (UUID v4)",
        alias="idempotencyKey",
    )
    expected_version: int = Field(
        ...,
        ge=0,
        description="Optimistic concurrency version",
        alias="expectedVersion",
    )

    @model_validator(mode="after")
    def validate_position_intent(self) -> "DisplayOrderRequest":
        """Enforce anchor and absolute-index requirements by mode."""
        _validate_position_intent(
            mode=self.position_intent.mode,
            absolute_index=self.absolute_index,
            anchor_value=self.anchor_item_id,
            anchor_field="anchorItemId",
        )
        return self


class DisplayOrderResponse(BaseModel):
    """Result of applying display order intent."""

    item_id: str = Field(
        ...,
        min_length=1,
        description="Resolved item identifier",
        alias="itemId",
    )
    target_category_id: str = Field(
        ...,
        min_length=1,
        description="Category where the item is ordered",
        alias="targetCategoryId",
    )
    resolved_display_order: int = Field(
        ...,
        ge=0,
        description="Persisted display order value",
        alias="resolvedDisplayOrder",
    )
    resolved_position: Optional[int] = Field(
        None,
        gt=0,
        description="Optional 1-based position for UI",
        alias="resolvedPosition",
    )
    category_version: int = Field(
        ...,
        ge=0,
        description="Updated category version after reorder",
        alias="categoryVersion",
    )
    reindexed: bool = Field(
        ...,
        description="Whether sibling items were normalized/reindexed",
    )


class CreateDisplayOrderPlacement(BaseModel):
    """Optional create-time placement block for resolving display order."""

    placement_intent: DisplayOrderPositionIntent = Field(
        ...,
        description="How to place an entity in an ordered list",
        alias="placementIntent",
    )
    anchor_item_id: Optional[str] = Field(
        None,
        description="Anchor item for relative positioning",
        alias="anchorItemId",
    )
    absolute_index: Optional[int] = Field(
        None,
        ge=0,
        description="Absolute index for ABSOLUTE_INDEX mode",
        alias="absoluteIndex",
    )

    @model_validator(mode="after")
    def validate_position_intent(self) -> "CreateDisplayOrderPlacement":
        """Enforce anchor and absolute-index requirements by mode."""
        _validate_position_intent(
            mode=self.placement_intent.mode,
            absolute_index=self.absolute_index,
            anchor_value=self.anchor_item_id,
            anchor_field="anchorItemId",
        )
        return self


class CategoryDisplayOrderRequest(BaseModel):
    """Configuration for reordering categories."""

    category_id: str = Field(
        ...,
        min_length=1,
        description="Category to move",
        alias="categoryId",
    )
    target_parent_category_id: Optional[str] = Field(
        ...,
        description="Target parent category. Null for root-level categories",
        alias="targetParentCategoryId",
    )
    position_intent: DisplayOrderPositionIntent = Field(
        ...,
        description="How to place an entity in an ordered list",
        alias="positionIntent",
    )
    anchor_category_id: Optional[str] = Field(
        ...,
        description="Required for BEFORE_ITEM and AFTER_ITEM",
        alias="anchorCategoryId",
    )
    absolute_index: Optional[int] = Field(
        ...,
        ge=0,
        description="Required for ABSOLUTE_INDEX (0-based)",
        alias="absoluteIndex",
    )
    idempotency_key: UUID4 = Field(
        ...,
        description="Client-provided idempotency key (UUID v4)",
        alias="idempotencyKey",
    )
    expected_version: int = Field(
        ...,
        ge=0,
        description="Optimistic concurrency version",
        alias="expectedVersion",
    )

    @model_validator(mode="after")
    def validate_position_intent(self) -> "CategoryDisplayOrderRequest":
        """Enforce anchor and absolute-index requirements by mode."""
        _validate_position_intent(
            mode=self.position_intent.mode,
            absolute_index=self.absolute_index,
            anchor_value=self.anchor_category_id,
            anchor_field="anchorCategoryId",
        )
        return self


class CategoryDisplayOrderResponse(BaseModel):
    """Result of applying category order intent."""

    category_id: str = Field(
        ...,
        min_length=1,
        description="Resolved category identifier",
        alias="categoryId",
    )
    target_parent_category_id: Optional[str] = Field(
        ...,
        description="Resolved parent category. Null for root-level categories",
        alias="targetParentCategoryId",
    )
    resolved_display_order: int = Field(
        ...,
        ge=0,
        description="Persisted display order value",
        alias="resolvedDisplayOrder",
    )
    resolved_position: Optional[int] = Field(
        None,
        gt=0,
        description="Optional 1-based position for UI",
        alias="resolvedPosition",
    )
    category_version: int = Field(
        ...,
        ge=0,
        description="Updated category version after reorder",
        alias="categoryVersion",
    )
    reindexed: bool = Field(
        ...,
        description="Whether sibling categories were normalized/reindexed",
    )


class CategoryOrderEntry(BaseModel):
    """Category order entry for bulk ordering."""

    category_id: str = Field(
        ...,
        min_length=1,
        description="Category identifier",
        alias="categoryId",
    )
    display_order: int = Field(
        ...,
        ge=0,
        description="Target display order for the category",
        alias="displayOrder",
    )


class CategoryDisplayOrdersRequest(BaseModel):
    """Bulk category display orders request."""

    category_orders: list[CategoryOrderEntry] = Field(
        ...,
        min_length=1,
        description="Ordered category display values",
        alias="categoryOrders",
    )


class CategoryItemOrderEntry(BaseModel):
    """Category item order entry for bulk ordering."""

    item_id: str = Field(
        ...,
        min_length=1,
        description="Item identifier",
        alias="itemId",
    )
    display_order: int = Field(
        ...,
        ge=0,
        description="Target display order for the item",
        alias="displayOrder",
    )


class CategoryItemDisplayOrdersRequest(BaseModel):
    """Bulk category item display orders request."""

    category_id: str = Field(
        ...,
        min_length=1,
        description="Category identifier",
        alias="categoryId",
    )
    item_orders: list[CategoryItemOrderEntry] = Field(
        ...,
        min_length=1,
        description="Ordered item display values for the category",
        alias="itemOrders",
    )


def _validate_position_intent(
    *,
    mode: DisplayOrderPositionMode,
    absolute_index: Optional[int],
    anchor_value: Optional[str],
    anchor_field: Literal["anchorItemId", "anchorCategoryId"],
) -> None:
    """Apply Zod-equivalent position-intent validation rules."""
    requires_anchor = mode in {
        DisplayOrderPositionMode.BEFORE_ITEM,
        DisplayOrderPositionMode.AFTER_ITEM,
    }
    requires_absolute_index = mode == DisplayOrderPositionMode.ABSOLUTE_INDEX

    if requires_anchor and not anchor_value:
        raise ValueError(
            f"{anchor_field} is required for BEFORE_ITEM and AFTER_ITEM"
        )

    if requires_absolute_index and absolute_index is None:
        raise ValueError("absoluteIndex is required for ABSOLUTE_INDEX")

    if not requires_anchor and anchor_value is not None:
        raise ValueError(
            (
                f"{anchor_field} must be null unless mode is "
                "BEFORE_ITEM or AFTER_ITEM"
            )
        )

    if not requires_absolute_index and absolute_index is not None:
        raise ValueError(
            "absoluteIndex must be null unless mode is ABSOLUTE_INDEX"
        )


DisplayOrderPositionModeType = DisplayOrderPositionMode
DisplayOrderPositionIntentType = DisplayOrderPositionIntent
CreateDisplayOrderPlacementType = CreateDisplayOrderPlacement
DisplayOrderRequestType = DisplayOrderRequest
DisplayOrderResponseType = DisplayOrderResponse
CategoryDisplayOrderRequestType = CategoryDisplayOrderRequest
CategoryDisplayOrderResponseType = CategoryDisplayOrderResponse
CategoryOrderEntryType = CategoryOrderEntry
CategoryDisplayOrdersRequestType = CategoryDisplayOrdersRequest
CategoryItemOrderEntryType = CategoryItemOrderEntry
CategoryItemDisplayOrdersRequestType = CategoryItemDisplayOrdersRequest
