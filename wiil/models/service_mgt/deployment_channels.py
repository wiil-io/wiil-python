"""Deployment channel schema definitions for multi-channel interactions.

Deployment Channels define the single communication channel through which a deployment is
accessible to end users. Each Deployment Configuration has exactly one Deployment Channel
(1:1 relationship). To expose an agent through multiple channels (e.g., both phone and web),
create separate Deployment Configurations for each channel.
"""

from typing import Any, Dict, Literal, Optional, Union

from pydantic import ConfigDict, Field
from pydantic import BaseModel as PydanticBaseModel

from wiil.models.base import BaseModel
from wiil.types.service_types import DeploymentType, MobilePlatform, OttCommunicationType


class PhoneChannelConfig(PydanticBaseModel):
    """Phone channel configuration.

    Configuration specific to phone-based channels supporting voice calls and SMS messaging.
    This configuration links to a PhoneConfiguration resource that manages the actual phone
    number and telephony provider settings.

    Architecture Context:
        - Used By: Call and SMS deployment channels
        - Relationship: References PhoneConfiguration via phoneConfigurationId
        - Features: Supports call forwarding to external numbers for escalation or overflow

    Attributes:
        phone_configuration_id: ID of the PhoneConfiguration resource
        has_forwarding_enabled: Whether call forwarding is enabled
        forwarding_phone_number: Phone number to forward calls to when forwarding is enabled

    Example:
        ```python
        phone_config = PhoneChannelConfig(
            phone_configuration_id="789",
            has_forwarding_enabled=False,
            forwarding_phone_number=None
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    phone_configuration_id: str = Field(
        ...,
        description="ID of the PhoneConfiguration resource that manages the phone number and telephony provider settings for this channel",
        alias="phoneConfigurationId"
    )


class WidgetConfiguration(PydanticBaseModel):
    """Chat widget configuration settings.

    Configuration for the chat widget appearance and behavior when embedded in websites.

    Attributes:
        position: Position of the chat widget on the webpage (left or right)
        theme: Visual theme for the chat widget
        custom_theme: Custom theme properties as key-value pairs for advanced styling

    Example:
        ```python
        widget_config = WidgetConfiguration(
            position="right",
            theme="light",
            custom_theme={"primary_color": "#007bff", "font_family": "Arial"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    position: Literal["left", "right"] = Field(
        "right",
        description="Position of the chat widget on the webpage (left or right side of the screen)"
    )
    theme: Literal["light", "dark", "custom"] = Field(
        "light",
        description="Visual theme for the chat widget (light, dark, or custom theme using customTheme settings)"
    )
    custom_theme: Optional[Dict[str, str]] = Field(
        None,
        description="Custom theme properties as key-value pairs for advanced widget styling (e.g., primary color, font family, border radius)",
        alias="customTheme"
    )


class WebChannelConfig(PydanticBaseModel):
    """Web channel configuration.

    Configuration specific to web-based chat widget channels that can be embedded in websites
    and web applications for browser-based real-time communication.

    Architecture Context:
        - Used By: Web deployment channels
        - Features: Embeddable chat widget, WebSocket communication, rich media support
        - Customization: Supports custom CSS and theming for brand consistency

    Attributes:
        communication_type: Type of over-the-top (OTT) communication protocol used
        custom_css_url: Optional URL to a custom CSS stylesheet
        widget_configuration: Configuration settings for the chat widget appearance and behavior

    Example:
        ```python
        web_config = WebChannelConfig(
            communication_type=OttCommunicationType.UNIFIED,
            custom_css_url="https://example.com/custom.css",
            widget_configuration=WidgetConfiguration(
                position="right",
                theme="light"
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    communication_type: OttCommunicationType = Field(
        OttCommunicationType.UNIFIED,
        description="Type of over-the-top (OTT) communication protocol used for the web channel (default: UNIFIED for combined text/media communication)",
        alias="communicationType"
    )
    widget_configuration: Optional[WidgetConfiguration] = Field(
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

    Attributes:
        package_name: Package name or bundle identifier for the mobile application
        platform: Mobile platform this channel targets (iOS or Android)

    Example:
        ```python
        mobile_config = MobileAppChannelConfig(
            package_name="com.company.app",
            platform=MobilePlatform.IOS
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    package_name: str = Field(
        "",
        description="Package name or bundle identifier for the mobile application (e.g., 'com.company.app' for Android or 'com.company.app' for iOS)",
        alias="packageName"
    )
    platform: MobilePlatform = Field(
        MobilePlatform.IOS,
        description="Mobile platform this channel targets (iOS or Android) for platform-specific SDK integration"
    )


class CallChannel(BaseModel):
    """Call-based deployment channel.

    Defines a voice telephony channel for inbound and outbound phone calls. Integrates with
    telephony providers (SignalWire, Twilio) through PhoneConfiguration.

    Architecture Context:
        - Channel Type: Phone (Voice Calls)
        - Integration: PBX systems, contact centers, SIP trunks, cloud telephony
        - Features: Call recording, DTMF input, call forwarding, SIP/VoIP support

    Attributes:
        id: Unique identifier
        channel_identifier: Phone number in E.164 format for inbound calls
        deployment_type: Channel type identifier (fixed to CALLS)
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether interactions should be recorded
        configuration: Phone-specific configuration including telephony provider settings
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        call_channel = CallChannel(
            id="123",
            channel_identifier="+12125551234",
            deployment_type=DeploymentType.CALLS,
            recording_enabled=True,
            configuration=PhoneChannelConfig(
                phone_configuration_id="789",
                has_forwarding_enabled=False
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Phone number in E.164 international format that serves as the inbound endpoint for voice calls (e.g., '+12125551234')",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.CALLS] = Field(
        DeploymentType.CALLS,
        description="Channel type identifier, fixed to CALLS for voice telephony channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel used in administrative interfaces and reporting",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether interactions through this channel should be recorded for compliance, quality assurance, and training purposes",
        alias="recordingEnabled"
    )
    configuration: PhoneChannelConfig = Field(
        ...,
        description="Phone-specific configuration including telephony provider settings and call forwarding options"
    )


class SmsChannel(BaseModel):
    """SMS-based deployment channel.

    Defines an SMS messaging channel for text-based communication. Uses the same telephony
    infrastructure as voice calls but optimized for asynchronous text messaging.

    Architecture Context:
        - Channel Type: Phone (SMS Messaging)
        - Integration: SMS gateways, telephony providers
        - Features: Asynchronous messaging, message history, multimedia support (MMS)

    Attributes:
        id: Unique identifier
        channel_identifier: Phone number in E.164 format for SMS messaging
        deployment_type: Channel type identifier (fixed to SMS)
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether interactions should be recorded
        configuration: Phone-specific configuration including telephony provider settings
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        sms_channel = SmsChannel(
            id="123",
            channel_identifier="+12125551234",
            deployment_type=DeploymentType.SMS,
            recording_enabled=True,
            configuration=PhoneChannelConfig(
                phone_configuration_id="789",
                has_forwarding_enabled=False
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Phone number in E.164 international format that serves as the endpoint for SMS messaging (e.g., '+12125551234')",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.SMS] = Field(
        DeploymentType.SMS,
        description="Channel type identifier, fixed to SMS for text messaging channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel used in administrative interfaces and reporting",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether interactions through this channel should be recorded for compliance, quality assurance, and training purposes",
        alias="recordingEnabled"
    )
    configuration: PhoneChannelConfig = Field(
        ...,
        description="Phone-specific configuration including telephony provider settings for SMS delivery"
    )


class WebChannel(BaseModel):
    """Web-based deployment channel.

    Defines a browser-based chat widget channel for website integration. Provides real-time
    messaging with rich media support through WebSocket connections.

    Architecture Context:
        - Channel Type: Web (Chat Widget)
        - Integration: Websites, web apps, customer portals, help centers
        - Features: Embeddable widget, WebSocket real-time communication, rich media, session persistence

    Attributes:
        id: Unique identifier
        channel_identifier: Website URL where the chat widget will be deployed
        deployment_type: Channel type identifier (fixed to WEB)
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether interactions should be recorded
        configuration: Web-specific configuration including chat widget appearance and theming
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        web_channel = WebChannel(
            id="123",
            channel_identifier="https://example.com",
            deployment_type=DeploymentType.WEB,
            recording_enabled=True,
            configuration=WebChannelConfig(
                communication_type=OttCommunicationType.UNIFIED,
                widget_configuration=WidgetConfiguration(position="right", theme="light")
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Website URL where the chat widget will be deployed (e.g., 'https://example.com' or 'localhost:3000' for development)",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.WEB] = Field(
        DeploymentType.WEB,
        description="Channel type identifier, fixed to WEB for browser-based chat widget channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel used in administrative interfaces and reporting",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether interactions through this channel should be recorded for compliance, quality assurance, and training purposes",
        alias="recordingEnabled"
    )
    configuration: WebChannelConfig = Field(
        ...,
        description="Web-specific configuration including chat widget appearance, positioning, and theming options"
    )


class MobileAppChannel(BaseModel):
    """Mobile app deployment channel.

    Defines a native mobile application channel for iOS and Android apps. Enables SDK-based
    integration with platform-specific UI components and capabilities.

    Architecture Context:
        - Channel Type: Mobile (Native App)
        - Integration: iOS apps, Android apps, cross-platform frameworks (React Native, Flutter)
        - Features: SDK integration, deep linking, platform-specific UI, push notifications
        - Status: Coming soon - currently in development

    Attributes:
        id: Unique identifier
        channel_identifier: Unique identifier for the mobile application deployment
        deployment_type: Channel type identifier (fixed to MOBILE)
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether interactions should be recorded
        configuration: Mobile-specific configuration including platform and app package identification
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        mobile_channel = MobileAppChannel(
            id="123",
            channel_identifier="com.company.app",
            deployment_type=DeploymentType.MOBILE,
            recording_enabled=True,
            configuration=MobileAppChannelConfig(
                package_name="com.company.app",
                platform=MobilePlatform.IOS
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    channel_identifier: str = Field(
        ...,
        description="Unique identifier for the mobile application deployment (typically the app bundle ID or package name)",
        alias="channelIdentifier"
    )
    deployment_type: Literal[DeploymentType.MOBILE] = Field(
        DeploymentType.MOBILE,
        description="Channel type identifier, fixed to MOBILE for native mobile application channels",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel used in administrative interfaces and reporting",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether interactions through this channel should be recorded for compliance, quality assurance, and training purposes",
        alias="recordingEnabled"
    )
    configuration: MobileAppChannelConfig = Field(
        ...,
        description="Mobile-specific configuration including platform selection and app package identification"
    )


class DeploymentChannel(BaseModel):
    """General deployment channel with union configuration.

    Provides type-safe channel configuration based on deployment type. This is the primary
    schema used for deployment channel entities throughout the system.

    Architecture Context:
        - Relationship: 1:1 with Deployment Configuration (each deployment has exactly one channel)
        - Pattern: Multi-channel deployments require separate Deployment Configurations per channel
        - Validation: Configuration must match the deployment type requirements

    Attributes:
        id: Unique identifier
        deployment_type: Type of deployment channel (CALLS, SMS, WEB, or MOBILE)
        channel_identifier: Channel-specific identifier (phone number, URL, or package name)
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether interactions should be recorded
        configuration: Channel-specific configuration object (union type)
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        channel = DeploymentChannel(
            id="123",
            deployment_type=DeploymentType.CALLS,
            channel_identifier="+12125551234",
            recording_enabled=True,
            configuration=PhoneChannelConfig(phone_configuration_id="789")
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    deployment_type: DeploymentType = Field(
        ...,
        description="Type of deployment channel determining the communication medium (CALLS for voice, SMS for text messaging, WEB for chat widget, MOBILE for native apps)",
        alias="deploymentType"
    )
    channel_identifier: str = Field(
        ...,
        description="Channel-specific identifier: phone number (E.164 format) for calls/SMS, website URL for web, or app package name for mobile",
        alias="channelIdentifier"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the channel used in administrative interfaces and reporting",
        alias="channelName"
    )
    recording_enabled: bool = Field(
        True,
        description="Whether interactions through this channel should be recorded for compliance, quality assurance, and training purposes",
        alias="recordingEnabled"
    )
    configuration: Union[PhoneChannelConfig, WebChannelConfig, MobileAppChannelConfig] = Field(
        ...,
        description="Channel-specific configuration object matching the deployment type (PhoneChannelConfig for calls/SMS, WebChannelConfig for web, MobileAppChannelConfig for mobile)"
    )


class CreateDeploymentChannel(PydanticBaseModel):
    """Schema for creating a new deployment channel.

    Flexible schema that validates channel configuration based on deployment type.
    Uses runtime validation to ensure channel-specific requirements are met.

    Architecture Context:
        - Purpose: Validates incoming requests to create new deployment channels
        - Validation: Type-specific validation ensures correct configuration for each channel type
        - Usage: Used by API endpoints for channel creation

    Attributes:
        deployment_type: Type of deployment channel to create
        channel_name: Optional human-readable name for the channel
        recording_enabled: Whether to enable interaction recording
        channel_identifier: Channel-specific identifier
        configuration: Channel-specific configuration object
        created_at: Unix timestamp when created (optional)
        updated_at: Unix timestamp when last updated (optional)

    Example:
        ```python
        create_channel = CreateDeploymentChannel(
            deployment_type=DeploymentType.CALLS,
            channel_identifier="+12125551234",
            recording_enabled=True,
            configuration=PhoneChannelConfig(phone_configuration_id="789")
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
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
        ...,
        description="Channel-specific configuration object matching the requirements of the deployment type"
    )
    created_at: Optional[int] = Field(
        None,
        description="Unix timestamp (milliseconds) when the channel was created (auto-generated if not provided)",
        alias="createdAt"
    )
    updated_at: Optional[int] = Field(
        None,
        description="Unix timestamp (milliseconds) when the channel was last updated (auto-generated if not provided)",
        alias="updatedAt"
    )


class UpdateDeploymentChannel(PydanticBaseModel):
    """Schema for updating an existing deployment channel.

    Supports partial updates to existing deployment channels. All fields are optional except id.

    Architecture Context:
        - Purpose: Enables modification of channel settings without recreating the deployment
        - Validation: Partial validation ensures only provided fields are validated
        - Usage: Used by API endpoints for channel updates

    Attributes:
        id: Unique identifier of the deployment channel to update
        deployment_type: Optional update to the channel type
        channel_name: Optional update to the human-readable channel name
        recording_enabled: Optional update to the recording settings
        channel_identifier: Optional update to the channel identifier
        configuration: Optional update to the channel-specific configuration object

    Example:
        ```python
        update_channel = UpdateDeploymentChannel(
            id="123",
            channel_name="Updated Support Line",
            recording_enabled=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(
        ...,
        description="Unique identifier of the deployment channel to update"
    )
    deployment_type: Optional[DeploymentType] = Field(
        None,
        description="Optional update to the channel type (generally not recommended to change after creation)",
        alias="deploymentType"
    )
    channel_name: Optional[str] = Field(
        None,
        description="Optional update to the human-readable channel name",
        alias="channelName"
    )
    recording_enabled: Optional[bool] = Field(
        None,
        description="Optional update to the recording settings for this channel",
        alias="recordingEnabled"
    )
    channel_identifier: Optional[str] = Field(
        None,
        description="Optional update to the channel identifier (phone number, URL, or package name)",
        alias="channelIdentifier"
    )
    configuration: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional update to the channel-specific configuration object"
    )
