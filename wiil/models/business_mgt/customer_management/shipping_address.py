"""Shipping address schema definitions for customer management."""

import re
from typing import Literal, Optional, TypedDict

from pydantic import Field, field_validator

from wiil.models.base import BaseModel, EntityModel

_PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{1,14}$")


class ShippingAddress(EntityModel):
    """Customer shipping address record with delivery details."""

    customer_id: str = Field(..., alias="customerId")
    street: str = Field(..., min_length=2)
    street2: Optional[str] = None
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    postal_code: str = Field(..., min_length=2, alias="postalCode")
    country: str = Field(..., min_length=2)
    recipient_name: Optional[str] = Field(None, alias="recipientName")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    instructions: Optional[str] = None
    is_primary: bool = Field(False, alias="isPrimary")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone_number(cls, value: Optional[str]) -> Optional[str]:
        """Normalize phone numbers to E.164 with leading +."""
        if value is None:
            return value
        if not _PHONE_PATTERN.fullmatch(value):
            raise ValueError("Invalid phone number format")
        return value if value.startswith("+") else f"+{value}"


class CreateShippingAddress(BaseModel):
    """Schema for creating a new shipping address."""

    customer_id: str = Field(..., alias="customerId")
    street: str = Field(..., min_length=2)
    street2: Optional[str] = None
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    postal_code: str = Field(..., min_length=2, alias="postalCode")
    country: str = Field(..., min_length=2)
    recipient_name: Optional[str] = Field(None, alias="recipientName")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    instructions: Optional[str] = None
    is_primary: bool = Field(False, alias="isPrimary")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone_number(cls, value: Optional[str]) -> Optional[str]:
        """Normalize phone numbers to E.164 with leading +."""
        if value is None:
            return value
        if not _PHONE_PATTERN.fullmatch(value):
            raise ValueError("Invalid phone number format")
        return value if value.startswith("+") else f"+{value}"


class UpdateShippingAddress(BaseModel):
    """Schema for updating an existing shipping address."""

    id: str
    customer_id: Optional[str] = Field(None, alias="customerId")
    street: Optional[str] = Field(None, min_length=2)
    street2: Optional[str] = None
    city: Optional[str] = Field(None, min_length=2)
    state: Optional[str] = Field(None, min_length=2)
    postal_code: Optional[str] = Field(None, min_length=2, alias="postalCode")
    country: Optional[str] = Field(None, min_length=2)
    recipient_name: Optional[str] = Field(None, alias="recipientName")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    instructions: Optional[str] = None
    is_primary: Optional[bool] = Field(None, alias="isPrimary")

    @field_validator("phone_number")
    @classmethod
    def normalize_phone_number(cls, value: Optional[str]) -> Optional[str]:
        """Normalize phone numbers to E.164 with leading +."""
        if value is None:
            return value
        if not _PHONE_PATTERN.fullmatch(value):
            raise ValueError("Invalid phone number format")
        return value if value.startswith("+") else f"+{value}"


class ShippingAddressFilters(TypedDict, total=False):
    """Filters for querying shipping addresses."""

    customer_id: Optional[str]
    is_primary: Optional[bool]
    country: Optional[str]
    city: Optional[str]
    state: Optional[str]


class ShippingAddressSorting(TypedDict):
    """Sorting options for shipping address queries."""

    field: Literal["created_at", "is_primary", "country", "city"]
    direction: Literal["asc", "desc"]


class ShippingAddressQueryOptions(TypedDict, total=False):
    """Query options for shipping address retrieval."""

    page: int
    page_size: int
    filters: Optional[ShippingAddressFilters]
    sorting: Optional[ShippingAddressSorting]
