"""Conversation and messaging type definitions and enumerations."""

from enum import Enum


class ConversationEventType(str, Enum):
    """Conversation event type enumeration."""

    OTT_CALL_COMPLETED = "OTT_CALL_COMPLETED"
    """Over-the-top call completed event"""

    TELEPHONY_CALL_COMPLETED = "TELEPHONY_CALL_COMPLETED"
    """Telephony call completed event"""

    TRANSCRIPTION_COMPLETED = "TRANSCRIPTION_COMPLETED"
    """Transcription completed event"""

    LLM_INTERACTION_COMPLETED = "LLM_INTERACTION_COMPLETED"
    """LLM interaction completed event"""

    SMS_SENT = "SMS_SENT"
    """SMS sent event"""


class ServiceConversationType(str, Enum):
    """Service conversation type enumeration."""

    OTT_CALL = "OTT_CALL"
    """Over-the-top call conversation"""

    OTT_CHAT = "OTT_CHAT"
    """Over-the-top chat conversation"""

    TELEPHONY_CALL = "TELEPHONY_CALL"
    """Telephony call conversation"""

    SMS = "SMS"
    """SMS conversation"""

    EMAIL = "EMAIL"
    """Email conversation"""

    WHATSAPP = "WHATSAPP"
    """WhatsApp conversation"""

    TELEGRAM = "TELEGRAM"
    """Telegram conversation"""


class ConversationStatus(str, Enum):
    """Conversation status enumeration."""

    PENDING = "pending"
    """Conversation pending"""

    STARTED = "started"
    """Conversation started"""

    ACTIVE = "active"
    """Conversation active"""

    PAUSED = "paused"
    """Conversation paused"""

    ENDED = "ended"
    """Conversation ended"""

    SUMMARIZED = "summarized"
    """Conversation summarized"""

    UPDATED_SUMMARIZED = "updated_summarized"
    """Conversation summary updated"""


class TranslationDirection(str, Enum):
    """Translation direction enumeration."""

    BIDIRECTIONAL = "bidirectional"
    """Bidirectional translation (both directions)"""

    UNIDIRECTIONAL = "unidirectional"
    """Unidirectional translation (one direction only)"""


class ConversationSummarySentiment(str, Enum):
    """Conversation summary sentiment enumeration."""

    POSITIVE = "positive"
    """Positive sentiment"""

    NEUTRAL = "neutral"
    """Neutral sentiment"""

    NEGATIVE = "negative"
    """Negative sentiment"""


class ConversationDirection(str, Enum):
    """Conversation direction enumeration."""

    INBOUND = "inbound"
    """Inbound conversation"""

    OUTBOUND = "outbound"
    """Outbound conversation"""


class MessageType(str, Enum):
    """Message type enumeration."""

    USER = "user"
    """User message"""

    AGENT = "assistant"
    """Agent/Assistant message"""
