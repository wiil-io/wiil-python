"""Product configuration schema definitions for business management."""

from enum import Enum
from typing import TYPE_CHECKING, List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)

if TYPE_CHECKING:
    # Imported only for typing; resolved at runtime via model_rebuild() in
    # product_variant.py to avoid a product_config <-> product_variant cycle.
    from wiil.models.business_mgt.product_management.product_variant import (
        CreateBusinessProductVariant,
    )


class AttributeDefType(str, Enum):
    """Attribute definition type."""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ENUM = "enum"
    DATE = "date"
    URL = "url"


class CategoryLocationScope(str, Enum):
    """Category location scope."""

    INHERITED = "inherited"
    LOCAL = "local"


class BarcodeFormat(str, Enum):
    """Supported barcode formats."""

    UPC_A = "UPC_A"
    UPC_E = "UPC_E"
    EAN_13 = "EAN_13"
    EAN_8 = "EAN_8"
    CODE_128 = "CODE_128"
    CODE_39 = "CODE_39"
    ITF_14 = "ITF_14"
    QR = "QR"


class AttributeDef(EntityModel):
    """Organization-level product attribute definition."""

    name: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    type: AttributeDefType
    unit: Optional[str] = None
    enum_values: Optional[List[str]] = Field(None, alias="enumValues")
    is_active: bool = Field(True, alias="isActive")


class CategoryAttributeBinding(BaseModel):
    """Category-to-attribute binding with category-specific settings."""

    attribute_def_id: str = Field(..., alias="attributeDefId")
    required: bool = False
    display_order: int = Field(0, alias="displayOrder")


class ProductAttributeValue(BaseModel):
    """Product attribute value referencing an attribute definition."""

    attribute_def_id: str = Field(..., alias="attributeDefId")
    value: str | float | bool


class ProductCategoryChannelMapping(BaseModel):
    """Per-channel external category ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_category_id: str = Field(..., alias="externalCategoryId")


class ProductChannelMapping(BaseModel):
    """Per-channel external product ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_product_id: str = Field(..., alias="externalProductId")
    external_category_id: Optional[str] = Field(
        None,
        alias="externalCategoryId",
    )


class ProductDimensions(BaseModel):
    """Product dimensions."""

    length: float = Field(..., gt=0)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    unit: Literal["inches", "cm"] = "inches"


class ProductCategory(EntityModel):
    """Product category schema."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    parent_id: Optional[str] = Field(None, alias="parentId")
    name: str = Field(..., min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[ProductCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    icon_id: Optional[str] = Field(None, alias="iconId")
    hero_image_id: Optional[str] = Field(None, alias="heroImageId")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_default: bool = Field(False, alias="isDefault")
    attribute_bindings: Optional[List[CategoryAttributeBinding]] = Field(
        None,
        alias="attributeBindings",
    )
    default_axis_ids: Optional[List[str]] = Field(None, alias="defaultAxisIds")
    default_channel_ids: Optional[List[str]] = Field(
        None,
        alias="defaultChannelIds",
    )
    tax_class_id: Optional[str] = Field(None, alias="taxClassId")
    target_margin: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        alias="targetMargin",
    )
    age_restricted: Optional[bool] = Field(None, alias="ageRestricted")
    require_image: Optional[bool] = Field(None, alias="requireImage")
    location_scope: Optional[CategoryLocationScope] = Field(
        None,
        alias="locationScope",
    )


class BusinessProduct(EntityModel):
    """Business product schema."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    channel_mappings: Optional[List[ProductChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    tags: Optional[List[str]] = None
    price: float = Field(..., ge=0)
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    sku: Optional[str] = None
    sku_pattern: Optional[str] = Field(None, alias="skuPattern")
    barcode: Optional[str] = None
    barcode_format: Optional[BarcodeFormat] = Field(
        None,
        alias="barcodeFormat",
    )
    is_alcoholic: Optional[bool] = Field(False, alias="isAlcoholic")
    category_id: str = Field(..., alias="categoryId")
    category: Optional[ProductCategory] = None
    brand: Optional[str] = None
    brand_id: Optional[str] = Field(None, alias="brandId")
    track_inventory: bool = Field(False, alias="trackInventory")
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    stocked_at: Optional[int] = Field(None, alias="stockedAt")
    reorder_point: Optional[int] = Field(None, ge=0, alias="reorderPoint")
    lead_time: Optional[int] = Field(None, ge=0, alias="leadTime")
    supplier_id: Optional[str] = Field(None, alias="supplierId")
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    shipping_class_id: Optional[str] = Field(None, alias="shippingClassId")
    hs_code: Optional[str] = Field(None, alias="HSCode")
    attributes: Optional[List[ProductAttributeValue]] = None
    tax_rule_ids: Optional[List[str]] = Field(None, alias="taxRuleIds")
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    order_count: Optional[int] = Field(None, ge=0, alias="orderCount")
    recent_order_count: Optional[int] = Field(
        None,
        ge=0,
        alias="recentOrderCount",
    )
    last_ordered_at: Optional[int] = Field(None, gt=0, alias="lastOrderedAt")


