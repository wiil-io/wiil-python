"""Menu set schema definitions for bundled menu items."""

from enum import Enum
from typing import List, Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.menu_management.menu_config import (
    BusinessMenuItem,
)


class MenuSetPricingMode(str, Enum):
    """How menu set pricing is resolved."""

    FIXED = "FIXED"
    SUM_OF_ITEMS = "SUM_OF_ITEMS"


class MenuSetTargetingMode(str, Enum):
    """How menu set members are selected."""

    EXPLICIT = "EXPLICIT"
    SELECTOR = "SELECTOR"


class MenuSetChannelMapping(BaseModel):
    """Per-channel external menu set ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_menu_set_id: str = Field(..., alias="externalMenuSetId")


class MenuSetItem(BaseModel):
    """Menu item entry within a menu set."""

    menu_item_id: str = Field(..., alias="menuItemId")
    menu_item_variant_id: str = Field(..., alias="menuItemVariantId")
    quantity: int = Field(..., gt=0)
    is_required: bool = Field(True, alias="isRequired")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class MenuSetSelector(BaseModel):
    """Selector definition for SELECTOR targeting mode."""

    menu_item_ids_any: List[str] = Field(
        default_factory=list,
        max_length=5000,
        alias="menuItemIdsAny",
    )
    menu_item_ids_all: List[str] = Field(
        default_factory=list,
        max_length=5000,
        alias="menuItemIdsAll",
    )
    all_menu_items: bool = Field(False, alias="allMenuItems")
    quantity_exact: Optional[int] = Field(None, gt=0, alias="quantityExact")
    quantity_min: Optional[int] = Field(None, ge=0, alias="quantityMin")
    quantity_max: Optional[int] = Field(None, gt=0, alias="quantityMax")

    @model_validator(mode="after")
    def validate_selector(self) -> "MenuSetSelector":
        """Validate selector mode and quantity constraints."""
        selector_modes = sum(
            [
                bool(self.menu_item_ids_any),
                bool(self.menu_item_ids_all),
                self.all_menu_items,
            ]
        )

        if selector_modes != 1:
            raise ValueError(
                "Exactly one of menuItemIdsAny, menuItemIdsAll, or "
                "allMenuItems must be set"
            )

        if self.quantity_exact is not None and (
            self.quantity_min is not None or self.quantity_max is not None
        ):
            raise ValueError(
                "quantityExact cannot be combined with quantityMin or "
                "quantityMax"
            )

        if (
            self.quantity_min is not None
            and self.quantity_max is not None
            and self.quantity_max < self.quantity_min
        ):
            raise ValueError(
                "quantityMax must be greater than or equal to quantityMin"
            )

        return self


class MenuSet(EntityModel):
    """Menu set schema for bundled menu configurations."""

    location_id: Optional[str] = Field(None, alias="locationId")
    menu_revision_id: Optional[str] = Field(None, alias="menuRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[MenuSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: MenuSetTargetingMode = Field(
        MenuSetTargetingMode.EXPLICIT,
        alias="targetingMode",
    )
    pricing_mode: MenuSetPricingMode = Field(
        MenuSetPricingMode.SUM_OF_ITEMS,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[MenuSetItem]] = None
    selector: Optional[MenuSetSelector] = None
    is_active: bool = Field(True, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")

    @model_validator(mode="after")
    def validate_menu_set(self) -> "MenuSet":
        """Validate pricing mode, targeting mode, and duplicate items."""
        if (
            self.pricing_mode == MenuSetPricingMode.FIXED
            and self.fixed_price is None
        ):
            raise ValueError(
                "fixedPrice is required when pricingMode is FIXED"
            )

        if (
            self.pricing_mode == MenuSetPricingMode.SUM_OF_ITEMS
            and self.fixed_price is not None
        ):
            raise ValueError(
                "fixedPrice must be null or omitted when pricingMode is "
                "SUM_OF_ITEMS"
            )

        if self.targeting_mode == MenuSetTargetingMode.EXPLICIT:
            if not self.items:
                raise ValueError(
                    "items is required when targetingMode is EXPLICIT"
                )
            if self.selector is not None:
                raise ValueError(
                    "selector must be null or omitted when targetingMode is "
                    "EXPLICIT"
                )

        if self.targeting_mode == MenuSetTargetingMode.SELECTOR:
            if self.selector is None:
                raise ValueError(
                    "selector is required when targetingMode is SELECTOR"
                )
            if self.items:
                raise ValueError(
                    "items must be empty when targetingMode is SELECTOR"
                )

        if not self.items:
            return self

        seen_item_keys: set[str] = set()
        for item in self.items:
            item_key = f"{item.menu_item_id}::{item.menu_item_variant_id}"
            if item_key in seen_item_keys:
                raise ValueError(
                    "Duplicate menuItemId + menuItemVariantId combination is "
                    "not allowed in a menu set"
                )
            seen_item_keys.add(item_key)

        return self


class CreateMenuSet(BaseModel):
    """Schema for creating a new menu set."""

    location_id: Optional[str] = Field(None, alias="locationId")
    menu_revision_id: Optional[str] = Field(None, alias="menuRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[MenuSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: MenuSetTargetingMode = Field(
        MenuSetTargetingMode.EXPLICIT,
        alias="targetingMode",
    )
    pricing_mode: MenuSetPricingMode = Field(
        MenuSetPricingMode.SUM_OF_ITEMS,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[MenuSetItem]] = None
    selector: Optional[MenuSetSelector] = None
    is_active: bool = Field(True, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdateMenuSet(BaseModel):
    """Schema for updating an existing menu set."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    menu_revision_id: Optional[str] = Field(None, alias="menuRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[MenuSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: Optional[MenuSetTargetingMode] = Field(
        None,
        alias="targetingMode",
    )
    pricing_mode: Optional[MenuSetPricingMode] = Field(
        None,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[MenuSetItem]] = None
    selector: Optional[MenuSetSelector] = None
    is_active: Optional[bool] = Field(None, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class MenuSetItemView(MenuSetItem):
    """Read-optimized set item with resolved menu item snapshot."""

    menu_item: Optional[BusinessMenuItem] = Field(None, alias="menuItem")


class MenuSetView(EntityModel):
    """Read-optimized menu set view model."""

    location_id: Optional[str] = Field(None, alias="locationId")
    menu_revision_id: Optional[str] = Field(None, alias="menuRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[MenuSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: MenuSetTargetingMode = Field(
        MenuSetTargetingMode.EXPLICIT,
        alias="targetingMode",
    )
    pricing_mode: MenuSetPricingMode = Field(
        MenuSetPricingMode.SUM_OF_ITEMS,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[MenuSetItemView]] = None
    selector: Optional[MenuSetSelector] = None
    is_active: bool = Field(True, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    resolved_price: Optional[float] = Field(None, ge=0, alias="resolvedPrice")


class MenuSetFilters(TypedDict, total=False):
    """Filters for querying menu sets."""

    search: Optional[str]
    location_id: Optional[str]
    menu_revision_id: Optional[str]
    code: Optional[str]
    targeting_mode: Optional[MenuSetTargetingMode]
    is_active: Optional[bool]
    pricing_mode: Optional[MenuSetPricingMode]


class MenuSetSorting(TypedDict):
    """Sorting options for menu set queries."""

    field: Literal["name", "created_at", "display_order"]
    direction: Literal["asc", "desc"]


class MenuSetQueryOptions(TypedDict, total=False):
    """Query options for menu set retrieval."""

    page: int
    page_size: int
    filters: Optional[MenuSetFilters]
    sorting: Optional[MenuSetSorting]
