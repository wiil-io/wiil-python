"""Dynamic agent setup base schemas for AI assistant configuration.

Provides foundational schemas for configuring AI assistants across different
channels (phone, web). These base schemas are extended by channel-specific
configurations in phone_agent_setup.py and web_agent_setup.py.
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import Field

from wiil.models.base import BaseModel
from wiil.models.type_definitions import AgentCapabilities, AgentRoleTemplateIdentifier, SupportedProprietor


# Processing status type
ProcessingStatus = Literal["pending", "in_progress", "completed", "failed"]


class DynamicBaseAgentSetup(BaseModel):
    """Base agent setup schema.

    Attributes:
        assistant_name: Name of the AI assistant (max 30 characters)
        instruction_configuration_id: ID of the instruction configuration
        role_template_identifier: Role/persona for the agent
        capabilities: List of enabled platform services
        knowledge_source_ids: Knowledge source IDs to associate
        language: Language ID (e.g., en, es, fr)
        voice: Voice ID for voice interactions
        provider_type: AI model provider type
        provider_model_id: Specific model ID from the provider
    """

    assistant_name: str = Field(
        ...,
        max_length=30,
        description="Name of the AI assistant to use in conversations",
        alias="assistantName"
    )
    instruction_configuration_id: Optional[str] = Field(
        None,
        description="ID of the instruction configuration to use for this assistant",
        alias="instructionConfigurationId"
    )
    role_template_identifier: Optional[AgentRoleTemplateIdentifier] = Field(
        None,
        description="The role or persona that the agent adopts with this instruction set"
    )
    capabilities: List[AgentCapabilities] = Field(
        default_factory=list,
        description="List of platform services (tools) enabled for this agent configuration"
    )
    knowledge_source_ids: Optional[List[str]] = Field(
        None,
        description="List of knowledge source IDs to associate with this assistant",
        alias="knowledgeSourceIds"
    )
    language: str = Field(
        "en",
        description="Language ID for the assistant, e.g., en, es, fr, etc."
    )
    voice: Optional[str] = Field(
        None,
        description="Voice ID for the assistant, if applicable, used for voice interactions"
    )
    provider_type: Optional[SupportedProprietor] = Field(
        None,
        description="The AI model provider type for this agent configuration, e.g., OPENAI, AZURE, etc.",
        alias="providerType"
    )
    provider_model_id: Optional[str] = Field(
        None,
        description="The specific model ID from the provider to use for this agent, e.g., gpt-4, gpt-3.5-turbo, etc.",
        alias="providerModelId"
    )


class DynamicModelConfiguration(BaseModel):
    """Model configuration schema.

    Attributes:
        provider_type: AI model provider type
        provider_model_id: Specific model ID from the provider
    """

    provider_type: SupportedProprietor = Field(
        ...,
        description="The AI model provider type for this agent configuration, e.g., OPENAI, AZURE, etc.",
        alias="providerType"
    )
    provider_model_id: str = Field(
        ...,
        description="The specific model ID from the provider to use for this agent, e.g., gpt-4, gpt-3.5-turbo, etc.",
        alias="providerModelId"
    )


class DynamicSTTModelConfiguration(DynamicModelConfiguration):
    """Speech-to-text model configuration schema.

    Attributes:
        provider_type: AI model provider type
        provider_model_id: Specific model ID from the provider
        language_id: Language ID for speech recognition
    """

    language_id: str = Field(
        "en",
        description="Language ID for the speech-to-text model, e.g., en, es, fr, etc.",
        alias="languageId"
    )


class DynamicTTSModelConfiguration(DynamicModelConfiguration):
    """Text-to-speech model configuration schema.

    Attributes:
        provider_type: AI model provider type
        provider_model_id: Specific model ID from the provider
        language_id: Language ID for speech synthesis
        voice_id: Voice ID for speech output
    """

    language_id: str = Field(
        "en",
        description="Language ID for the text-to-speech model, e.g., en, es, fr, etc.",
        alias="languageId"
    )
    voice_id: Optional[str] = Field(
        None,
        description="Voice ID for the text-to-speech model, if applicable",
        alias="voiceId"
    )


class DynamicAgentProcessingState(BaseModel):
    """Agent processing state schema for tracking long-running setup operations.

    Attributes:
        status: Current processing status (pending, in_progress, completed, failed)
        progress_percentage: Progress percentage (0-100)
        message: Additional details about current state
    """

    status: ProcessingStatus = Field(
        ...,
        description="Current processing status of the agent setup"
    )
    progress_percentage: int = Field(
        ...,
        ge=0,
        le=100,
        description="Progress percentage of the agent setup process",
        alias="progressPercentage"
    )
    message: Optional[str] = Field(
        None,
        description="Optional message providing additional details about the current processing state"
    )


class DynamicAgentSetupResult(BaseModel):
    """Agent setup result schema.

    Extends BaseModel to include id, createdAt, and updatedAt fields.

    Attributes:
        processing_state: Real-time processing state for async operations
        success: Whether the setup was successful (nullable during processing)
        agent_configuration_id: ID of the created agent configuration
        instruction_configuration_id: ID of the created instruction configuration
        error_message: Error message if setup failed
        metadata: Additional metadata about the setup
    """

    processing_state: DynamicAgentProcessingState = Field(
        ...,
        description="Real-time processing state of the agent setup",
        alias="processingState"
    )
    success: Optional[bool] = Field(
        None,
        description="Indicates if the assistant setup was successful"
    )
    agent_configuration_id: Optional[str] = Field(
        None,
        description="ID of the agent configuration created for this assistant",
        alias="agentConfigurationId"
    )
    instruction_configuration_id: Optional[str] = Field(
        None,
        description="ID of the instruction configuration created for this assistant",
        alias="instructionConfigurationId"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if the setup failed, otherwise undefined",
        alias="errorMessage"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the assistant setup, if any"
    )
