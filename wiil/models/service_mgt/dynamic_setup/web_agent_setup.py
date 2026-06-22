"""Web agent setup schemas for AI assistant configuration.

Provides schemas for configuring AI assistants deployed on web channels.
Extends the base agent setup with web-specific settings like website URL,
communication type, and optional voice interaction configurations.
"""

from typing import List, Optional

from pydantic import Field, field_validator, model_validator

from wiil.models.base import BaseModel
from wiil.models.service_mgt.dynamic_setup.base_agent_setup import (
    DynamicAgentSetupResult,
    DynamicBaseAgentSetup,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
)
from wiil.models.type_definitions import OttCommunicationType


class DynamicWebAgentSetup(DynamicBaseAgentSetup):
    """Web agent setup schema.

    Extends the base agent setup with web-specific settings.

    Attributes:
        website_url: URL of the website for this assistant
        communication_type: Communication method (text, voice, unified)
        stt_configuration: Speech-to-text configuration for voice
        tts_configuration: Text-to-speech configuration for voice
    """

    website_url: str = Field(
        ...,
        description="URL of the website to use for this assistant",
        alias="websiteUrl"
    )
    communication_type: OttCommunicationType = Field(
        OttCommunicationType.UNIFIED,
        description="Type of over-the-top communication method for the web channel. options: text, voice, unified",
        alias="communicationType"
    )
    stt_configuration: Optional[DynamicSTTModelConfiguration] = Field(
        None,
        description="Speech-to-text model configuration for the web assistant, if using voice interactions",
        alias="sttConfiguration"
    )
    tts_configuration: Optional[DynamicTTSModelConfiguration] = Field(
        None,
        description="Text-to-speech model configuration for the web assistant, if using voice interactions",
        alias="ttsConfiguration"
    )

    @model_validator(mode="after")
    def validate_stt_tts_pair(self) -> "DynamicWebAgentSetup":
        """Validate that STT and TTS configurations are provided together."""
        has_stt = self.stt_configuration is not None
        has_tts = self.tts_configuration is not None
        if has_stt != has_tts:
            raise ValueError(
                "Both sttConfiguration and ttsConfiguration must be provided together, or neither"
            )
        return self

    @field_validator("communication_type", mode="before")
    @classmethod
    def normalize_communication_type(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, OttCommunicationType):
            return value
        if isinstance(value, str):
            return OttCommunicationType(value.lower())
        return value


class DynamicWebAgentSetupResult(DynamicAgentSetupResult):
    """Web agent setup result schema.

    Extends the base setup result with web-specific fields.

    Attributes:
        integration_snippets: Code snippets for deploying the web assistant
    """

    integration_snippets: Optional[List[str]] = Field(
        None,
        description="List of code snippets or integration details for deploying the web assistant",
        alias="integrationSnippets"
    )


class UpdateDynamicWebAgent(BaseModel):
    """Schema for updating an existing web agent configuration.

    All fields are optional except id.
    """

    id: str = Field(
        ...,
        description="ID of the existing web agent configuration to update"
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
    website_url: Optional[str] = Field(None, alias="websiteUrl")
    communication_type: Optional[OttCommunicationType] = Field(None, alias="communicationType")
    stt_configuration: Optional[DynamicSTTModelConfiguration] = Field(None, alias="sttConfiguration")
    tts_configuration: Optional[DynamicTTSModelConfiguration] = Field(None, alias="ttsConfiguration")

    @field_validator("communication_type", mode="before")
    @classmethod
    def normalize_communication_type(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, OttCommunicationType):
            return value
        if isinstance(value, str):
            return OttCommunicationType(value.lower())
        return value
