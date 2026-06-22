"""Reservation section and table-placement schema definitions."""

from enum import Enum
from typing import Literal, Optional

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel


class TableShape(str, Enum):
    """Table shape values for floor planning."""

    ROUND = "round"
    SQUARE = "square"
    BOOTH = "booth"
    RECT = "rect"
    CURVED = "curved"
    HIGH_TOP = "high_top"
    BAR = "bar"


class Point2D(BaseModel):
    """2D point."""

    x: float
    y: float


class SectionGeometry(BaseModel):
    """Section geometry definition."""

    kind: Literal["auto", "rect", "polygon"]
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    points: Optional[list[Point2D]] = None
    rotation: Optional[float] = Field(None, ge=-360, le=360)


class TablePlacement(EntityModel):
    """Table placement in a section."""

    table_resource_id: str = Field(..., alias="tableResourceId")
    floor_plan_section_id: str = Field(..., alias="floorPlanSectionId")
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

    @model_validator(mode="after")
    def validate_bounds(self) -> "TablePlacement":
        if self.max_party < self.min_party:
            raise ValueError(
                "maxParty must be greater than or equal to minParty"
            )
        if self.table_resource_id in self.combinable_with:
            raise ValueError("combinableWith cannot include the table itself")
        return self


class CreateTablePlacement(BaseModel):
    """Schema for creating table placements."""

    table_resource_id: str = Field(..., alias="tableResourceId")
    floor_plan_section_id: str = Field(..., alias="floorPlanSectionId")
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


class UpdateTablePlacement(BaseModel):
    """Schema for updating table placements."""

    id: str
    table_resource_id: Optional[str] = Field(None, alias="tableResourceId")
    floor_plan_section_id: Optional[str] = Field(
        None,
        alias="floorPlanSectionId",
    )
    number: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    shape: Optional[TableShape] = None
    rotation: Optional[float] = None
    min_party: Optional[int] = Field(None, gt=0, alias="minParty")
    max_party: Optional[int] = Field(None, gt=0, alias="maxParty")
    combinable_with: Optional[list[str]] = Field(None, alias="combinableWith")
    server_section_id: Optional[str] = Field(None, alias="serverSectionId")


class Section(EntityModel):
    """Section schema."""

    location_id: str = Field(..., alias="locationId")
    floor_plan_id: str = Field(..., alias="floorPlanId")
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    geometry: Optional[SectionGeometry] = None
    sort_order: int = Field(0, ge=0, alias="sortOrder")
    is_active: bool = Field(True, alias="isActive")
    tables: list[TablePlacement] = Field(default_factory=list)


class CreateSection(BaseModel):
    """Schema for creating sections."""

    location_id: str = Field(..., alias="locationId")
    floor_plan_id: str = Field(..., alias="floorPlanId")
    name: str = Field(..., min_length=1)
    capacity: int = Field(..., gt=0)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    geometry: Optional[SectionGeometry] = None
    sort_order: int = Field(0, ge=0, alias="sortOrder")
    is_active: bool = Field(True, alias="isActive")
    tables: list[TablePlacement] = Field(default_factory=list)


class UpdateSection(BaseModel):
    """Schema for updating sections."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    floor_plan_id: Optional[str] = Field(None, alias="floorPlanId")
    name: Optional[str] = Field(None, min_length=1)
    capacity: Optional[int] = Field(None, gt=0)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    geometry: Optional[SectionGeometry] = None
    sort_order: Optional[int] = Field(None, ge=0, alias="sortOrder")
    is_active: Optional[bool] = Field(None, alias="isActive")
    tables: Optional[list[TablePlacement]] = None


class TablePlacementWithContext(BaseModel):
    """Table placement with its containing floor-plan section context."""

    placement: TablePlacement
    section: Section
