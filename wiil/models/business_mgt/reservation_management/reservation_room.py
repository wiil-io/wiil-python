"""Room reservation schema definitions."""

from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    ExternalRef,
    PaymentStatus,
    ReservationStatus,
)


class RoomRatePerNight(BaseModel):
    """Room rate details."""

    date: str
    amount: float = Field(..., ge=0)


class RoomReservation(EntityModel):
    """Room reservation schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    resource_id: str = Field(..., alias="resourceId")
    guest_id: str = Field(..., alias="guestId")
    persons_number: int = Field(..., gt=0, alias="personsNumber")
    check_in: int = Field(..., alias="checkIn")
    check_out: int = Field(..., alias="checkOut")
    nights: int = Field(..., gt=0)
    source: Optional[str] = None
    rate_per_night: list[RoomRatePerNight] = Field(
        default_factory=list,
        alias="ratePerNight",
    )
    total_with_tax: float = Field(..., ge=0, alias="totalWithTax")
    deposit: float = Field(0.0, ge=0)
    payment_status: Optional[PaymentStatus] = Field(
        None,
        alias="paymentStatus",
    )
    status: ReservationStatus = ReservationStatus.PENDING
    notes: Optional[str] = None
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")

    @model_validator(mode="after")
    def validate_dates(self) -> "RoomReservation":
        if self.check_out <= self.check_in:
            raise ValueError("checkOut must be greater than checkIn")
        return self


class CreateRoomReservation(BaseModel):
    """Schema for creating room reservations."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    resource_id: str = Field(..., alias="resourceId")
    guest_id: str = Field(..., alias="guestId")
    persons_number: int = Field(..., gt=0, alias="personsNumber")
    check_in: int = Field(..., alias="checkIn")
    check_out: int = Field(..., alias="checkOut")
    nights: int = Field(..., gt=0)
    source: Optional[str] = None
    rate_per_night: list[RoomRatePerNight] = Field(
        default_factory=list,
        alias="ratePerNight",
    )
    total_with_tax: float = Field(..., ge=0, alias="totalWithTax")
    deposit: float = Field(0.0, ge=0)
    payment_status: Optional[PaymentStatus] = Field(
        None,
        alias="paymentStatus",
    )
    status: ReservationStatus = ReservationStatus.PENDING
    notes: Optional[str] = None
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class UpdateRoomReservation(BaseModel):
    """Schema for updating room reservations."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    guest_id: Optional[str] = Field(None, alias="guestId")
    persons_number: Optional[int] = Field(None, gt=0, alias="personsNumber")
    check_in: Optional[int] = Field(None, alias="checkIn")
    check_out: Optional[int] = Field(None, alias="checkOut")
    nights: Optional[int] = Field(None, gt=0)
    source: Optional[str] = None
    rate_per_night: Optional[list[RoomRatePerNight]] = Field(
        None,
        alias="ratePerNight",
    )
    total_with_tax: Optional[float] = Field(None, ge=0, alias="totalWithTax")
    deposit: Optional[float] = Field(None, ge=0)
    payment_status: Optional[PaymentStatus] = Field(
        None,
        alias="paymentStatus",
    )
    status: Optional[ReservationStatus] = None
    notes: Optional[str] = None
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class DateRangeFilter(TypedDict, total=False):
    """Date range filter."""

    start: Optional[int]
    end: Optional[int]


class RoomReservationFilters(TypedDict, total=False):
    """Filters for room reservation queries."""

    search: Optional[str]
    locationId: Optional[str]
    channelId: Optional[str]
    resourceId: Optional[str]
    guestId: Optional[str]
    status: Optional[list[ReservationStatus]]
    paymentStatus: Optional[list[PaymentStatus]]
    dateRange: Optional[DateRangeFilter]
    externalSource: Optional[str]


class RoomReservationSorting(TypedDict):
    """Sorting options for room reservations."""

    field: Literal["checkIn", "checkOut", "createdAt"]
    direction: Literal["asc", "desc"]


class RoomReservationQueryOptions(TypedDict, total=False):
    """Query options for room reservation retrieval."""

    page: int
    pageSize: int
    filters: Optional[RoomReservationFilters]
    sorting: Optional[RoomReservationSorting]
