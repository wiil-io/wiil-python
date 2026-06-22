"""Base assistant setup schema definitions.

This module mirrors src/core/assistant-setups/base-assistant-setup.schema.ts
"""

from typing import List, Optional

from pydantic import Field, model_validator

from wiil.models.base import BaseModel
from wiil.models.service_mgt.instruction_config import CreateInstructionConfiguration
from wiil.models.service_mgt.provisioning_config import SttModelConfig, TtsModelConfig


class BaseAssistant(BaseModel):
    """Base schema for setting up an AI assistant.

    At least one of instruction_configuration_id or custom_instruction_configuration
    must be provided.

    Attributes:
        assistant_name: Name of the assistant
        support_model_id: ID of the support model to use
        voice_id: Optional voice ID for the assistant
        language_id: Optional language ID for the assistant
        instruction_configuration_id: ID of existing instruction configuration
        custom_instruction_configuration: Custom instruction configuration
        knowledge_source_ids: IDs of knowledge sources to use

    Example:
        ```python
        assistant = BaseAssistant(
            assistant_name="Customer Support",
            support_model_id="model-123",
            instruction_configuration_id="inst-456",
            knowledge_source_ids=["ks-789"]
        )
        ```
    """

    assistant_name: str = Field(
        ...,
        description="Name of the assistant",
        alias="assistantName"
    )
    support_model_id: str = Field(
        ...,
        description="ID of the support model to use",
        alias="supportModelId"
    )
    voice_id: Optional[str] = Field(
        None,
        description="Optional voice ID for the assistant",
        alias="voiceId"
    )
    language_id: Optional[str] = Field(
        None,
        description="Optional language ID for the assistant",
        alias="languageId"
    )
    instruction_configuration_id: Optional[str] = Field(
        None,
        description="ID of existing instruction configuration",
        alias="instructionConfigurationId"
    )
    custom_instruction_configuration: Optional[CreateInstructionConfiguration] = Field(
        None,
        description="Custom instruction configuration to create",
        alias="customInstructionConfiguration"
    )
    knowledge_source_ids: List[str] = Field(
        default_factory=list,
        description="IDs of knowledge sources to use",
        alias="knowledgeSourceIds"
    )

    @model_validator(mode="after")
    def validate_instruction_config(self) -> "BaseAssistant":
        """Validate that at least one instruction config is provided."""
        has_instruction_id = self.instruction_configuration_id is not None
        has_custom_instruction = self.custom_instruction_configuration is not None

        if not has_instruction_id and not has_custom_instruction:
            raise ValueError(
                "Either instructionConfigurationId or customInstructionConfiguration must be provided"
            )
        return self


class AdvanceBaseAssistant(BaseAssistant):
    """Advanced base assistant schema with STT and TTS configurations.

    Extends BaseAssistant with speech-to-text and text-to-speech model
    configurations for voice-based interactions.

    Attributes:
        stt_config: Speech-to-text model configuration
        tts_config: Text-to-speech model configuration

    Example:
        ```python
        assistant = AdvanceBaseAssistant(
            assistant_name="Voice Support",
            support_model_id="model-123",
            instruction_configuration_id="inst-456",
            stt_config=SttModelConfig(
                model_id="whisper-v3",
                default_language="en-US"
            ),
            tts_config=TtsModelConfig(
                model_id="eleven-labs-v2",
                voice_id="adam",
                default_language="en-US"
            )
        )
        ```
    """

    stt_config: SttModelConfig = Field(
        ...,
        description="Speech-to-text model configuration",
        alias="sttConfig"
    )
    tts_config: TtsModelConfig = Field(
        ...,
        description="Text-to-speech model configuration",
        alias="ttsConfig"
    )
