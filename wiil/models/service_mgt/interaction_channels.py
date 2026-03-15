"""Deployment channel schema definitions for multi-channel interactions.

Deployment Channels define the single communication channel through which a deployment is accessible
to end users. Each Deployment Configuration has exactly one Deployment Channel (1:1 relationship).
To expose an agent through multiple channels (e.g., both phone and web), create separate Deployment
Configurations for each channel.
"""

from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, field_validator

from wiil.models.base import BaseModel
from wiil.models.type_definitions import (
    DeploymentProvisioningType,
    DeploymentStatus,
    DeploymentType,
    MobilePlatform,
    OttCommunicationType,
)


class PhoneChannelConfig(PydanticBaseModel):
    """Phone channel configuration.

    Configuration specific to phone-based channels supporting voice calls and SMS messaging.
    This configuration links to a PhoneConfiguration resource that manages the actual phone number
    and telephony provider settings.

    Architecture Context:
        - Used By: Call and SMS deployment channels
        - Relationship: References PhoneConfiguration via phoneConfigurationId
        - Features: Supports call forwarding to external numbers for escalation or overflow
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    phone_configuration_id: str = Field(
        ...,
        description="ID of the PhoneConfiguration resource that manages the phone number and telephony provider settings",
        alias="phoneConfigurationId"
    )


class WebChannelConfig(PydanticBaseModel):
    """Web channel configuration.

    Configuration specific to web-based chat widget channels that can be embedded in websites
    and web applications for browser-based real-time communication.

    Architecture Context:
        - Used By: Web deployment channels
        - Features: Embeddable chat widget, WebSocket communication, rich media support
        - Customization: Supports custom CSS and theming for brand consistency
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    communication_type: OttCommunicationType = Field(
        OttCommunicationType.UNIFIED,
        description="Type of over-the-top (OTT) communication protocol used for the web channel",
        alias="communicationType"
    )
    widget_configuration: Optional[Dict[str, Any]] = Field(
        None,
        description="Configuration settings for the chat widget appearance and behavior",
        alias="widgetConfiguration"
    )


class MobileAppChannelConfig(PydanticBaseModel):
    """Mobile app channel configuration.

    Configuration specific to mobile application channels for native iOS and Android integrations.
    Enables SDK-based integration with platform-specific UI components.

    Architecture Context:
        - Used By: Mobile deployment channels
        - Features: SDK-based integration, deep linking, platform-specific UI
        - Status: Coming soon - currently in development
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    package_name: str = Field(
        "",
        description="Package name or bundle identifier for the mobile application",
        alias="packageName"
    )
    platform: MobilePlatform = Field(
        MobilePlatform.IOS,
        description="Mobile platform this channel targets (iOS or Android)"
    )


# Channel configuration union type
ChannelConfiguration = Union[PhoneChannelConfig, WebChannelConfig, MobileAppChannelConfig]


class DeploymentChannel(BaseModel):
    """Deployment channel.

    Defines the single communication channel through which a Deployment Configuration is accessible.
    Each Deployment Configuration has exactly one Deployment Channel (1:1 relationship).

    Architecture Context:
        - Relationship: 1:1 with Deployment Configuration (belongs to exactly one deployment)
        - Channel Types: Phone (calls/SMS), Web (chat widget), or Mobile App
        - Pattern: To expose an agent through multiple channels, create separate Deployment Configurations

    Attributes:
        deployment_type: Type of deployment channel (CALLS, SMS, WEB, or MOBILE)
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether interactions should be recorded
        channel_identifier: Channel-specific identifier (phone number, URL, or package name)
        configuration: Channel-specific configuration object
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    deployment_type: DeploymentType = Field(
        ...,
        description="Type of deployment channel (CALLS, SMS, WEB, or MOBILE)",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether interactions through this channel should be recorded",
        alias="recordingEnabled"
    )
    channel_identifier: str = Field(
        ...,
        description="Channel-specific identifier: phone number (E.164 format) for calls/SMS, website URL for web, or app package name for mobile",
        alias="channelIdentifier"
    )
    configuration: ChannelConfiguration = Field(
        ...,
        description="Channel-specific configuration object matching the deployment type"
    )


