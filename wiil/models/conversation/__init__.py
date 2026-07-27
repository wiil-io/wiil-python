"""Conversation models for WIIL SDK.

This module contains all conversation-related models including:
- Conversation configurations and management
- Message schemas (chat and email)
- Outbound messaging requests (call, email, SMS)
- Translation sessions, participants, and transcripts
"""

# Conversation configuration models
from wiil.models.conversation.conversation_config import (
    BaseConversationConfig,
    CallTransfer,
    ConversationContext,
    ConversationFilters,
    ConversationQueryOptions,
    ConversationSorting,
    ConversationStateHistory,
    ConversationSummary,
    DateRange,
    DisplayMessage,
    Message,
    ServiceConversationConfig,
)

# Conversation message models
from wiil.models.conversation.conversation_message import (
    AssistantChatMessage,
    AssistantEmailMessage,
    BaseChatMessage,
    BaseEmailMessage,
    ChatMessage,
    ConversationMessage,
    HumanAgentChatMessage,
    HumanAgentEmailMessage,
    SystemMessage,
    UserChatMessage,
    UserEmailMessage,
)

# Outbound messaging models
from wiil.models.conversation.outbound_call import (
    BusinessCallRequest,
    CallRequestFilters,
    CallRequestQueryOptions,
    CallRequestSorting,
    CallingHours,
    CreateCallRequest,
    CallRequestResult,
    UpdateCallRequest,
)
from wiil.models.conversation.outbound_email import (
    CreateEmailRequest,
    EmailAttachment,
    EmailRecord,
    EmailRecordFilters,
    EmailRecordQueryOptions,
    EmailRecordSorting,
    EmailRecipient,
    EmailRequest,
    EmailRequestFilters,
    EmailRequestQueryOptions,
    EmailRequestResult,
    EmailRequestSorting,
    UpdateEmailRequest,
)
from wiil.models.conversation.outbound_sms import (
    CreateSmsRequest,
    SmsRequest,
    SmsRequestFilters,
    SmsRequestQueryOptions,
    SmsRequestResult,
    SmsRequestSorting,
    UpdateSmsRequest,
)
from wiil.models.conversation.outbound_template import (
    CreateEmailTemplate,
    CreateSmsTemplate,
    CreateWhatsappTemplate,
    EmailTemplate,
    OutboundTemplate,
    OutboundTemplateBase,
    OutboundTemplateFilters,
    OutboundTemplateQueryOptions,
    OutboundTemplateSorting,
    SmsTemplate,
    TemplateVariable,
    UpdateEmailTemplate,
    UpdateSmsTemplate,
    UpdateWhatsappTemplate,
    WhatsappTemplate,
)

# Translation conversation models
from wiil.models.conversation.translation_conversation import (
    # Session models
    TranslationSession,
    TranslationSessionStatus,
    TranslationSessionStateHistory,
    CreateTranslationSession,
    UpdateTranslationSession,
    TransitionTranslationSession,
    # Participant models
    TranslationParticipant,
    TranslationParticipantRole,
    CreateTranslationParticipant,
    UpdateTranslationParticipant,
    # Transcript entry models
    TranslationTranscriptEntry,
    CreateTranslationTranscriptEntry,
    # Request/response DTOs
    TranslationSessionRequest,
    TranslationSessionParticipantRequest,
    TranslationSessionInitiatorRequest,
    TranslationSessionAccess,
    TranslationParticipantAccess,
)

# Translation direction enum (from types to avoid duplication)
from wiil.types.conversation_types import TranslationDirection

__all__ = [
    # Conversation configuration models
    "BaseConversationConfig",
    "CallTransfer",
    "ConversationContext",
    "ConversationFilters",
    "ConversationQueryOptions",
    "ConversationSorting",
    "ConversationStateHistory",
    "ConversationSummary",
    "DateRange",
    "DisplayMessage",
    "Message",
    "ServiceConversationConfig",
    # Conversation message models
    "AssistantChatMessage",
    "AssistantEmailMessage",
    "BaseChatMessage",
    "BaseEmailMessage",
    "ChatMessage",
    "ConversationMessage",
    "HumanAgentChatMessage",
    "HumanAgentEmailMessage",
    "SystemMessage",
    "UserChatMessage",
    "UserEmailMessage",
    # Outbound messaging models
    "BusinessCallRequest",
    "CallRequestFilters",
    "CallRequestQueryOptions",
    "CallRequestSorting",
    "CallRequestResult",
    "CallingHours",
    "CreateCallRequest",
    "UpdateCallRequest",
    "CreateEmailRequest",
    "EmailRecord",
    "EmailRecordFilters",
    "EmailRecordQueryOptions",
    "EmailRecordSorting",
    "EmailAttachment",
    "EmailRecipient",
    "EmailRequest",
    "EmailRequestFilters",
    "EmailRequestQueryOptions",
    "EmailRequestResult",
    "EmailRequestSorting",
    "UpdateEmailRequest",
    "CreateSmsRequest",
    "SmsRequest",
    "SmsRequestFilters",
    "SmsRequestQueryOptions",
    "SmsRequestResult",
    "SmsRequestSorting",
    "UpdateSmsRequest",
    "CreateEmailTemplate",
    "CreateSmsTemplate",
    "CreateWhatsappTemplate",
    "EmailTemplate",
    "OutboundTemplate",
    "OutboundTemplateBase",
    "OutboundTemplateFilters",
    "OutboundTemplateQueryOptions",
    "OutboundTemplateSorting",
    "SmsTemplate",
    "TemplateVariable",
    "UpdateEmailTemplate",
    "UpdateSmsTemplate",
    "UpdateWhatsappTemplate",
    "WhatsappTemplate",
    # Translation session models
    "TranslationSession",
    "TranslationSessionStatus",
    "TranslationSessionStateHistory",
    "CreateTranslationSession",
    "UpdateTranslationSession",
    "TransitionTranslationSession",
    # Translation participant models
    "TranslationParticipant",
    "TranslationParticipantRole",
    "CreateTranslationParticipant",
    "UpdateTranslationParticipant",
    # Translation transcript models
    "TranslationTranscriptEntry",
    "CreateTranslationTranscriptEntry",
    # Translation request/response DTOs
    "TranslationSessionRequest",
    "TranslationSessionParticipantRequest",
    "TranslationSessionInitiatorRequest",
    "TranslationSessionAccess",
    "TranslationParticipantAccess",
    # Translation direction enum
    "TranslationDirection",
]
