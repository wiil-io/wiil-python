"""Reservation table-layout schema definitions."""

from enum import Enum
from typing import Any, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class CanvasUnit(str, Enum):
    """Canvas unit values."""

    PX = "px"
    FT = "ft"
    M = "m"


class CanvasDimensions(BaseModel):
    """Canvas dimensions for floor-plan rendering."""

    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    unit: CanvasUnit = CanvasUnit.PX


class FloorPlan(EntityModel):
    """Table-layout floor-plan schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: str
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    is_active: bool = Field(True, alias="isActive")
    canvas_dimensions: CanvasDimensions = Field(..., alias="canvasDimensions")
    capacity: int = Field(..., gt=0)
    metadata: Optional[dict[str, Any]] = None


class CreateFloorPlan(BaseModel):
    """Schema for creating floor plans."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: str
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    is_active: bool = Field(True, alias="isActive")
    canvas_dimensions: CanvasDimensions = Field(..., alias="canvasDimensions")
    capacity: int = Field(..., gt=0)
    metadata: Optional[dict[str, Any]] = None


class UpdateFloorPlan(BaseModel):
    """Schema for updating floor plans."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    is_active: Optional[bool] = Field(None, alias="isActive")
    canvas_dimensions: Optional[CanvasDimensions] = Field(
        None,
        alias="canvasDimensions",
    )
    capacity: Optional[int] = Field(None, gt=0)
    metadata: Optional[dict[str, Any]] = None


class FloorPlanFilters(TypedDict, total=False):
    """Filters for floor-plan queries."""

    locationId: Optional[str]
    isActive: Optional[bool]


class FloorPlanQueryOptions(TypedDict, total=False):
    """Query options for floor-plan retrieval."""

    page: int
    pageSize: int
    filters: Optional[FloorPlanFilters]
