"""Property inquiry schema definitions for real estate lead management.

This module mirrors src/core/business-mgt/property-inquiry.schema.ts
"""

from typing import Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.business_mgt.customer import Customer
from wiil.models.type_definitions.business_definitions import (
    CalendarProvider,
    PropertyInquiryStatus,
    PropertyInquiryType,
)


class PropertyInquiry(BaseModel):
    """Property inquiry for tracking customer interest in properties.

    Attributes:
        id: Unique identifier
        property_id: ID of the property being inquired about
        customer_id: ID of existing contact in system
        customer: Contact details of the inquirer (populated)
        inquiry_type: Type of inquiry
        message: Inquiry message from the contact
        source: Source of the inquiry
        status: Current status of the inquiry
        preferred_viewing_date: Contact's preferred viewing date
        preferred_viewing_time: Contact's preferred viewing time
        scheduled_viewing_date: Scheduled viewing date
        viewing_completed: Whether the viewing has been completed
        viewing_notes: Notes from the viewing
        follow_up_date: Next follow-up date
        follow_up_notes: Notes for follow-up
        assigned_agent_id: ID of the assigned agent
        converted_to_transaction: Whether inquiry converted to a transaction
        transaction_id: ID of the resulting transaction
        transaction_type: Type of transaction (purchase or lease)
        interested_in_buying: Whether contact is interested in buying
        interested_in_renting: Whether contact is interested in renting
        budget_min: Minimum budget
        budget_max: Maximum budget
        notes: Internal notes about the inquiry
        assigned_user_account_id: User account managing the appointment
        calendar_id: Calendar ID where appointment is stored
        calendar_event_id: External calendar event ID
        calendar_provider: Calendar provider type
        cancel_reason: Reason for cancellation
        service_conversation_config_id: Configuration ID for service conversation
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        inquiry = PropertyInquiry(
            id="inq-123",
            property_id="prop-456",
            customer_id="cust-789",
            inquiry_type=PropertyInquiryType.GENERAL,
            source="website",
            status=PropertyInquiryStatus.NEW,
            interested_in_buying=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    property_id: str = Field(
        ...,
        description="ID of the property being inquired about",
        alias="propertyId"
    )

    # Contact Information
    customer_id: str = Field(
        ...,
        description="ID of existing contact in system",
        alias="customerId"
    )
    customer: Optional[Customer] = Field(
        None,
        description="Contact details of the inquirer (populated)"
    )

    # Inquiry Details
    inquiry_type: PropertyInquiryType = Field(
        ...,
        description="Type of inquiry",
        alias="inquiryType"
    )
    message: Optional[str] = Field(None, description="Inquiry message from the contact")
    source: str = Field(
        "direct",
        description="Source of the inquiry (website, referral, agent, etc.)"
    )

    # Status
    status: PropertyInquiryStatus = Field(
        PropertyInquiryStatus.NEW,
        description="Current status of the inquiry"
    )

    # Scheduling
    preferred_viewing_date: Optional[int] = Field(
        None,
        description="Contact's preferred viewing date (timestamp)",
        alias="preferredViewingDate"
    )
    preferred_viewing_time: Optional[str] = Field(
        None,
        description="Contact's preferred viewing time",
        alias="preferredViewingTime"
    )
    scheduled_viewing_date: Optional[int] = Field(
        None,
        description="Scheduled viewing date (timestamp)",
        alias="scheduledViewingDate"
    )
    viewing_completed: bool = Field(
        False,
        description="Whether the viewing has been completed",
        alias="viewingCompleted"
    )
    viewing_notes: Optional[str] = Field(
        None,
        description="Notes from the viewing",
        alias="viewingNotes"
    )

    # Follow-up
    follow_up_date: Optional[int] = Field(
        None,
        description="Next follow-up date (timestamp)",
        alias="followUpDate"
    )
    follow_up_notes: Optional[str] = Field(
        None,
        description="Notes for follow-up",
        alias="followUpNotes"
    )
    assigned_agent_id: Optional[str] = Field(
        None,
        description="ID of the assigned agent",
        alias="assignedAgentId"
    )

    # Conversion Tracking
    converted_to_transaction: bool = Field(
        False,
        description="Whether inquiry converted to a transaction",
        alias="convertedToTransaction"
    )
    transaction_id: Optional[str] = Field(
        None,
        description="ID of the resulting transaction",
        alias="transactionId"
    )
    transaction_type: Optional[Literal["purchase", "lease"]] = Field(
        None,
        description="Type of transaction (purchase or lease)",
        alias="transactionType"
    )

    # Interest Details
    interested_in_buying: bool = Field(
        False,
        description="Whether contact is interested in buying",
        alias="interestedInBuying"
    )
    interested_in_renting: bool = Field(
        False,
        description="Whether contact is interested in renting",
        alias="interestedInRenting"
    )
    budget_min: Optional[float] = Field(
        None,
        ge=0,
        description="Minimum budget",
        alias="budgetMin"
    )
    budget_max: Optional[float] = Field(
        None,
        ge=0,
        description="Maximum budget",
        alias="budgetMax"
    )

    # Notes
    notes: Optional[str] = Field(None, description="Internal notes about the inquiry")

    # Calendar Integration
    assigned_user_account_id: Optional[str] = Field(
        None,
        description="User account managing the appointment",
        alias="assignedUserAccountId"
    )
    calendar_id: Optional[str] = Field(
        None,
        description="Calendar ID where appointment is stored",
        alias="calendarId"
    )
    calendar_event_id: Optional[str] = Field(
        None,
        description="External calendar event ID",
        alias="calendarEventId"
    )
    calendar_provider: Optional[CalendarProvider] = Field(
        None,
        description="Calendar provider type",
        alias="calendarProvider"
    )
    cancel_reason: Optional[str] = Field(
        None,
        description="Reason for cancellation, if applicable",
        alias="cancelReason"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        description="Configuration ID for service conversation",
        alias="serviceConversationConfigId"
    )


class CreatePropertyInquiry(PydanticBaseModel):
    """Schema for creating a new property inquiry."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    property_id: str = Field(..., alias="propertyId")
    customer_id: str = Field(..., alias="customerId")
    inquiry_type: PropertyInquiryType = Field(..., alias="inquiryType")
    message: Optional[str] = None
    source: str = "direct"
    status: PropertyInquiryStatus = PropertyInquiryStatus.NEW
    preferred_viewing_date: Optional[int] = Field(None, alias="preferredViewingDate")
    preferred_viewing_time: Optional[str] = Field(None, alias="preferredViewingTime")
    scheduled_viewing_date: Optional[int] = Field(None, alias="scheduledViewingDate")
    viewing_completed: bool = Field(False, alias="viewingCompleted")
    viewing_notes: Optional[str] = Field(None, alias="viewingNotes")
    follow_up_date: Optional[int] = Field(None, alias="followUpDate")
    follow_up_notes: Optional[str] = Field(None, alias="followUpNotes")
    assigned_agent_id: Optional[str] = Field(None, alias="assignedAgentId")
    converted_to_transaction: bool = Field(False, alias="convertedToTransaction")
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
    assigned_user_account_id: Optional[str] = Field(None, alias="assignedUserAccountId")
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(None, alias="calendarProvider")
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId"
    )


