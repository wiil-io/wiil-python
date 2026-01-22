"""Phone number configuration and purchase schema definitions.

Phone number schemas manage the complete lifecycle of phone number acquisition from
telephony providers: discovery of available inventory, purchase transactions, and
provisioning into Phone Configurations.
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import ConfigDict, Field
from pydantic import BaseModel as PydanticBaseModel

from wiil.models.base import BaseModel
from wiil.types.service_types import PhoneNumberType, PhonePurchaseStatus, ProviderType


class PhoneProviderRegion(PydanticBaseModel):
    """Phone provider region information.

    Represents geographic region information from telephony providers, used for
    filtering and searching available phone numbers by location.

    Attributes:
        region_id: Unique identifier for the region from provider
        region_name: Human-readable region name
        country_code: ISO 3166-1 alpha-2 country code
        country_name: Full country name
        provider_type: Telephony provider offering numbers in this region

    Example:
        ```python
        region = PhoneProviderRegion(
            region_id="us-west",
            region_name="US West",
            country_code="US",
            country_name="United States",
            provider_type=ProviderType.TWILIO
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    region_id: str = Field(
        ...,
        description="Unique identifier for the region (e.g., 'us-west', 'uk-london')",
        alias="regionId"
    )
    region_name: str = Field(
        ...,
        description="Human-readable region name (e.g., 'US West', 'United Kingdom')",
        alias="regionName"
    )
    country_code: Optional[str] = Field(
        None,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')",
        alias="countryCode"
    )
    country_name: Optional[str] = Field(
        None,
        description="Full country name (e.g., 'United States')",
        alias="countryName"
    )
    provider_type: ProviderType = Field(
        ...,
        description="Telephony provider offering numbers in this region",
        alias="providerType"
    )


class PhoneCapabilities(PydanticBaseModel):
    """Phone number capabilities.

    Defines which features are supported by a phone number.

    Attributes:
        voice: Supports voice calls
        sms: Supports SMS messaging
        mms: Supports MMS messaging
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    voice: bool = Field(..., description="Whether this number supports voice calls")
    sms: bool = Field(..., description="Whether this number supports SMS", alias="SMS")
    mms: bool = Field(..., description="Whether this number supports MMS", alias="MMS")


class BasePhoneNumberInfo(PydanticBaseModel):
    """Base phone number information.

    Common properties shared across all phone number providers.

    Attributes:
        friendly_name: Human-readable name for the phone number
        phone_number: Phone number in E.164 format
        lata: Local Access and Transport Area code
        rate_center: Rate center for the phone number
        region: Geographic region
        postal_code: Postal/ZIP code
        country_code: ISO country code
        capabilities: Phone number capabilities
        beta: Whether this is a beta number
        number_type: Type of phone number

    Example:
        ```python
        phone_info = BasePhoneNumberInfo(
            friendly_name="Customer Support Line",
            phone_number="+12125551234",
            country_code="US",
            capabilities=PhoneCapabilities(voice=True, sms=True, mms=False),
            beta=False,
            number_type=PhoneNumberType.LOCAL
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    friendly_name: str = Field(
        ...,
        description="Human-readable display name",
        alias="friendlyName"
    )
    phone_number: str = Field(
        ...,
        description="Phone number in E.164 format (e.g., '+12125551234')",
        alias="phoneNumber"
    )
    lata: Optional[str] = Field(
        None,
        description="Local Access and Transport Area code"
    )
    rate_center: Optional[str] = Field(
        None,
        description="Rate center for billing and routing",
        alias="rateCenter"
    )
    region: Optional[str] = Field(
        None,
        description="State or province code (e.g., 'NY', 'CA')"
    )
    postal_code: Optional[str] = Field(
        None,
        description="Postal or ZIP code",
        alias="postalCode"
    )
    country_code: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')",
        alias="countryCode"
    )
    capabilities: PhoneCapabilities = Field(
        ...,
        description="Capabilities supported by this phone number"
    )
    beta: bool = Field(
        ...,
        description="Whether this is a beta phone number"
    )
    number_type: PhoneNumberType = Field(
        ...,
        description="Type of phone number (LOCAL, TOLL_FREE, etc.)",
        alias="numberType"
    )


