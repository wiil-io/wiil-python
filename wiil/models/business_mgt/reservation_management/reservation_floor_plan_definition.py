"""Aggregate floor plan definition schema definitions.

Composes the floor plan, its sections, and nested table placements into a
single graph. The Create* variants support atomic creation of a floor plan
together with its sections and tables in one payload, while the response
variant returns the fully hydrated graph.
"""

from typing import Any, Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.reservation_management.reservation_section import (  # noqa: E501
    Section,
    SectionGeometry,
    TableShape,
)
from wiil.models.business_mgt.reservation_management.reservation_table_layout import (  # noqa: E501
    CanvasDimensions,
)


class CreateFloorPlanTablePlacementInput(BaseModel):
    """Inline table placement input used when creating a floor plan."""

    number: str
    x: float
    y: float
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    shape: TableShape
    rotation: Optional[float] = None
    min_party: int = Field(..., gt=0, alias="minParty")
    max_party: int = Field(..., gt=0, alias="maxParty")
    combinable_with: list[str] = Field(
        default_factory=list,
        alias="combinableWith",
    )
    server_section_id: Optional[str] = Field(None, alias="serverSectionId")


class CreateFloorPlanSectionInput(BaseModel):
    """Inline section input used when creating a floor plan."""

    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: bool = Field(True, alias="isActive")
    sort_order: int = Field(0, ge=0, alias="sortOrder")
    geometry: Optional[SectionGeometry] = None
    tables: list[CreateFloorPlanTablePlacementInput] = Field(
        ...,
        min_length=1,
    )


class CreateFloorPlanDefinition(BaseModel):
    """Schema for atomically creating a floor plan with sections and tables."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: str
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    is_active: bool = Field(True, alias="isActive")
    canvas_dimensions: CanvasDimensions = Field(..., alias="canvasDimensions")
    capacity: int = Field(..., gt=0)
    metadata: Optional[dict[str, Any]] = None
    sections: list[CreateFloorPlanSectionInput] = Field(..., min_length=1)


class FloorPlanDefinition(EntityModel):
    """Fully hydrated floor plan definition graph."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: str
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    is_active: bool = Field(True, alias="isActive")
    canvas_dimensions: CanvasDimensions = Field(..., alias="canvasDimensions")
    capacity: int = Field(..., gt=0)
    metadata: Optional[dict[str, Any]] = None
    sections: list[Section] = Field(default_factory=list)
