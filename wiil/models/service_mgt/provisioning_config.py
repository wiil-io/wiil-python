"""Provisioning configuration chain schema definitions.

Provisioning chains orchestrate the complete voice interaction pipeline by linking Speech-to-Text (STT),
Agent Configuration, and Text-to-Speech (TTS) models. Used for voice-based deployments with CHAINED
provisioning type.
"""

from typing import Any, Dict, Optional, Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.service_mgt.dynamic_setup import (
    DynamicModelConfiguration,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
)


class SttModelConfig(PydanticBaseModel):
    """Speech-to-Text model configuration.

    Defines the STT model used to convert user speech to text in voice-based interactions.
    Part of the provisioning chain's input processing stage.

    Architecture Context:
        - Used In: ProvisioningConfigChain (sttConfig field)
        - Purpose: Converts incoming voice to text for agent processing
        - Pipeline Position: First stage (Speech -> Text)

    Attributes:
        model_id: Identifier of the STT model from Wiil registry
        default_language: Default language code for speech recognition in ISO format
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="Identifier of the STT (Speech-to-Text) model from Wiil registry (e.g., 'whisper-v3', 'google-stt-enhanced')",
        alias="modelId"
    )
    default_language: str = Field(
        "en-US",
        description="Default language code for speech recognition in ISO 639-1 format with region (e.g., 'en-US', 'es-ES')",
        alias="defaultLanguage"
    )


class TtsModelConfig(PydanticBaseModel):
    """Text-to-Speech model configuration.

    Defines the TTS model and voice used to convert agent text responses to speech in voice interactions.
    Part of the provisioning chain's output generation stage.

    Architecture Context:
        - Used In: ProvisioningConfigChain (ttsConfig field)
        - Purpose: Converts agent text responses to natural speech
        - Pipeline Position: Final stage (Text -> Speech)
        - Voice Selection: References voices from WiilSupportModel.supportedVoices

    Attributes:
        model_id: Identifier of the TTS model from Wiil registry
        voice_id: Identifier of the specific voice for speech synthesis
        default_language: Default language code for speech synthesis
        voice_settings: Optional voice-specific settings (pitch, speed, stability, etc.)
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="Identifier of the TTS (Text-to-Speech) model from Wiil registry (e.g., 'eleven-labs-v2', 'google-tts-wavenet')",
        alias="modelId"
    )
    voice_id: str = Field(
        ...,
        description="Identifier of the specific voice to use for speech synthesis (e.g., 'adam', 'rachel')",
        alias="voiceId"
    )
    default_language: str = Field(
        "en-US",
        description="Default language code for speech synthesis in ISO 639-1 format with region (e.g., 'en-US', 'es-MX')",
        alias="defaultLanguage"
    )
    voice_settings: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional voice-specific settings as key-value pairs for fine-tuning speech output",
        alias="voiceSettings"
    )


class ProvisioningConfigChain(BaseModel):
    """Provisioning configuration chain.

    Represents a complete voice interaction processing pipeline that chains Speech-to-Text (STT),
    Agent Configuration, and Text-to-Speech (TTS) for end-to-end voice conversations. Referenced
    by Deployment Configurations with CHAINED provisioning type.

    Architecture Context:
        - Used By: Deployment Configuration (provisioningConfigChainId for CHAINED type)
        - Purpose: Orchestrates complete voice interaction pipeline
        - Pipeline Flow: User Speech -> STT -> Text -> Agent -> Text Response -> TTS -> Agent Speech
        - Organization: Scoped to organization for multi-tenant isolation

    Voice Processing Pipeline:
        1. STT Stage: Converts incoming user speech to text using sttConfig
        2. Agent Stage: Processes text through agent (referenced by agentConfigurationId)
        3. TTS Stage: Converts agent text response to speech using ttsConfig

    Attributes:
        chain_name: Human-readable name for the provisioning chain
        description: Optional description of the chain's purpose and configuration
        stt_config: Speech-to-text model configuration (pipeline stage 1)
        agent_configuration_id: ID of the agent configuration (pipeline stage 2)
        tts_config: Text-to-speech model configuration (pipeline stage 3)
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    chain_name: str = Field(
        ...,
        description="Human-readable name for the provisioning chain (e.g., 'Customer Support Voice Chain')",
        alias="chainName"
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the chain's purpose, use case, and configuration details"
    )
    stt_config: SttModelConfig = Field(
        ...,
        description="Speech-to-Text model configuration for the first stage of the pipeline",
        alias="sttConfig"
    )
    agent_configuration_id: str = Field(
        ...,
        description="ID of the agent configuration to use in the middle stage of the pipeline",
        alias="agentConfigurationId"
    )
    tts_config: TtsModelConfig = Field(
        ...,
        description="Text-to-Speech model configuration for the final stage of the pipeline",
        alias="ttsConfig"
    )


class CreateProvisioningConfig(PydanticBaseModel):
    """Schema for creating a new provisioning configuration chain.

    Omits auto-generated fields that are populated by the system.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    chain_name: str = Field(..., alias="chainName")
    description: Optional[str] = None
    stt_config: DynamicSTTModelConfiguration = Field(..., alias="sttConfig")
    processing_config: DynamicModelConfiguration = Field(..., alias="processingConfig")
    tts_config: DynamicTTSModelConfiguration = Field(..., alias="ttsConfig")


