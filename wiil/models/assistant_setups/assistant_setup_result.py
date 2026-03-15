"""Assistant setup result schema definitions.

This module mirrors src/core/assistant-setups/assistant-setup-result.schema.ts
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from wiil.models.service_mgt.agent_config import AgentConfiguration
from wiil.models.service_mgt.interaction_channels import DeploymentChannel
from wiil.models.service_mgt.deployment_config import DeploymentConfiguration
from wiil.models.service_mgt.instruction_config import InstructionConfiguration


class AssistantSetupResult(BaseModel):
    """Result schema for assistant setup operations.

    Contains the complete result of an assistant setup operation including
    all created configurations and deployment details.

    Attributes:
        success: Whether the setup was successful
        agent_configuration: The created agent configuration
        instruction_configuration: The created instruction configuration
        deployment_channels: List of deployment channels created
        deployment_configurations: List of deployment configurations created
        error_message: Error message if setup failed
        metadata: Additional metadata about the setup

    Example:
        ```python
        result = AssistantSetupResult(
            success=True,
            agent_configuration=agent_config,
            instruction_configuration=instruction_config,
            deployment_channels=[channel],
            deployment_configurations=[deployment],
            metadata={"setup_time_ms": 1234}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    success: bool = Field(
        ...,
        description="Whether the setup operation was successful"
    )
    agent_configuration: AgentConfiguration = Field(
        ...,
        description="The created agent configuration",
        alias="agentConfiguration"
    )
    instruction_configuration: InstructionConfiguration = Field(
        ...,
        description="The created instruction configuration",
        alias="instructionConfiguration"
    )
    deployment_channels: List[DeploymentChannel] = Field(
        ...,
        description="List of deployment channels created",
        alias="deploymentChannels"
    )
    deployment_configurations: List[DeploymentConfiguration] = Field(
        ...,
        description="List of deployment configurations created",
        alias="deploymentConfigurations"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if setup failed",
        alias="errorMessage"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the setup"
    )
