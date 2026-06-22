"""Phone agent setup schemas for AI assistant configuration.

Provides schemas for configuring AI assistants deployed on phone/telephony channels.
Extends the base agent setup with phone-specific settings like phone configuration,
test numbers, and required voice interaction configurations (STT/TTS).
"""

from typing import Optional

from pydantic import Field, model_validator

from wiil.models.base import BaseModel
from wiil.models.service_mgt.dynamic_setup.base_agent_setup import (
    DynamicAgentSetupResult,
    DynamicBaseAgentSetup,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
)


class DynamicPhoneAgentSetup(DynamicBaseAgentSetup):
    """Phone agent setup schema.

    Extends the base agent setup with phone-specific settings.

    Attributes:
        phone_configuration_id: ID of the phone configuration
        test_phone_number: Phone number for testing
        stt_configuration: Speech-to-text configuration (required for voice)
        tts_configuration: Text-to-speech configuration (required for voice)
    """

    phone_configuration_id: Optional[str] = Field(
        None,
        description="ID of the phone configuration to use for this assistant",
        alias="phoneConfigurationId"
    )
    test_phone_number: Optional[str] = Field(
        None,
        description="Optional phone number to use for testing the phone assistant setup",
        alias="testPhoneNumber"
    )
    stt_configuration: Optional[DynamicSTTModelConfiguration] = Field(
        None,
        description="Speech-to-text model configuration for the phone assistant",
        alias="sttConfiguration"
    )
    tts_configuration: Optional[DynamicTTSModelConfiguration] = Field(
        None,
        description="Text-to-speech model configuration for the phone assistant",
        alias="ttsConfiguration"
    )

    @model_validator(mode="after")
    def validate_stt_tts_pair(self) -> "DynamicPhoneAgentSetup":
        """Validate that STT and TTS configurations are provided together."""
        has_stt = self.stt_configuration is not None
        has_tts = self.tts_configuration is not None
        if has_stt != has_tts:
            raise ValueError(
                "Both sttConfiguration and ttsConfiguration must be provided together, or neither"
            )
        return self


class DynamicPhoneAgentSetupResult(DynamicAgentSetupResult):
    """Phone agent setup result schema.

    Extends the base setup result with phone-specific fields.

    Attributes:
        phone_number: Phone number associated with the configuration
    """

    phone_number: Optional[str] = Field(
        None,
        description="Phone number associated with the phone configuration used for this assistant",
        alias="phoneNumber"
    )


class UpdateDynamicPhoneAgent(BaseModel):
    """Schema for updating an existing phone agent configuration.

    All fields are optional except id. Phone configuration cannot be changed after creation.
    """

    id: str = Field(
        ...,
        description="ID of the existing phone agent configuration to update"
    )
    assistant_name: Optional[str] = Field(
        None,
        max_length=30,
        alias="assistantName"
    )
    instruction_configuration_id: Optional[str] = Field(None, alias="instructionConfigurationId")
    role_template_identifier: Optional[str] = None
    capabilities: Optional[list] = None
    knowledge_source_ids: Optional[list] = Field(None, alias="knowledgeSourceIds")
    language: Optional[str] = None
    voice: Optional[str] = None
    provider_type: Optional[str] = Field(None, alias="providerType")
    provider_model_id: Optional[str] = Field(None, alias="providerModelId")
    test_phone_number: Optional[str] = Field(None, alias="testPhoneNumber")
    stt_configuration: Optional[DynamicSTTModelConfiguration] = Field(None, alias="sttConfiguration")
    tts_configuration: Optional[DynamicTTSModelConfiguration] = Field(None, alias="ttsConfiguration")