class CallChannel(BaseModel):
    """Call-based deployment channel.

    Defines a voice telephony channel for inbound and outbound phone calls. Integrates with
    telephony providers (SignalWire, Twilio) through PhoneConfiguration.

    Architecture Context:
        - Channel Type: Phone (Voice Calls)
        - Integration: PBX systems, contact centers, SIP trunks, cloud telephony
        - Features: Call recording, DTMF input, call forwarding, SIP/VoIP support
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Phone number in E.164 international format (e.g., '+12125551234')",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.CALLS] = Field(
        DeploymentType.CALLS,
        description="Channel type identifier, fixed to CALLS for voice telephony channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    configuration: PhoneChannelConfig = Field(
        ...,
        description="Phone-specific configuration including telephony provider settings"
    )


class SmsChannel(BaseModel):
    """SMS-based deployment channel.

    Defines an SMS messaging channel for text-based communication. Uses the same telephony
    infrastructure as voice calls but optimized for asynchronous text messaging.

    Architecture Context:
        - Channel Type: Phone (SMS Messaging)
        - Integration: SMS gateways, telephony providers
        - Features: Asynchronous messaging, message history, multimedia support (MMS)
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Phone number in E.164 international format",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.SMS] = Field(
        DeploymentType.SMS,
        description="Channel type identifier, fixed to SMS for text messaging channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    configuration: PhoneChannelConfig = Field(
        ...,
        description="Phone-specific configuration for SMS delivery"
    )


class WebChannel(BaseModel):
    """Web-based deployment channel.

    Defines a browser-based chat widget channel for website integration. Provides real-time
    messaging with rich media support through WebSocket connections.

    Architecture Context:
        - Channel Type: Web (Chat Widget)
        - Integration: Websites, web apps, customer portals, help centers
        - Features: Embeddable widget, WebSocket real-time communication, rich media, session persistence
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Website URL where the chat widget will be deployed",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.WEB] = Field(
        DeploymentType.WEB,
        description="Channel type identifier, fixed to WEB for browser-based chat widget channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    configuration: WebChannelConfig = Field(
        ...,
        description="Web-specific configuration including chat widget appearance and theming"
    )


class MobileAppChannel(BaseModel):
    """Mobile app deployment channel.

    Defines a native mobile application channel for iOS and Android apps. Enables SDK-based
    integration with platform-specific UI components and capabilities.

    Architecture Context:
        - Channel Type: Mobile (Native App)
        - Integration: iOS apps, Android apps, cross-platform frameworks
        - Features: SDK integration, deep linking, platform-specific UI, push notifications
        - Status: Coming soon - currently in development
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Unique identifier for the mobile application deployment",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.MOBILE] = Field(
        DeploymentType.MOBILE,
        description="Channel type identifier, fixed to MOBILE for native mobile application channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    configuration: MobileAppChannelConfig = Field(
        ...,
        description="Mobile-specific configuration including platform selection"
    )


# Channel type aliases
CallChannelType = CallChannel
SmsChannelType = SmsChannel
WebChannelType = WebChannel
MobileAppChannelType = MobileAppChannel


