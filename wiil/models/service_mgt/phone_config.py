"""Phone configuration schema definitions for telephony management.

Phone Configurations manage telephony resources including phone numbers from various
providers (SignalWire, Twilio). They track provider information, channel associations,
and operational status.
"""

from typing import Any, Dict, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.service_types import PhoneStatus, ProviderType


class PhoneConfiguration(BaseModel):
    """Phone Configuration model.

    Manages a phone number resource from a telephony provider, tracking its
    configuration, status, and associations with deployment channels. A single
    phone number can support both voice calls and SMS through separate channel
    associations.

    Architecture Context:
        - Referenced By: PhoneChannelConfig (via phoneConfigurationId)
        - Purpose: Manages telephony resources and provider integration
        - Dual Channel Support: One phone number can have both voice and SMS channels
        - Providers: SignalWire, Twilio, and other SIP/VoIP providers

    Phone Number Lifecycle:
        - PENDING: Purchase initiated, awaiting provisioning
        - ACTIVE: Operational and ready for deployments
        - INACTIVE: Purchased but not yet activated
        - SUSPENDED: Temporarily disabled
        - RELEASED: Disconnected and returned to provider

    Attributes:
        id: Unique identifier
        phone_number: Phone number in E.164 format
        provider_phone_number_id: Provider's identifier for this number
        phone_request_id: Original purchase transaction ID
        friendly_name: Human-readable display name
        region_id: Region where number is registered
        monthly_price: Monthly recurring cost
        region_or_country_name: Human-readable region/country name
        country_code: ISO 3166-1 alpha-2 country code
        provider_type: Telephony service provider
        provider_account_id: Provider account identifier
        is_imported: Whether number was imported from external system
        status: Current operational status
        is_ported: Whether number was ported from another provider
        marked_for_release: Whether marked for disconnection
        metadata: Provider-specific metadata
        voice_channel_id: ID of voice deployment channel
        sms_channel_id: ID of SMS deployment channel
        voice_channel: Populated voice channel configuration
        sms_channel: Populated SMS channel configuration
        is_ussms_permitted: Whether US SMS messaging is permitted
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        phone_config = PhoneConfiguration(
            id="123",
            phone_number="+12125551234",
            provider_phone_number_id="PN123abc",
            phone_request_id="REQ456",
            friendly_name="Customer Support Line",
            region_id="us-ny",
            monthly_price=1.00,
            region_or_country_name="New York, United States",
            country_code="US",
            provider_type=ProviderType.SIGNALWIRE,
            status=PhoneStatus.ACTIVE,
            is_imported=False,
            is_ported=False,
            is_ussms_permitted=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    phone_number: str = Field(
        ...,
        description="Phone number in E.164 format (e.g., '+12125551234')",
        alias="phoneNumber"
    )
    provider_phone_number_id: str = Field(
        ...,
        description="Provider's unique identifier for this phone number",
        alias="providerPhoneNumberId"
    )
    phone_request_id: str = Field(
        ...,
        description="Original phone number purchase transaction ID",
        alias="phoneRequestId"
    )
    friendly_name: Optional[str] = Field(
        None,
        description="Human-readable display name",
        alias="friendlyName"
    )
    region_id: Optional[str] = Field(
        None,
        description="Region identifier where number is registered",
        alias="regionId"
    )
    monthly_price: Optional[float] = Field(
        None,
        description="Monthly recurring cost in USD",
        alias="monthlyPrice"
    )
    region_or_country_name: Optional[str] = Field(
        None,
        description="Human-readable region or country name",
        alias="regionOrCountryName"
    )
    country_code: Optional[str] = Field(
        None,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')",
        alias="countryCode"
    )
    provider_type: ProviderType = Field(
        ProviderType.SIGNALWIRE,
        description="Telephony service provider",
        alias="providerType"
    )
    provider_account_id: Optional[str] = Field(
        None,
        description="Account identifier with the provider",
        alias="providerAccountId"
    )
    is_imported: bool = Field(
        False,
        description="Whether imported from external system",
        alias="isImported"
    )
    status: PhoneStatus = Field(
        PhoneStatus.INACTIVE,
        description="Current operational status"
    )
    is_ported: bool = Field(
        False,
        description="Whether ported from another provider",
        alias="isPorted"
    )
    marked_for_release: Optional[bool] = Field(
        False,
        description="Whether marked for disconnection",
        alias="markedForRelease"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Provider-specific metadata"
    )
    voice_channel_id: Optional[str] = Field(
        None,
        description="ID of voice deployment channel",
        alias="voiceChannelId"
    )
    sms_channel_id: Optional[str] = Field(
        None,
        description="ID of SMS deployment channel",
        alias="smsChannelId"
    )
    voice_channel: Optional[Any] = Field(
        None,
        description="Populated voice channel configuration",
        alias="voiceChannel"
    )
    sms_channel: Optional[Any] = Field(
        None,
        description="Populated SMS channel configuration",
        alias="smsChannel"
    )
    is_ussms_permitted: bool = Field(
        False,
        description="Whether US SMS messaging is permitted",
        alias="isUSSMSPermitted"
    )


class UpdatePhoneConfiguration(BaseModel):
    """Schema for updating an existing phone configuration.

    Only allows updating the friendly name.

    Example:
        ```python
        update_data = UpdatePhoneConfiguration(
            id="123",
            friendly_name="Updated Support Line Name"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    friendly_name: Optional[str] = Field(None, alias="friendlyName")
