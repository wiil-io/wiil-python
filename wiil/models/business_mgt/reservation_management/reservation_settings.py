"""Reservation settings schema definitions."""

from typing import Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    ReservationSettingType,
)


class RentalTierDefinition(BaseModel):
    """Tier definition for rental pricing rules."""

    id: str
    name: str
    duration_minutes: int = Field(..., gt=0, alias="durationMinutes")
    sort_order: int = Field(0, ge=0, alias="sortOrder")


class TableReservationSettings(BaseModel):
    """Table reservation settings block."""

    setting_type: ReservationSettingType = Field(
        ReservationSettingType.CAPACITY,
        alias="settingType",
    )
    default_duration_minutes: int = Field(
        90,
        gt=0,
        alias="defaultDurationMinutes",
    )
    turnover_minutes: int = Field(15, ge=0, alias="turnoverMinutes")
    slot_interval_minutes: int = Field(15, gt=0, alias="slotIntervalMinutes")
    max_party_size: Optional[int] = Field(None, gt=0, alias="maxPartySize")
    advance_booking_days: int = Field(30, gt=0, alias="advanceBookingDays")


class RoomReservationSettings(BaseModel):
    """Room reservation settings block."""

    check_in_time: str = Field(
        "15:00",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        alias="checkInTime",
    )
    check_out_time: str = Field(
        "11:00",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        alias="checkOutTime",
    )
    min_stay_nights: int = Field(1, gt=0, alias="minStayNights")
    max_stay_nights: Optional[int] = Field(None, gt=0, alias="maxStayNights")
    advance_booking_days: int = Field(90, gt=0, alias="advanceBookingDays")


class RentalReservationSettings(BaseModel):
    """Rental reservation settings block."""

    tiers: list[RentalTierDefinition] = Field(default_factory=list)
    require_waiver: bool = Field(False, alias="requireWaiver")
    require_id_verification: bool = Field(
        False,
        alias="requireIdVerification",
    )
    default_deposit_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        alias="defaultDepositPercent",
    )


class ReservationSettings(EntityModel):
    """Reservation settings schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    table: Optional[TableReservationSettings] = None
    room: Optional[RoomReservationSettings] = None
    rental: Optional[RentalReservationSettings] = None
    support_table_reservations: bool = Field(
        False,
        alias="supportTableReservations",
    )
    support_room_reservations: bool = Field(
        False,
        alias="supportRoomReservations",
    )
    support_rental_reservations: bool = Field(
        False,
        alias="supportRentalReservations",
    )


class CreateReservationSettings(BaseModel):
    """Schema for creating reservation settings."""

    location_id: Optional[str] = Field(None, alias="locationId")
    table: Optional[TableReservationSettings] = None
    room: Optional[RoomReservationSettings] = None
    rental: Optional[RentalReservationSettings] = None
    support_table_reservations: bool = Field(
        False,
        alias="supportTableReservations",
    )
    support_room_reservations: bool = Field(
        False,
        alias="supportRoomReservations",
    )
    support_rental_reservations: bool = Field(
        False,
        alias="supportRentalReservations",
    )


class UpdateReservationSettings(BaseModel):
    """Schema for updating reservation settings."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    table: Optional[TableReservationSettings] = None
    room: Optional[RoomReservationSettings] = None
    rental: Optional[RentalReservationSettings] = None
    support_table_reservations: Optional[bool] = Field(
        None,
        alias="supportTableReservations",
    )
    support_room_reservations: Optional[bool] = Field(
        None,
        alias="supportRoomReservations",
    )
    support_rental_reservations: Optional[bool] = Field(
        None,
        alias="supportRentalReservations",
    )


class ReservationSettingsFilters(TypedDict, total=False):
    """Filters for reservation settings queries."""

    locationId: Optional[str]


class ReservationSettingsQueryOptions(TypedDict, total=False):
    """Query options for reservation settings retrieval."""

    page: int
    pageSize: int
    filters: Optional[ReservationSettingsFilters]
