"""Reservation slot-query request/response schemas."""

import re
from typing import Literal, Optional, Union

from pydantic import Field, field_validator, model_validator

from wiil.models.base import BaseModel
from wiil.models.business_mgt.reservation_management.reservation_room import (
    RoomRatePerNight,
)
from wiil.models.type_definitions.business_definitions import ResourceType

_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_TIME_OF_DAY_PATTERN = re.compile(
    r"^(0?[1-9]|1[0-2]):[0-5]\d\s?(AM|PM)$",
    re.IGNORECASE,
)


class TableReservationSlotQueryRequest(BaseModel):
    """Slot query request for table reservations."""

    resource_type: Literal[ResourceType.TABLE] = Field(
        ResourceType.TABLE,
        alias="resourceType",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    local_date: str = Field(..., alias="localDate")
    max_results: int = Field(20, gt=0, le=1000, alias="maxResults")
    party_size: int = Field(..., gt=0, alias="partySize")
    floor_plan_id: Optional[str] = Field(None, alias="floorPlanId")
    floor_plan_section_id: Optional[str] = Field(
        None,
        alias="floorPlanSectionId",
    )

    @field_validator("local_date")
    @classmethod
    def validate_local_date(cls, value: str) -> str:
        if not _DATE_PATTERN.fullmatch(value):
            raise ValueError("localDate must be YYYY-MM-DD")
        return value


class RoomReservationSlotQueryRequest(BaseModel):
    """Slot query request for room reservations."""

    resource_type: Literal[ResourceType.ROOM] = Field(
        ResourceType.ROOM,
        alias="resourceType",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    local_date: str = Field(..., alias="localDate")
    max_results: int = Field(20, gt=0, le=1000, alias="maxResults")
    nights: int = Field(1, gt=0)
    occupancy: Optional[int] = Field(None, gt=0)

    @field_validator("local_date")
    @classmethod
    def validate_local_date(cls, value: str) -> str:
        if not _DATE_PATTERN.fullmatch(value):
            raise ValueError("localDate must be YYYY-MM-DD")
        return value


class RentalReservationSlotQueryRequest(BaseModel):
    """Slot query request for rental reservations."""

    resource_type: Literal[ResourceType.RENTAL] = Field(
        ResourceType.RENTAL,
        alias="resourceType",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    local_date: str = Field(..., alias="localDate")
    max_results: int = Field(20, gt=0, le=1000, alias="maxResults")
    return_date: Optional[str] = Field(None, alias="returnDate")
    tier_id: Optional[str] = Field(None, alias="tierId")
    duration_minutes: Optional[int] = Field(
        None,
        gt=0,
        alias="durationMinutes",
    )

    @field_validator("local_date", "return_date")
    @classmethod
    def validate_dates(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not _DATE_PATTERN.fullmatch(value):
            raise ValueError("date must match YYYY-MM-DD")
        return value


ReservationSlotQueryRequest = Union[
    TableReservationSlotQueryRequest,
    RoomReservationSlotQueryRequest,
    RentalReservationSlotQueryRequest,
]


class ReservationCandidateSlot(BaseModel):
    """Common candidate slot shape for table availability."""

    resource_id: str = Field(..., alias="resourceId")
    start_time_of_day: str = Field(..., alias="startTimeOfDay")
    start_minute_of_day: int = Field(
        ...,
        ge=0,
        le=1439,
        alias="startMinuteOfDay",
    )
    end_minute_of_day: int = Field(
        ...,
        ge=1,
        le=1440,
        alias="endMinuteOfDay",
    )
    start_time_utc_sec: int = Field(..., alias="startTimeUtcSec")
    end_time_utc_sec: int = Field(..., alias="endTimeUtcSec")
    is_available: bool = Field(True, alias="isAvailable")
    capacity_remaining: Optional[int] = Field(
        None,
        ge=0,
        alias="capacityRemaining",
    )
    price_quote: Optional[float] = Field(None, ge=0, alias="priceQuote")

    @field_validator("start_time_of_day")
    @classmethod
    def validate_time_of_day(cls, value: str) -> str:
        if not _TIME_OF_DAY_PATTERN.fullmatch(value):
            raise ValueError("startTimeOfDay must be h:mm AM/PM")
        return value

    @model_validator(mode="after")
    def validate_bounds(self) -> "ReservationCandidateSlot":
        if self.end_minute_of_day <= self.start_minute_of_day:
            raise ValueError(
                "endMinuteOfDay must be greater than startMinuteOfDay"
            )
        if self.end_time_utc_sec <= self.start_time_utc_sec:
            raise ValueError(
                "endTimeUtcSec must be greater than startTimeUtcSec"
            )
        return self


class TableReservationSlotQueryResponse(BaseModel):
    """Slot query response for table reservations."""

    resource_type: Literal[ResourceType.TABLE] = Field(
        ResourceType.TABLE,
        alias="resourceType",
    )
    local_date: str = Field(..., alias="localDate")
    generated_at: int = Field(..., alias="generatedAt")
    slots: list[ReservationCandidateSlot]


class RoomCandidateSlot(BaseModel):
    """Candidate slot shape for room availability."""

    resource_id: str = Field(..., alias="resourceId")
    check_in_date: str = Field(..., alias="checkInDate")
    check_out_date: str = Field(..., alias="checkOutDate")
    nights: int = Field(..., gt=0)
    occupancy: Optional[int] = Field(None, gt=0)
    rooms_available: int = Field(..., ge=0, alias="roomsAvailable")
    rate_per_night: list[RoomRatePerNight] = Field(
        default_factory=list,
        alias="ratePerNight",
    )
    total_with_tax: float = Field(..., ge=0, alias="totalWithTax")
    is_available: bool = Field(True, alias="isAvailable")

    @field_validator("check_in_date", "check_out_date")
    @classmethod
    def validate_dates(cls, value: str) -> str:
        if not _DATE_PATTERN.fullmatch(value):
            raise ValueError("date must match YYYY-MM-DD")
        return value

    @model_validator(mode="after")
    def validate_check_out_after_check_in(self) -> "RoomCandidateSlot":
        if self.check_out_date <= self.check_in_date:
            raise ValueError("checkOutDate must be after checkInDate")
        return self


class RoomReservationSlotQueryResponse(BaseModel):
    """Slot query response for room reservations."""

    resource_type: Literal[ResourceType.ROOM] = Field(
        ResourceType.ROOM,
        alias="resourceType",
    )
    check_in_date: str = Field(..., alias="checkInDate")
    check_out_date: str = Field(..., alias="checkOutDate")
    nights: int = Field(..., gt=0)
    generated_at: int = Field(..., alias="generatedAt")
    slots: list[RoomCandidateSlot]


class RentalCandidateSlot(BaseModel):
    """Candidate slot shape for rental availability."""

    resource_id: str = Field(..., alias="resourceId")
    pickup_date: str = Field(..., alias="pickupDate")
    return_date: str = Field(..., alias="returnDate")
    pickup_time_of_day: Optional[str] = Field(None, alias="pickupTimeOfDay")
    return_time_of_day: Optional[str] = Field(None, alias="returnTimeOfDay")
    duration_minutes: Optional[int] = Field(
        None,
        gt=0,
        alias="durationMinutes",
    )
    start_time_utc_sec: int = Field(..., alias="startTimeUtcSec")
    end_time_utc_sec: int = Field(..., alias="endTimeUtcSec")
    units_available: int = Field(..., ge=0, alias="unitsAvailable")
    total_with_tax: float = Field(..., ge=0, alias="totalWithTax")
    price_quote: Optional[float] = Field(None, ge=0, alias="priceQuote")
    is_available: bool = Field(True, alias="isAvailable")

    @field_validator("pickup_date", "return_date")
    @classmethod
    def validate_dates(cls, value: str) -> str:
        if not _DATE_PATTERN.fullmatch(value):
            raise ValueError("date must match YYYY-MM-DD")
        return value

    @field_validator("pickup_time_of_day", "return_time_of_day")
    @classmethod
    def validate_time_of_day(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not _TIME_OF_DAY_PATTERN.fullmatch(value):
            raise ValueError("time must match h:mm AM/PM")
        return value

    @model_validator(mode="after")
    def validate_bounds(self) -> "RentalCandidateSlot":
        if self.return_date < self.pickup_date:
            raise ValueError("returnDate must be on or after pickupDate")
        if self.end_time_utc_sec <= self.start_time_utc_sec:
            raise ValueError(
                "endTimeUtcSec must be greater than startTimeUtcSec"
            )
        has_pickup = self.pickup_time_of_day is not None
        has_return = self.return_time_of_day is not None
        if has_pickup != has_return:
            raise ValueError(
                "pickupTimeOfDay and returnTimeOfDay must both "
                "be present or both absent"
            )
        return self


class RentalReservationSlotQueryResponse(BaseModel):
    """Slot query response for rental reservations."""

    resource_type: Literal[ResourceType.RENTAL] = Field(
        ResourceType.RENTAL,
        alias="resourceType",
    )
    pickup_date: str = Field(..., alias="pickupDate")
    return_date: str = Field(..., alias="returnDate")
    generated_at: int = Field(..., alias="generatedAt")
    slots: list[RentalCandidateSlot]


ReservationSlotQueryResponse = Union[
    TableReservationSlotQueryResponse,
    RoomReservationSlotQueryResponse,
    RentalReservationSlotQueryResponse,
]