class CreateWebChannel(PydanticBaseModel):
    """Schema for creating a new web channel."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(..., alias="channelIdentifier")
    deployment_type: Literal[DeploymentType.WEB] = Field(
        DeploymentType.WEB,
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    configuration: WebChannelConfig


class CreateMobileAppChannel(PydanticBaseModel):
    """Schema for creating a new mobile app channel."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(..., alias="channelIdentifier")
    deployment_type: Literal[DeploymentType.MOBILE] = Field(
        DeploymentType.MOBILE,
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    configuration: MobileAppChannelConfig


class DeploymentChannelRequest(PydanticBaseModel):
    """Deployment channel creation request.

    Flexible schema that validates channel configuration based on deployment type.
    Uses runtime validation to ensure channel-specific requirements are met.

    Architecture Context:
        - Purpose: Validates incoming requests to create new deployment channels
        - Validation: Type-specific validation ensures correct configuration for each channel type
        - Usage: Used by API endpoints for channel creation
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    deployment_type: DeploymentType = Field(
        ...,
        description="Type of deployment channel to create (CALLS, SMS, WEB, or MOBILE)",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether to enable interaction recording for this channel",
        alias="recordingEnabled"
    )
    channel_identifier: str = Field(
        ...,
        description="Channel-specific identifier (phone number for calls/SMS, URL for web, package name for mobile)",
        alias="channelIdentifier"
    )
    configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Channel-specific configuration object matching the requirements of the deployment type"
    )
    created_at: Optional[int] = Field(None, alias="createdAt")
    updated_at: Optional[int] = Field(None, alias="updatedAt")

    @field_validator("deployment_type", mode="before")
    @classmethod
    def normalize_deployment_type(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()
        return value


class DeploymentChannelUpdateRequest(PydanticBaseModel):
    """Deployment channel update request.

    Supports partial updates to existing deployment channels. All fields are optional except id.

    Architecture Context:
        - Purpose: Enables modification of channel settings without recreating the deployment
        - Validation: Partial validation ensures only provided fields are validated
        - Usage: Used by API endpoints for channel updates
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier of the deployment channel to update")
    deployment_type: Optional[DeploymentType] = Field(None, alias="deploymentType")
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: Optional[bool] = Field(None, alias="recordingEnabled")
    channel_identifier: Optional[str] = Field(None, alias="channelIdentifier")
    configuration: Optional[Dict[str, Any]] = None

    @field_validator("deployment_type", mode="before")
    @classmethod
    def normalize_deployment_type(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()
        return value


class ChannelSetupRequest(PydanticBaseModel):
    """Channel setup request.

    Complete setup request for creating a new deployment with its associated channel and configurations.
    This is a convenience schema that combines channel creation with deployment configuration references.

    Architecture Context:
        - Purpose: Simplifies deployment creation by bundling channel and configuration references
        - Relationship: Creates a Deployment Configuration with associated channel, project, agent, and instruction
        - Pattern: One request creates the complete deployment stack
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel: DeploymentChannelRequest = Field(
        ...,
        description="Deployment channel configuration to create"
    )
    project_id: str = Field(
        ...,
        description="ID of the project this deployment belongs to",
        alias="projectId"
    )
    agent_configuration_id: str = Field(
        ...,
        description="ID of the agent configuration that defines the agent's core behavior",
        alias="agentConfigurationId"
    )
    instruction_configuration_id: str = Field(
        ...,
        description="ID of the instruction configuration that provides behavioral guidelines",
        alias="instructionConfigurationId"
    )


class ChannelUpdateRequest(PydanticBaseModel):
    """Channel update request.

    Partial update request for modifying an existing deployment and its associated channel.
    Supports updating the channel configuration and/or changing the referenced configurations.

    Architecture Context:
        - Purpose: Enables modification of deployment configuration references and channel settings
        - Flexibility: All fields are optional for partial updates
        - Usage: Used to update deployments without full recreation
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    channel: DeploymentChannelUpdateRequest = Field(
        ...,
        description="Partial update to the deployment channel configuration"
    )
    project_id: Optional[str] = Field(None, alias="projectId")
    agent_configuration_id: Optional[str] = Field(None, alias="agentConfigurationId")
    instruction_configuration_id: Optional[str] = Field(None, alias="instructionConfigurationId")


class DeploymentChannelWithDeployment(PydanticBaseModel):
    """Deployment channel with deployment information.

    Extended view that includes both the channel configuration and its associated deployment details.
    This schema is typically used for detailed views where the complete deployment context is needed.

    Architecture Context:
        - Purpose: Provides complete deployment context in a single response
        - Usage: Used for detail views and administrative interfaces
        - Relationship: Combines DeploymentChannel with its associated Deployment Configuration
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for the deployment channel")
    deployment_type: DeploymentType = Field(..., alias="deploymentType")
    channel_name: Optional[str] = Field(None, alias="channelName")
    recording_enabled: bool = Field(True, alias="recordingEnabled")
    channel_identifier: str = Field(..., alias="channelIdentifier")
    configuration: ChannelConfiguration
    deployment: Optional[Dict[str, Any]] = Field(
        None,
        description="Associated deployment configuration details (null if not associated)"
    )


# Type aliases for legacy compatibility
CreateDeploymentChannel = DeploymentChannelRequest
UpdateDeploymentChannel = DeploymentChannelUpdateRequest
DeploymentChannelType = DeploymentChannel
DeploymentChannelUpdate = DeploymentChannelUpdateRequest
DeploymentChannelUpdateRequestType = ChannelUpdateRequest
DeploymentChannelInfo = DeploymentChannelWithDeployment


class DeploymentChannelDeletionRequest(PydanticBaseModel):
    """Request to delete a deployment channel."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier of the deployment channel to delete")
    delete_phone_config: bool = Field(
        True,
        description="Whether to also delete associated phone configurations",
        alias="deletePhoneConfig"
    )
