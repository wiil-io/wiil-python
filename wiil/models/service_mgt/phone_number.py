"""Phone number configuration and purchase schema definitions.

Phone number schemas manage the complete lifecycle of phone number acquisition from
telephony providers: discovery of available inventory, purchase transactions, and
provisioning into Phone Configurations.
"""

from typing import Literal, Optional

from pydantic import ConfigDict, Field
from pydantic import BaseModel as PydanticBaseModel

from wiil.types.service_types import PhoneNumberType, ProviderType


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
        iso_country: ISO country code
        capabilities: Phone number capabilities
        beta: Whether this is a beta number
        number_type: Type of phone number

    Example:
        ```python
        phone_info = BasePhoneNumberInfo(
            friendly_name="Customer Support Line",
            phone_number="+12125551234",
            iso_country="US",
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
    iso_country: str = Field(
        ...,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')",
        alias="isoCountry"
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
            iso_country="US",
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
            iso_country="US",
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
