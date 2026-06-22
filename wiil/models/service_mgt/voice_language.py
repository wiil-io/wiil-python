"""Voice and language configuration schema definitions.

Voice and language configurations define the supported voices and languages for text-to-speech
synthesis and speech-to-text recognition. These configurations are referenced by support models
and provisioning chains for voice-based interactions.
"""

from typing import List, Literal, Optional

from pydantic import Field

from wiil.models.base import BaseModel


# Voice gender type
VoiceGender = Literal["male", "female", "neutral"]


class Voice(BaseModel):
    """Voice configuration for TTS synthesis.

    Represents a synthetic voice option available for text-to-speech (TTS) synthesis. Voices are
    associated with TTS models in the Wiil support registry and selected in provisioning chains
    for voice-based deployments.

    Architecture Context:
        - Used By: WiilSupportModel (supportedVoices array for TTS models)
        - Referenced In: TtsModelConfig (voiceId selection) and ProvisioningConfigChain
        - Purpose: Defines available voice options for agent speech synthesis

    Voice Characteristics:
        - Identity: Unique ID and human-readable name
        - Gender: Male, female, or neutral classification
        - Language: Optimal language for the voice
        - Default: Flag for platform default selection

    Attributes:
        voice_id: Unique identifier for the voice used in configurations
        name: Human-readable name of the voice for display in UI
        description: Description of the voice characteristics including tone, accent, and use cases
        gender: Gender classification of the voice (male, female, or neutral)
        language: Language code this voice is optimized for, null if multi-language
        is_default: Whether this is the default voice for its language or model
    """

    voice_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier for the voice used in TTS configurations (e.g., 'adam', 'rachel', 'en-us-neural-female')",
        alias="voiceId"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name of the voice displayed in user interfaces (e.g., 'Adam', 'Rachel', 'Google Neural Female')"
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Description of the voice characteristics including tone, accent, pitch, and recommended use cases"
    )
    gender: VoiceGender = Field(
        ...,
        description="Gender classification of the voice (male, female, or neutral) used for filtering and user preference matching"
    )
    language: Optional[str] = Field(
        None,
        description="Language code this voice is optimized for in ISO 639-1 format with optional region (e.g., 'en-US', 'es-ES'), null if multi-language"
    )
    is_default: bool = Field(
        False,
        description="Whether this is the default voice selection for its language or TTS model",
        alias="isDefault"
    )


class Language(BaseModel):
    """Language configuration for speech processing.

    Represents a language supported by the platform for speech processing (STT/TTS). Languages are
    associated with models in the Wiil support registry and selected in provisioning chains
    for voice-based and text-based interactions.

    Architecture Context:
        - Used By: WiilSupportModel (supportLanguages array)
        - Referenced In: SttModelConfig and TtsModelConfig (defaultLanguage selection)
        - Purpose: Defines supported languages for speech recognition and synthesis

    Language Support Levels:
        - Production: Fully supported, tested languages (is_experimental: false)
        - Experimental: Beta or limited support languages (is_experimental: true)
        - Default: Platform default for automatic selection (is_default: true)

    Attributes:
        language_id: Unique identifier for the language
        name: Human-readable name of the language for display
        code: Standard language code in ISO 639-1 format with optional region
        is_default: Whether this is the default language for the platform or model
        is_experimental: Whether this language is in experimental/beta support
    """

    language_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier for the language, typically lowercase with region (e.g., 'en-us', 'es-mx', 'fr-ca')",
        alias="languageId"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name of the language with region specification for user interfaces"
    )
    code: str = Field(
        ...,
        description="Standard language code in ISO 639-1 format with optional ISO 3166-1 region code (e.g., 'en-US', 'es-ES', 'zh-CN')"
    )
    is_default: bool = Field(
        False,
        description="Whether this is the default language for the platform or model",
        alias="isDefault"
    )
    is_experimental: bool = Field(
        False,
        description="Whether this language is in experimental or beta support status",
        alias="isExperimental"
    )


# Type aliases for arrays
SupportedVoices = List[Voice]
SupportedLanguages = List[Language]
