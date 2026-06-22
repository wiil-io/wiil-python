"""Menu item variant schema definitions for business management."""

from typing import List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class MenuItemVariantChannelMapping(BaseModel):
    """Per-channel external menu variant ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_variant_id: str = Field(..., alias="externalVariantId")
    external_menu_item_id: Optional[str] = Field(
        None,
        alias="externalMenuItemId",
    )


class MenuItemVariant(EntityModel):
    """Menu item variant - size/option for a menu item."""

    menu_item_id: str = Field(..., alias="menuItemId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    is_available: bool = Field(True, alias="isAvailable")
    is_active: bool = Field(True, alias="isActive")
    is_default: bool = Field(False, alias="isDefault")
    variant_channel_mappings: Optional[
        List[MenuItemVariantChannelMapping]
    ] = Field(
        None,
        alias="variantChannelMappings",
    )
    order_count: Optional[int] = Field(None, ge=0, alias="orderCount")
    recent_order_count: Optional[int] = Field(
        None,
        ge=0,
        alias="recentOrderCount",
    )
    last_ordered_at: Optional[int] = Field(None, gt=0, alias="lastOrderedAt")


class CreateMenuItemVariant(BaseModel):
    """Schema for creating a new menu item variant."""

    menu_item_id: str = Field(..., alias="menuItemId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    is_available: bool = Field(True, alias="isAvailable")
    is_active: bool = Field(True, alias="isActive")
    is_default: bool = Field(False, alias="isDefault")
    variant_channel_mappings: Optional[
        List[MenuItemVariantChannelMapping]
    ] = Field(
        None,
        alias="variantChannelMappings",
    )


class CreateBusinessMenuItemVariant(BaseModel):
    """Schema for a variant supplied when creating a business menu item.

    Mirrors CreateMenuItemVariant with menuItemId omitted, since the parent
    menu item is created in the same request.
    """

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    is_available: bool = Field(True, alias="isAvailable")
    is_active: bool = Field(True, alias="isActive")
    is_default: bool = Field(False, alias="isDefault")
    variant_channel_mappings: Optional[
        List[MenuItemVariantChannelMapping]
    ] = Field(
        None,
        alias="variantChannelMappings",
    )


class UpdateMenuItemVariant(BaseModel):
    """Schema for updating an existing menu item variant."""

    id: str
    menu_item_id: Optional[str] = Field(None, alias="menuItemId")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    is_active: Optional[bool] = Field(None, alias="isActive")
    is_default: Optional[bool] = Field(None, alias="isDefault")
    variant_channel_mappings: Optional[
        List[MenuItemVariantChannelMapping]
    ] = Field(
        None,
        alias="variantChannelMappings",
    )


class PriceRange(TypedDict, total=False):
    """Optional min/max price range filter."""

    min: Optional[float]
    max: Optional[float]


class MenuItemVariantFilters(TypedDict, total=False):
    """Filters for querying menu item variants."""

    search: Optional[str]
    menu_item_id: Optional[str]
    is_active: Optional[bool]
    is_available: Optional[bool]
    price_range: Optional[PriceRange]


class MenuItemVariantSorting(TypedDict):
    """Sorting options for menu item variant queries."""

    field: Literal["name", "price", "created_at"]
    direction: Literal["asc", "desc"]


class MenuItemVariantQueryOptions(TypedDict, total=False):
    """Query options for menu item variant retrieval."""

    page: int
    page_size: int
    filters: Optional[MenuItemVariantFilters]
    sorting: Optional[MenuItemVariantSorting]
