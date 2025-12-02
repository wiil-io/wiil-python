"""Translation conversation schema definitions for real-time translation services.

Translation conversations manage the lifecycle, participants, and message history of real-time language
translation sessions. Tracks individual translation messages, participant metadata, session duration,
and conversation status for multilingual communication across language barriers.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel, LanguageCode
from wiil.types.conversation_types import ConversationStatus, TranslationDirection


class TranslationMessage(PydanticBaseModel):
    """Translation message schema - represents one translation interaction.

    Individual translation message capturing the complete translation pipeline from speaker's original speech
    to translated output for the listener. Tracks both source and target text, languages, participants, and
    the provisioning chain used for STT → Translation → TTS processing.

    Architecture Context:
        - Used In: TranslationServiceLog.transcribed_conversation_log array
        - Processing Pipeline: Speaker audio → STT (original_text) → Translation (translated_text) → TTS → Target participant
        - Provisioning: References ProvisioningConfigChain with isTranslation=true
        - Bidirectional: Each spoken utterance creates messages for both participants in their languages

    Translation Flow:
        1. Participant A speaks in Language A → captured as audio
        2. STT transcribes audio → original_text in Language A
        3. Translation model translates → translated_text in Language B
        4. TTS synthesizes translated_text → audio for Participant B
        5. TranslationMessage stored with both texts, languages, and metadata

    Metadata Examples:
        - audio_url: URL to original audio recording
        - confidence_score: STT transcription confidence (0-1)
        - processing_time_ms: Total pipeline latency
        - translation_model: LLM model used for translation
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    message_id: str = Field(
        ...,
        description="Unique identifier for this translation message (typically UUID) used for message ordering, deduplication, and reference tracking",
        alias="messageId"
    )
    speaker_participant_id: str = Field(
        ...,
        description="ID of the participant who spoke this message in their original language (references TranslationParticipant)",
        alias="speakerParticipantId"
    )
    target_participant_id: str = Field(
        ...,
        description="ID of the participant who will receive the translated message in their language (references TranslationParticipant)",
        alias="targetParticipantId"
    )
    original_text: Optional[str] = Field(
        None,
        description="Transcribed text from the speaker in their original language as output by STT model (e.g., 'Hello, how are you?' from English speaker)",
        alias="originalText"
    )
    translated_text: Optional[str] = Field(
        None,
        description="Translated text in the target participant's language as output by translation model (e.g., 'Hola, ¿cómo estás?' for Spanish listener)",
        alias="translatedText"
    )
    original_language: LanguageCode = Field(
        ...,
        description="ISO 639-1 language code of the original spoken message matching the speaker's native language (e.g., 'en-US', 'es-ES', 'fr-FR')",
        alias="originalLanguage"
    )
    target_language: LanguageCode = Field(
        ...,
        description="ISO 639-1 language code for the translation output matching the target participant's native language (e.g., 'ja-JP', 'de-DE', 'zh-CN')",
        alias="targetLanguage"
    )
    provisioning_config_id: str = Field(
        ...,
        description="ID of the provisioning configuration chain that processed this translation including STT, translation LLM, and TTS models (references ProvisioningConfigChain with isTranslation=true)",
        alias="provisioningConfigId"
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp in milliseconds when this message was processed through the translation pipeline, used for message ordering and latency analysis"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata as key-value pairs including audio recording URLs, STT confidence scores, processing times, translation model details, or quality metrics"
    )


