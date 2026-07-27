"""Translation conversation schema definitions for real-time translation services.

This module defines schemas for translation sessions, participants, transcript entries,
and request/response DTOs for real-time language translation.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel, LanguageCode
from wiil.types.conversation_types import TranslationDirection


class TranslationSessionStatus(str, Enum):
    """Translation session lifecycle status."""

    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TranslationParticipantRole(str, Enum):
    """Role a participant plays within a translation session."""

    INITIATOR = "initiator"
    PARTICIPANT = "participant"


class TranslationSessionStateHistory(BaseModel):
    """A single lifecycle transition entry in a session's ordered state history."""

    status: TranslationSessionStatus = Field(
        ...,
        description="Lifecycle status at this point in time"
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp when this status was set"
    )
    reason: Optional[str] = Field(
        None,
        description="Reason for the status transition"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional transition context"
    )


class TranslationSession(EntityModel):
    """Durable root for a participant-to-participant translation session."""

    project_id: Optional[str] = Field(
        None,
        alias="projectId",
        description="Project associated with this translation session"
    )
    external_initiator_id: str = Field(
        ...,
        alias="externalInitiatorId",
        description="External identifier of the party that initiated the session"
    )
    external_session_id: Optional[str] = Field(
        None,
        alias="externalSessionId",
        description="External session identifier supplied by the initiating system"
    )
    translation_config_id: Optional[str] = Field(
        None,
        alias="translationConfigId",
        description="Translation configuration used by this session"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        alias="sdrtnId",
        description="Real-time networking session identifier"
    )
    direction: TranslationDirection = Field(
        TranslationDirection.BIDIRECTIONAL,
        description="Permitted translation direction"
    )
    status: TranslationSessionStatus = Field(
        TranslationSessionStatus.PENDING,
        description="Current translation session lifecycle status"
    )
    started_at: Optional[int] = Field(
        None,
        alias="startedAt",
        description="Unix timestamp when translation started"
    )
    ended_at: Optional[int] = Field(
        None,
        alias="endedAt",
        description="Unix timestamp when translation ended"
    )
    duration_in_seconds: Optional[int] = Field(
        None,
        ge=0,
        alias="durationInSeconds",
        description="Total active translation duration in seconds"
    )
    summary: Optional[str] = Field(
        None,
        description="Optional summary of the completed translation session"
    )
    state_history: Optional[List[TranslationSessionStateHistory]] = Field(
        None,
        alias="stateHistory",
        description="Ordered lifecycle transition history"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional implementation-specific session metadata"
    )


class CreateTranslationSession(BaseModel):
    """Creation payload for a new translation session."""

    project_id: Optional[str] = Field(
        None,
        alias="projectId",
        description="Project associated with this translation session"
    )
    external_initiator_id: str = Field(
        ...,
        alias="externalInitiatorId",
        description="External identifier of the party that initiated the session"
    )
    external_session_id: Optional[str] = Field(
        None,
        alias="externalSessionId",
        description="External session identifier supplied by the initiating system"
    )
    translation_config_id: Optional[str] = Field(
        None,
        alias="translationConfigId",
        description="Translation configuration used by this session"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        alias="sdrtnId",
        description="Real-time networking session identifier"
    )
    direction: TranslationDirection = Field(
        TranslationDirection.BIDIRECTIONAL,
        description="Permitted translation direction"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional implementation-specific session metadata"
    )


class UpdateTranslationSession(BaseModel):
    """Mutable translation session fields."""

    id: str = Field(
        ...,
        description="Translation session ID to update"
    )
    project_id: Optional[str] = Field(
        None,
        alias="projectId",
        description="Project associated with this translation session"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        alias="sdrtnId",
        description="Real-time networking session identifier"
    )
    summary: Optional[str] = Field(
        None,
        description="Optional summary of the completed translation session"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional implementation-specific session metadata"
    )


