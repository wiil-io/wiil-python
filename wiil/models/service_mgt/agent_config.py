"""Agent configuration schema definitions.

Agent Configurations define the core behavior, capabilities, and personality of AI agents.
They reference LLM models and instruction configurations, and can be reused across multiple
deployments. The Instruction Configuration (1:N relationship) governs agent behavior.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, field_validator

from wiil.models.base import BaseModel
from wiil.models.service_mgt.call_transfer_config import CallTransferConfig
from wiil.models.service_mgt.support_llm import WiilSupportModel
from wiil.models.type_definitions import AssistantType, LLMType


class AgentConfiguration(BaseModel):
    """Agent configuration for AI assistant behavior.

    Agent Configurations define the core behavior, capabilities, and personality of AI agents in the
    Service Configuration architecture. They are designed to be reusable across multiple deployments,
    with each agent governed by an Instruction Configuration (1:N relationship). Multiple Agent
    Configurations can share the same Instruction Configuration for consistent behavioral guidelines.

    Architecture Context:
        - Managed By: Service Configuration (lifecycle management)
        - Used By: Deployment Configurations (N:1 - multiple deployments can use the same agent)
        - Associated With: Instruction Configuration (1:N - one instruction set can govern multiple agents)
        - References: Wiil Support Model Registry (via modelId)
        - Reusability: Designed to be reused across multiple deployments with different channels

    Configuration Layers:
        - Agent Configuration: Defines capabilities, model, and operational mode
        - Instruction Configuration: Defines behavioral guidelines and conversation flow
        - Together they create a complete agent persona

    Attributes:
        model_id: Identifier of the LLM model from Wiil Support Registry
        name: Personal name for the AI agent (max 30 characters)
        default_function_state: Default operational mode (TEXT, VOICE, MULTI_MODE)
        uses_wiil_support_model: Whether this agent uses Wiil's supported model registry
        required_model_config: Additional model parameters
        instruction_configuration_id: ID of the instruction configuration providing behavioral guidelines
        assistant_type: Channel specialization type (GENERAL, WEB, PHONE, etc.)
        call_transfer_config: Call transfer configurations for phone deployments
        metadata: Additional metadata for organization and filtering
        model: Auto-populated model information from registry
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="Identifier of the LLM model from Wiil Support Registry to power this agent",
        alias="modelId"
    )
    name: str = Field(
        ...,
        max_length=30,
        description="Personal name for the AI agent used in conversations (e.g., 'Sarah', 'James')"
    )
    default_function_state: LLMType = Field(
        LLMType.MULTI_MODE,
        description="Default operational mode (TEXT, VOICE, MULTI_MODE)",
        alias="defaultFunctionState"
    )
    uses_wiil_support_model: bool = Field(
        True,
        description="Whether this agent uses a model from Wiil's curated registry (true) or a custom external model (false)",
        alias="usesWiilSupportModel"
    )
    required_model_config: Optional[Dict[str, Any]] = Field(
        None,
        description="Model-specific configuration parameters as key-value pairs (e.g., { voiceId: 'adam', languageId: 'en-US' })",
        alias="requiredModelConfig"
    )
    instruction_configuration_id: str = Field(
        ...,
        description="ID of the Instruction Configuration providing behavioral guidelines. Multiple agents can share the same instruction configuration (N:1)",
        alias="instructionConfigurationId"
    )
    assistant_type: AssistantType = Field(
        AssistantType.GENERAL,
        description="Channel specialization type for optimization (GENERAL, WEB, PHONE, EMAIL)",
        alias="assistantType"
    )
    call_transfer_config: List[CallTransferConfig] = Field(
        default_factory=list,
        description="Array of call transfer configurations for phone deployments"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata for organization including tags, categories, department"
    )
    model: Optional[WiilSupportModel] = Field(
        None,
        description="Complete model information auto-populated from Wiil registry (null if not loaded)"
    )


class CreateAgentConfiguration(PydanticBaseModel):
    """Schema for creating a new agent configuration.

    Omits auto-generated fields (id, timestamps, model) that are populated by the system.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: Optional[str] = Field(None, alias="modelId")
    name: str = Field(..., max_length=30)
    default_function_state: LLMType = Field(LLMType.MULTI_MODE, alias="defaultFunctionState")
    uses_wiil_support_model: bool = Field(True, alias="usesWiilSupportModel")
    required_model_config: Optional[Dict[str, Any]] = Field(None, alias="requiredModelConfig")
    instruction_configuration_id: str = Field(..., alias="instructionConfigurationId")
    assistant_type: AssistantType = Field(AssistantType.GENERAL, alias="assistantType")
    call_transfer_config: List[CallTransferConfig] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("assistant_type", mode="before")
    @classmethod
    def normalize_assistant_type(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()
        return value


class UpdateAgentConfiguration(PydanticBaseModel):
    """Schema for updating an existing agent configuration.

    All fields are optional except id.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    model_id: Optional[str] = Field(None, alias="modelId")
    name: Optional[str] = Field(None, max_length=30)
    default_function_state: Optional[LLMType] = Field(None, alias="defaultFunctionState")
    uses_wiil_support_model: Optional[bool] = Field(None, alias="usesWiilSupportModel")
    required_model_config: Optional[Dict[str, Any]] = Field(None, alias="requiredModelConfig")
    instruction_configuration_id: Optional[str] = Field(None, alias="instructionConfigurationId")
    assistant_type: Optional[AssistantType] = Field(None, alias="assistantType")
    call_transfer_config: Optional[List[CallTransferConfig]] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator("assistant_type", mode="before")
    @classmethod
    def normalize_assistant_type(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.lower()
        return value


class AgentConfigurationDeleteRequest(PydanticBaseModel):
    """Request to delete an agent configuration."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier of the agent configuration to delete")
    delete_phone_config: bool = Field(
        True,
        description="Whether to also delete associated phone configurations",
        alias="deletePhoneConfig"
    )