class CreateAttributeDef(BaseModel):
    """Schema for creating an attribute definition."""

    name: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    type: AttributeDefType
    unit: Optional[str] = None
    enum_values: Optional[List[str]] = Field(None, alias="enumValues")
    is_active: bool = Field(True, alias="isActive")


class UpdateAttributeDef(BaseModel):
    """Schema for updating an attribute definition."""

    id: str
    name: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    type: Optional[AttributeDefType] = None
    unit: Optional[str] = None
    enum_values: Optional[List[str]] = Field(None, alias="enumValues")
    is_active: Optional[bool] = Field(None, alias="isActive")


class CreateProductCategory(BaseModel):
    """Schema for creating a product category."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    parent_id: Optional[str] = Field(None, alias="parentId")
    name: str = Field(..., min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[ProductCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    icon_id: Optional[str] = Field(None, alias="iconId")
    hero_image_id: Optional[str] = Field(None, alias="heroImageId")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_default: bool = Field(False, alias="isDefault")
    attribute_bindings: Optional[List[CategoryAttributeBinding]] = Field(
        None,
        alias="attributeBindings",
    )
    default_axis_ids: Optional[List[str]] = Field(None, alias="defaultAxisIds")
    default_channel_ids: Optional[List[str]] = Field(
        None,
        alias="defaultChannelIds",
    )
    tax_class_id: Optional[str] = Field(None, alias="taxClassId")
    target_margin: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        alias="targetMargin",
    )
    age_restricted: Optional[bool] = Field(None, alias="ageRestricted")
    require_image: Optional[bool] = Field(None, alias="requireImage")
    location_scope: Optional[CategoryLocationScope] = Field(
        None,
        alias="locationScope",
    )
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateProductCategory(BaseModel):
    """Schema for updating a product category."""

    id: str
    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    parent_id: Optional[str] = Field(None, alias="parentId")
    name: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[List[ProductCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    icon_id: Optional[str] = Field(None, alias="iconId")
    hero_image_id: Optional[str] = Field(None, alias="heroImageId")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_default: Optional[bool] = Field(None, alias="isDefault")
    attribute_bindings: Optional[List[CategoryAttributeBinding]] = Field(
        None,
        alias="attributeBindings",
    )
    default_axis_ids: Optional[List[str]] = Field(None, alias="defaultAxisIds")
    default_channel_ids: Optional[List[str]] = Field(
        None,
        alias="defaultChannelIds",
    )
    tax_class_id: Optional[str] = Field(None, alias="taxClassId")
    target_margin: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        alias="targetMargin",
    )
    age_restricted: Optional[bool] = Field(None, alias="ageRestricted")
    require_image: Optional[bool] = Field(None, alias="requireImage")
    location_scope: Optional[CategoryLocationScope] = Field(
        None,
        alias="locationScope",
    )
    placement: Optional[CreateDisplayOrderPlacement] = None


class CreateBusinessProduct(BaseModel):
    """Schema for creating a business product."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    channel_mappings: Optional[List[ProductChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    tags: Optional[List[str]] = None
    price: float = Field(..., ge=0)
    variants: List["CreateBusinessProductVariant"] = Field(
        ...,
        min_length=1,
    )
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    sku: Optional[str] = None
    sku_pattern: Optional[str] = Field(None, alias="skuPattern")
    barcode: Optional[str] = None
    barcode_format: Optional[BarcodeFormat] = Field(
        None,
        alias="barcodeFormat",
    )
    is_alcoholic: Optional[bool] = Field(False, alias="isAlcoholic")
    category_id: Optional[str] = Field(None, alias="categoryId")
    brand: Optional[str] = None
    brand_id: Optional[str] = Field(None, alias="brandId")
    track_inventory: bool = Field(False, alias="trackInventory")
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    stocked_at: Optional[int] = Field(None, alias="stockedAt")
    reorder_point: Optional[int] = Field(None, ge=0, alias="reorderPoint")
    lead_time: Optional[int] = Field(None, ge=0, alias="leadTime")
    supplier_id: Optional[str] = Field(None, alias="supplierId")
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    shipping_class_id: Optional[str] = Field(None, alias="shippingClassId")
    hs_code: Optional[str] = Field(None, alias="HSCode")
    attributes: Optional[List[ProductAttributeValue]] = None
    tax_rule_ids: Optional[List[str]] = Field(None, alias="taxRuleIds")
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateBusinessProduct(BaseModel):
    """Schema for updating a business product."""

    id: str
    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    channel_mappings: Optional[List[ProductChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    image_urls: Optional[List[str]] = Field(None, alias="imageUrls")
    tags: Optional[List[str]] = None
    price: Optional[float] = Field(None, ge=0)
    cost: Optional[float] = Field(None, ge=0)
    compare_at_price: Optional[float] = Field(
        None,
        ge=0,
        alias="compareAtPrice",
    )
    sku: Optional[str] = None
    sku_pattern: Optional[str] = Field(None, alias="skuPattern")
    barcode: Optional[str] = None
    barcode_format: Optional[BarcodeFormat] = Field(
        None,
        alias="barcodeFormat",
    )
    is_alcoholic: Optional[bool] = Field(None, alias="isAlcoholic")
    category_id: Optional[str] = Field(None, alias="categoryId")
    brand: Optional[str] = None
    brand_id: Optional[str] = Field(None, alias="brandId")
    track_inventory: Optional[bool] = Field(None, alias="trackInventory")
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        alias="lowStockThreshold",
    )
    stocked_at: Optional[int] = Field(None, alias="stockedAt")
    reorder_point: Optional[int] = Field(None, ge=0, alias="reorderPoint")
    lead_time: Optional[int] = Field(None, ge=0, alias="leadTime")
    supplier_id: Optional[str] = Field(None, alias="supplierId")
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    shipping_class_id: Optional[str] = Field(None, alias="shippingClassId")
    hs_code: Optional[str] = Field(None, alias="HSCode")
    attributes: Optional[List[ProductAttributeValue]] = None
    tax_rule_ids: Optional[List[str]] = Field(None, alias="taxRuleIds")
    is_active: Optional[bool] = Field(None, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    placement: Optional[CreateDisplayOrderPlacement] = None


class ProductCatalog(BaseModel):
    """Product category and its items."""

    product_category: ProductCategory = Field(..., alias="productCategory")
    items: List[BusinessProduct]


class ProductCategoryWithDescendants(ProductCategory):
    """Product category read model with nested descendants."""

    descendants: Optional[List["ProductCategoryWithDescendants"]] = None
    descendant_ids: Optional[List[str]] = Field(None, alias="descendantIds")
    descendant_count: Optional[int] = Field(
        None,
        ge=0,
        alias="descendantCount",
    )


ProductCategoryWithDescendants.model_rebuild()


class AttributeDefFilters(TypedDict, total=False):
    """Filters for querying attribute definitions."""

    search: Optional[str]
    type: Optional[AttributeDefType]
    is_active: Optional[bool]


class AttributeDefSorting(TypedDict):
    """Sorting options for attribute definitions."""

    field: Literal["name", "slug", "created_at"]
    direction: Literal["asc", "desc"]


class AttributeDefQueryOptions(TypedDict, total=False):
    """Query options for attribute definition retrieval."""

    page: int
    page_size: int
    filters: Optional[AttributeDefFilters]
    sorting: Optional[AttributeDefSorting]


class ProductCategoryFilters(TypedDict, total=False):
    """Filters for querying product categories."""

    search: Optional[str]
    parent_id: Optional[str]
    include_descendants: Optional[bool]
    location_scope: Optional[CategoryLocationScope]
    age_restricted: Optional[bool]


class ProductCategorySorting(TypedDict):
    """Sorting options for product category queries."""

    field: Literal["name", "display_order", "created_at"]
    direction: Literal["asc", "desc"]


class ProductCategoryQueryOptions(TypedDict, total=False):
    """Query options for product category retrieval."""

    page: int
    page_size: int
    filters: Optional[ProductCategoryFilters]
    sorting: Optional[ProductCategorySorting]


class PriceRangeFilter(TypedDict, total=False):
    """Price range filter for business products."""

    min: Optional[float]
    max: Optional[float]


class BusinessProductFilters(TypedDict, total=False):
    """Filters for querying business products."""

    search: Optional[str]
    location_id: Optional[str]
    category_id: Optional[str]
    is_active: Optional[bool]
    brand: Optional[str]
    brand_id: Optional[str]
    track_inventory: Optional[bool]
    price_range: Optional[PriceRangeFilter]
    low_stock: Optional[bool]
    is_alcoholic: Optional[bool]
    tags: Optional[List[str]]


class BusinessProductSorting(TypedDict):
    """Sorting options for business product queries."""

    field: Literal["name", "price", "created_at", "display_order"]
    direction: Literal["asc", "desc"]


class BusinessProductQueryOptions(TypedDict, total=False):
    """Query options for business product retrieval."""

    page: int
    page_size: int
    filters: Optional[BusinessProductFilters]
    sorting: Optional[BusinessProductSorting]
