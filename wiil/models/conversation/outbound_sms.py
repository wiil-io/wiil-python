"""Outbound SMS request schema definitions for text messaging campaigns.

Provides schemas for composing, scheduling, and tracking outbound SMS messages
sent through AI-powered communication workflows. Supports direct messaging,
template-based content with variable substitution, and scheduled delivery.
"""

from typing import Any, Dict, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.types.conversation_types import SmsStatus


class SmsRequest(EntityModel):
    """SMS request schema for composing outbound text messages.

    Represents a complete outbound SMS request with content, recipient,
    and scheduling options. Supports template-based composition with
    variable substitution for personalized messaging.

    Message Length:
        - Standard SMS: 160 characters (GSM-7 encoding)
        - Unicode SMS: 70 characters per segment
        - Long messages automatically split into segments by carrier

    Architecture Context:
        - Template Support: References SmsTemplate for structured content
        - Conversation Tracking: Links to ServiceConversationConfig for threading
        - Carrier Integration: Works with Twilio, SignalWire, and other providers

    Attributes:
        phone_configuration_id: Phone configuration ID for sender number settings
            and carrier routing. When omitted, uses organization default.
        to: Recipient phone number in E.164 international format (e.g., '+12125551234').
            Must be a valid mobile number capable of receiving SMS.
        from_number: Sender phone number in E.164 format or short code (e.g., '12345').
            Must be a verified SMS-enabled number or short code owned by the organization.
        body: Text content of the SMS message. Standard SMS supports 160 characters,
            unicode 70 characters per segment.
        template_id: Pre-defined SMS template ID for structured content with
            variable placeholders.
        variables: Template variable substitutions as key-value pairs
            (e.g., {firstName: 'John', appointmentTime: '3:00 PM'}).
        scheduled_at: Unix timestamp in milliseconds for scheduled delivery.
        service_conversation_config_id: Linked conversation record ID for threading.
        metadata: Additional custom metadata for campaign tracking.

    Example:
        ```python
        sms = SmsRequest(
            to="+12125551234",
            from_number="+12125559999",
            body="Hi {{firstName}}, your appointment is confirmed for {{time}}.",
            variables={"firstName": "John", "time": "3:00 PM"}
        )
        ```
    """

    phone_configuration_id: Optional[str] = Field(
        None,
        alias="phoneConfigurationId",
        description="Phone configuration ID for sender number settings and carrier routing"
    )
    to: str = Field(
        ...,
        description="Recipient phone number in E.164 international format (e.g., '+12125551234')"
    )
    from_number: Optional[str] = Field(
        None,
        alias="from",
        description="Sender phone number in E.164 format or short code (e.g., '12345') displayed to the recipient. Must be a verified SMS-enabled number or short code owned by the organization. Uses default from phoneConfigurationId if omitted."
    )
    body: str = Field(
        ...,
        description="Text content of the SMS message (160 chars standard, 70 chars unicode per segment)"
    )
    template_id: Optional[str] = Field(
        None,
        alias="templateId",
        description="Pre-defined SMS template ID for structured content"
    )
    variables: Optional[Dict[str, Any]] = Field(
        None,
        description="Template variable substitutions as key-value pairs"
    )
    scheduled_at: Optional[int] = Field(
        None,
        alias="scheduledAt",
        description="Unix timestamp in milliseconds for scheduled delivery"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
        description="Linked conversation record ID for SMS thread tracking"
    )
    status: SmsStatus = Field(
        SmsStatus.QUEUED,
        description="Current delivery status of the SMS request"
    )
    max_retries: Optional[int] = Field(
        None,
        alias="maxRetries",
        ge=0,
        le=5,
        description="Maximum number of retry attempts if SMS delivery fails (0-5)"
    )
    retry_count: int = Field(
        0,
        alias="retryCount",
        ge=0,
        le=5,
        description="Current count of retry attempts made for this SMS request"
    )
    retry_delay_minutes: Optional[int] = Field(
        None,
        alias="retryDelayMinutes",
        gt=0,
        description="Delay in minutes between retry attempts for failed deliveries"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom metadata for campaign tracking"
    )


class CreateSmsRequest(BaseModel):
    """Schema for creating a new SMS request.

    Omits auto-generated fields (id, timestamps, audit fields) that are
    populated by the system upon creation.

    Example:
        ```python
        create_request = CreateSmsRequest(
            to="+12125551234",
            body="Your verification code is 123456"
        )
        ```
    """

    phone_configuration_id: Optional[str] = Field(
        None,
        alias="phoneConfigurationId",
        description="Phone configuration ID for sender number settings"
    )
    to: str = Field(
        ...,
        description="Recipient phone number in E.164 format"
    )
    from_number: Optional[str] = Field(
        None,
        alias="from",
        description="Sender phone number in E.164 format or short code (e.g., '12345') displayed to the recipient. Must be a verified SMS-enabled number or short code owned by the organization. Uses default from phoneConfigurationId if omitted."
    )
    body: str = Field(
        ...,
        description="Text content of the SMS message"
    )
    template_id: Optional[str] = Field(
        None,
        alias="templateId",
        description="Pre-defined SMS template ID"
    )
    variables: Optional[Dict[str, Any]] = Field(
        None,
        description="Template variable substitutions"
    )
    scheduled_at: Optional[int] = Field(
        None,
        alias="scheduledAt",
        description="Unix timestamp for scheduled delivery"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
        description="Linked conversation record ID"
    )
    status: SmsStatus = Field(SmsStatus.QUEUED)
    max_retries: Optional[int] = Field(None, alias="maxRetries", ge=0, le=5)
    retry_count: int = Field(0, alias="retryCount", ge=0, le=5)
    retry_delay_minutes: Optional[int] = Field(None, alias="retryDelayMinutes", gt=0)
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom metadata"
    )


class UpdateSmsRequest(CreateSmsRequest):
    """Schema for updating an existing SMS request."""

    id: str = Field(..., description="Unique identifier of the SmsRequest to update")


class SmsRequestResult(BaseModel):
    """Result schema for SMS request operations.

    Attributes:
        success: Whether the SMS request was successful.
        request: Original SMS request details.
        error_message: Error message if the request failed.
    """

    success: Optional[bool] = Field(
        default=False,
        description="Whether the SMS request was successful"
    )
    request: Optional[SmsRequest] = Field(
        None,
        description="Original SMS request details"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if the request failed"
    )


NumberRange = TypedDict(
    "NumberRange",
    {"from": Optional[int], "to": Optional[int]},
    total=False,
)


class SmsRequestFilters(TypedDict, total=False):
    """SMS request filter options."""

    search: Optional[str]
    phone_configuration_id: Optional[str]
    to: Optional[str]
    from_number: Optional[str]
    template_id: Optional[str]
    status: Optional[SmsStatus]
    service_conversation_config_id: Optional[str]
    scheduled_at_range: Optional[NumberRange]


class SmsRequestSorting(TypedDict):
    """SMS request sorting options."""

    field: Literal["createdAt", "scheduledAt", "status", "retryCount"]
    direction: Literal["asc", "desc"]


class SmsRequestQueryOptions(TypedDict, total=False):
    """SMS request query options."""

    page: int
    page_size: int
    filters: Optional[SmsRequestFilters]
    sorting: Optional[SmsRequestSorting]