class TranslationParticipant(BaseModel):
    """Translation participant schema.

    Represents an individual participant in a translation session including their language preferences,
    authentication credentials, role, and message history. Participants can be anchors (session initiators)
    or secondary participants joining the translation conversation.

    Architecture Context:
        - Extends: BaseModel with participant-specific fields
        - Relationship to Session: N:1 - Multiple participants in one translation session
        - Referenced By: TranslationMessage via speaker_participant_id and target_participant_id
        - Access Control: participant_token authenticates WebRTC connections

    Participant Roles:
        - Anchor (is_anchor=true): Session initiator, typically the customer or primary caller
        - Secondary (is_anchor=false): Joining participant, typically agent or secondary caller

    Message Storage:
        - transcriptions: Translation messages where this participant is either speaker or target
        - participant_transcribed_logs: Full conversation messages for audit and quality review

    Integration:
        - partner_participant_record_id links to external systems (CRM, HR, contact databases)
        - Enables unified participant profiles across multiple sessions
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    translation_service_log_id: Optional[str] = Field(
        None,
        description="ID of the translation service log this participant belongs to (N:1 relationship, references TranslationServiceLog)",
        alias="translationServiceLogId"
    )
    partner_participant_record_id: Optional[str] = Field(
        None,
        description="External partner or system participant record ID for integration with CRM, HR systems, or contact databases enabling unified participant profiles",
        alias="partnerParticipantRecordId"
    )
    name: Optional[str] = Field(
        None,
        description="Human-readable name of the participant for display in UI and logs (e.g., 'John Smith', 'Customer Support Agent')"
    )
    is_anchor: bool = Field(
        False,
        description="Flag indicating if this participant is the anchor/initiator of the session (true for session starter, false for joining participants)",
        alias="isAnchor"
    )
    native_language: str = Field(
        ...,
        min_length=2,
        max_length=5,
        description="ISO 639-1 language code of the participant's native spoken language (2-5 characters, e.g., 'en', 'en-US', 'es-MX') used for translation direction",
        alias="nativeLanguage"
    )
    participant_access_id: int = Field(
        ...,
        description="Unique numeric identifier for the participant used for WebRTC connection authentication and audio stream routing",
        alias="participantAccessId"
    )
    participant_token: str = Field(
        ...,
        description="Authentication token for the participant's WebRTC connection, short-lived credential for secure session access (expires after session)",
        alias="participantToken"
    )
    transcriptions: Optional[List[TranslationMessage]] = Field(
        None,
        description="Array of translation messages where this participant is either the speaker or target, populated for participant-specific message history views"
    )
    participant_transcribed_logs: Optional[List["ConversationMessage"]] = Field(
        None,
        description="Array of full conversation messages for this participant including both original and translated content for comprehensive audit logs and quality review",
        alias="participantTranscribedLogs"
    )


class CreateTranslationParticipant(PydanticBaseModel):
    """Schema for creating a new translation participant.
    Omits auto-generated fields (id, created_at, updated_at).
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    translation_service_log_id: Optional[str] = Field(
        None,
        description="ID of the translation service log this participant belongs to (N:1 relationship, references TranslationServiceLog)",
        alias="translationServiceLogId"
    )
    partner_participant_record_id: Optional[str] = Field(
        None,
        description="External partner or system participant record ID for integration with CRM, HR systems, or contact databases enabling unified participant profiles",
        alias="partnerParticipantRecordId"
    )
    name: Optional[str] = Field(
        None,
        description="Human-readable name of the participant for display in UI and logs (e.g., 'John Smith', 'Customer Support Agent')"
    )
    is_anchor: bool = Field(
        False,
        description="Flag indicating if this participant is the anchor/initiator of the session (true for session starter, false for joining participants)",
        alias="isAnchor"
    )
    native_language: str = Field(
        ...,
        min_length=2,
        max_length=5,
        description="ISO 639-1 language code of the participant's native spoken language (2-5 characters, e.g., 'en', 'en-US', 'es-MX') used for translation direction",
        alias="nativeLanguage"
    )
    participant_access_id: int = Field(
        ...,
        description="Unique numeric identifier for the participant used for WebRTC connection authentication and audio stream routing",
        alias="participantAccessId"
    )
    participant_token: str = Field(
        ...,
        description="Authentication token for the participant's WebRTC connection, short-lived credential for secure session access (expires after session)",
        alias="participantToken"
    )
    transcriptions: Optional[List[TranslationMessage]] = Field(
        None,
        description="Array of translation messages where this participant is either the speaker or target, populated for participant-specific message history views"
    )
    participant_transcribed_logs: Optional[List["ConversationMessage"]] = Field(
        None,
        description="Array of full conversation messages for this participant including both original and translated content for comprehensive audit logs and quality review",
        alias="participantTranscribedLogs"
    )


