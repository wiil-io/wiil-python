"""Reservation maintenance-block schema definitions."""

from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel


class MaintenanceBlock(EntityModel):
    """Maintenance block schema."""

    resource_instance_id: str = Field(..., alias="resourceInstanceId")
    location_id: Optional[str] = Field(None, alias="locationId")
    start_date: int = Field(..., alias="startDate")
    end_date: int = Field(..., alias="endDate")
    reason: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self) -> "MaintenanceBlock":
        if self.end_date < self.start_date:
            raise ValueError(
                "endDate must be greater than or equal to startDate"
            )
        return self


class CreateMaintenanceBlock(BaseModel):
    """Schema for creating maintenance blocks."""

    resource_instance_id: str = Field(..., alias="resourceInstanceId")
    location_id: Optional[str] = Field(None, alias="locationId")
    start_date: int = Field(..., alias="startDate")
    end_date: int = Field(..., alias="endDate")
    reason: Optional[str] = None


class UpdateMaintenanceBlock(BaseModel):
    """Schema for updating maintenance blocks."""

    id: str
    resource_instance_id: Optional[str] = Field(
        None,
        alias="resourceInstanceId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    start_date: Optional[int] = Field(None, alias="startDate")
    end_date: Optional[int] = Field(None, alias="endDate")
    reason: Optional[str] = None


class DateRangeFilter(TypedDict, total=False):
    """Date range filter."""

    start: Optional[int]
    end: Optional[int]


class MaintenanceBlockFilters(TypedDict, total=False):
    """Filters for maintenance-block queries."""

    resource_instance_id: Optional[str]
    location_id: Optional[str]
    date_range: Optional[DateRangeFilter]


class MaintenanceBlockSorting(TypedDict):
    """Sorting options for maintenance-block queries."""

    field: Literal["start_date", "end_date", "created_at"]
    direction: Literal["asc", "desc"]


class MaintenanceBlockQueryOptions(TypedDict, total=False):
    """Query options for maintenance-block retrieval."""

    page: int
    page_size: int
    filters: Optional[MaintenanceBlockFilters]
    sorting: Optional[MaintenanceBlockSorting]
