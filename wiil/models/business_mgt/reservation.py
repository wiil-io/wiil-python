"""Reservation schema definitions for managing resource reservations.

This module contains Pydantic models for managing reservation settings and
reservations for tables, rooms, rentals, and other bookable resources.
"""

from typing import Optional

from pydantic import ConfigDict, EmailStr, Field

from wiil.models.base import BaseModel
from wiil.types.business_types import (
    AppointmentStatus,
    ReservationSettingType,
    ResourceReservationDurationUnit,
    ResourceType,
)


class ReservationSettings(BaseModel):
    """Reservation settings schema.

    Configuration for default reservation behavior and policies by resource type.

    Attributes:
        reservation_type: Type of reservation (table, room, rentals, etc.)
        setting_type: Type of reservation setting
        default_reservation_duration: Default reservation duration
        default_reservation_duration_unit: Unit of the default reservation duration
        is_active: Whether this reservation setting is active

    Example:
        ```python
        settings = ReservationSettings(
            id="settings_123",
            reservation_type=ResourceType.TABLE,
            setting_type=ReservationSettingType.CAPACITY,
            default_reservation_duration=2,
            default_reservation_duration_unit=ResourceReservationDurationUnit.HOURS,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    reservation_type: ResourceType = Field(
        ...,
        description="Resource type this setting applies to: ROOM, TABLE, RENTAL, or OTHER",
        alias="reservationType"
    )
    setting_type: ReservationSettingType = Field(
        ...,
        description="Configuration category defining what aspect of reservations this setting controls",
        alias="settingType"
    )
    default_reservation_duration: Optional[int] = Field(
        1,
        gt=0,
        description="Standard reservation length in specified units",
        alias="defaultReservationDuration"
    )
    default_reservation_duration_unit: Optional[ResourceReservationDurationUnit] = Field(
        ResourceReservationDurationUnit.HOURS,
        description="Time unit for defaultReservationDuration: HOURS, DAYS, or MINUTES",
        alias="defaultReservationDurationUnit"
    )
    is_active: bool = Field(
        False,
        description="Whether this configuration is currently active and applied to new reservations",
        alias="isActive"
    )


class Reservation(BaseModel):
    """Reservation schema for managing bookings.

    Complete reservation record for tables, rooms, rentals, or other bookable resources.

    Attributes:
        reservation_type: Type of reservation
        resource_id: ID of the reserved resource (table, room, etc.)
        customer_id: Customer ID if registered
        customer_name: Customer's full name
        customer_email: Customer's email address
        start_time: Reservation start time as Unix timestamp
        end_time: Reservation end time as Unix timestamp
        duration: Duration based on resource type
        persons_number: Number of people for the reservation
        total_price: Total price for the reservation
        deposit_paid: Deposit amount paid
        status: Current reservation status
        notes: Special requests or notes
        cancel_reason: Reason for cancellation, if applicable
        is_resource_reservation: Indicates if this reservation is for a specific resource
        service_conversation_config_id: Configuration ID for service conversation

    Example:
        ```python
        reservation = Reservation(
            id="res_123",
            reservation_type=ResourceType.TABLE,
            resource_id="table_5",
            customer_id="cust_123",
            customer_name="John Doe",
            customer_email="john@example.com",
            start_time=1234567890,
            duration=2,
            persons_number=4,
            total_price=0.0,
            deposit_paid=0.0,
            status=AppointmentStatus.CONFIRMED,
            is_resource_reservation=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    reservation_type: ResourceType = Field(
        ...,
        description="Category of reservation: ROOM, TABLE, RENTAL, or OTHER",
        alias="reservationType"
    )
    resource_id: Optional[str] = Field(
        None,
        description="References specific Resource from reservation-resource being reserved",
        alias="resourceId"
    )
    customer_id: str = Field(
        ...,
        description="References Customer who made this reservation",
        alias="customerId"
    )
    customer_name: Optional[str] = Field(
        None,
        description="Customer's full name captured at reservation time",
        alias="customerName"
    )
    customer_email: Optional[EmailStr] = Field(
        None,
        description="Customer's email for confirmation messages and updates",
        alias="customerEmail"
    )
    start_time: int = Field(
        ...,
        description="Unix timestamp for reservation start",
        alias="startTime"
    )
    end_time: Optional[int] = Field(
        None,
        description="Unix timestamp for reservation end",
        alias="endTime"
    )
    duration: Optional[float] = Field(
        None,
        ge=0,
        description="Reservation length in units matching reservationType"
    )
    persons_number: Optional[int] = Field(
        None,
        ge=0,
        description="Party size or occupancy count",
        alias="personsNumber"
    )
    total_price: Optional[float] = Field(
        None,
        ge=0,
        description="Total reservation cost in account's currency",
        alias="totalPrice"
    )
    deposit_paid: float = Field(
        0.0,
        ge=0,
        description="Deposit amount already paid to secure reservation",
        alias="depositPaid"
    )
    status: AppointmentStatus = Field(
        AppointmentStatus.PENDING,
        description="Current reservation status tracking from booking through check-in to completion"
    )
    notes: Optional[str] = Field(
        None,
        description="Customer's special requests or preferences"
    )
    cancel_reason: Optional[str] = Field(
        None,
        description="Reason provided when reservation is cancelled",
        alias="cancelReason"
    )
    is_resource_reservation: bool = Field(
        False,
        description="Whether this is a specific resource reservation or general availability booking",
        alias="isResourceReservation"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        description="References the AI Powered Services conversation configuration",
        alias="serviceConversationConfigId"
    )


class CreateReservationSettings(BaseModel):
    """Schema for creating new reservation settings.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateReservationSettings(
            reservation_type=ResourceType.ROOM,
            setting_type=ReservationSettingType.RESOURCE_SPECIFIC,
            default_reservation_duration=1,
            default_reservation_duration_unit=ResourceReservationDurationUnit.NIGHTS,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    reservation_type: ResourceType = Field(..., alias="reservationType")
    setting_type: ReservationSettingType = Field(..., alias="settingType")
    default_reservation_duration: Optional[int] = Field(1, gt=0, alias="defaultReservationDuration")
    default_reservation_duration_unit: Optional[ResourceReservationDurationUnit] = Field(
        ResourceReservationDurationUnit.HOURS,
        alias="defaultReservationDurationUnit"
    )
    is_active: bool = Field(False, alias="isActive")


class UpdateReservationSettings(BaseModel):
    """Schema for updating existing reservation settings.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateReservationSettings(
            id="settings_123",
            is_active=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    reservation_type: Optional[ResourceType] = Field(None, alias="reservationType")
    setting_type: Optional[ReservationSettingType] = Field(None, alias="settingType")
    default_reservation_duration: Optional[int] = Field(None, gt=0, alias="defaultReservationDuration")
    default_reservation_duration_unit: Optional[ResourceReservationDurationUnit] = Field(
        None,
        alias="defaultReservationDurationUnit"
    )
    is_active: Optional[bool] = Field(None, alias="isActive")


class CreateReservation(BaseModel):
    """Schema for creating a new reservation.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateReservation(
            reservation_type=ResourceType.TABLE,
            resource_id="table_10",
            customer_id="cust_456",
            customer_name="Jane Smith",
            customer_email="jane@example.com",
            start_time=1234567890,
            duration=1.5,
            persons_number=2,
            status=AppointmentStatus.PENDING,
            is_resource_reservation=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    reservation_type: ResourceType = Field(..., alias="reservationType")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    customer_id: str = Field(..., alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[EmailStr] = Field(None, alias="customerEmail")
    start_time: int = Field(..., alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[float] = Field(None, ge=0)
    persons_number: Optional[int] = Field(None, ge=0, alias="personsNumber")
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    deposit_paid: float = Field(0.0, ge=0, alias="depositPaid")
    status: AppointmentStatus = AppointmentStatus.PENDING
    notes: Optional[str] = None
    is_resource_reservation: bool = Field(False, alias="isResourceReservation")
    service_conversation_config_id: Optional[str] = Field(None, alias="serviceConversationConfigId")


class UpdateReservation(BaseModel):
    """Schema for updating an existing reservation.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateReservation(
            id="res_123",
            status=AppointmentStatus.CONFIRMED,
            notes="Window table requested"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    reservation_type: Optional[ResourceType] = Field(None, alias="reservationType")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[EmailStr] = Field(None, alias="customerEmail")
    start_time: Optional[int] = Field(None, alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[float] = Field(None, ge=0)
    persons_number: Optional[int] = Field(None, ge=0, alias="personsNumber")
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    deposit_paid: Optional[float] = Field(None, ge=0, alias="depositPaid")
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    is_resource_reservation: Optional[bool] = Field(None, alias="isResourceReservation")
    service_conversation_config_id: Optional[str] = Field(None, alias="serviceConversationConfigId")
