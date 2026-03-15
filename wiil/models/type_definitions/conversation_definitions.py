"""Conversation type definitions and enumerations.

This module mirrors src/core/type-definitions/conversation.type.definition.ts
"""

from enum import Enum


class ConversationEventType(str, Enum):
    """Conversation event type enumeration."""

    OTT_CALL_COMPLETED = "OTT_CALL_COMPLETED"
    TELEPHONY_CALL_COMPLETED = "TELEPHONY_CALL_COMPLETED"
    TRANSCRIPTION_COMPLETED = "TRANSCRIPTION_COMPLETED"
    LLM_INTERACTION_COMPLETED = "LLM_INTERACTION_COMPLETED"
    SMS_SENT = "SMS_SENT"


class ServiceConversationType(str, Enum):
    """Service conversation type enumeration."""

    OTT_CALL = "OTT_CALL"
    OTT_CHAT = "OTT_CHAT"
    TELEPHONY_CALL = "TELEPHONY_CALL"
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"


class ConversationStatus(str, Enum):
    """Conversation status enumeration."""

    PENDING = "pending"
    STARTED = "started"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    SUMMARIZED = "summarized"
    UPDATED_SUMMARIZED = "updated_summarized"


class TranslationDirection(str, Enum):
    """Translation direction enumeration."""

    BIDIRECTIONAL = "bidirectional"
    UNIDIRECTIONAL = "unidirectional"


class ConversationSummarySentiment(str, Enum):
    """Conversation summary sentiment enumeration."""

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
