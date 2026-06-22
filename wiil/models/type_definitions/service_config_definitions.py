"""Service configuration type definitions and enumerations.

This module mirrors src/core/type-definitions/service-config.definitions.ts
"""

from enum import Enum

from wiil.models.type_definitions.account_definitions import (
    BusinessSupportServices,
)


class DeploymentType(str, Enum):
    """Deployment type enumeration."""

    CALLS = "calls"
    SMS = "sms"
    WEB = "web"
    MOBILE = "mobile-app"
    WHATSAPP = "whatsapp"
    EMAIL = "email"


class DeploymentStatus(str, Enum):
    """Deployment status enumeration."""

    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class ProviderType(str, Enum):
    """Provider type enumeration."""

    TWILIO = "twilio"
    SIGNALWIRE = "signal-wire"
    TELNYX = "telnyx"
    MESSAGEBIRD = "messagebird"
    SNS = "sns"


class EmailProviderType(str, Enum):
    """Email provider type enumeration."""

    GOOGLE = "google"
    OUTLOOK = "outlook"
    SENDGRID = "sendgrid"
    SES = "ses"
    MAILGUN = "mailgun"
    POSTMARK = "postmark"
    SMTP = "smtp"


class PhonePurchaseStatus(str, Enum):
    """Phone purchase status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PhoneStatus(str, Enum):
    """Phone status enumeration."""

    ACTIVE = "ACTIVE"
    """Used in both SMS and Call channels."""

    INACTIVE = "INACTIVE"
    """Not used."""

    SMS_ACTIVE = "SMS_ACTIVE"
    """Used in SMS channel."""

    CALL_ACTIVE = "CALL_ACTIVE"
    """Used in Call channel."""


class PhoneNumberType(str, Enum):
    """Phone number type enumeration."""

    LOCAL = "local"
    TOLL_FREE = "toll-free"


class MobilePlatform(str, Enum):
    """Mobile platform enumeration."""

    IOS = "ios"
    ANDROID = "android"


class OttCommunicationType(str, Enum):
    """OTT communication type enumeration."""

    TEXT = "text"
    VOICE = "voice"
    UNIFIED = "unified"


class DeploymentProvisioningType(str, Enum):
    """Deployment provisioning type enumeration."""

    DIRECT = "direct"
    CHAINED = "chained"


class AssistantType(str, Enum):
    """Assistant type enumeration."""

    PHONE = "phone"
    WEB = "web"
    EMAIL = "email"
    GENERAL = "general"
    """For general purpose assistants not tied to a specific channel."""


class LLMType(str, Enum):
    """LLM type enumeration."""

    STS = "sts"
    TTS = "tts"
    STT = "stt"
    TRANSCRIBE = "transcribe"
    TEXT_PROCESSING = "text"
    MULTI_MODE = "multi_mode"


class SupportedProprietor(str, Enum):
    """Supported proprietor enumeration."""

    OPENAI = "OpenAI"
    GOOGLE = "Google"
    ANTHROPIC = "Anthropic"
    GROQ = "Groq"
    XAI = "xAI"
    DEEPGRAM = "Deepgram"
    ELEVENLABS = "ElevenLabs"
    DEEPSEEK = "DeepSeek"
    CARTESIA = "Cartesia"


class SupportedLLMKit(str, Enum):
    """Supported LLM kit enumeration."""

    OPEN_AI = "openai-kit"
    GOOGLE = "google-kit"
    ANTHROPIC = "anthropic-kit"
    GROQ = "groq-kit"
    XAI = "xai-kit"
    DEEPGRAM = "deepgram-kit"
    ELEVENLABS = "elevenlabs-kit"
    DEEPSEEK = "deepseek-kit"
    CARTESIA = "cartesia-kit"


class LLMRequestType(str, Enum):
    """LLM request type enumeration."""

    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    MULTIMODAL = "multimodal"


class AgentRoleTemplateIdentifier(str, Enum):
    """Agent role template identifier enumeration."""

    CUSTOMER_SUPPORT_GENERAL = "customer-support-general"
    TECHNICAL_SUPPORT_SPECIALIST = "technical-support-specialist"
    SALES_REPRESENTATIVE = "sales-representative"
    ONBOARDING_SPECIALIST = "onboarding-specialist"
    BILLING_SUPPORT_SPECIALIST = "billing-support-specialist"


# AgentCapabilities is an alias for BusinessSupportServices
AgentCapabilities = BusinessSupportServices