class UpdatePropertyInquiry(PydanticBaseModel):
    """Schema for updating a property inquiry."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    property_id: Optional[str] = Field(None, alias="propertyId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    inquiry_type: Optional[PropertyInquiryType] = Field(None, alias="inquiryType")
    message: Optional[str] = None
    source: Optional[str] = None
    status: Optional[PropertyInquiryStatus] = None
    preferred_viewing_date: Optional[int] = Field(None, alias="preferredViewingDate")
    preferred_viewing_time: Optional[str] = Field(None, alias="preferredViewingTime")
    scheduled_viewing_date: Optional[int] = Field(None, alias="scheduledViewingDate")
    viewing_completed: Optional[bool] = Field(None, alias="viewingCompleted")
    viewing_notes: Optional[str] = Field(None, alias="viewingNotes")
    follow_up_date: Optional[int] = Field(None, alias="followUpDate")
    follow_up_notes: Optional[str] = Field(None, alias="followUpNotes")
    assigned_agent_id: Optional[str] = Field(None, alias="assignedAgentId")
    converted_to_transaction: Optional[bool] = Field(None, alias="convertedToTransaction")
    transaction_id: Optional[str] = Field(None, alias="transactionId")
    transaction_type: Optional[Literal["purchase", "lease"]] = Field(
        None,
        alias="transactionType"
    )
    interested_in_buying: Optional[bool] = Field(None, alias="interestedInBuying")
    interested_in_renting: Optional[bool] = Field(None, alias="interestedInRenting")
    budget_min: Optional[float] = Field(None, alias="budgetMin")
    budget_max: Optional[float] = Field(None, alias="budgetMax")
    notes: Optional[str] = None
    assigned_user_account_id: Optional[str] = Field(None, alias="assignedUserAccountId")
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    calendar_event_id: Optional[str] = Field(None, alias="calendarEventId")
    calendar_provider: Optional[CalendarProvider] = Field(None, alias="calendarProvider")
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId"
    )


class UpdatePropertyInquiryStatus(PydanticBaseModel):
    """Quick status update schema for property inquiries.

    Allows updating status and viewing/follow-up details without full update.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Inquiry ID")
    status: PropertyInquiryStatus = Field(..., description="New status")
    scheduled_viewing_date: Optional[int] = Field(
        None,
        description="Scheduled viewing date",
        alias="scheduledViewingDate"
    )
    viewing_completed: Optional[bool] = Field(
        None,
        description="Whether viewing is completed",
        alias="viewingCompleted"
    )
    viewing_notes: Optional[str] = Field(
        None,
        description="Viewing notes",
        alias="viewingNotes"
    )
    follow_up_date: Optional[int] = Field(
        None,
        description="Follow-up date",
        alias="followUpDate"
    )
    follow_up_notes: Optional[str] = Field(
        None,
        description="Follow-up notes",
        alias="followUpNotes"
    )
