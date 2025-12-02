"""Conversation models for WIIL SDK.

This module contains all conversation-related models including:
- Conversation configurations and management
- Message schemas (chat and email)
- Translation services and configurations
- Translation conversations and participants
"""

# Conversation configuration models
from wiil.models.conversation.conversation_config import (
    BaseConversationConfig,
    CallTransfer,
    ConversationStateHistory,
    ConversationSummary,
    DecommissionConfig,
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
    UserChatMessage,
    UserEmailMessage,
)

# Translation configuration models
from wiil.models.conversation.translation_config import (
    CreateTranslationServiceRequest,
    TranslationConversationConfig,
    TranslationServiceRequest,
)

# Translation conversation models
from wiil.models.conversation.translation_conversation import (
    CreateTranslationParticipant,
    CreateTranslationServiceLog,
    TranslationMessage,
    TranslationParticipant,
    TranslationServiceLog,
    UpdateTranslationParticipant,
    UpdateTranslationServiceLog,
)

__all__ = [
    # Conversation configuration models
    "BaseConversationConfig",
    "CallTransfer",
    "ConversationStateHistory",
    "ConversationSummary",
    "DecommissionConfig",
    "Message",
    "ServiceConversationConfig",
    # Conversation message models
    "AssistantChatMessage",
    "AssistantEmailMessage",
    "BaseChatMessage",
    "BaseEmailMessage",
    "ChatMessage",
    "ConversationMessage",
    "UserChatMessage",
    "UserEmailMessage",
    # Translation configuration models
    "CreateTranslationServiceRequest",
    "TranslationConversationConfig",
    "TranslationServiceRequest",
    # Translation conversation models
    "CreateTranslationParticipant",
    "CreateTranslationServiceLog",
    "TranslationMessage",
    "TranslationParticipant",
    "TranslationServiceLog",
    "UpdateTranslationParticipant",
    "UpdateTranslationServiceLog",
]
