"""Product configuration schema definitions for business management.

This module contains Pydantic models for managing product categories, products,
and inventory information for retail operations.
"""

from typing import Literal, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel


class ProductDimensions(BaseModel):
    """Product dimensions for shipping calculations.

    Attributes:
        length: Product length in specified units
        width: Product width in specified units
        height: Product height in specified units
        unit: Measurement unit for dimensions

    Example:
        ```python
        dimensions = ProductDimensions(
            length=10.5,
            width=5.0,
            height=3.0,
            unit="inches"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    length: float = Field(
        ...,
        gt=0,
        description="Product length in specified units"
    )
    width: float = Field(
        ...,
        gt=0,
        description="Product width in specified units"
    )
    height: float = Field(
        ...,
        gt=0,
        description="Product height in specified units"
    )
    unit: Literal["inches", "cm"] = Field(
        "inches",
        description="Measurement unit for length, width, and height dimensions"
    )


class ProductCategory(BaseModel):
    """Product category for organizing products.

    Category for product organization (e.g., Electronics, Clothing, Home & Garden).
    Used by AI Powered Services when presenting product options to customers.

    Attributes:
        name: Category name for product organization
        description: Category description
        display_order: Numeric order for category display
        is_default: Whether this is the default category for uncategorized products

    Example:
        ```python
        category = ProductCategory(
            id="cat_123",
            name="Electronics",
            description="Electronic devices and accessories",
            display_order=1,
            is_default=False
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
        description="Category name for product organization"
    )
    description: Optional[str] = Field(
        None,
        description="Category description providing context about the type of products included"
    )
    display_order: Optional[int] = Field(
        None,
        description="Numeric order for category display in product catalog",
        alias="displayOrder"
    )
    is_default: bool = Field(
        False,
        description="Whether this is the default category for uncategorized products",
        alias="isDefault"
    )


class BusinessProduct(BaseModel):
    """Business product model.

    Product in the catalog with pricing, inventory tracking, and physical attributes.

    Attributes:
        name: Product name
        description: Product description
        price: Product price
        sku: Stock Keeping Unit identifier
        barcode: Product barcode
        category_id: Category ID
        category: Product category
        brand: Product brand name
        track_inventory: Whether to track inventory
        stock_quantity: Current stock quantity
        low_stock_threshold: Low stock alert threshold
        weight: Product weight
        dimensions: Product dimensions
        is_active: Whether product is available for sale
        display_order: Display order in category

    Example:
        ```python
        product = BusinessProduct(
            id="prod_123",
            name="Wireless Mouse",
            description="Ergonomic wireless mouse",
            price=29.99,
            sku="WM-001",
            category_id="cat_123",
            brand="TechBrand",
            track_inventory=True,
            stock_quantity=100,
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
        description="Display name of the product shown to customers"
    )
    description: Optional[str] = Field(
        None,
        description="Detailed product description including features and specifications"
    )
    price: float = Field(
        ...,
        ge=0,
        description="Base price for this product in the account's currency"
    )
    sku: Optional[str] = Field(
        None,
        description="Stock Keeping Unit identifier for internal inventory tracking"
    )
    barcode: Optional[str] = Field(
        None,
        description="Product barcode (UPC, EAN, ISBN) for point-of-sale scanning"
    )
    category_id: str = Field(
        ...,
        description="References ProductCategory this product belongs to",
        alias="categoryId"
    )
    category: Optional[ProductCategory] = Field(
        None,
        description="Populated ProductCategory object for convenient access"
    )
    brand: Optional[str] = Field(
        None,
        description="Product brand or manufacturer name"
    )
    track_inventory: bool = Field(
        False,
        description="Whether inventory tracking is enabled for this product",
        alias="trackInventory"
    )
    stock_quantity: Optional[int] = Field(
        None,
        ge=0,
        description="Current available stock quantity",
        alias="stockQuantity"
    )
    low_stock_threshold: Optional[int] = Field(
        None,
        ge=0,
        description="Stock level that triggers low inventory alerts",
        alias="lowStockThreshold"
    )
    weight: Optional[float] = Field(
        None,
        gt=0,
        description="Product weight for shipping calculations"
    )
    dimensions: Optional[ProductDimensions] = Field(
        None,
        description="Physical dimensions of the product for shipping cost estimation"
    )
    is_active: bool = Field(
        True,
        description="Whether product is active and available for sale",
        alias="isActive"
    )
    display_order: Optional[int] = Field(
        None,
        description="Display order within category. Lower numbers appear first",
        alias="displayOrder"
    )


class CreateProductCategory(BaseModel):
    """Schema for creating a new product category.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateProductCategory(
            name="Home & Garden",
            description="Home improvement and garden supplies",
            display_order=3
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
    is_default: bool = Field(False, alias="isDefault")


class UpdateProductCategory(BaseModel):
    """Schema for updating an existing product category.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateProductCategory(
            id="cat_123",
            name="Updated Category Name"
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
    is_default: Optional[bool] = Field(None, alias="isDefault")


class CreateBusinessProduct(BaseModel):
    """Schema for creating a new business product.

    Omits auto-generated fields and category object.

    Example:
        ```python
        create_data = CreateBusinessProduct(
            name="Wireless Keyboard",
            description="Mechanical keyboard with RGB",
            price=79.99,
            sku="KB-001",
            category_id="cat_123",
            track_inventory=True,
            stock_quantity=50
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
    sku: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[str] = Field(None, alias="categoryId")
    category: Optional[str] = None
    brand: Optional[str] = None
    track_inventory: bool = Field(False, alias="trackInventory")
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(None, ge=0, alias="lowStockThreshold")
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdateBusinessProduct(BaseModel):
    """Schema for updating an existing business product.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateBusinessProduct(
            id="prod_123",
            price=34.99,
            stock_quantity=75
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
    sku: Optional[str] = None
    barcode: Optional[str] = None
    category_id: Optional[str] = Field(None, alias="categoryId")
    category: Optional[str] = None
    brand: Optional[str] = None
    track_inventory: Optional[bool] = Field(None, alias="trackInventory")
    stock_quantity: Optional[int] = Field(None, ge=0, alias="stockQuantity")
    low_stock_threshold: Optional[int] = Field(None, ge=0, alias="lowStockThreshold")
    weight: Optional[float] = Field(None, gt=0)
    dimensions: Optional[ProductDimensions] = None
    is_active: Optional[bool] = Field(None, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
