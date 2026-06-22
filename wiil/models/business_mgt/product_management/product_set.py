"""Product set schema definitions for bundled products."""

from enum import Enum
from typing import List, Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.product_management.product_config import (
    BusinessProduct,
)


class ProductSetPricingMode(str, Enum):
    """Product set pricing mode."""

    FIXED = "FIXED"
    SUM_OF_ITEMS = "SUM_OF_ITEMS"


class ProductSetTargetingMode(str, Enum):
    """Product set targeting mode."""

    EXPLICIT = "EXPLICIT"
    SELECTOR = "SELECTOR"


class ProductSetChannelMapping(BaseModel):
    """Per-channel external product set ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_product_set_id: str = Field(..., alias="externalProductSetId")


class ProductSetItem(BaseModel):
    """Product included in a product set."""

    product_id: str = Field(..., alias="productId")
    product_variant_id: Optional[str] = Field(None, alias="productVariantId")
    quantity: int = Field(..., gt=0)
    is_required: bool = Field(True, alias="isRequired")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class ProductSetSelector(BaseModel):
    """Selector criteria for dynamic product-set membership."""

    product_ids_any: List[str] = Field(
        default_factory=list,
        max_length=5000,
        alias="productIdsAny",
    )
    product_ids_all: List[str] = Field(
        default_factory=list,
        max_length=5000,
        alias="productIdsAll",
    )
    all_products: bool = Field(False, alias="allProducts")
    quantity_exact: Optional[int] = Field(None, gt=0, alias="quantityExact")
    quantity_min: Optional[int] = Field(None, ge=0, alias="quantityMin")
    quantity_max: Optional[int] = Field(None, gt=0, alias="quantityMax")

    @model_validator(mode="after")
    def validate_selector(self) -> "ProductSetSelector":
        """Validate selector mode and quantity constraints."""
        selector_modes = sum(
            [
                len(self.product_ids_any) > 0,
                len(self.product_ids_all) > 0,
                self.all_products,
            ]
        )
        if selector_modes != 1:
            raise ValueError(
                "Exactly one of productIdsAny, productIdsAll, or allProducts "
                "must be set"
            )
        if self.quantity_exact is not None:
            if self.quantity_min is not None or self.quantity_max is not None:
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


class ProductSet(EntityModel):
    """Product set schema."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[ProductSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: ProductSetTargetingMode = Field(
        ProductSetTargetingMode.EXPLICIT,
        alias="targetingMode",
    )
    pricing_mode: ProductSetPricingMode = Field(
        ProductSetPricingMode.SUM_OF_ITEMS,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[ProductSetItem]] = None
    selector: Optional[ProductSetSelector] = None
    is_active: bool = Field(True, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")

    @model_validator(mode="after")
    def validate_product_set(self) -> "ProductSet":
        """Validate pricing mode, targeting mode, and duplicate items."""
        if self.pricing_mode == ProductSetPricingMode.FIXED:
            if self.fixed_price is None:
                raise ValueError(
                    "fixedPrice is required when pricingMode is FIXED"
                )
        if self.pricing_mode == ProductSetPricingMode.SUM_OF_ITEMS:
            if self.fixed_price is not None:
                raise ValueError(
                    "fixedPrice must be null or omitted when pricingMode is "
                    "SUM_OF_ITEMS"
                )

        if self.targeting_mode == ProductSetTargetingMode.EXPLICIT:
            if not self.items:
                raise ValueError(
                    "items is required when targetingMode is EXPLICIT"
                )
            if self.selector is not None:
                raise ValueError(
                    "selector must be null or omitted when targetingMode is "
                    "EXPLICIT"
                )

        if self.targeting_mode == ProductSetTargetingMode.SELECTOR:
            if self.selector is None:
                raise ValueError(
                    "selector is required when targetingMode is SELECTOR"
                )
            if self.items:
                raise ValueError(
                    "items must be empty when targetingMode is SELECTOR"
                )

        if self.items:
            seen_item_keys: set[str] = set()
            for item in self.items:
                item_key = (
                    f"{item.product_id}::{item.product_variant_id or '*'}"
                )
                if item_key in seen_item_keys:
                    raise ValueError(
                        "Duplicate productId + productVariantId combination "
                        "is not allowed in a product set"
                    )
                seen_item_keys.add(item_key)
        return self


class CreateProductSet(BaseModel):
    """Schema for creating a product set."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[ProductSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: ProductSetTargetingMode = Field(
        ProductSetTargetingMode.EXPLICIT,
        alias="targetingMode",
    )
    pricing_mode: ProductSetPricingMode = Field(
        ProductSetPricingMode.SUM_OF_ITEMS,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[ProductSetItem]] = None
    selector: Optional[ProductSetSelector] = None
    is_active: bool = Field(True, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdateProductSet(BaseModel):
    """Schema for updating a product set."""

    id: str
    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    code: Optional[str] = Field(None, min_length=1)
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[ProductSetChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    targeting_mode: Optional[ProductSetTargetingMode] = Field(
        None,
        alias="targetingMode",
    )
    pricing_mode: Optional[ProductSetPricingMode] = Field(
        None,
        alias="pricingMode",
    )
    fixed_price: Optional[float] = Field(None, ge=0, alias="fixedPrice")
    items: Optional[List[ProductSetItem]] = None
    selector: Optional[ProductSetSelector] = None
    is_active: Optional[bool] = Field(None, alias="isActive")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class ProductSetItemDisplay(ProductSetItem):
    """Product set item read model with resolved product snapshot."""

    product: Optional[BusinessProduct] = None


class ProductSetDisplay(ProductSet):
    """Product set read model with resolved items and pricing."""

    items: Optional[List[ProductSetItemDisplay]] = None
    resolved_price: Optional[float] = Field(None, ge=0, alias="resolvedPrice")


class ProductSetFilters(TypedDict, total=False):
    """Filters for querying product sets."""

    search: Optional[str]
    product_revision_id: Optional[str]
    location_id: Optional[str]
    code: Optional[str]
    targeting_mode: Optional[ProductSetTargetingMode]
    is_active: Optional[bool]
    pricing_mode: Optional[ProductSetPricingMode]


class ProductSetSorting(TypedDict):
    """Sorting options for product set queries."""

    field: Literal["name", "created_at", "display_order"]
    direction: Literal["asc", "desc"]


class ProductSetQueryOptions(TypedDict, total=False):
    """Query options for product set retrieval."""

    page: int
    page_size: int
    filters: Optional[ProductSetFilters]
    sorting: Optional[ProductSetSorting]
