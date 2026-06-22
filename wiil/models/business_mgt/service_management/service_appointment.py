"""Service appointment schema and query definitions."""

from typing import Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.order import OrderPricing
from wiil.models.type_definitions.business_definitions import (
    AppointmentStatus,
    CalendarProvider,
    ExternalRef,
)


class ServiceAppointment(EntityModel):
    """Service appointment entity."""

    business_service_id: str = Field(..., alias="businessServiceId")
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    customer_id: str = Field(..., alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    start_time: int = Field(..., gt=0, alias="startTime")
    end_time: Optional[int] = Field(None, gt=0, alias="endTime")
    duration: int = Field(30, gt=0)
    total_price: float = Field(0, ge=0, alias="totalPrice")
    pricing: Optional[OrderPricing] = None
    deposit_paid: float = Field(0, ge=0, alias="depositPaid")
    status: AppointmentStatus = AppointmentStatus.PENDING
    provider_id: Optional[str] = Field(None, alias="providerId")
    service_provider_id: Optional[str] = Field(None, alias="serviceProviderId")
    slot_index: Optional[int] = Field(None, ge=0, alias="slotIndex")
    assigned_user_account_id: Optional[str] = Field(
        None,
        alias="assignedUserAccountId",
    )
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(
        None,
        alias="calendarProvider",
    )
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
    )
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class CreateServiceAppointment(BaseModel):
    """Schema for creating a service appointment.

    Omits auto-generated fields (id) and cancelReason (set during
    cancellation).
    """

    business_service_id: str = Field(..., alias="businessServiceId")
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    customer_id: str = Field(..., alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    start_time: int = Field(..., gt=0, alias="startTime")
    end_time: Optional[int] = Field(None, gt=0, alias="endTime")
    duration: int = Field(30, gt=0)
    total_price: float = Field(0, ge=0, alias="totalPrice")
    pricing: Optional[OrderPricing] = None
    deposit_paid: float = Field(0, ge=0, alias="depositPaid")
    status: AppointmentStatus = AppointmentStatus.PENDING
    provider_id: Optional[str] = Field(None, alias="providerId")
    service_provider_id: Optional[str] = Field(None, alias="serviceProviderId")
    slot_index: Optional[int] = Field(None, ge=0, alias="slotIndex")
    assigned_user_account_id: Optional[str] = Field(
        None,
        alias="assignedUserAccountId",
    )
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(
        None,
        alias="calendarProvider",
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
    )
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class UpdateServiceAppointment(BaseModel):
    """Schema for updating a service appointment.

    All fields optional except id (required). Includes cancelReason for
    cancellation updates.
    """

    id: str
    business_service_id: Optional[str] = Field(None, alias="businessServiceId")
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    customer_name: Optional[str] = Field(None, alias="customerName")
    customer_email: Optional[str] = Field(None, alias="customerEmail")
    start_time: Optional[int] = Field(None, gt=0, alias="startTime")
    end_time: Optional[int] = Field(None, gt=0, alias="endTime")
    duration: Optional[int] = Field(None, gt=0)
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    pricing: Optional[OrderPricing] = None
    deposit_paid: Optional[float] = Field(None, ge=0, alias="depositPaid")
    status: Optional[AppointmentStatus] = None
    provider_id: Optional[str] = Field(None, alias="providerId")
    service_provider_id: Optional[str] = Field(None, alias="serviceProviderId")
    slot_index: Optional[int] = Field(None, ge=0, alias="slotIndex")
    assigned_user_account_id: Optional[str] = Field(
        None,
        alias="assignedUserAccountId",
    )
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(
        None,
        alias="calendarProvider",
    )
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
    )
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class ServiceAppointmentFilters(TypedDict, total=False):
    """Filter options for service appointment queries."""

    customerId: Optional[str]
    businessServiceId: Optional[str]
    serviceId: Optional[str]
    providerId: Optional[str]
    status: Optional[AppointmentStatus]


class ServiceAppointmentSorting(TypedDict):
    """Sorting options for service appointment queries."""

    field: str
    direction: str


class ServiceAppointmentQueryOptions(TypedDict, total=False):
    """Query options for service appointment retrieval."""

    page: int
    pageSize: int
    filters: Optional[ServiceAppointmentFilters]
    sorting: Optional[ServiceAppointmentSorting]
