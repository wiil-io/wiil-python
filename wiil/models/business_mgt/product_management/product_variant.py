"""Product variant schema definitions for SKU-level variants."""

from typing import Dict, List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.product_management.product_config import (
    CreateBusinessProduct,
    ProductDimensions,
)
from wiil.types.business_types import InventoryUnit


class ProductVariantChannelMapping(BaseModel):
    """Per-channel external variant ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_variant_id: str = Field(..., alias="externalVariantId")
    external_product_id: Optional[str] = Field(None, alias="externalProductId")


class ProductVariant(EntityModel):
    """Product variant schema."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    product_id: str = Field(..., alias="productId")
    axis_values: Dict[str, str] = Field(..., alias="axisValues")
    sku: Optional[str] = None
    barcode: Optional[str] = None
    part_number: Optional[str] = Field(None, alias="partNumber")
    global_trade_item_number: Optional[str] = Field(
        None,
        alias="globalTradeItemNumber",
    )
    price: Optional[float] = Field(None, ge=0)
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    unit_definition_id: Optional[str] = Field(None, alias="unitDefinitionId")
    inventory_unit: Optional[InventoryUnit] = Field(
        None,
        alias="inventoryUnit",
    )
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    image_id: Optional[str] = Field(None, alias="imageId")
    image_ids: Optional[List[str]] = Field(None, alias="imageIds")
    channel_mappings: Optional[List[ProductVariantChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")
    is_default: bool = Field(False, alias="isDefault")
    order_count: Optional[int] = Field(None, ge=0, alias="orderCount")
    recent_order_count: Optional[int] = Field(
        None,
        ge=0,
        alias="recentOrderCount",
    )
    last_ordered_at: Optional[int] = Field(None, gt=0, alias="lastOrderedAt")


class CreateProductVariant(BaseModel):
    """Schema for creating a product variant."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    product_id: str = Field(..., alias="productId")
    axis_values: Dict[str, str] = Field(..., alias="axisValues")
    sku: Optional[str] = None
    barcode: Optional[str] = None
    part_number: Optional[str] = Field(None, alias="partNumber")
    global_trade_item_number: Optional[str] = Field(
        None,
        alias="globalTradeItemNumber",
    )
    price: Optional[float] = Field(None, ge=0)
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    unit_definition_id: Optional[str] = Field(None, alias="unitDefinitionId")
    inventory_unit: Optional[InventoryUnit] = Field(
        None,
        alias="inventoryUnit",
    )
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    image_id: Optional[str] = Field(None, alias="imageId")
    image_ids: Optional[List[str]] = Field(None, alias="imageIds")
    channel_mappings: Optional[List[ProductVariantChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")
    is_default: bool = Field(False, alias="isDefault")


class CreateBusinessProductVariant(BaseModel):
    """Schema for a variant supplied when creating a business product.

    Mirrors CreateProductVariant with productId omitted, since the parent
    product is created in the same request.
    """

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    axis_values: Dict[str, str] = Field(..., alias="axisValues")
    sku: Optional[str] = None
    barcode: Optional[str] = None
    part_number: Optional[str] = Field(None, alias="partNumber")
    global_trade_item_number: Optional[str] = Field(
        None,
        alias="globalTradeItemNumber",
    )
    price: Optional[float] = Field(None, ge=0)
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    unit_definition_id: Optional[str] = Field(None, alias="unitDefinitionId")
    inventory_unit: Optional[InventoryUnit] = Field(
        None,
        alias="inventoryUnit",
    )
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    image_id: Optional[str] = Field(None, alias="imageId")
    image_ids: Optional[List[str]] = Field(None, alias="imageIds")
    channel_mappings: Optional[List[ProductVariantChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")
    is_default: bool = Field(False, alias="isDefault")


class UpdateProductVariant(BaseModel):
    """Schema for updating a product variant."""

    id: str
    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    product_id: Optional[str] = Field(None, alias="productId")
    axis_values: Optional[Dict[str, str]] = Field(None, alias="axisValues")
    sku: Optional[str] = None
    barcode: Optional[str] = None
    part_number: Optional[str] = Field(None, alias="partNumber")
    global_trade_item_number: Optional[str] = Field(
        None,
        alias="globalTradeItemNumber",
    )
    price: Optional[float] = Field(None, ge=0)
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    unit_definition_id: Optional[str] = Field(None, alias="unitDefinitionId")
    inventory_unit: Optional[InventoryUnit] = Field(
        None,
        alias="inventoryUnit",
    )
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    image_id: Optional[str] = Field(None, alias="imageId")
    image_ids: Optional[List[str]] = Field(None, alias="imageIds")
    channel_mappings: Optional[List[ProductVariantChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: Optional[bool] = Field(None, alias="isActive")
    is_default: Optional[bool] = Field(None, alias="isDefault")


class ProductVariantFilters(TypedDict, total=False):
    """Filters for querying product variants."""

    product_id: Optional[str]
    axis_value_id: Optional[str]
    sku: Optional[str]
    is_active: Optional[bool]
    in_stock: Optional[bool]


class ProductVariantSorting(TypedDict):
    """Sorting options for product variant queries."""

    field: Literal["sku", "price", "stock_quantity", "created_at"]
    direction: Literal["asc", "desc"]


class ProductVariantQueryOptions(TypedDict, total=False):
    """Query options for product variant retrieval."""

    page: int
    page_size: int
    filters: Optional[ProductVariantFilters]
    sorting: Optional[ProductVariantSorting]


# Resolve the forward reference declared on CreateBusinessProduct.variants
# (defined in product_config.py) now that CreateBusinessProductVariant exists.
# This is done here, not in product_config.py, to avoid a
# product_config <-> product_variant import cycle.
CreateBusinessProduct.model_rebuild()