class TransitionTranslationSession(BaseModel):
    """Command for changing a translation session's lifecycle status."""

    id: str = Field(
        ...,
        description="Translation session ID to transition"
    )
    status: TranslationSessionStatus = Field(
        ...,
        description="Lifecycle status to apply"
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp of the lifecycle transition"
    )
    reason: Optional[str] = Field(
        None,
        description="Reason for the lifecycle transition"
    )
    duration_in_seconds: Optional[int] = Field(
        None,
        ge=0,
        alias="durationInSeconds",
        description="Final active duration when ending the session"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional transition context"
    )


class TranslationParticipant(EntityModel):
    """A participant in a translation session."""

    translation_session_id: str = Field(
        ...,
        alias="translationSessionId",
        description="Translation session this participant belongs to"
    )
    external_participant_id: Optional[str] = Field(
        None,
        alias="externalParticipantId",
        description="Participant identifier supplied by the integrating system"
    )
    display_name: Optional[str] = Field(
        None,
        alias="displayName",
        description="Participant display name"
    )
    role: TranslationParticipantRole = Field(
        ...,
        description="Participant role within the translation session"
    )
    language: LanguageCode = Field(
        ...,
        description="Participant's spoken language"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional implementation-specific participant metadata"
    )


class CreateTranslationParticipant(BaseModel):
    """Creation payload for a new translation participant."""

    translation_session_id: str = Field(
        ...,
        alias="translationSessionId",
        description="Translation session this participant belongs to"
    )
    external_participant_id: Optional[str] = Field(
        None,
        alias="externalParticipantId",
        description="Participant identifier supplied by the integrating system"
    )
    display_name: Optional[str] = Field(
        None,
        alias="displayName",
        description="Participant display name"
    )
    role: TranslationParticipantRole = Field(
        ...,
        description="Participant role within the translation session"
    )
    language: LanguageCode = Field(
        ...,
        description="Participant's spoken language"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional implementation-specific participant metadata"
    )


class UpdateTranslationParticipant(BaseModel):
    """Mutable participant fields."""

    id: str = Field(
        ...,
        description="Translation participant ID to update"
    )
    display_name: Optional[str] = Field(
        None,
        alias="displayName",
        description="Participant display name"
    )
    language: Optional[LanguageCode] = Field(
        None,
        description="Participant's spoken language"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional implementation-specific participant metadata"
    )


class TranslationTranscriptEntry(EntityModel):
    """An immutable completed transcript entry within a translation session."""

    translation_session_id: str = Field(
        ...,
        alias="translationSessionId",
        description="Translation session this transcript entry belongs to"
    )
    sequence_number: int = Field(
        ...,
        gt=0,
        alias="sequenceNumber",
        description="Monotonic sequence number ordering this entry within the session"
    )
    speaker_participant_id: str = Field(
        ...,
        alias="speakerParticipantId",
        description="Participant who produced the source utterance"
    )
    target_participant_id: str = Field(
        ...,
        alias="targetParticipantId",
        description="Participant for whom the utterance was translated"
    )
    source_text: str = Field(
        ...,
        min_length=1,
        alias="sourceText",
        description="Transcribed source-language text"
    )
    translated_text: str = Field(
        ...,
        min_length=1,
        alias="translatedText",
        description="Completed target-language translation"
    )
    source_language: LanguageCode = Field(
        ...,
        alias="sourceLanguage",
        description="Language of the source utterance"
    )
    target_language: LanguageCode = Field(
        ...,
        alias="targetLanguage",
        description="Language of the translated text"
    )
    provisioning_config_id: str = Field(
        ...,
        alias="provisioningConfigId",
        description="Provisioning configuration that produced the translation"
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp when the transcript entry was translated"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Audio references, confidence scores, timing, or other translation metadata"
    )


