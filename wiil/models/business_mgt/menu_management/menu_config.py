"""Business menu configuration schema definitions.

Strict Pydantic models mirroring
type-ref/menu-management/menu-config.schema.ts.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.menu_management.menu_item_variant import (
    CreateBusinessMenuItemVariant,
)


class MenuCategoryChannelMapping(BaseModel):
    """Per-channel external category ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_category_id: str = Field(..., alias="externalCategoryId")


class MenuItemChannelMapping(BaseModel):
    """Per-channel external menu item ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_menu_item_id: str = Field(..., alias="externalMenuItemId")
    external_category_id: Optional[str] = Field(
        None,
        alias="externalCategoryId",
    )


class NutritionalInfo(BaseModel):
    """Optional nutritional information for menu items."""

    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None


class MenuCategory(EntityModel):
    """Menu category for organizing menu items."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[List[MenuCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )


class BusinessMenuItem(EntityModel):
    """Business menu item model."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category_id: str = Field(..., alias="categoryId")
    category: Optional[MenuCategory] = None
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    nutritional_info: Optional[NutritionalInfo] = Field(
        None,
        alias="nutritionalInfo",
    )
    is_available: bool = Field(True, alias="isAvailable")
    preparation_time: Optional[int] = Field(
        None,
        gt=0,
        alias="preparationTime",
    )
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[List[MenuItemChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    day_parts: Optional[List[Dict[str, Any]]] = Field(None, alias="dayParts")
    order_count: Optional[int] = Field(None, ge=0, alias="orderCount")
    recent_order_count: Optional[int] = Field(
        None,
        ge=0,
        alias="recentOrderCount",
    )
    last_ordered_at: Optional[int] = Field(None, gt=0, alias="lastOrderedAt")


class CreateMenuCategory(BaseModel):
    """Schema for creating a new menu category."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[List[MenuCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )


class CreateBusinessMenuItem(BaseModel):
    """Schema for creating a new business menu item."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    variants: List[CreateBusinessMenuItemVariant] = Field(..., min_length=1)
    category_id: Optional[str] = Field(None, alias="categoryId")
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    nutritional_info: Optional[NutritionalInfo] = Field(
        None,
        alias="nutritionalInfo",
    )
    is_available: bool = Field(True, alias="isAvailable")
    preparation_time: Optional[int] = Field(
        None,
        gt=0,
        alias="preparationTime",
    )
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[List[MenuItemChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    day_parts: Optional[List[Dict[str, Any]]] = Field(None, alias="dayParts")


class UpdateMenuCategory(BaseModel):
    """Schema for updating an existing menu category."""

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[List[MenuCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )


class UpdateBusinessMenuItem(BaseModel):
    """Schema for updating an existing business menu item."""

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    category_id: Optional[str] = Field(None, alias="categoryId")
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    nutritional_info: Optional[NutritionalInfo] = Field(
        None,
        alias="nutritionalInfo",
    )
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    preparation_time: Optional[int] = Field(
        None,
        gt=0,
        alias="preparationTime",
    )
    is_active: Optional[bool] = Field(None, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[List[MenuItemChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    day_parts: Optional[List[Dict[str, Any]]] = Field(None, alias="dayParts")


class BusinessMenuItemFilters(TypedDict, total=False):
    """Filters for querying business menu items."""

    search: Optional[str]
    location_id: Optional[str]
    category_id: Optional[str]
    is_active: Optional[bool]
    is_available: Optional[bool]
    allergens: Optional[List[str]]


class BusinessMenuItemSorting(TypedDict):
    """Sorting options for business menu item queries."""

    field: Literal["name", "price", "created_at", "display_order"]
    direction: Literal["asc", "desc"]


class BusinessMenuItemQueryOptions(TypedDict, total=False):
    """Query options for business menu item retrieval."""

    page: int
    page_size: int
    filters: Optional[BusinessMenuItemFilters]
    sorting: Optional[BusinessMenuItemSorting]
