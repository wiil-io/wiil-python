"""Agent configuration schema definitions.

Agent Configurations define the core behavior, capabilities, and personality of AI agents.
They reference LLM models and instruction configurations, and can be reused across
multiple deployments.
"""

from typing import Any, Dict, List, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.service_mgt.call_transfer_config import CallTransferConfig
from wiil.models.service_mgt.support_llm import TravnexSupportModel
from wiil.types.service_types import AssistantType, LLMType


class AgentConfiguration(BaseModel):
    """Agent Configuration model.

    Agent Configurations define the core behavior, capabilities, and personality of AI agents.
    They are designed to be reusable across multiple deployments, with each agent governed
    by an Instruction Configuration (1:N relationship).

    Architecture Context:
        - Managed By: Service Configuration (lifecycle management)
        - Used By: Deployment Configurations (N:1)
        - Associated With: Instruction Configuration (1:N)
        - References: Travnex Support Model Registry (via modelId)

    Attributes:
        id: Unique identifier for the agent configuration
        model_id: Identifier of the LLM model from Travnex Support Registry
        name: Human-readable name for the agent
        default_function_state: Default operational mode
        uses_travnex_support_model: Whether using Travnex's model registry
        required_model_config: Additional model parameters
        instruction_configuration_id: ID of the instruction configuration
        assistant_type: Channel specialization type
        call_transfer_config: Call transfer configurations
        metadata: Additional metadata
        model: Auto-populated model information from registry
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        agent = AgentConfiguration(
            id="123",
            model_id="YUSI21217J1",
            name="Customer Support Agent",
            default_function_state=LLMType.MULTI_MODE,
            uses_travnex_support_model=True,
            instruction_configuration_id="456",
            assistant_type=AssistantType.PHONE,
            call_transfer_config=[
                CallTransferConfig(
                    transfer_number="+15551234567",
                    transfer_type="warm",
                    transfer_conditions=["escalate", "speak to manager"]
                )
            ],
            metadata={"department": "support"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(
        ...,
        description="LLM model identifier from Travnex Support Registry",
        alias="modelId"
    )
    name: str = Field(
        ...,
        description="Human-readable name for the agent configuration"
    )
    default_function_state: LLMType = Field(
        LLMType.MULTI_MODE,
        description="Default operational mode (TEXT, VOICE, MULTI_MODE)",
        alias="defaultFunctionState"
    )
    uses_travnex_support_model: bool = Field(
        True,
        description="Whether using Travnex's supported model registry",
        alias="usesTravnexSupportModel"
    )
    required_model_config: Optional[Dict[str, Any]] = Field(
        None,
        description="Model-specific configuration parameters",
        alias="requiredModelConfig"
    )
    instruction_configuration_id: str = Field(
        ...,
        description="ID of the Instruction Configuration providing behavioral guidelines",
        alias="instructionConfigurationId"
    )
    assistant_type: AssistantType = Field(
        AssistantType.GENERAL,
        description="Channel specialization type (GENERAL, WEB, PHONE, EMAIL)",
        alias="assistantType"
    )
    call_transfer_config: List[CallTransferConfig] = Field(
        default_factory=list,
        description="Call transfer configurations for phone deployments"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata for organization and filtering"
    )
    model: Optional[TravnexSupportModel] = Field(
        None,
        description="Auto-populated model information from registry"
    )


class CreateAgentConfiguration(BaseModel):
    """Schema for creating a new agent configuration.

    Omits auto-generated fields (id, timestamps, model).

    Example:
        ```python
        create_data = CreateAgentConfiguration(
            model_id="YUSI21217J1",
            name="Sales Assistant",
            default_function_state=LLMType.MULTI_MODE,
            uses_travnex_support_model=True,
            instruction_configuration_id="789",
            assistant_type=AssistantType.WEB,
            required_model_config={"voiceId": "rachel", "languageId": "en-US"},
            call_transfer_config=[],
            metadata={"team": "sales"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    model_id: str = Field(..., alias="modelId")
    name: str
    default_function_state: LLMType = Field(LLMType.MULTI_MODE, alias="defaultFunctionState")
    uses_travnex_support_model: bool = Field(True, alias="usesTravnexSupportModel")
    required_model_config: Optional[Dict[str, Any]] = Field(None, alias="requiredModelConfig")
    instruction_configuration_id: str = Field(..., alias="instructionConfigurationId")
    assistant_type: AssistantType = Field(AssistantType.GENERAL, alias="assistantType")
    call_transfer_config: List[CallTransferConfig] = Field(
        default_factory=list
    )
    metadata: Optional[Dict[str, Any]] = None


class UpdateAgentConfiguration(BaseModel):
    """Schema for updating an existing agent configuration.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateAgentConfiguration(
            id="123",
            name="Updated Sales Assistant",
            metadata={"team": "enterprise-sales"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    model_id: Optional[str] = Field(None, alias="modelId")
    name: Optional[str] = None
    default_function_state: Optional[LLMType] = Field(None, alias="defaultFunctionState")
    uses_travnex_support_model: Optional[bool] = Field(None, alias="usesTravnexSupportModel")
    required_model_config: Optional[Dict[str, Any]] = Field(None, alias="requiredModelConfig")
    instruction_configuration_id: Optional[str] = Field(None, alias="instructionConfigurationId")
    assistant_type: Optional[AssistantType] = Field(None, alias="assistantType")
    call_transfer_config: Optional[List[CallTransferConfig]] = None
    metadata: Optional[Dict[str, Any]] = None
