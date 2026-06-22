"""Outbound email request and delivery tracking schema definitions.

Provides schemas for composing, scheduling, and tracking outbound emails sent through
AI-powered communication workflows. Supports HTML/text content, attachments, templates
with variable substitution, scheduled delivery, and comprehensive delivery status tracking.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict

from pydantic import EmailStr, Field

from wiil.models.base import BaseModel, EntityModel
from wiil.types.conversation_types import EmailStatus


class EmailRecipient(BaseModel):
    """Email recipient schema for To, CC, and BCC fields.

    Represents an email recipient with address and optional display name.
    Used in EmailRequest for specifying primary recipients, CC, and BCC lists.

    Attributes:
        email: Email address of the recipient in standard format (e.g., 'user@example.com').
            Must be a valid, deliverable email address.
        name: Optional display name for the recipient shown in email clients
            (e.g., 'John Smith'). When provided, email displays as
            'John Smith <user@example.com>'.

    Example:
        ```python
        recipient = EmailRecipient(
            email="john.smith@example.com",
            name="John Smith"
        )
        ```
    """

    email: EmailStr = Field(
        ...,
        description="Email address of the recipient in standard format"
    )
    name: Optional[str] = Field(
        None,
        description="Optional display name for the recipient shown in email clients"
    )


class EmailAttachment(BaseModel):
    """Email attachment schema for file attachments.

    Represents a file attachment to include with an outbound email.
    Content must be base64-encoded for safe JSON transmission.

    Size Limits:
        - Individual attachments typically limited to 10-25MB depending on provider
        - Total message size including all attachments should not exceed 25MB

    Attributes:
        filename: Name of the attachment file as displayed to the recipient
            (e.g., 'invoice.pdf', 'report.xlsx'). Include appropriate file extension.
        content: Base64-encoded file content. Encode binary files to base64 string
            for safe transmission in JSON payloads.
        content_type: MIME type of the attachment indicating file format
            (e.g., 'application/pdf', 'image/png', 'text/csv').

    Example:
        ```python
        import base64

        with open("invoice.pdf", "rb") as f:
            content = base64.b64encode(f.read()).decode()

        attachment = EmailAttachment(
            filename="invoice.pdf",
            content=content,
            content_type="application/pdf"
        )
        ```
    """

    filename: str = Field(
        ...,
        description="Name of the attachment file as displayed to the recipient"
    )
    content: str = Field(
        ...,
        description="Base64-encoded file content"
    )
    content_type: str = Field(
        ...,
        alias="contentType",
        description="MIME type of the attachment (e.g., 'application/pdf', 'image/png')"
    )


class EmailRequest(EntityModel):
    """Email request schema for composing outbound emails.

    Represents a complete outbound email request with content, recipients,
    attachments, and scheduling options. Supports HTML and plain text content,
    template-based composition with variable substitution, and scheduled delivery.

    Architecture Context:
        - Template Support: References EmailTemplate for structured content
        - Conversation Tracking: Links to ServiceConversationConfig for threading
        - Provider Integration: Works with SendGrid, SES, and other email services

    Attributes:
        email_configuration_id: Email configuration ID for sender settings, SMTP/API
            credentials, and domain authentication. When omitted, uses org default.
        template_id: Pre-defined email template ID for structured content with
            variable placeholders. Template content merged with variables field.
        to: Array of primary email recipients. At least one recipient required.
        cc: Array of carbon copy recipients who receive a copy with visibility
            to other recipients.
        bcc: Array of blind carbon copy recipients who receive a copy without
            visibility to other recipients.
        reply_to: Reply-to email address that receives responses when recipients
            reply to this email.
        subject: Email subject line. Supports variable substitution with {{variable}}.
        body_html: HTML content of the email body supporting rich formatting.
        body_text: Plain text alternative content for accessibility.
        variables: Template variable substitutions as key-value pairs.
        attachments: Array of file attachments to include with the email.
        scheduled_at: Unix timestamp in milliseconds for scheduled delivery.
        service_conversation_config_id: Linked conversation record ID for threading.
        metadata: Additional custom metadata for campaign tracking.

    Example:
        ```python
        email = EmailRequest(
            to=[EmailRecipient(email="customer@example.com", name="Customer")],
            subject="Your Order Confirmation - #{{order_id}}",
            body_html="<h1>Thank you, {{name}}!</h1><p>Your order is confirmed.</p>",
            variables={"order_id": "12345", "name": "John"}
        )
        ```
    """

    email_configuration_id: Optional[str] = Field(
        None,
        alias="emailConfigurationId",
        description="Email configuration ID for sender settings, API credentials, and domain authentication. May be provided or system falls back to default platform email."
    )
    configured_email_address: Optional[str] = Field(
        None,
        alias="configuredEmailAddress",
        description="Configured sender email address for this request. May be provided or system falls back to default platform email."
    )
    template_id: Optional[str] = Field(
        None,
        alias="templateId",
        description="Pre-defined email template ID for structured content"
    )
    to: List[EmailRecipient] = Field(
        ...,
        min_length=1,
        description="Array of primary email recipients (at least one required)"
    )
    cc: Optional[List[EmailRecipient]] = Field(
        None,
        description="Array of carbon copy recipients"
    )
    bcc: Optional[List[EmailRecipient]] = Field(
        None,
        description="Array of blind carbon copy recipients"
    )
    reply_to: Optional[str] = Field(
        None,
        alias="replyTo",
        description="Reply-to email address for responses"
    )
    subject: str = Field(
        ...,
        description="Email subject line (supports {{variable}} substitution)"
    )
    body_html: str = Field(
        ...,
        alias="bodyHtml",
        description="HTML content of the email body"
    )
    body_text: Optional[str] = Field(
        None,
        alias="bodyText",
        description="Plain text alternative content for accessibility"
    )
    variables: Optional[Dict[str, Any]] = Field(
        None,
        description="Template variable substitutions as key-value pairs"
    )
    attachments: Optional[List[EmailAttachment]] = Field(
        None,
        description="Array of file attachments (total size should not exceed 25MB)"
    )
    scheduled_at: Optional[int] = Field(
        None,
        alias="scheduledAt",
        description="Unix timestamp in milliseconds for scheduled delivery"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
        description="Linked conversation record ID for email thread tracking"
    )
    status: EmailStatus = Field(
        EmailStatus.QUEUED,
        description="Current delivery status of the email request"
    )
    max_retries: Optional[int] = Field(
        None,
        alias="maxRetries",
        ge=0,
        le=5,
        description="Maximum number of retry attempts if email delivery fails (0-5)"
    )
    retry_count: int = Field(
        0,
        alias="retryCount",
        ge=0,
        le=5,
        description="Current count of retry attempts made for this email request"
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


class CreateEmailRequest(BaseModel):
    """Schema for creating a new email request.

    Omits auto-generated fields (id, timestamps, audit fields) that are
    populated by the system upon creation.

    Example:
        ```python
        create_request = CreateEmailRequest(
            to=[EmailRecipient(email="customer@example.com")],
            subject="Welcome!",
            body_html="<h1>Welcome to our service!</h1>"
        )
        ```
    """

    email_configuration_id: Optional[str] = Field(None, alias="emailConfigurationId")
    configured_email_address: Optional[str] = Field(None, alias="configuredEmailAddress")
    template_id: Optional[str] = Field(None, alias="templateId")
    to: List[EmailRecipient] = Field(..., min_length=1)
    cc: Optional[List[EmailRecipient]] = Field(None)
    bcc: Optional[List[EmailRecipient]] = Field(None)
    reply_to: Optional[str] = Field(None, alias="replyTo")
    subject: str = Field(...)
    body_html: str = Field(..., alias="bodyHtml")
    body_text: Optional[str] = Field(None, alias="bodyText")
    variables: Optional[Dict[str, Any]] = Field(None)
    attachments: Optional[List[EmailAttachment]] = Field(None)
    scheduled_at: Optional[int] = Field(None, alias="scheduledAt")
    service_conversation_config_id: Optional[str] = Field(None, alias="serviceConversationConfigId")
    status: EmailStatus = Field(EmailStatus.QUEUED)
    max_retries: Optional[int] = Field(None, alias="maxRetries", ge=0, le=5)
    retry_count: int = Field(0, alias="retryCount", ge=0, le=5)
    retry_delay_minutes: Optional[int] = Field(None, alias="retryDelayMinutes", gt=0)
    metadata: Optional[Dict[str, Any]] = Field(None)


class UpdateEmailRequest(CreateEmailRequest):
    """Schema for updating an existing email request."""

    id: str = Field(..., description="Unique identifier of the EmailRequest to update")


class EmailRecord(EntityModel):
    """Email record model for delivery tracking."""

    email_request_id: str = Field(
        ...,
        alias="emailRequestId",
        description="Reference to the original EmailRequest this record tracks"
    )
    provider_message_id: str = Field(
        ...,
        alias="providerMessageId",
        description="Provider-specific message ID from the email service"
    )
    status: EmailStatus = Field(..., description="Current delivery status from provider webhooks")
    sent_at: Optional[int] = Field(None, alias="sentAt", description="Unix timestamp when email was sent")
    delivered_at: Optional[int] = Field(None, alias="deliveredAt", description="Unix timestamp when email was confirmed delivered")
    bounced_at: Optional[int] = Field(None, alias="bouncedAt", description="Unix timestamp when email bounced")
    error_code: Optional[str] = Field(None, alias="errorCode", description="Provider-specific error code if delivery failed")
    error_message: Optional[str] = Field(None, alias="errorMessage", description="Provider error message describing failure reason")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional provider-specific metadata from webhooks")


class EmailRequestResult(BaseModel):
    """Result schema for email request operations.

    Attributes:
        success: Whether the email request was successful.
        request: Original email request details.
        error_message: Error message if the request failed.
    """

    success: Optional[bool] = Field(
        default=False,
        description="Whether the email request was successful"
    )
    request: Optional[EmailRequest] = Field(
        None,
        description="Original email request details"
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


class EmailRequestFilters(TypedDict, total=False):
    """Email request filter options."""

    search: Optional[str]
    email_configuration_id: Optional[str]
    configured_email_address: Optional[str]
    template_id: Optional[str]
    status: Optional[EmailStatus]
    service_conversation_config_id: Optional[str]
    scheduled_at_range: Optional[NumberRange]


class EmailRequestSorting(TypedDict):
    """Email request sorting options."""

    field: Literal["createdAt", "scheduledAt", "status", "subject", "retryCount"]
    direction: Literal["asc", "desc"]


class EmailRequestQueryOptions(TypedDict, total=False):
    """Email request query options."""

    page: int
    page_size: int
    filters: Optional[EmailRequestFilters]
    sorting: Optional[EmailRequestSorting]


class EmailRecordFilters(TypedDict, total=False):
    """Email record filter options."""

    email_request_id: Optional[str]
    provider_message_id: Optional[str]
    status: Optional[EmailStatus]
    sent_at_range: Optional[NumberRange]
    delivered_at_range: Optional[NumberRange]


class EmailRecordSorting(TypedDict):
    """Email record sorting options."""

    field: Literal["createdAt", "status", "sentAt", "deliveredAt"]
    direction: Literal["asc", "desc"]


class EmailRecordQueryOptions(TypedDict, total=False):
    """Email record query options."""

    page: int
    page_size: int
    filters: Optional[EmailRecordFilters]
    sorting: Optional[EmailRecordSorting]
