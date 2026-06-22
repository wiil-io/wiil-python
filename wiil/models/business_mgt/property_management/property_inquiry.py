"""Property inquiry schemas for property management.

This module mirrors
type-ref/business-mgt/property-management/property-inquiry.schema.ts.
"""

from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.customer_management import Customer
from wiil.models.type_definitions.business_definitions import (
    PropertyInquiryStatus,
    PropertyInquiryType,
)


class PropertyInquiry(EntityModel):
    """Tracks customer inquiries about properties."""

    property_id: str = Field(..., alias="propertyId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    customer: Optional[Customer] = None
    inquiry_type: PropertyInquiryType = Field(..., alias="inquiryType")
    message: Optional[str] = None
    source: str = "direct"
    status: PropertyInquiryStatus = PropertyInquiryStatus.NEW
    preferred_viewing_date: Optional[int] = Field(
        None,
        alias="preferredViewingDate"
    )
    preferred_viewing_time: Optional[str] = Field(
        None,
        alias="preferredViewingTime"
    )
    scheduled_viewing_date: Optional[int] = Field(
        None,
        alias="scheduledViewingDate"
    )
    viewing_completed: bool = Field(False, alias="viewingCompleted")
    viewing_notes: Optional[str] = Field(None, alias="viewingNotes")
    follow_up_date: Optional[int] = Field(None, alias="followUpDate")
    follow_up_notes: Optional[str] = Field(None, alias="followUpNotes")
    assigned_agent_id: Optional[str] = Field(None, alias="assignedAgentId")
    converted_to_transaction: bool = Field(
        False,
        alias="convertedToTransaction"
    )
    transaction_id: Optional[str] = Field(None, alias="transactionId")
    transaction_type: Optional[Literal["purchase", "lease"]] = Field(
        None,
        alias="transactionType"
    )
    interested_in_buying: bool = Field(False, alias="interestedInBuying")
    interested_in_renting: bool = Field(False, alias="interestedInRenting")
    budget_min: Optional[float] = Field(None, ge=0, alias="budgetMin")
    budget_max: Optional[float] = Field(None, ge=0, alias="budgetMax")
    notes: Optional[str] = None
    appointment_record_id: Optional[str] = Field(
        None,
        alias="appointmentRecordId"
    )
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId"
    )


class CreatePropertyInquiry(BaseModel):
    """Schema for creating a property inquiry."""

    property_id: str = Field(..., alias="propertyId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    inquiry_type: PropertyInquiryType = Field(..., alias="inquiryType")
    message: Optional[str] = None
    source: str = "direct"
    status: PropertyInquiryStatus = PropertyInquiryStatus.NEW
    preferred_viewing_date: Optional[int] = Field(
        None,
        alias="preferredViewingDate"
    )
    preferred_viewing_time: Optional[str] = Field(
        None,
        alias="preferredViewingTime"
    )
    scheduled_viewing_date: Optional[int] = Field(
        None,
        alias="scheduledViewingDate"
    )
    viewing_completed: bool = Field(False, alias="viewingCompleted")
    viewing_notes: Optional[str] = Field(None, alias="viewingNotes")
    follow_up_date: Optional[int] = Field(None, alias="followUpDate")
    follow_up_notes: Optional[str] = Field(None, alias="followUpNotes")
    assigned_agent_id: Optional[str] = Field(None, alias="assignedAgentId")
    converted_to_transaction: bool = Field(
        False,
        alias="convertedToTransaction"
    )
    transaction_id: Optional[str] = Field(None, alias="transactionId")
    transaction_type: Optional[Literal["purchase", "lease"]] = Field(
        None,
        alias="transactionType"
    )
    interested_in_buying: bool = Field(False, alias="interestedInBuying")
    interested_in_renting: bool = Field(False, alias="interestedInRenting")
    budget_min: Optional[float] = Field(None, ge=0, alias="budgetMin")
    budget_max: Optional[float] = Field(None, ge=0, alias="budgetMax")
    notes: Optional[str] = None
    appointment_record_id: Optional[str] = Field(
        None,
        alias="appointmentRecordId"
    )
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId"
    )


