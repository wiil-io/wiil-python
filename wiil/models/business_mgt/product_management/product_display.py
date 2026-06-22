"""Product display schema definitions for catalog rendering."""

from typing import List, Optional

from pydantic import Field

from wiil.models.base import BaseModel
from wiil.models.business_mgt.product_management.product_config import (
    BusinessProduct,
    ProductCategory,
)
from wiil.models.business_mgt.product_management.product_variant import (
    ProductVariant,
)
from wiil.types.business_types import StockStatus


class ProductVariantDisplay(ProductVariant):
    """Product variant read model with resolved stock status."""

    stock_status: StockStatus = Field(..., alias="stockStatus")


class PriceRangeDisplay(BaseModel):
    """Computed min/max price range across variants."""

    min: float = Field(..., ge=0)
    max: float = Field(..., ge=0)


class ProductDisplay(BusinessProduct):
    """Product read model with variants and computed price range."""

    variants: List[ProductVariantDisplay] = Field(..., min_length=1)
    price_range: Optional[PriceRangeDisplay] = Field(None, alias="priceRange")
    is_variant_selectable: bool = Field(True, alias="isVariantSelectable")


class ProductCatalogDisplay(BaseModel):
    """Category and its products for catalog rendering."""

    product_category: ProductCategory = Field(..., alias="productCategory")
    items: List[ProductDisplay]


BusinessProductCatalogDisplay = List[ProductCatalogDisplay]
