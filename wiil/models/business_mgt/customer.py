"""Customer schema definitions for business management.

This module contains Pydantic models for managing customer records, including
contact information, preferences, and custom fields.
"""

from typing import Any, Dict, List, Optional

from pydantic import ConfigDict, EmailStr, Field

from wiil.models.base import Address, BaseModel
from wiil.types.business_types import BestTimeToCall, CallPriority, PreferredContactMethod


class Customer(BaseModel):
    """Customer record for business management.

    Individual customer record with contact details, preferences, and behavioral tracking.
    Used by AI Powered Services for personalized communications and order history.

    Attributes:
        customer_id: External system customer ID for integration purposes
        phone_number: Customer's primary phone number in E.164 format
        firstname: Customer's first name
        lastname: Customer's last name
        company: Company name if customer represents a business
        timezone: Customer's timezone for scheduling purposes
        email: Customer's primary email address
        preferred_language: Customer's preferred language for communication
        call_priority: Priority level for customer calls and support
        preferred_contact_method: Customer's preferred method of contact
        best_time_to_call: Best time of day to contact customer by phone
        notes: Internal notes about the customer
        tags: Labels or categories assigned to the customer
        custom_fields: Additional custom fields for business-specific customer data
        channel_id: Communication channel ID associated with the customer creation
        address: Customer's primary address information
        is_validated_names: Whether the customer's name has been validated for accuracy

    Example:
        ```python
        customer = Customer(
            id="cust_123",
            phone_number="+14155552671",
            firstname="John",
            lastname="Doe",
            email="john.doe@example.com",
            preferred_language="en",
            call_priority=CallPriority.MEDIUM,
            preferred_contact_method=PreferredContactMethod.EMAIL,
            is_validated_names=True,
            address=Address(
                street="123 Main St",
                city="San Francisco",
                state="CA",
                postal_code="94102",
                country="USA"
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    customer_id: Optional[str] = Field(
        None,
        description="External system customer ID for integration with third-party CRM or legacy systems",
        alias="customerId"
    )
    phone_number: Optional[str] = Field(
        None,
        description="Primary phone number in E.164 format (e.g., +14155552671)"
    )
    firstname: Optional[str] = Field(
        None,
        description="Customer's first name for personalized communications"
    )
    lastname: Optional[str] = Field(
        None,
        description="Customer's last name combined with firstname for full identification"
    )
    company: Optional[str] = Field(
        None,
        description="Company name when customer represents a business entity"
    )
    timezone: Optional[str] = Field(
        None,
        description="IANA timezone identifier (e.g., 'America/New_York') for scheduling"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Primary email for confirmations, receipts, and AI-generated summaries"
    )
    preferred_language: str = Field(
        "en",
        description="ISO 639-1 language code (e.g., 'en', 'es', 'fr') for AI conversations"
    )
    call_priority: CallPriority = Field(
        CallPriority.MEDIUM,
        description="Priority level for calls and support: HIGH (VIP/urgent), MEDIUM (standard), LOW (non-urgent)"
    )
    preferred_contact_method: PreferredContactMethod = Field(
        PreferredContactMethod.EMAIL,
        description="Preferred channel for notifications: EMAIL, PHONE, SMS"
    )
    best_time_to_call: Optional[BestTimeToCall] = Field(
        None,
        description="Optimal time window (MORNING, AFTERNOON, EVENING) for phone contact"
    )
    notes: Optional[str] = Field(
        None,
        description="Internal staff notes about customer preferences, requirements, history"
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Categorization labels for segmentation (e.g., ['vip', 'gluten-free'])"
    )
    custom_fields: Optional[Dict[str, Any]] = Field(
        None,
        description="Extensible key-value storage for business-specific attributes"
    )
    channel_id: Optional[str] = Field(
        None,
        description="ID of the communication channel where customer record was created",
        alias="channelId"
    )
    address: Optional[Address] = Field(
        None,
        description="Primary physical address for delivery orders and on-site services"
    )
    is_validated_names: bool = Field(
        False,
        description="Whether first/last names have been verified through ID verification",
        alias="isValidatedNames"
    )


class CreateCustomer(BaseModel):
    """Schema for creating a new customer.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateCustomer(
            phone_number="+14155552671",
            firstname="Jane",
            lastname="Smith",
            email="jane.smith@example.com",
            preferred_language="en",
            call_priority=CallPriority.HIGH,
            preferred_contact_method=PreferredContactMethod.SMS
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    customer_id: Optional[str] = Field(None, alias="customerId")
    phone_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    company: Optional[str] = None
    timezone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_language: str = "en"
    call_priority: CallPriority = CallPriority.MEDIUM
    preferred_contact_method: PreferredContactMethod = PreferredContactMethod.EMAIL
    best_time_to_call: Optional[BestTimeToCall] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    channel_id: Optional[str] = Field(None, alias="channelId")
    address: Optional[Address] = None
    is_validated_names: bool = Field(False, alias="isValidatedNames")


class UpdateCustomer(BaseModel):
    """Schema for updating an existing customer.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateCustomer(
            id="cust_123",
            email="newemail@example.com",
            call_priority=CallPriority.HIGH
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    customer_id: Optional[str] = Field(None, alias="customerId")
    phone_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    company: Optional[str] = None
    timezone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_language: Optional[str] = None
    call_priority: Optional[CallPriority] = None
    preferred_contact_method: Optional[PreferredContactMethod] = None
    best_time_to_call: Optional[BestTimeToCall] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    channel_id: Optional[str] = Field(None, alias="channelId")
    address: Optional[Address] = None
    is_validated_names: Optional[bool] = Field(None, alias="isValidatedNames")