class UpdatePropertyInquiry(BaseModel):
    """Schema for updating a property inquiry."""

    id: str
    property_id: Optional[str] = Field(None, alias="propertyId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    inquiry_type: Optional[PropertyInquiryType] = Field(
        None,
        alias="inquiryType"
    )
    message: Optional[str] = None
    source: Optional[str] = None
    status: Optional[PropertyInquiryStatus] = None
    preferred_viewing_date: Optional[int] = Field(
        None,
        alias="preferredViewingDate"
    )
    preferred_viewing_time: Optional[str] = Field(
        None,
        alias="preferredViewingTime"
    )
    scheduled_viewing_date: Optional[int] = Field(
        None,
        alias="scheduledViewingDate"
    )
    viewing_completed: Optional[bool] = Field(None, alias="viewingCompleted")
    viewing_notes: Optional[str] = Field(None, alias="viewingNotes")
    follow_up_date: Optional[int] = Field(None, alias="followUpDate")
    follow_up_notes: Optional[str] = Field(None, alias="followUpNotes")
    assigned_agent_id: Optional[str] = Field(None, alias="assignedAgentId")
    converted_to_transaction: Optional[bool] = Field(
        None,
        alias="convertedToTransaction"
    )
    transaction_id: Optional[str] = Field(None, alias="transactionId")
    transaction_type: Optional[Literal["purchase", "lease"]] = Field(
        None,
        alias="transactionType"
    )
    interested_in_buying: Optional[bool] = Field(
        None,
        alias="interestedInBuying"
    )
    interested_in_renting: Optional[bool] = Field(
        None,
        alias="interestedInRenting"
    )
    budget_min: Optional[float] = Field(None, ge=0, alias="budgetMin")
    budget_max: Optional[float] = Field(None, ge=0, alias="budgetMax")
    notes: Optional[str] = None
    appointment_record_id: Optional[str] = Field(
        None,
        alias="appointmentRecordId"
    )
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId"
    )


class UpdatePropertyInquiryStatus(BaseModel):
    """Schema for quick status updates on an inquiry."""

    id: str
    status: PropertyInquiryStatus
    scheduled_viewing_date: Optional[int] = Field(
        None,
        alias="scheduledViewingDate"
    )
    viewing_completed: Optional[bool] = Field(None, alias="viewingCompleted")
    viewing_notes: Optional[str] = Field(None, alias="viewingNotes")
    follow_up_date: Optional[int] = Field(None, alias="followUpDate")
    follow_up_notes: Optional[str] = Field(None, alias="followUpNotes")


class DateRangeFilter(TypedDict, total=False):
    """Date-range filter with optional start/end timestamps."""

    start: Optional[int]
    end: Optional[int]


class PropertyInquiryFilters(TypedDict, total=False):
    """Filter options for property inquiry queries."""

    search: Optional[str]
    propertyId: Optional[str]
    customerId: Optional[str]
    status: Optional[list[PropertyInquiryStatus]]
    inquiryType: Optional[PropertyInquiryType]
    assignedAgentId: Optional[str]
    source: Optional[str]
    convertedToTransaction: Optional[bool]
    interestedInBuying: Optional[bool]
    interestedInRenting: Optional[bool]
    viewingCompleted: Optional[bool]
    dateRange: Optional[DateRangeFilter]
    followUpDateRange: Optional[DateRangeFilter]


class PropertyInquirySorting(TypedDict):
    """Sorting options for property inquiry queries."""

    field: Literal[
        "createdAt",
        "scheduledViewingDate",
        "followUpDate",
        "status",
    ]
    direction: Literal["asc", "desc"]


class PropertyInquiryQueryOptions(TypedDict):
    """Query options for property inquiry retrieval."""

    page: int
    pageSize: int
    filters: Optional[PropertyInquiryFilters]
    sorting: Optional[PropertyInquirySorting]
