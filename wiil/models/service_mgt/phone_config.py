"""Phone configuration schema definitions for telephony management.

Phone Configurations manage telephony resources including phone numbers from various providers
(SignalWire, Twilio). They track provider information, channel associations, and operational status.
Referenced by Phone Channel configurations for call and SMS deployments.
"""

from typing import Any, Dict, Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions import PhoneStatus, ProviderType


class PhoneConfiguration(EntityModel):
    """Phone configuration for telephony management.

    Manages a phone number resource from a telephony provider, tracking its configuration, status,
    and associations with deployment channels. A single phone number can support both voice calls
    and SMS through separate channel associations.

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
        phone_number: Phone number, short code, or alphanumeric sender ID
        provider_phone_number_id: Unique identifier from the telephony provider
        phone_request_id: Reference ID for the original purchase transaction
        friendly_name: Human-readable display name for administrative interfaces
        region_id: Region identifier where this number is registered
        monthly_price: Monthly recurring cost for maintaining this phone number
        region_or_country_name: Human-readable region or country name
        country_code: ISO 3166-1 alpha-2 country code
        provider_type: Telephony service provider (SIGNALWIRE, TWILIO, etc.)
        is_imported: Whether this number was imported from external system
        status: Current operational status
        is_ported: Whether this number was ported from another provider
        marked_for_release: Whether marked for disconnection
        metadata: Additional provider-specific metadata
        voice_channel_id: ID of the voice/call deployment channel
        sms_channel_id: ID of the SMS deployment channel
        voice_channel: Populated voice channel configuration
        sms_channel: Populated SMS channel configuration
        is_us_sms_permitted: Whether US SMS messaging is permitted
    """

    phone_number: str = Field(
        ...,
        description="Phone number, short code, or alphanumeric sender ID",
        alias="phoneNumber"
    )
    provider_phone_number_id: str = Field(
        ...,
        description="Unique identifier for this phone number from the telephony provider's system",
        alias="providerPhoneNumberId"
    )
    phone_request_id: str = Field(
        ...,
        description="Reference ID for the original phone number purchase transaction",
        alias="phoneRequestId"
    )
    friendly_name: Optional[str] = Field(
        None,
        description="Human-readable display name for this phone number",
        alias="friendlyName"
    )
    region_id: Optional[str] = Field(
        None,
        description="Region identifier where this phone number is registered",
        alias="regionId"
    )
    monthly_price: Optional[float] = Field(
        None,
        description="Monthly recurring cost for maintaining this phone number",
        alias="monthlyPrice"
    )
    region_or_country_name: Optional[str] = Field(
        None,
        description="Human-readable name of the region or country",
        alias="regionOrCountryName"
    )
    country_code: Optional[str] = Field(
        None,
        description="ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB', 'CA')",
        alias="countryCode"
    )
    provider_type: ProviderType = Field(
        ProviderType.SIGNALWIRE,
        description="Telephony service provider managing this phone number",
        alias="providerType"
    )
    is_imported: bool = Field(
        False,
        description="Flag indicating if this phone number was imported from an external system",
        alias="isImported"
    )
    status: PhoneStatus = Field(
        PhoneStatus.INACTIVE,
        description="Current operational status (PENDING, ACTIVE, INACTIVE, SUSPENDED, RELEASED)"
    )
    is_ported: bool = Field(
        False,
        description="Flag indicating if this phone number was ported from another provider",
        alias="isPorted"
    )
    marked_for_release: Optional[bool] = Field(
        False,
        description="Flag indicating if this phone number is marked for release/disconnection",
        alias="markedForRelease"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional provider-specific metadata or custom attributes"
    )
    voice_channel_id: Optional[str] = Field(
        None,
        description="ID of the voice/call deployment channel associated with this phone number",
        alias="voiceChannelId"
    )
    sms_channel_id: Optional[str] = Field(
        None,
        description="ID of the SMS deployment channel associated with this phone number",
        alias="smsChannelId"
    )
    voice_channel: Optional[Dict[str, Any]] = Field(
        None,
        description="Populated voice deployment channel configuration",
        alias="voiceChannel"
    )
    sms_channel: Optional[Dict[str, Any]] = Field(
        None,
        description="Populated SMS deployment channel configuration",
        alias="smsChannel"
    )
    is_us_sms_permitted: bool = Field(
        False,
        description="Compliance flag indicating if US SMS messaging is permitted for this phone number",
        alias="isUSSMSPermitted"
    )


class UpdatePhoneConfiguration(BaseModel):
    """Schema for updating an existing phone configuration.

    Only allows updating the friendly name and requires the id to identify the configuration.
    """

    id: str
    friendly_name: Optional[str] = Field(None, alias="friendlyName")