class SWPhoneNumberInfo(BasePhoneNumberInfo):
    """SignalWire-specific phone number information.

    Extends base phone number schema with SignalWire-specific fields.

    Attributes:
        latitude: Geographic latitude
        longitude: Geographic longitude
        provider_type: Always SIGNALWIRE

    Example:
        ```python
        sw_phone = SWPhoneNumberInfo(
            friendly_name="SW Support Line",
            phone_number="+12125551234",
            country_code="US",
            capabilities=PhoneCapabilities(voice=True, sms=True, mms=False),
            beta=False,
            number_type=PhoneNumberType.LOCAL,
            latitude="40.7128",
            longitude="-74.0060",
            provider_type=ProviderType.SIGNALWIRE
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    latitude: Optional[str] = None
    longitude: Optional[str] = None
    provider_type: Literal[ProviderType.SIGNALWIRE] = Field(
        ProviderType.SIGNALWIRE,
        alias="providerType"
    )


class TwilioPhoneNumberInfo(BasePhoneNumberInfo):
    """Twilio-specific phone number information.

    Extends base phone number schema with Twilio-specific fields.

    Attributes:
        locality: City or locality name
        latitude: Geographic latitude
        longitude: Geographic longitude
        provider_type: Always TWILIO

    Example:
        ```python
        twilio_phone = TwilioPhoneNumberInfo(
            friendly_name="Twilio Support Line",
            phone_number="+12125551234",
            country_code="US",
            capabilities=PhoneCapabilities(voice=True, sms=True, mms=True),
            beta=False,
            number_type=PhoneNumberType.LOCAL,
            locality="New York",
            latitude=40.7128,
            longitude=-74.0060,
            provider_type=ProviderType.TWILIO
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    locality: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    provider_type: Literal[ProviderType.TWILIO] = Field(
        ProviderType.TWILIO,
        alias="providerType"
    )


class PhoneProviderRequest(PydanticBaseModel):
    """Phone provider request schema.

    Used to request available phone numbers from a specific provider and region.

    Attributes:
        provider_type: Telephony provider type
        region: Geographic region identifier

    Example:
        ```python
        request = PhoneProviderRequest(
            provider_type=ProviderType.TWILIO,
            region="us-west"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    provider_type: ProviderType = Field(
        ...,
        alias="providerType"
    )
    region: str


class PhoneProviderResponse(PydanticBaseModel):
    """Phone provider response schema.

    Response from phone number provider API calls.

    Attributes:
        provider_type: Telephony provider type
        success: Whether the request was successful
        status: HTTP status code
        data: Response data from provider

    Example:
        ```python
        response = PhoneProviderResponse(
            provider_type=ProviderType.TWILIO,
            success=True,
            status=200,
            data={"availableNumbers": [...]}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    provider_type: ProviderType = Field(
        ...,
        alias="providerType"
    )
    success: bool
    status: Optional[int] = None
    data: Any


class PhoneNumberPurchase(BaseModel):
    """Phone number purchase transaction schema.

    Represents a phone number purchase request and its lifecycle through the purchase process.

    Attributes:
        friendly_name: Human-readable name for the purchased number
        phone_number: The phone number being purchased
        provider_type: Provider from which the number is being purchased
        amount: Purchase amount (must be positive)
        currency: Currency code (3 characters, default: "USD")
        status: Current status of the purchase (default: PENDING)
        number_type: Type of phone number (default: LOCAL)
        status_details: Additional details about the current status
        completed_at: Timestamp when purchase was completed
        metadata: Additional metadata for the purchase

    Example:
        ```python
        purchase = PhoneNumberPurchase(
            id="32422DEGER56",
            friendly_name="Main Support Line",
            phone_number="+12125551234",
            provider_type=ProviderType.TWILIO,
            amount=1.00,
            currency="USD",
            status=PhonePurchaseStatus.COMPLETED,
            number_type=PhoneNumberType.LOCAL,
            completed_at=1234567890
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

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
    provider_type: ProviderType = Field(
        ...,
        description="Telephony provider from which the number is being purchased",
        alias="providerType"
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Purchase price for this phone number"
    )
    currency: str = Field(
        "USD",
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code for the purchase amount"
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


class CreatePhoneNumberPurchase(PydanticBaseModel):
    """Schema for creating a new phone number purchase.

    Omits auto-generated and transaction-specific fields.

    Attributes:
        friendly_name: Human-readable name for the purchased number
        phone_number: The phone number being purchased
        provider_type: Provider from which the number is being purchased
        number_type: Type of phone number (default: LOCAL)

    Example:
        ```python
        new_purchase = CreatePhoneNumberPurchase(
            friendly_name="New Support Line",
            phone_number="+12125551234",
            provider_type=ProviderType.TWILIO,
            number_type=PhoneNumberType.LOCAL
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    friendly_name: str = Field(..., alias="friendlyName")
    phone_number: str = Field(..., alias="phoneNumber")
    provider_type: ProviderType = Field(..., alias="providerType")
    number_type: PhoneNumberType = Field(
        PhoneNumberType.LOCAL,
        alias="numberType"
    )


class PhoneNumberPricing(PydanticBaseModel):
    """Phone number pricing information schema.

    Represents pricing details for phone numbers from various providers.

    Attributes:
        number_type: Type of phone number
        country: Full country name
        country_code: ISO country code
        phone_number_prices: Array of pricing tiers
        price: Final price for the number
        price_unit: Unit of pricing (e.g., "per month")
        provider_type: Provider offering the number
        currency: Currency code (3 characters, default: "USD")

    Example:
        ```python
        pricing = PhoneNumberPricing(
            number_type=PhoneNumberType.LOCAL,
            country="United States",
            country_code="US",
            phone_number_prices=[
                {"base_price": "1.00", "current_price": "1.00"}
            ],
            price=1.00,
            price_unit="per month",
            provider_type=ProviderType.TWILIO,
            currency="USD"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    number_type: PhoneNumberType = Field(
        ...,
        alias="number_type"
    )
    country: str
    country_code: str = Field(..., alias="countryCode")
    phone_number_prices: List[Dict[str, str]] = Field(
        ...,
        alias="phoneNumberPrices"
    )
    price: float
    price_unit: str = Field(..., alias="priceUnit")
    provider_type: ProviderType = Field(..., alias="providerType")
    currency: str = Field(
        "USD",
        min_length=3,
        max_length=3
    )
