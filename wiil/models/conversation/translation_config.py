"""Translation configuration schema definitions for translation services.

Translation configurations manage real-time language translation sessions between participants speaking
different languages. Enables cross-language communication through speech-to-text transcription, translation,
and text-to-speech synthesis. Used for multilingual customer support, international business meetings,
and cross-border communications.
"""

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel, LanguageCode


class TranslationServiceRequest(BaseModel):
    """Translation service request schema.

    Request payload for initiating a real-time translation session between two participants speaking
    different languages. Specifies participant identifiers, their native languages, and optional
    configuration for the translation service provisioning.

    Architecture Context:
        - Extends: BaseModel with translation-specific fields
        - Creates: TranslationServiceLog when session is initiated
        - Participants: 1:N - One request can lead to multiple participant records
        - Session Tracking: session_id enables grouping related translation requests

    Translation Flow:
        1. Client submits TranslationServiceRequest with participant details
        2. System creates TranslationServiceLog and participant records
        3. Real-time translation session begins with bidirectional audio streaming
        4. Speech transcribed → translated → synthesized for each participant

    Use Cases:
        - Customer calling support in different language than agent
        - International business calls requiring real-time translation
        - Multilingual conference calls with language bridges
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    initiator_id: str = Field(
        ...,
        description="Unique identifier for the initiator participant who is requesting the translation service (typically the customer or caller starting the session)"
    )
    initiator_language_code: LanguageCode = Field(
        ...,
        description="ISO 639-1 language code of the initiator's native spoken language (e.g., 'en-US' for American English, 'es-MX' for Mexican Spanish, 'fr-FR' for French)"
    )
    participant_language_code: LanguageCode = Field(
        ...,
        description="ISO 639-1 language code of the other participant's native spoken language (e.g., 'ja-JP' for Japanese, 'de-DE' for German, 'zh-CN' for Mandarin Chinese)"
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for tracking and grouping related translation requests in multi-participant scenarios or session resumption"
    )
    translation_config_id: Optional[str] = Field(
        None,
        description="Optional translation configuration ID to use specific provisioning chain for this translation service (references ProvisioningConfigChain with isTranslation=true)"
    )


class CreateTranslationServiceRequest(PydanticBaseModel):
    """Schema for creating a new translation service request.
    Omits auto-generated fields (id, created_at, updated_at).
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    initiator_id: str = Field(
        ...,
        description="Unique identifier for the initiator participant who is requesting the translation service (typically the customer or caller starting the session)"
    )
    initiator_language_code: LanguageCode = Field(
        ...,
        description="ISO 639-1 language code of the initiator's native spoken language (e.g., 'en-US' for American English, 'es-MX' for Mexican Spanish, 'fr-FR' for French)"
    )
    participant_language_code: LanguageCode = Field(
        ...,
        description="ISO 639-1 language code of the other participant's native spoken language (e.g., 'ja-JP' for Japanese, 'de-DE' for German, 'zh-CN' for Mandarin Chinese)"
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for tracking and grouping related translation requests in multi-participant scenarios or session resumption"
    )
    translation_config_id: Optional[str] = Field(
        None,
        description="Optional translation configuration ID to use specific provisioning chain for this translation service (references ProvisioningConfigChain with isTranslation=true)"
    )


class TranslationConversationConfig(PydanticBaseModel):
    """Translation conversation configuration schema.

    Configuration details for an active translation session including WebRTC connection identifiers,
    channel information, and participant access credentials. Returned when a translation session is
    successfully initiated, providing clients with necessary connection parameters.

    Architecture Context:
        - Generated By: Translation service initialization endpoint
        - Used For: Establishing WebRTC connections for real-time audio streaming
        - Participants: Contains access credentials for both initiator and participant
        - Security: Tokens are short-lived and session-specific for secure communication

    WebRTC Connection:
        - sdrtn_id: Session Description for Real-Time Networking identifier
        - Enables peer-to-peer audio streaming with low latency
        - Supports bidirectional translation in real-time

    Participant Authentication:
        - Each participant receives unique access_id and token
        - Tokens authenticate WebRTC connections
        - Session-scoped credentials prevent unauthorized access
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    sdrtn_id: Optional[str] = Field(
        None,
        description="SDRTN (Session Description and Real-Time Networking) identifier for WebRTC connections enabling peer-to-peer audio streaming between participants"
    )
    channel_identifier: str = Field(
        ...,
        description="Unique identifier for the communication channel (phone number in E.164 format, WebRTC channel ID, or conference room identifier) used for routing and session tracking"
    )
    initiator_access_id: str = Field(
        ...,
        description="Unique access identifier for the initiator participant used to authenticate their WebRTC connection and track their audio stream"
    )
    initiator_token: str = Field(
        ...,
        description="Short-lived authentication token for the initiator's communication channel, grants access to the translation session (expires after session or timeout)"
    )
    participant_access_id: str = Field(
        ...,
        description="Unique access identifier for the other participant used to authenticate their WebRTC connection and track their audio stream"
    )
    participant_token: str = Field(
        ...,
        description="Short-lived authentication token for the participant's communication channel, grants access to the translation session (expires after session or timeout)"
    )
