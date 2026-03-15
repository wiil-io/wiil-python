"""WIIL Platform support model schema definitions.

The WIIL Platform Support Model Registry maintains a curated list of LLM models from various providers
(OpenAI, Anthropic, etc.) that are supported by the platform. This registry includes model metadata,
capabilities, and associated voices/languages for configuration and deployment.
"""

from typing import List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.service_mgt.voice_language import Language, Voice
from wiil.models.type_definitions import LLMType, SupportedProprietor


class WiilSupportModel(PydanticBaseModel):
    """WIIL Platform supported model configuration.

    Represents a language model registered in the WIIL Platform's support registry. The registry
    provides a centralized catalog of available models with their capabilities, supported languages,
    and voices. Agent Configurations reference these models via modelId.

    Architecture Context:
        - Used By: Agent Configuration (modelId reference)
        - Purpose: Central registry of supported LLM models with their capabilities
        - Model Types: TEXT (text-only), VOICE (speech), MULTI_MODE (combined), etc.
        - Providers: OpenAI, Anthropic, Google, ElevenLabs, and other LLM proprietors

    Model Lifecycle:
        - Active: Available for new deployments (discontinued: false)
        - Discontinued: Legacy support only, not recommended for new deployments (discontinued: true)

    Model ID Distinction:
        - modelId: WIIL Platform unique model identifier (NOT the provider's model ID)
        - provider_model_id: Original model ID from the provider's system

    Attributes:
        model_id: WIIL Platform unique model identifier used in Agent Configuration references
        proprietor: Model proprietor/provider organization (OPENAI, ANTHROPIC, etc.)
        name: Human-readable name of the model for display in UI
        provider_model_id: Original model ID from the provider's system
        description: Description of the model's capabilities and use cases
        type: Type of LLM functionality (TEXT, VOICE, MULTI_MODE, etc.)
        discontinued: Whether this model has been discontinued
        supported_voices: Array of voice configurations supported by this model
        support_languages: Array of languages supported by this model

    Example:
        ```python
        model = WiilSupportModel(
            model_id="YUSI21217J1",
            proprietor=SupportedProprietor.OPENAI,
            name="GPT-4 Turbo",
            provider_model_id="gpt-4-1106-preview",
            description="Latest GPT-4 model with improved performance",
            type=LLMType.TEXT,
            discontinued=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="WIIL Platform unique model identifier (NOT the provider's model ID) used in Agent Configuration references",
        alias="modelId"
    )
    proprietor: SupportedProprietor = Field(
        ...,
        description="Model proprietor/provider organization that developed and maintains the model (OPENAI, ANTHROPIC, GOOGLE, ELEVENLABS, etc.)"
    )
    name: str = Field(
        ...,
        description="Human-readable name of the model for display in administrative interfaces and model selection UI"
    )
    provider_model_id: Optional[str] = Field(
        None,
        description="Original model identifier from the provider's system (e.g., 'gpt-4-1106-preview' for OpenAI)"
    )
    description: str = Field(
        ...,
        description="Comprehensive description of the model's capabilities, recommended use cases, strengths, and limitations"
    )
    type: LLMType = Field(
        ...,
        description="Type of LLM functionality provided by this model (TEXT, VOICE, STT, MULTI_MODE, etc.)"
    )
    discontinued: bool = Field(
        False,
        description="Whether this model has been discontinued by the provider and is only available for legacy support"
    )
    supported_voices: Optional[List[Voice]] = Field(
        None,
        description="Array of voice configurations supported by this model (populated for TTS/voice models, null for text-only models)",
        alias="supportedVoices"
    )
    support_languages: Optional[List[Language]] = Field(
        None,
        description="Array of languages supported by this model for processing and generation (null if language-agnostic)",
        alias="supportLanguages"
    )
