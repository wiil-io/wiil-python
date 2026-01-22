"""Business menu configuration schema definitions.

This module contains Pydantic models for managing menu categories, menu items,
and QR codes for menu access.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel


class NutritionalInfo(PydanticBaseModel):
    """Nutritional information for menu items.

    Attributes:
        calories: Caloric content per serving
        protein: Protein content in grams
        carbs: Carbohydrate content in grams
        fat: Fat content in grams
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    calories: Optional[float] = Field(None, description="Caloric content per serving")
    protein: Optional[float] = Field(None, description="Protein content in grams")
    carbs: Optional[float] = Field(None, description="Carbohydrate content in grams")
    fat: Optional[float] = Field(None, description="Fat content in grams")


class MenuCategory(BaseModel):
    """Menu category for organizing menu items.

    Category for menu organization (e.g., Appetizers, Main Course, Desserts).
    Used by AI Powered Services when presenting menu options to customers.

    Attributes:
        name: Category name for menu organization
        description: Category description providing context
        display_order: Numeric order for category display in menu listings

    Example:
        ```python
        category = MenuCategory(
            id="cat_123",
            name="Main Course",
            description="Entrees and main dishes",
            display_order=2
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., min_length=1, description="Category name for menu organization")
    description: Optional[str] = Field(
        None,
        description="Category description providing context about the type of items included"
    )
    display_order: Optional[int] = Field(
        None,
        description="Numeric order for category display. Lower numbers appear first",
        alias="displayOrder"
    )


class BusinessMenuItem(BaseModel):
    """Business menu item model.

    Menu item in the catalog with pricing, ingredients, and availability information.

    Attributes:
        name: Display name of the menu item
        description: Detailed item description
        price: Base price for this menu item
        category_id: References MenuCategory this item belongs to
        category: Populated MenuCategory object
        ingredients: List of primary ingredients
        allergens: Common allergens present
        nutritional_info: Optional nutritional information
        is_available: Real-time availability status
        preparation_time: Estimated preparation time in minutes
        is_active: Whether item is active in the menu catalog
        display_order: Display order within category

    Example:
        ```python
        item = BusinessMenuItem(
            id="item_123",
            name="Grilled Salmon",
            description="Fresh Atlantic salmon with herbs",
            price=24.99,
            category_id="cat_123",
            ingredients=["salmon", "herbs", "lemon"],
            allergens=["fish"],
            is_available=True,
            preparation_time=20,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        min_length=1,
        description="Display name of the menu item shown to customers"
    )
    description: Optional[str] = Field(
        None,
        description="Detailed item description including preparation style and ingredients"
    )
    price: float = Field(
        ...,
        ge=0,
        description="Base price for this menu item in the account's currency"
    )
    category_id: str = Field(
        ...,
        description="References MenuCategory this item belongs to",
        alias="categoryId"
    )
    category: Optional[MenuCategory] = Field(
        None,
        description="Populated MenuCategory object for convenient access"
    )
    ingredients: Optional[List[str]] = Field(
        None,
        description="List of primary ingredients for dietary information"
    )
    allergens: Optional[List[str]] = Field(
        None,
        description="Common allergens present (e.g., ['nuts', 'dairy', 'gluten'])"
    )
    nutritional_info: Optional[NutritionalInfo] = Field(
        None,
        description="Optional nutritional information for health-conscious customers",
        alias="nutritionalInfo"
    )
    is_available: bool = Field(
        True,
        description="Real-time availability status (e.g., sold out, temporarily unavailable)",
        alias="isAvailable"
    )
    preparation_time: Optional[int] = Field(
        None,
        gt=0,
        description="Estimated preparation time in minutes",
        alias="preparationTime"
    )
    is_active: bool = Field(
        True,
        description="Whether item is active in the menu catalog",
        alias="isActive"
    )
    display_order: Optional[int] = Field(
        None,
        description="Display order within category. Lower numbers appear first",
        alias="displayOrder"
    )


class MenuQRCode(PydanticBaseModel):
    """Menu QR code for digital menu access.

    QR code configuration for accessing digital menu interface.

    Attributes:
        id: Unique identifier for this QR code instance
        menu_url: URL to the digital menu accessed by scanning
        qr_code_image: Base64 encoded QR code image
        table_number: Optional table number for dine-in scenarios

    Example:
        ```python
        qr_code = MenuQRCode(
            id="qr_123",
            menu_url="https://menu.example.com/view/abc123",
            table_number="Table 5"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for this QR code instance")
    menu_url: str = Field(
        ...,
        description="URL to the digital menu accessed by scanning this QR code",
        alias="menuUrl"
    )
    qr_code_image: Optional[str] = Field(
        None,
        description="Base64 encoded QR code image for printing or digital display",
        alias="qrCodeImage"
    )
    table_number: Optional[str] = Field(
        None,
        description="Optional table number for dine-in scenarios",
        alias="tableNumber"
    )


class CreateMenuCategory(BaseModel):
    """Schema for creating a new menu category.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateMenuCategory(
            name="Desserts",
            description="Sweet treats and desserts",
            display_order=4
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")


class CreateBusinessMenuItem(BaseModel):
    """Schema for creating a new business menu item.

    Omits auto-generated fields and allows optional category specification.

    Example:
        ```python
        create_data = CreateBusinessMenuItem(
            name="Caesar Salad",
            description="Classic Caesar with romaine and parmesan",
            price=12.99,
            category_id="cat_123",
            is_available=True,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category_id: Optional[str] = Field(None, alias="categoryId")
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    nutritional_info: Optional[NutritionalInfo] = Field(None, alias="nutritionalInfo")
    is_available: bool = Field(True, alias="isAvailable")
    preparation_time: Optional[int] = Field(None, gt=0, alias="preparationTime")
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdateMenuCategory(BaseModel):
    """Schema for updating an existing menu category.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateMenuCategory(
            id="cat_123",
            name="Updated Category Name",
            display_order=5
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdateBusinessMenuItem(BaseModel):
    """Schema for updating an existing business menu item.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateBusinessMenuItem(
            id="item_123",
            price=26.99,
            is_available=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    category_id: Optional[str] = Field(None, alias="categoryId")
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    nutritional_info: Optional[NutritionalInfo] = Field(None, alias="nutritionalInfo")
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    preparation_time: Optional[int] = Field(None, gt=0, alias="preparationTime")
    is_active: Optional[bool] = Field(None, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