class UpdateTranslationParticipant(PydanticBaseModel):
    """Schema for updating an existing translation participant.
    All fields are optional except id.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for the translation participant")
    translation_service_log_id: Optional[str] = Field(
        None,
        description="ID of the translation service log this participant belongs to (N:1 relationship, references TranslationServiceLog)",
        alias="translationServiceLogId"
    )
    partner_participant_record_id: Optional[str] = Field(
        None,
        description="External partner or system participant record ID for integration with CRM, HR systems, or contact databases enabling unified participant profiles",
        alias="partnerParticipantRecordId"
    )
    name: Optional[str] = Field(
        None,
        description="Human-readable name of the participant for display in UI and logs (e.g., 'John Smith', 'Customer Support Agent')"
    )
    is_anchor: Optional[bool] = Field(
        None,
        description="Flag indicating if this participant is the anchor/initiator of the session (true for session starter, false for joining participants)",
        alias="isAnchor"
    )
    native_language: Optional[str] = Field(
        None,
        min_length=2,
        max_length=5,
        description="ISO 639-1 language code of the participant's native spoken language (2-5 characters, e.g., 'en', 'en-US', 'es-MX') used for translation direction",
        alias="nativeLanguage"
    )
    participant_access_id: Optional[int] = Field(
        None,
        description="Unique numeric identifier for the participant used for WebRTC connection authentication and audio stream routing",
        alias="participantAccessId"
    )
    participant_token: Optional[str] = Field(
        None,
        description="Authentication token for the participant's WebRTC connection, short-lived credential for secure session access (expires after session)",
        alias="participantToken"
    )
    transcriptions: Optional[List[TranslationMessage]] = Field(
        None,
        description="Array of translation messages where this participant is either the speaker or target, populated for participant-specific message history views"
    )
    participant_transcribed_logs: Optional[List["ConversationMessage"]] = Field(
        None,
        description="Array of full conversation messages for this participant including both original and translated content for comprehensive audit logs and quality review",
        alias="participantTranscribedLogs"
    )


class TranslationServiceLog(BaseModel):
    """Translation service log schema.

    Complete record of a translation session including participant information, session metadata, message
    history, and operational status. Primary entity for managing and tracking real-time translation services
    across organizations and projects.

    Architecture Context:
        - Extends: BaseModel with translation session-specific fields
        - Relationship to Participants: 1:N - One session has multiple participants
        - Relationship to Messages: 1:N - One session contains multiple translation messages
        - Scoped To: Organization and optionally Project for multi-tenant isolation

    Translation Directions:
        - BIDIRECTIONAL: Both participants receive translations (A→B and B→A simultaneously)
        - UNIDIRECTIONAL: Only one direction of translation (e.g., customer to agent only)

    Session Lifecycle:
        - ACTIVE: Translation session in progress with real-time audio streaming
        - COMPLETED: Session successfully concluded, participants disconnected
        - FAILED: Session encountered errors (connection lost, processing failures)
        - ABANDONED: Session abandoned by participants before completion

    Message Logging:
        - transcribed_conversation_log: Central message array for session-level history
        - log_transcription_in_participant_records: Controls whether messages also stored per-participant
        - Enables both session-wide and participant-specific message retrieval

    Use Cases:
        - Multilingual customer support call tracking
        - International business meeting transcripts
        - Cross-border service interaction logs
        - Quality assurance and compliance auditing
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    organization_id: str = Field(
        ...,
        description="ID of the organization requesting the translation service for multi-tenant isolation, billing attribution, and access control"
    )
    project_id: Optional[str] = Field(
        None,
        description="Optional ID of the project associated with the translation service for organizational grouping, reporting, and project-specific analytics (references Project)"
    )
    partner_initiator_id: str = Field(
        ...,
        description="Unique identifier for the initiator participant from external partner systems for cross-platform tracking and CRM integration"
    )
    partner_session_id: Optional[str] = Field(
        None,
        description="Optional external session ID for tracking the translation session in partner systems, enables correlation with external call/meeting records"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        description="SDRTN (Session Description and Real-Time Networking) identifier for WebRTC connections enabling low-latency peer-to-peer audio streaming between participants"
    )
    translation_config_id: Optional[str] = Field(
        None,
        description="ID of the translation configuration chain to use for this service including STT, translation LLM, and TTS models (references ProvisioningConfigChain with isTranslation=true)",
        alias="translationConfigId"
    )
    participants: Optional[List[str]] = Field(
        None,
        description="Array of participant IDs involved in this translation session (references TranslationParticipant records, typically 2 for standard sessions, more for conference scenarios)"
    )
    duration_in_seconds: int = Field(
        60,
        description="Duration of the translation session in seconds for billing calculations, analytics reporting, and session quality metrics (default: 60 for minimum billing)",
        alias="durationInSeconds"
    )
    status: ConversationStatus = Field(
        ConversationStatus.ACTIVE,
        description="Current operational status of the translation session (ACTIVE: in progress, COMPLETED: concluded, FAILED: errors, ABANDONED: participants disconnected prematurely)"
    )
    direction: TranslationDirection = Field(
        TranslationDirection.BIDIRECTIONAL,
        description="Translation direction mode (BIDIRECTIONAL: both participants receive translations simultaneously, UNIDIRECTIONAL: one-way translation only for specific use cases)"
    )
    transcribed_conversation_log: Optional[List[TranslationMessage]] = Field(
        None,
        description="Array of translation messages capturing the complete conversation history with original and translated text for both participants, used for session playback and audit",
        alias="transcribedConversationLog"
    )
    log_transcription_in_participant_records: bool = Field(
        False,
        description="Flag controlling whether translation messages are also stored in individual participant records (true for participant-specific history, false for session-only storage to reduce duplication)",
        alias="logTranscriptionInParticipantRecords"
    )
    translation_summary: Optional[str] = Field(
        None,
        description="Optional AI-generated summary of the translation session including key discussion points, outcomes, and quality assessment for reporting and analytics",
        alias="translationSummary"
    )
    created_day: Optional[str] = Field(
        None,
        description="The day the translation session was created in YYYY-MM-DD ISO format for daily aggregation queries, analytics partitioning, and billing period grouping"
    )


