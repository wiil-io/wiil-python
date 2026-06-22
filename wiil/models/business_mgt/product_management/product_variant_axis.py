"""Variant axis schema definitions for product variants."""

from typing import List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import VariantAxisType


class VariantAxisValue(BaseModel):
    """Single selectable value within a variant axis."""

    id: str
    label: str = Field(..., min_length=1)
    swatch_color: Optional[str] = Field(None, alias="swatchColor")
    image_id: Optional[str] = Field(None, alias="imageId")
    numeric_value: Optional[float] = Field(None, alias="numericValue")
    sort_order: int = Field(0, alias="sortOrder")


class VariantAxis(EntityModel):
    """A product variation dimension (e.g. size or color)."""

    name: str = Field(..., min_length=1)
    type: VariantAxisType
    values: List[VariantAxisValue] = Field(..., min_length=1)
    is_active: bool = Field(True, alias="isActive")


class CreateVariantAxis(BaseModel):
    """Schema for creating a variant axis."""

    name: str = Field(..., min_length=1)
    type: VariantAxisType
    values: List[VariantAxisValue] = Field(..., min_length=1)
    is_active: bool = Field(True, alias="isActive")


class UpdateVariantAxis(BaseModel):
    """Schema for updating a variant axis."""

    id: str
    name: Optional[str] = Field(None, min_length=1)
    type: Optional[VariantAxisType] = None
    values: Optional[List[VariantAxisValue]] = Field(None, min_length=1)
    is_active: Optional[bool] = Field(None, alias="isActive")


class VariantAxisDisplay(BaseModel):
    """Variant axis read model optimized for UI display."""

    id: str
    name: str
    type: VariantAxisType
    values: List[VariantAxisValue]
    display_order: int = Field(0, alias="displayOrder")


class VariantAxisFilters(TypedDict, total=False):
    """Filters for querying variant axes."""

    search: Optional[str]
    type: Optional[VariantAxisType]
    is_active: Optional[bool]


class VariantAxisSorting(TypedDict):
    """Sorting options for variant axis queries."""

    field: Literal["name", "created_at"]
    direction: Literal["asc", "desc"]


class VariantAxisQueryOptions(TypedDict, total=False):
    """Query options for variant axis retrieval."""

    page: int
    page_size: int
    filters: Optional[VariantAxisFilters]
    sorting: Optional[VariantAxisSorting]
