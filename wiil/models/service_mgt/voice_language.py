"""Voice and language configuration models.

This module contains voice and language configurations for text-to-speech
synthesis and speech-to-text recognition.
"""

from typing import Literal, Optional

from pydantic import ConfigDict, Field
from pydantic import BaseModel as PydanticBaseModel

# Voice gender type
VoiceGender = Literal["male", "female", "neutral"]


class Voice(PydanticBaseModel):
    """Voice configuration for text-to-speech synthesis.

    Represents a synthetic voice option available for TTS. Voices are
    associated with TTS models and selected in provisioning chains.

    Attributes:
        voice_id: Unique identifier for the voice
        name: Human-readable name of the voice
        description: Description of voice characteristics
        gender: Gender classification (male, female, or neutral)
        language: Language code this voice is optimized for
        is_default: Whether this is the default voice

    Example:
        ```python
        voice = Voice(
            voice_id="adam",
            name="Adam",
            description="Deep, authoritative male voice",
            gender="male",
            language="en-US",
            is_default=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    voice_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier for the voice (e.g., 'adam', 'rachel')",
        alias="voiceId"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name of the voice"
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Description of voice characteristics and use cases"
    )
    gender: VoiceGender = Field(
        ...,
        description="Gender classification of the voice"
    )
    language: Optional[str] = Field(
        None,
        description="Language code this voice is optimized for (e.g., 'en-US')"
    )
    is_default: bool = Field(
        False,
        description="Whether this is the default voice",
        alias="isDefault"
    )


class Language(PydanticBaseModel):
    """Language configuration for speech processing.

    Represents a language supported by the platform for speech
    processing (STT/TTS) and text-based interactions.

    Attributes:
        language_id: Unique identifier for the language
        name: Human-readable name of the language
        code: Standard language code in ISO 639-1 format
        is_default: Whether this is the default language
        is_experimental: Whether this language is experimental/beta

    Example:
        ```python
        language = Language(
            language_id="en-us",
            name="English (United States)",
            code="en-US",
            is_default=True,
            is_experimental=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    language_id: str = Field(
        ...,
        min_length=1,
        description="Unique identifier for the language (e.g., 'en-us')",
        alias="languageId"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name with region (e.g., 'English (United States)')"
    )
    code: str = Field(
        ...,
        description="ISO 639-1 language code with region (e.g., 'en-US')"
    )
    is_default: bool = Field(
        False,
        description="Whether this is the default language",
        alias="isDefault"
    )
    is_experimental: bool = Field(
        False,
        description="Whether this language is experimental/beta",
        alias="isExperimental"
    )
