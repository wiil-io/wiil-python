"""Product axis binding schema definitions."""

from typing import Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class ProductAxisBinding(EntityModel):
    """Links a product to an applicable variant axis."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    product_id: str = Field(..., alias="productId")
    axis_id: str = Field(..., alias="axisId")
    display_order: int = Field(0, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")


class CreateProductAxisBinding(BaseModel):
    """Schema for creating a product axis binding."""

    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    product_id: str = Field(..., alias="productId")
    axis_id: str = Field(..., alias="axisId")
    display_order: int = Field(0, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")


class UpdateProductAxisBinding(BaseModel):
    """Schema for updating a product axis binding."""

    id: str
    product_revision_id: Optional[str] = Field(None, alias="productRevisionId")
    product_id: Optional[str] = Field(None, alias="productId")
    axis_id: Optional[str] = Field(None, alias="axisId")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: Optional[bool] = Field(None, alias="isActive")
