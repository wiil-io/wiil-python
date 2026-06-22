"""Outbound template schema definitions for reusable message templates."""

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.types.conversation_types import OutboundTemplateChannel


class TemplateVariable(BaseModel):
    """Template variable placeholder definition."""

    key: str = Field(..., min_length=1, description="Variable key/name")
    required: bool = Field(False, description="Whether variable must be provided")
    description: Optional[str] = Field(None, description="Variable description")
    default_value: Optional[str] = Field(
        None,
        alias="defaultValue",
        description="Default value if not provided"
    )


class OutboundTemplateBase(EntityModel):
    """Base outbound template model."""

    name: str = Field(..., min_length=1, description="Template display name")
    code: str = Field(..., min_length=1, description="Unique template code")
    channel: OutboundTemplateChannel = Field(..., description="Communication channel")
    is_active: bool = Field(True, alias="isActive", description="Whether template is active")
    description: Optional[str] = Field(None, description="Template description")
    variables: List[TemplateVariable] = Field(default_factory=list, description="Template variables")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class EmailTemplate(OutboundTemplateBase):
    """Outbound email template."""

    channel: Literal[OutboundTemplateChannel.EMAIL] = Field(
        OutboundTemplateChannel.EMAIL,
        description="Email channel identifier"
    )
    subject_template: str = Field(
        ...,
        alias="subjectTemplate",
        min_length=1,
        description="Email subject template"
    )
    body_html_template: str = Field(
        ...,
        alias="bodyHtmlTemplate",
        min_length=1,
        description="Email HTML body template"
    )
    body_text_template: Optional[str] = Field(
        None,
        alias="bodyTextTemplate",
        description="Plain text body template"
    )
    default_reply_to: Optional[str] = Field(
        None,
        alias="defaultReplyTo",
        description="Default reply-to email address"
    )


class SmsTemplate(OutboundTemplateBase):
    """Outbound SMS template."""

    channel: Literal[OutboundTemplateChannel.SMS] = Field(
        OutboundTemplateChannel.SMS,
        description="SMS channel identifier"
    )
    body_template: str = Field(
        ...,
        alias="bodyTemplate",
        min_length=1,
        description="SMS message body template"
    )


class WhatsappTemplate(OutboundTemplateBase):
    """Outbound WhatsApp template."""

    channel: Literal[OutboundTemplateChannel.WHATSAPP] = Field(
        OutboundTemplateChannel.WHATSAPP,
        description="WhatsApp channel identifier"
    )
    body_template: str = Field(
        ...,
        alias="bodyTemplate",
        min_length=1,
        description="WhatsApp message body template"
    )


OutboundTemplate = Union[EmailTemplate, SmsTemplate, WhatsappTemplate]


class CreateEmailTemplate(BaseModel):
    """Schema for creating an email template."""

    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    channel: Literal[OutboundTemplateChannel.EMAIL] = Field(OutboundTemplateChannel.EMAIL)
    is_active: bool = Field(True, alias="isActive")
    description: Optional[str] = Field(None)
    variables: List[TemplateVariable] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(None)
    subject_template: str = Field(..., alias="subjectTemplate", min_length=1)
    body_html_template: str = Field(..., alias="bodyHtmlTemplate", min_length=1)
    body_text_template: Optional[str] = Field(None, alias="bodyTextTemplate")
    default_reply_to: Optional[str] = Field(None, alias="defaultReplyTo")


class CreateSmsTemplate(BaseModel):
    """Schema for creating an SMS template."""

    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    channel: Literal[OutboundTemplateChannel.SMS] = Field(OutboundTemplateChannel.SMS)
    is_active: bool = Field(True, alias="isActive")
    description: Optional[str] = Field(None)
    variables: List[TemplateVariable] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(None)
    body_template: str = Field(..., alias="bodyTemplate", min_length=1)


class CreateWhatsappTemplate(BaseModel):
    """Schema for creating a WhatsApp template."""

    name: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    channel: Literal[OutboundTemplateChannel.WHATSAPP] = Field(OutboundTemplateChannel.WHATSAPP)
    is_active: bool = Field(True, alias="isActive")
    description: Optional[str] = Field(None)
    variables: List[TemplateVariable] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(None)
    body_template: str = Field(..., alias="bodyTemplate", min_length=1)


class UpdateEmailTemplate(CreateEmailTemplate):
    """Schema for updating an email template."""

    id: str = Field(..., description="Unique identifier of the EmailTemplate to update")


class UpdateSmsTemplate(CreateSmsTemplate):
    """Schema for updating an SMS template."""

    id: str = Field(..., description="Unique identifier of the SmsTemplate to update")


class UpdateWhatsappTemplate(CreateWhatsappTemplate):
    """Schema for updating a WhatsApp template."""

    id: str = Field(..., description="Unique identifier of the WhatsappTemplate to update")


class OutboundTemplateFilters(TypedDict, total=False):
    """Outbound template query filters."""

    search: Optional[str]
    channel: Optional[OutboundTemplateChannel]
    is_active: Optional[bool]
    tags: Optional[List[str]]


class OutboundTemplateSorting(TypedDict):
    """Outbound template sorting options."""

    field: Literal["name", "code", "channel", "createdAt", "updatedAt"]
    direction: Literal["asc", "desc"]


class OutboundTemplateQueryOptions(TypedDict, total=False):
    """Outbound template pagination/query options."""

    page: int
    page_size: int
    filters: Optional[OutboundTemplateFilters]
    sorting: Optional[OutboundTemplateSorting]
