"""Table reservation schema definitions."""

from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    ExternalRef,
    ReservationStatus,
)


class TableReservation(EntityModel):
    """Table reservation schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    resource_id: str = Field(..., alias="resourceId")
    customer_id: str = Field(..., alias="customerId")
    floor_plan_id: Optional[str] = Field(None, alias="floorPlanId")
    floor_plan_section_id: Optional[str] = Field(
        None,
        alias="floorPlanSectionId",
    )
    persons_number: int = Field(..., gt=0, alias="personsNumber")
    time: int
    duration: int = Field(..., gt=0)
    status: ReservationStatus = ReservationStatus.PENDING
    source: Optional[str] = None
    notes: Optional[str] = None
    is_vip: bool = Field(False, alias="isVip")
    special_requests: Optional[str] = Field(None, alias="specialRequests")
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class CreateTableReservation(BaseModel):
    """Schema for creating table reservations."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    resource_id: str = Field(..., alias="resourceId")
    customer_id: str = Field(..., alias="customerId")
    floor_plan_id: Optional[str] = Field(None, alias="floorPlanId")
    floor_plan_section_id: Optional[str] = Field(
        None,
        alias="floorPlanSectionId",
    )
    persons_number: int = Field(..., gt=0, alias="personsNumber")
    time: int
    duration: int = Field(..., gt=0)
    status: ReservationStatus = ReservationStatus.PENDING
    source: Optional[str] = None
    notes: Optional[str] = None
    is_vip: bool = Field(False, alias="isVip")
    special_requests: Optional[str] = Field(None, alias="specialRequests")
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class UpdateTableReservation(BaseModel):
    """Schema for updating table reservations."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    floor_plan_id: Optional[str] = Field(None, alias="floorPlanId")
    floor_plan_section_id: Optional[str] = Field(
        None,
        alias="floorPlanSectionId",
    )
    persons_number: Optional[int] = Field(None, gt=0, alias="personsNumber")
    time: Optional[int] = None
    duration: Optional[int] = Field(None, gt=0)
    status: Optional[ReservationStatus] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    is_vip: Optional[bool] = Field(None, alias="isVip")
    special_requests: Optional[str] = Field(None, alias="specialRequests")
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class DateRangeFilter(TypedDict, total=False):
    """Date range filter."""

    start: Optional[int]
    end: Optional[int]


class TableReservationFilters(TypedDict, total=False):
    """Filters for table reservation queries."""

    search: Optional[str]
    location_id: Optional[str]
    channel_id: Optional[str]
    customer_id: Optional[str]
    status: Optional[list[ReservationStatus]]
    table_id: Optional[str]
    date_range: Optional[DateRangeFilter]
    external_source: Optional[str]


class TableReservationSorting(TypedDict):
    """Sorting options for table reservations."""

    field: Literal["time", "duration", "created_at"]
    direction: Literal["asc", "desc"]


class TableReservationQueryOptions(TypedDict, total=False):
    """Query options for table reservation retrieval."""

    page: int
    page_size: int
    filters: Optional[TableReservationFilters]
    sorting: Optional[TableReservationSorting]
