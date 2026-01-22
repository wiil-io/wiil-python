"""Wiil support model schema definitions.

This module contains models for the Wiil Support Model Registry which maintains
a curated list of LLM models from various providers.
"""

from typing import Any, Dict, List, Optional

from pydantic import ConfigDict, Field
from pydantic import BaseModel as PydanticBaseModel

from wiil.models.service_mgt.voice_language import Language, Voice
from wiil.types.service_types import LLMType, SupportedProprietor


class WiilSupportModel(PydanticBaseModel):
    """Wiil supported model configuration.

    Represents a language model registered in the Wiil platform's support registry.
    The registry provides a centralized catalog of available models with their capabilities,
    supported languages, and voices.

    Attributes:
        model_id: Unique identifier for the model in Wiil registry
        proprietor: Model proprietor/provider organization
        name: Human-readable name of the model
        provider_model_id: Original model ID from provider if different
        description: Description of model capabilities and use cases
        type: Type of LLM functionality
        discontinued: Whether model has been discontinued
        supported_voices: Array of voice configurations for TTS models
        support_languages: Array of supported languages

    Example:
        ```python
        model = WiilSupportModel(
            model_id="YUSI21217J1",
            proprietor=SupportedProprietor.OPENAI,
            name="GPT-4 Turbo",
            provider_model_id="gpt-4-1106-preview",
            description="Latest GPT-4 model with improved performance",
            type=LLMType.TEXT_PROCESSING,
            discontinued=False,
            supported_voices=None,
            support_languages=[
                Language(
                    language_id="en",
                    name="English",
                    code="en-US",
                    is_default=True
                )
            ]
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="Unique identifier for the model in Wiil registry (e.g., 'YUSI21217J1')",
        alias="modelId"
    )
    proprietor: SupportedProprietor = Field(
        ...,
        description="Model proprietor/provider organization"
    )
    name: str = Field(
        ...,
        description="Human-readable name for display in UI"
    )
    provider_model_id: Optional[str] = Field(
        None,
        description="Original model ID from provider if different"
    )
    description: str = Field(
        ...,
        description="Comprehensive description of model capabilities"
    )
    type: LLMType = Field(
        ...,
        description="Type of LLM functionality provided"
    )
    discontinued: bool = Field(
        False,
        description="Whether model has been discontinued"
    )
    supported_voices: Optional[List[Voice]] = Field(
        None,
        description="Array of voice configurations for TTS models",
        alias="supportedVoices"
    )
    support_languages: Optional[List[Language]] = Field(
        None,
        description="Array of languages supported by this model",
        alias="supportLanguages"
    )
