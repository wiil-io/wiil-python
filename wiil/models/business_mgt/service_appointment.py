"""Service appointment schema definitions for managing appointment bookings.

This module contains Pydantic models for managing service appointments with
calendar integration and service provider assignment.
"""

from typing import Optional

from pydantic import ConfigDict, EmailStr, Field

from wiil.models.base import BaseModel
from wiil.types.business_types import AppointmentStatus, CalendarProvider


class ServiceAppointment(BaseModel):
    """Service appointment schema.

    Complete service appointment record with customer information, timing, pricing,
    and calendar integration.

    Attributes:
        business_service_id: ID of the service being booked
        customer_id: Customer ID if registered
        customer_name: Customer's full name
        customer_email: Customer's email address
        start_time: Appointment start time as Unix timestamp
        end_time: Appointment end time as Unix timestamp
        duration: Duration in minutes
        total_price: Total price for the service
        deposit_paid: Deposit amount paid
        status: Current appointment status
        assigned_user_account_id: User account managing the appointment
        calendar_id: Calendar ID where appointment is stored
        calendar_event_id: External calendar event ID
        calendar_provider: Calendar provider type
        cancel_reason: Reason for cancellation, if applicable
        service_conversation_config_id: Configuration ID for service conversation

    Example:
        ```python
        appointment = ServiceAppointment(
            id="appt_123",
            business_service_id="service_456",
            customer_id="cust_789",
            customer_name="John Doe",
            customer_email="john@example.com",
            start_time=1234567890,
            duration=60,
            total_price=100.00,
            deposit_paid=25.00,
            status=AppointmentStatus.CONFIRMED,
            assigned_user_account_id="user_999"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    business_service_id: str = Field(
        ...,
        description="References Business Service from service-config being booked",
        alias="businessServiceId"
    )
    customer_id: str = Field(
        ...,
        description="References Customer who booked this appointment",
        alias="customerId"
    )
    customer_name: Optional[str] = Field(
        None,
        description="Customer's full name captured at booking time",
        alias="customerName"
    )
    customer_email: Optional[EmailStr] = Field(
        None,
        description="Customer's email for confirmation and reminder messages",
        alias="customerEmail"
    )
    start_time: int = Field(
        ...,
        description="Unix timestamp for appointment start",
        alias="startTime"
    )
    end_time: Optional[int] = Field(
        None,
        description="Unix timestamp for appointment end",
        alias="endTime"
    )
    duration: Optional[int] = Field(
        30,
        gt=0,
        description="Appointment length in minutes"
    )
    total_price: Optional[float] = Field(
        0.0,
        ge=0,
        description="Total service cost in account's currency",
        alias="totalPrice"
    )
    deposit_paid: float = Field(
        0.0,
        ge=0,
        description="Deposit amount already paid to secure appointment",
        alias="depositPaid"
    )
    status: AppointmentStatus = Field(
        AppointmentStatus.PENDING,
        description="Current appointment status tracking from booking through completion"
    )
    assigned_user_account_id: Optional[str] = Field(
        None,
        description="References Service Person assigned to perform this service",
        alias="assignedUserAccountId"
    )
    calendar_id: Optional[str] = Field(
        None,
        description="External calendar system ID where this appointment is synced",
        alias="calendarId"
    )
    calendar_event_id: Optional[str] = Field(
        None,
        description="Event ID in external calendar system",
        alias="calendarEventId"
    )
    calendar_provider: Optional[CalendarProvider] = Field(
        None,
        description="Calendar system type (GOOGLE, OUTLOOK, CALENDLY, etc.)",
        alias="calendarProvider"
    )
    cancel_reason: Optional[str] = Field(
        None,
        description="Reason provided when appointment is cancelled",
        alias="cancelReason"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        description="References the AI Powered Services conversation configuration",
        alias="serviceConversationConfigId"
    )


class CreateServiceAppointment(BaseModel):
    """Schema for creating a new service appointment.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateServiceAppointment(
            business_service_id="service_123",
            customer_id="cust_456",
            customer_name="Jane Smith",
            customer_email="jane@example.com",
            start_time=1234567890,
            duration=45,
            total_price=75.00,
            status=AppointmentStatus.PENDING
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    business_service_id: str = Field(..., alias="businessServiceId")
    customer_id: str = Field(..., alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[EmailStr] = Field(None, alias="customerEmail")
    start_time: int = Field(..., alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[int] = Field(30, gt=0)
    total_price: Optional[float] = Field(0.0, ge=0, alias="totalPrice")
    deposit_paid: float = Field(0.0, ge=0, alias="depositPaid")
    status: AppointmentStatus = AppointmentStatus.PENDING
    assigned_user_account_id: Optional[str] = Field(None, alias="assignedUserAccountId")
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(None, alias="calendarProvider")
    service_conversation_config_id: Optional[str] = Field(None, alias="serviceConversationConfigId")


class UpdateServiceAppointment(BaseModel):
    """Schema for updating an existing service appointment.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateServiceAppointment(
            id="appt_123",
            status=AppointmentStatus.COMPLETED,
            end_time=1234567950
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    business_service_id: Optional[str] = Field(None, alias="businessServiceId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[EmailStr] = Field(None, alias="customerEmail")
    start_time: Optional[int] = Field(None, alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[int] = Field(None, gt=0)
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    deposit_paid: Optional[float] = Field(None, ge=0, alias="depositPaid")
    status: Optional[AppointmentStatus] = None
    assigned_user_account_id: Optional[str] = Field(None, alias="assignedUserAccountId")
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(None, alias="calendarProvider")
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(None, alias="serviceConversationConfigId")