class UpdateProvisioningConfig(PydanticBaseModel):
    """Schema for updating an existing provisioning configuration chain.

    All fields are optional except id.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    chain_name: Optional[str] = Field(None, alias="chainName")
    description: Optional[str] = None
    stt_config: Optional[DynamicSTTModelConfiguration] = Field(None, alias="sttConfig")
    processing_config: Optional[DynamicModelConfiguration] = Field(None, alias="processingConfig")
    tts_config: Optional[DynamicTTSModelConfiguration] = Field(None, alias="ttsConfig")


class TranslationChainConfig(BaseModel):
    """Translation chain configuration.

    Extends the provisioning chain concept with translation-specific processing capabilities.
    Enables real-time language translation in voice interactions (e.g., English caller to Spanish agent).

    Architecture Context:
        - Extension Of: ProvisioningConfigChain with translation capabilities
        - Purpose: Real-time language translation for multilingual support
        - Pipeline Flow: Speech (Lang A) -> STT -> Text (Lang A) -> Translation -> Text (Lang B) -> TTS -> Speech (Lang B)
        - Use Case: Cross-language customer support, international business

    Translation Pipeline:
        1. STT Stage: Converts incoming speech to text in source language
        2. Translation Stage: Translates text between languages using processingModelId
        3. TTS Stage: Converts translated text to speech in target language

    Attributes:
        chain_name: Human-readable name for the translation chain
        description: Optional description of language pair and configuration
        stt_config: Speech-to-text configuration for source language recognition
        processing_model_id: ID of the LLM model used for translation processing
        tts_config: Text-to-speech configuration for target language synthesis
        is_translation: Flag indicating this chain performs translation
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    chain_name: str = Field(
        ...,
        description="Human-readable name for the translation chain (e.g., 'EN-ES Translation')",
        alias="chainName"
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the translation language pair and configuration"
    )
    stt_config: SttModelConfig = Field(
        ...,
        description="Speech-to-Text configuration for recognizing speech in the source language",
        alias="sttConfig"
    )
    processing_model_id: str = Field(
        ...,
        description="ID of the LLM model used for translation processing between languages",
        alias="processingModelId"
    )
    tts_config: TtsModelConfig = Field(
        ...,
        description="Text-to-Speech configuration for synthesizing speech in the target language",
        alias="ttsConfig"
    )
    is_translation: bool = Field(
        True,
        description="Flag indicating this chain performs real-time language translation",
        alias="isTranslation"
    )


class CreateTranslationChainConfig(PydanticBaseModel):
    """Schema for creating a new translation chain configuration.

    Omits auto-generated fields and sets isTranslation to true by default.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    chain_name: str = Field(..., alias="chainName")
    description: Optional[str] = None
    stt_config: DynamicSTTModelConfiguration = Field(..., alias="sttConfig")
    processing_config: DynamicModelConfiguration = Field(..., alias="processingConfig")
    tts_config: DynamicTTSModelConfiguration = Field(..., alias="ttsConfig")
    is_translation: bool = Field(True, alias="isTranslation")


class UpdateTranslationChainConfig(PydanticBaseModel):
    """Schema for updating an existing translation chain configuration.

    All fields are optional except id.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    chain_name: Optional[str] = Field(None, alias="chainName")
    description: Optional[str] = None
    stt_config: Optional[DynamicSTTModelConfiguration] = Field(None, alias="sttConfig")
    processing_config: Optional[DynamicModelConfiguration] = Field(None, alias="processingConfig")
    tts_config: Optional[DynamicTTSModelConfiguration] = Field(None, alias="ttsConfig")
    is_translation: Optional[bool] = Field(None, alias="isTranslation")


# Union types
ChainConfiguration = Union[ProvisioningConfigChain, TranslationChainConfig]
CreateChainConfiguration = Union[CreateProvisioningConfig, CreateTranslationChainConfig]
UpdateChainConfiguration = Union[UpdateProvisioningConfig, UpdateTranslationChainConfig]
