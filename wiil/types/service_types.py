"""Service configuration type definitions and enumerations."""

from enum import Enum


class DeploymentType(str, Enum):
    """Deployment type enumeration."""

    CALLS = "calls"
    """Voice calls deployment"""

    SMS = "sms"
    """SMS deployment"""

    WEB = "web"
    """Web deployment"""

    MOBILE = "mobile-app"
    """Mobile app deployment"""

    WHATSAPP = "whatsapp"
    """WhatsApp deployment"""

    EMAIL = "email"
    """Email deployment"""


class DeploymentStatus(str, Enum):
    """Deployment status enumeration."""

    PENDING = "pending"
    """Deployment pending"""

    ACTIVE = "active"
    """Deployment active"""

    PAUSED = "paused"
    """Deployment paused"""

    ARCHIVED = "archived"
    """Deployment archived"""


class ProviderType(str, Enum):
    """Telephony provider type enumeration."""

    TWILIO = "twilio"
    """Twilio provider"""

    SIGNALWIRE = "signal-wire"
    """SignalWire provider"""

    TELNYX = "telnyx"
    """Telnyx provider"""


class PhonePurchaseStatus(str, Enum):
    """Phone number purchase status."""

    PENDING = "pending"
    """Purchase pending"""

    COMPLETED = "completed"
    """Purchase completed"""

    FAILED = "failed"
    """Purchase failed"""

    CANCELLED = "cancelled"
    """Purchase cancelled"""


class PhoneStatus(str, Enum):
    """Phone number status enumeration."""

    ACTIVE = "ACTIVE"
    """Active for both SMS and calls"""

    INACTIVE = "INACTIVE"
    """Inactive (not used)"""

    SMS_ACTIVE = "SMS_ACTIVE"
    """Active for SMS channel only"""

    CALL_ACTIVE = "CALL_ACTIVE"
    """Active for call channel only"""


class PhoneNumberType(str, Enum):
    """Phone number type enumeration."""

    LOCAL = "local"
    """Local phone number"""

    TOLL_FREE = "toll-free"
    """Toll-free phone number"""


class MobilePlatform(str, Enum):
    """Mobile platform enumeration."""

    IOS = "ios"
    """iOS platform"""

    ANDROID = "android"
    """Android platform"""


class OttCommunicationType(str, Enum):
    """Over-the-top communication type."""

    TEXT = "text"
    """Text communication"""

    VOICE = "voice"
    """Voice communication"""

    UNIFIED = "unified"
    """Unified text and voice"""


class DeploymentProvisioningType(str, Enum):
    """Deployment provisioning type."""

    DIRECT = "direct"
    """Direct provisioning"""

    CHAINED = "chained"
    """Chained provisioning"""


class AssistantType(str, Enum):
    """Assistant channel specialization type."""

    PHONE = "phone"
    """Phone-optimized assistant"""

    WEB = "web"
    """Web-optimized assistant"""

    EMAIL = "email"
    """Email-optimized assistant"""

    GENERAL = "general"
    """General multi-channel assistant (not tied to a specific channel)"""


class LLMType(str, Enum):
    """LLM operational mode type."""

    STS = "sts"
    """Speech-to-speech"""

    TTS = "tts"
    """Text-to-speech"""

    STT = "stt"
    """Speech-to-text"""

    TRANSCRIBE = "transcribe"
    """Transcription mode"""

    TEXT_PROCESSING = "text"
    """Text processing mode"""

    MULTI_MODE = "multi_mode"
    """Multi-modal (text and voice)"""


class SupportedProprietor(str, Enum):
    """Supported LLM model proprietor."""

    OPENAI = "OpenAI"
    """OpenAI"""

    GOOGLE = "Google"
    """Google"""

    ANTHROPIC = "Anthropic"
    """Anthropic"""

    GROQ = "Groq"
    """Groq"""

    DEEPGRAM = "Deepgram"
    """Deepgram"""

    ELEVENLABS = "ElevenLabs"
    """ElevenLabs"""

    DEEPSEEK = "DeepSeek"
    """DeepSeek"""

    CARTESIA = "Cartesia"
    """Cartesia"""


class SupportedLLMKit(str, Enum):
    """Supported LLM integration kit."""

    OPEN_AI = "openai-kit"
    """OpenAI kit"""

    GOOGLE = "google-kit"
    """Google kit"""

    ANTHROPIC = "anthropic-kit"
    """Anthropic kit"""

    GROQ = "groq-kit"
    """Groq kit"""

    DEEPGRAM = "deepgram-kit"
    """Deepgram kit"""

    ELEVENLABS = "elevenlabs-kit"
    """ElevenLabs kit"""

    DEEPSEEK = "deepseek-kit"
    """DeepSeek kit"""

    CARTESIA = "cartesia-kit"
    """Cartesia kit"""


class ModelProprietor(str, Enum):
    """Model proprietor enumeration."""

    OPENAI = "OpenAI"
    """OpenAI"""

    GOOGLE = "Google"
    """Google"""

    ANTHROPIC = "Anthropic"
    """Anthropic"""

    GROQ = "Groq"
    """Groq"""

    DEEPGRAM = "Deepgram"
    """Deepgram"""

    ELEVENLABS = "ElevenLabs"
    """ElevenLabs"""

    DEEPSEEK = "DeepSeek"
    """DeepSeek"""

    CARTESIA = "Cartesia"
    """Cartesia"""


class LLMRequestType(str, Enum):
    """LLM request type enumeration."""

    TEXT = "text"
    """Text request"""

    AUDIO = "audio"
    """Audio request"""

    IMAGE = "image"
    """Image request"""

    VIDEO = "video"
    """Video request"""

    MULTIMODAL = "multimodal"
    """Multimodal request"""
