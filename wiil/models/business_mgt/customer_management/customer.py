"""Customer schema definitions for business management."""

import re
from typing import Any, Dict, List, Literal, Optional, TypedDict

from pydantic import EmailStr, Field, field_validator

from wiil.models.base import Address, BaseModel, EntityModel
from wiil.types.business_types import BestTimeToCall, PreferredContactMethod

_PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{1,14}$")


class Customer(EntityModel):
    """Customer record with contact details and preferences."""

    customer_id: Optional[str] = Field(None, alias="customerId")
    phone_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    company: Optional[str] = None
    timezone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_language: str = "en"
    preferred_contact_method: PreferredContactMethod = Field(
        PreferredContactMethod.EMAIL,
    )
    best_time_to_call: Optional[BestTimeToCall] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    channel_id: Optional[str] = Field(None, alias="channelId")
    address: Optional[Address] = None
    is_validated_names: bool = Field(False, alias="isValidatedNames")
    customer_group_id: Optional[str] = Field(None, alias="customerGroupId")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone_number(cls, value: Optional[str]) -> Optional[str]:
        """Normalize phone numbers to E.164 with leading +."""
        if value is None:
            return value
        if not _PHONE_PATTERN.fullmatch(value):
            raise ValueError("Invalid phone number format")
        return value if value.startswith("+") else f"+{value}"


class CreateCustomer(BaseModel):
    """Schema for creating a new customer."""

    customer_id: Optional[str] = Field(None, alias="customerId")
    phone_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    company: Optional[str] = None
    timezone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_language: str = "en"
    preferred_contact_method: PreferredContactMethod = Field(
        PreferredContactMethod.EMAIL,
    )
    best_time_to_call: Optional[BestTimeToCall] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    address: Optional[Address] = None
    is_validated_names: bool = Field(False, alias="isValidatedNames")
    customer_group_id: Optional[str] = Field(None, alias="customerGroupId")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone_number(cls, value: Optional[str]) -> Optional[str]:
        """Normalize phone numbers to E.164 with leading +."""
        if value is None:
            return value
        if not _PHONE_PATTERN.fullmatch(value):
            raise ValueError("Invalid phone number format")
        return value if value.startswith("+") else f"+{value}"


class UpdateCustomer(BaseModel):
    """Schema for updating an existing customer."""

    id: str
    customer_id: Optional[str] = Field(None, alias="customerId")
    phone_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    company: Optional[str] = None
    timezone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_language: Optional[str] = None
    preferred_contact_method: Optional[PreferredContactMethod] = None
    best_time_to_call: Optional[BestTimeToCall] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    address: Optional[Address] = None
    is_validated_names: Optional[bool] = Field(None, alias="isValidatedNames")
    customer_group_id: Optional[str] = Field(None, alias="customerGroupId")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone_number(cls, value: Optional[str]) -> Optional[str]:
        """Normalize phone numbers to E.164 with leading +."""
        if value is None:
            return value
        if not _PHONE_PATTERN.fullmatch(value):
            raise ValueError("Invalid phone number format")
        return value if value.startswith("+") else f"+{value}"


class CustomerFilters(TypedDict, total=False):
    """Filters for querying customers."""

    search: Optional[str]
    preferred_contact_method: Optional[List[PreferredContactMethod]]
    tags: Optional[List[str]]
    channel_id: Optional[str]
    customer_group_id: Optional[str]


class CustomerSorting(TypedDict):
    """Sorting options for customer queries."""

    field: Literal["firstname", "lastname", "created_at"]
    direction: Literal["asc", "desc"]


class CustomerQueryOptions(TypedDict, total=False):
    """Query options for customer retrieval."""

    page: int
    page_size: int
    filters: Optional[CustomerFilters]
    sorting: Optional[CustomerSorting]
