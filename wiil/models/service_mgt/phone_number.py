"""Phone number configuration and purchase schema definitions.

Phone number schemas manage the complete lifecycle of phone number acquisition from telephony providers:
discovery of available inventory, purchase transactions, and provisioning into Phone Configurations.
Supports multiple providers (SignalWire, Twilio) with provider-specific extensions.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions import PhoneNumberType, PhonePurchaseStatus


class PhoneCapabilities(BaseModel):
    """Phone number capabilities."""

    voice: bool = Field(
        ...,
        description="Whether this phone number supports voice calls"
    )
    sms: bool = Field(
        ...,
        description="Whether this phone number supports SMS text messaging",
        alias="SMS"
    )
    mms: bool = Field(
        ...,
        description="Whether this phone number supports MMS multimedia messaging",
        alias="MMS"
    )


class BasePhoneNumberInfo(BaseModel):
    """Base phone number information.

    Common properties shared across all phone number providers.

    Attributes:
        friendly_name: Human-readable name for the phone number
        phone_number: The phone number in E.164 format
        lata: Local Access and Transport Area code
        rate_center: Rate center for the phone number
        region: Geographic region
        postal_code: Postal/ZIP code for the phone number
        country_code: ISO country code
        capabilities: Phone number capabilities
        beta: Whether this is a beta number
        number_type: Type of phone number (local, toll-free, etc.)
    """

    friendly_name: str = Field(
        ...,
        description="Human-readable display name for this phone number",
        alias="friendlyName"
    )
    phone_number: str = Field(
        ...,
        description="Phone number in E.164 international format",
        alias="phoneNumber"
    )
    lata: Optional[str] = Field(
        None,
        description="Local Access and Transport Area (LATA) code for North American numbers"
    )
    rate_center: Optional[str] = Field(
        None,
        description="Rate center name for billing and routing purposes",
        alias="rateCenter"
    )
    region: Optional[str] = Field(
        None,
        description="State or province code where the number is registered"
    )
    postal_code: Optional[str] = Field(
        None,
        description="Postal or ZIP code associated with this phone number",
        alias="postalCode"
    )
    country_code: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code for this phone number",
        alias="countryCode"
    )
    capabilities: PhoneCapabilities = Field(
        ...,
        description="Capabilities supported by this phone number"
    )
    beta: bool = Field(
        ...,
        description="Whether this is a beta phone number (experimental or limited availability)"
    )
    number_type: PhoneNumberType = Field(
        ...,
        description="Type of phone number (LOCAL, TOLL_FREE, MOBILE, etc.)",
        alias="numberType"
    )


class PhoneProviderResponse(BaseModel):
    """Response from phone number provider API calls."""

    success: bool
    status: Optional[int] = None
    data: Any = None


class PhoneNumberPurchase(EntityModel):
    """Phone number purchase transaction.

    Represents a phone number purchase request and its lifecycle through the purchase process.

    Attributes:
        friendly_name: Human-readable name for the purchased number
        phone_number: The phone number being purchased
        country_code: ISO country code for the phone number
        charged_credits: Amount charged for the phone number purchase
        status: Current status of the purchase
        number_type: Type of phone number
        status_details: Additional details about the current status
        completed_at: Timestamp when purchase was completed
        metadata: Additional metadata for the purchase
    """

    friendly_name: str = Field(
        ...,
        description="Human-readable name for the phone number being purchased",
        alias="friendlyName"
    )
    phone_number: str = Field(
        ...,
        description="Phone number in E.164 international format being purchased",
        alias="phoneNumber"
    )
    country_code: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="ISO 3166-1 alpha-2 country code for the phone number",
        alias="countryCode"
    )
    charged_credits: float = Field(
        ...,
        gt=0,
        description="Amount charged for the phone number purchase",
        alias="chargedCredits"
    )
    status: PhonePurchaseStatus = Field(
        PhonePurchaseStatus.PENDING,
        description="Current status of the purchase transaction"
    )
    number_type: PhoneNumberType = Field(
        PhoneNumberType.LOCAL,
        description="Type of phone number being purchased",
        alias="numberType"
    )
    status_details: Optional[str] = Field(
        None,
        description="Additional details about the current status",
        alias="statusDetails"
    )
    completed_at: Optional[int] = Field(
        None,
        description="Unix timestamp when the purchase was successfully completed",
        alias="completedAt"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata for the purchase"
    )


class CreatePhoneNumberPurchase(BaseModel):
    """Schema for creating a new phone number purchase.

    Omits auto-generated and transaction-specific fields.
    """

    friendly_name: str = Field(..., alias="friendlyName")
    phone_number: str = Field(..., alias="phoneNumber")
    country_code: str = Field(..., min_length=2, max_length=2, alias="countryCode")
    number_type: PhoneNumberType = Field(PhoneNumberType.LOCAL, alias="numberType")


class BusinessPhoneNumberPurchaseRequest(BaseModel):
    """Schema for business phone number purchase request."""

    phone_number: str = Field(
        ...,
        description="Phone number in international format to be purchased",
        alias="phoneNumber"
    )
    friendly_name: Optional[str] = Field(
        None,
        description="Human-readable display name for the phone number being purchased",
        alias="friendlyName"
    )


# Legacy type aliases
PhoneNumberPurchaseRequest = CreatePhoneNumberPurchase


class PhoneNumberPrice(BaseModel):
    """Phone number price tier."""

    base_price: str = Field(..., alias="base_price")
    current_price: str = Field(..., alias="current_price")


class PhoneNumberPricing(BaseModel):
    """Phone number pricing information.

    Represents pricing details for phone numbers from various providers.

    Attributes:
        number_type: Type of phone number
        country: Full country name
        country_code: ISO country code
        phone_number_prices: Array of pricing tiers
        price: Final price for the number
        price_unit: Unit of pricing (e.g., "per month")
        currency: Currency code (3 characters, default: "USD")
    """

    number_type: PhoneNumberType = Field(..., alias="number_type")
    country: str
    country_code: str = Field(..., alias="countryCode")
    phone_number_prices: List[PhoneNumberPrice] = Field(..., alias="phoneNumberPrices")
    price: float
    price_unit: str = Field(..., alias="priceUnit")
    currency: str = Field("USD", min_length=3, max_length=3)
