"""Phone assistant setup schema definitions.

This module mirrors src/core/assistant-setups/phone-assistant-setup.schema.ts
"""

from pydantic import Field

from wiil.models.assistant_setups.base_assistant_setup import (
    AdvanceBaseAssistant,
    BaseAssistant,
)


class PhoneAssistantSetup(BaseAssistant):
    """Schema for setting up a phone AI assistant.

    Extends BaseAssistant with phone-specific configuration.

    Attributes:
        phone_configuration_id: Phone configuration ID for the phone channel

    Example:
        ```python
        setup = PhoneAssistantSetup(
            assistant_name="Phone Support",
            support_model_id="model-123",
            instruction_configuration_id="inst-456",
            phone_configuration_id="phone-789"
        )
        ```
    """

    phone_configuration_id: str = Field(
        ...,
        description="Phone configuration ID for the phone channel where this assistant will be deployed",
        alias="phoneConfigurationId"
    )


class ChainedPhoneAssistantSetup(AdvanceBaseAssistant):
    """Schema for setting up a phone AI assistant with advanced configurations.

    Extends AdvanceBaseAssistant with phone-specific configuration and
    STT/TTS model configurations for voice processing chains.

    Attributes:
        phone_configuration_id: Phone configuration ID for the phone channel

    Example:
        ```python
        setup = ChainedPhoneAssistantSetup(
            assistant_name="Advanced Phone Support",
            support_model_id="model-123",
            instruction_configuration_id="inst-456",
            phone_configuration_id="phone-789",
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

    phone_configuration_id: str = Field(
        ...,
        description="Phone configuration ID for the phone channel where this assistant will be deployed",
        alias="phoneConfigurationId"
    )
