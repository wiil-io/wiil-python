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

    COMPLETED = "completed"
    """Conversation completed"""

    FAILED = "failed"
    """Conversation failed"""

    ABANDONED = "abandoned"
    """Conversation abandoned"""

    TRANSFERRED = "transferred"
    """Conversation transferred"""


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

    MIXED = "mixed"
    """Mixed sentiment"""


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

    HUMAN_AGENT = "human_agent"
    """Human agent message"""

    SYSTEM = "system"
    """System-generated message"""


class SystemMessageEventType(str, Enum):
    """System message event type enumeration."""

    HANDOVER_REQUESTED = "handover_requested"
    HANDOVER_ACCEPTED = "handover_accepted"
    HANDOVER_COMPLETED = "handover_completed"
    HANDOVER_FAILED = "handover_failed"
    AGENT_JOINED = "agent_joined"
    AGENT_LEFT = "agent_left"
    CONVERSATION_TRANSFERRED = "conversation_transferred"


class CallRequestStatus(str, Enum):
    """Outbound call request status."""

    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScheduleType(str, Enum):
    """Schedule type for outbound calls."""

    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    RECURRING = "recurring"


class EmailStatus(str, Enum):
    """Email delivery status."""

    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    FAILED = "failed"
    COMPLAINED = "complained"


class SmsStatus(str, Enum):
    """SMS delivery status."""

    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    UNDELIVERED = "undelivered"


class OutboundTemplateChannel(str, Enum):
    """Outbound template channel enumeration."""

    EMAIL = "EMAIL"
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