class CreateTranslationTranscriptEntry(BaseModel):
    """Creation payload for a new translation transcript entry."""

    translation_session_id: str = Field(
        ...,
        alias="translationSessionId",
        description="Translation session this transcript entry belongs to"
    )
    sequence_number: int = Field(
        ...,
        gt=0,
        alias="sequenceNumber",
        description="Monotonic sequence number ordering this entry within the session"
    )
    speaker_participant_id: str = Field(
        ...,
        alias="speakerParticipantId",
        description="Participant who produced the source utterance"
    )
    target_participant_id: str = Field(
        ...,
        alias="targetParticipantId",
        description="Participant for whom the utterance was translated"
    )
    source_text: str = Field(
        ...,
        min_length=1,
        alias="sourceText",
        description="Transcribed source-language text"
    )
    translated_text: str = Field(
        ...,
        min_length=1,
        alias="translatedText",
        description="Completed target-language translation"
    )
    source_language: LanguageCode = Field(
        ...,
        alias="sourceLanguage",
        description="Language of the source utterance"
    )
    target_language: LanguageCode = Field(
        ...,
        alias="targetLanguage",
        description="Language of the translated text"
    )
    provisioning_config_id: str = Field(
        ...,
        alias="provisioningConfigId",
        description="Provisioning configuration that produced the translation"
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp when the transcript entry was translated"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Audio references, confidence scores, timing, or other translation metadata"
    )


class TranslationSessionParticipantRequest(BaseModel):
    """Participant details supplied when requesting a translation session."""

    external_participant_id: Optional[str] = Field(
        None,
        alias="externalParticipantId",
        description="Participant identifier supplied by the integrating system, when known"
    )
    language: LanguageCode = Field(
        ...,
        description="Participant's spoken language"
    )
    display_name: Optional[str] = Field(
        None,
        alias="displayName",
        description="Participant display name"
    )


class TranslationSessionInitiatorRequest(BaseModel):
    """Initiating participant details supplied when requesting a translation session."""

    external_participant_id: str = Field(
        ...,
        alias="externalParticipantId",
        description="Identifier of the initiating participant supplied by the integrating system"
    )
    language: LanguageCode = Field(
        ...,
        description="Participant's spoken language"
    )
    display_name: Optional[str] = Field(
        None,
        alias="displayName",
        description="Participant display name"
    )


class TranslationSessionRequest(BaseModel):
    """Request to create a two-party translation session."""

    project_id: Optional[str] = Field(
        None,
        alias="projectId",
        description="Project associated with the translation session"
    )
    external_session_id: Optional[str] = Field(
        None,
        alias="externalSessionId",
        description="External session identifier supplied by the requesting system"
    )
    translation_config_id: Optional[str] = Field(
        None,
        alias="translationConfigId",
        description="Translation configuration to use"
    )
    direction: TranslationDirection = Field(
        TranslationDirection.BIDIRECTIONAL,
        description="Permitted translation direction"
    )
    initiator: TranslationSessionInitiatorRequest = Field(
        ...,
        description="Party initiating the translation session"
    )
    participant: TranslationSessionParticipantRequest = Field(
        ...,
        description="Party receiving the translation session request"
    )


class TranslationParticipantAccess(BaseModel):
    """Runtime access credentials for one translation participant."""

    participant_id: str = Field(
        ...,
        alias="participantId",
        description="Persisted translation participant ID"
    )
    access_id: str = Field(
        ...,
        alias="accessId",
        description="Short-lived access identifier for the participant"
    )
    token: str = Field(
        ...,
        description="Short-lived authentication token for the participant"
    )


class TranslationSessionAccess(BaseModel):
    """Runtime access details returned after creating a translation session."""

    translation_session_id: str = Field(
        ...,
        alias="translationSessionId",
        description="Persisted translation session ID"
    )
    sdrtn_id: Optional[str] = Field(
        None,
        alias="sdrtnId",
        description="Real-time networking session identifier"
    )
    channel_identifier: str = Field(
        ...,
        alias="channelIdentifier",
        description="Communication channel identifier"
    )
    initiator: TranslationParticipantAccess = Field(
        ...,
        description="Runtime access for the initiating participant"
    )
    participant: TranslationParticipantAccess = Field(
        ...,
        description="Runtime access for the other participant"
    )
