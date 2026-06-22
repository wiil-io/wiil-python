"""Menu catalog schema definitions for business management."""

from typing import List, Optional

from pydantic import Field

from wiil.models.base import BaseModel
from wiil.models.business_mgt.menu_management.menu_config import (
    BusinessMenuItem,
    MenuCategory,
)
from wiil.models.business_mgt.menu_management.menu_item_variant import (
    MenuItemVariant,
)
from wiil.models.business_mgt.menu_management.modifier import ModifierGroupView


class PriceRange(BaseModel):
    """Resolved min/max price across menu item variants."""

    min: float = Field(..., ge=0)
    max: float = Field(..., ge=0)


class MenuItemCatalog(BusinessMenuItem):
    """Menu item schema for catalog display."""

    variants: List[MenuItemVariant] = Field(..., min_length=1)
    price_range: Optional[PriceRange] = Field(None, alias="priceRange")
    is_variant_selectable: bool = Field(True, alias="isVariantSelectable")
    modifier_groups: List[ModifierGroupView] = Field(
        default_factory=list,
        alias="modifierGroups",
    )


class MenuCatalog(BaseModel):
    """Represents a category with its menu items and variants."""

    category: MenuCategory
    items: List[MenuItemCatalog]


BusinessMenuCatalog = List[MenuCatalog]