class CreateTranslationServiceLog(PydanticBaseModel):
    """Schema for creating a new translation service log.
    Omits auto-generated fields (id, created_at, updated_at).
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    organization_id: str = Field(
        ...,
        description="ID of the organization requesting the translation service for multi-tenant isolation, billing attribution, and access control"
    )
    project_id: Optional[str] = Field(
        None,
        description="Optional ID of the project associated with the translation service for organizational grouping, reporting, and project-specific analytics (references Project)"
    )
    partner_initiator_id: str = Field(
        ...,
        description="Unique identifier for the initiator participant from external partner systems for cross-platform tracking and CRM integration"
    )
    partner_session_id: Optional[str] = Field(
        None,
        description="Optional external session ID for tracking the translation session in partner systems, enables correlation with external call/meeting records"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        description="SDRTN (Session Description and Real-Time Networking) identifier for WebRTC connections enabling low-latency peer-to-peer audio streaming between participants"
    )
    translation_config_id: Optional[str] = Field(
        None,
        description="ID of the translation configuration chain to use for this service including STT, translation LLM, and TTS models (references ProvisioningConfigChain with isTranslation=true)",
        alias="translationConfigId"
    )
    participants: Optional[List[str]] = Field(
        None,
        description="Array of participant IDs involved in this translation session (references TranslationParticipant records, typically 2 for standard sessions, more for conference scenarios)"
    )
    duration_in_seconds: int = Field(
        60,
        description="Duration of the translation session in seconds for billing calculations, analytics reporting, and session quality metrics (default: 60 for minimum billing)",
        alias="durationInSeconds"
    )
    status: ConversationStatus = Field(
        ConversationStatus.ACTIVE,
        description="Current operational status of the translation session (ACTIVE: in progress, COMPLETED: concluded, FAILED: errors, ABANDONED: participants disconnected prematurely)"
    )
    direction: TranslationDirection = Field(
        TranslationDirection.BIDIRECTIONAL,
        description="Translation direction mode (BIDIRECTIONAL: both participants receive translations simultaneously, UNIDIRECTIONAL: one-way translation only for specific use cases)"
    )
    transcribed_conversation_log: Optional[List[TranslationMessage]] = Field(
        None,
        description="Array of translation messages capturing the complete conversation history with original and translated text for both participants, used for session playback and audit",
        alias="transcribedConversationLog"
    )
    log_transcription_in_participant_records: bool = Field(
        False,
        description="Flag controlling whether translation messages are also stored in individual participant records (true for participant-specific history, false for session-only storage to reduce duplication)",
        alias="logTranscriptionInParticipantRecords"
    )
    translation_summary: Optional[str] = Field(
        None,
        description="Optional AI-generated summary of the translation session including key discussion points, outcomes, and quality assessment for reporting and analytics",
        alias="translationSummary"
    )
    created_day: Optional[str] = Field(
        None,
        description="The day the translation session was created in YYYY-MM-DD ISO format for daily aggregation queries, analytics partitioning, and billing period grouping"
    )


class UpdateTranslationServiceLog(PydanticBaseModel):
    """Schema for updating an existing translation service log.
    All fields are optional except id.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for the translation service log")
    organization_id: Optional[str] = Field(
        None,
        description="ID of the organization requesting the translation service for multi-tenant isolation, billing attribution, and access control"
    )
    project_id: Optional[str] = Field(
        None,
        description="Optional ID of the project associated with the translation service for organizational grouping, reporting, and project-specific analytics (references Project)"
    )
    partner_initiator_id: Optional[str] = Field(
        None,
        description="Unique identifier for the initiator participant from external partner systems for cross-platform tracking and CRM integration"
    )
    partner_session_id: Optional[str] = Field(
        None,
        description="Optional external session ID for tracking the translation session in partner systems, enables correlation with external call/meeting records"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        description="SDRTN (Session Description and Real-Time Networking) identifier for WebRTC connections enabling low-latency peer-to-peer audio streaming between participants"
    )
    translation_config_id: Optional[str] = Field(
        None,
        description="ID of the translation configuration chain to use for this service including STT, translation LLM, and TTS models (references ProvisioningConfigChain with isTranslation=true)",
        alias="translationConfigId"
    )
    participants: Optional[List[str]] = Field(
        None,
        description="Array of participant IDs involved in this translation session (references TranslationParticipant records, typically 2 for standard sessions, more for conference scenarios)"
    )
    duration_in_seconds: Optional[int] = Field(
        None,
        description="Duration of the translation session in seconds for billing calculations, analytics reporting, and session quality metrics (default: 60 for minimum billing)",
        alias="durationInSeconds"
    )
    status: Optional[ConversationStatus] = Field(
        None,
        description="Current operational status of the translation session (ACTIVE: in progress, COMPLETED: concluded, FAILED: errors, ABANDONED: participants disconnected prematurely)"
    )
    direction: Optional[TranslationDirection] = Field(
        None,
        description="Translation direction mode (BIDIRECTIONAL: both participants receive translations simultaneously, UNIDIRECTIONAL: one-way translation only for specific use cases)"
    )
    transcribed_conversation_log: Optional[List[TranslationMessage]] = Field(
        None,
        description="Array of translation messages capturing the complete conversation history with original and translated text for both participants, used for session playback and audit",
        alias="transcribedConversationLog"
    )
    log_transcription_in_participant_records: Optional[bool] = Field(
        None,
        description="Flag controlling whether translation messages are also stored in individual participant records (true for participant-specific history, false for session-only storage to reduce duplication)",
        alias="logTranscriptionInParticipantRecords"
    )
    translation_summary: Optional[str] = Field(
        None,
        description="Optional AI-generated summary of the translation session including key discussion points, outcomes, and quality assessment for reporting and analytics",
        alias="translationSummary"
    )
    created_day: Optional[str] = Field(
        None,
        description="The day the translation session was created in YYYY-MM-DD ISO format for daily aggregation queries, analytics partitioning, and billing period grouping"
    )


# Forward reference resolution
from wiil.models.conversation.conversation_message import ConversationMessage  # noqa: E402

TranslationParticipant.model_rebuild()
CreateTranslationParticipant.model_rebuild()
UpdateTranslationParticipant.model_rebuild()
