"""Provisioning configuration chain schema definitions.

Provisioning chains orchestrate the complete voice interaction pipeline by linking
Speech-to-Text (STT), Agent Configuration, and Text-to-Speech (TTS) models.
"""

from typing import Any, Dict, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel


class SttModelConfig(BaseModel):
    """Speech-to-Text model configuration.

    Defines the STT model used to convert user speech to text in voice-based
    interactions. Part of the provisioning chain's input processing stage.

    Pipeline Position: First stage (Speech → Text)

    Attributes:
        model_id: Identifier of the STT model from Wiil registry
        default_language: Default language code for speech recognition

    Example:
        ```python
        stt_config = SttModelConfig(
            model_id="whisper-v3",
            default_language="en-US"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="STT model identifier (e.g., 'whisper-v3', 'google-stt-enhanced')",
        alias="modelId"
    )
    default_language: str = Field(
        "en-US",
        description="Default language code in ISO 639-1 format (e.g., 'en-US')",
        alias="defaultLanguage"
    )


class TtsModelConfig(BaseModel):
    """Text-to-Speech model configuration.

    Defines the TTS model and voice used to convert agent text responses to speech
    in voice interactions. Part of the provisioning chain's output generation stage.

    Pipeline Position: Final stage (Text → Speech)

    Attributes:
        model_id: Identifier of the TTS model from Wiil registry
        voice_id: Identifier of the specific voice for speech synthesis
        default_language: Default language code for speech synthesis
        voice_settings: Optional voice-specific settings

    Example:
        ```python
        tts_config = TtsModelConfig(
            model_id="eleven-labs-v2",
            voice_id="adam",
            default_language="en-US",
            voice_settings={"stability": 0.75, "similarity_boost": 0.5}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="TTS model identifier (e.g., 'eleven-labs-v2', 'google-tts-wavenet')",
        alias="modelId"
    )
    voice_id: str = Field(
        ...,
        description="Voice identifier (e.g., 'adam', 'rachel', 'en-us-neural-female')",
        alias="voiceId"
    )
    default_language: str = Field(
        "en-US",
        description="Default language code in ISO 639-1 format (e.g., 'en-US')",
        alias="defaultLanguage"
    )
    voice_settings: Optional[Dict[str, Any]] = Field(
        None,
        description="Voice-specific settings (pitch, speed, stability, etc.)",
        alias="voiceSettings"
    )


class ProvisioningConfigChain(BaseModel):
    """Provisioning configuration chain.

    Represents a complete voice interaction processing pipeline that chains
    Speech-to-Text (STT), Agent Configuration, and Text-to-Speech (TTS) for
    end-to-end voice conversations.

    Pipeline Flow:
        User Speech → STT → Text → Agent → Text Response → TTS → Agent Speech

    Attributes:
        id: Unique identifier
        name: Human-readable name
        stt_config: STT model configuration
        tts_config: TTS model configuration
        agent_configuration_id: ID of the agent configuration
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        chain = ProvisioningConfigChain(
            id="123",
            name="Customer Support Voice Pipeline",
            stt_config=SttModelConfig(
                model_id="whisper-v3",
                default_language="en-US"
            ),
            tts_config=TtsModelConfig(
                model_id="eleven-labs-v2",
                voice_id="adam",
                default_language="en-US"
            ),
            agent_configuration_id="agent-456"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    chain_name: str = Field(
        ...,
        description="Human-readable name for the provisioning chain",
        alias="chainName"
    )
    stt_config: SttModelConfig = Field(
        ...,
        description="Speech-to-Text model configuration",
        alias="sttConfig"
    )
    tts_config: TtsModelConfig = Field(
        ...,
        description="Text-to-Speech model configuration",
        alias="ttsConfig"
    )
    agent_configuration_id: str = Field(
        ...,
        description="ID of the agent configuration in the chain",
        alias="agentConfigurationId"
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the chain's purpose and configuration"
    )


class CreateProvisioningConfigChain(BaseModel):
    """Schema for creating a new provisioning chain."""

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    chain_name: str = Field(..., alias="chainName")
    stt_config: SttModelConfig = Field(..., alias="sttConfig")
    tts_config: TtsModelConfig = Field(..., alias="ttsConfig")
    agent_configuration_id: str = Field(..., alias="agentConfigurationId")
    description: Optional[str] = None


class UpdateProvisioningConfigChain(BaseModel):
    """Schema for updating an existing provisioning chain."""

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    chain_name: Optional[str] = Field(None, alias="chainName")
    stt_config: Optional[SttModelConfig] = Field(None, alias="sttConfig")
    tts_config: Optional[TtsModelConfig] = Field(None, alias="ttsConfig")
    agent_configuration_id: Optional[str] = Field(None, alias="agentConfigurationId")
    description: Optional[str] = None
