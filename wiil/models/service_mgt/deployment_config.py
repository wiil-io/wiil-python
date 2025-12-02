"""Deployment configuration schema definitions.

Deployment Configuration is the central composition entity in the Service Configuration architecture.
It brings together agent behavior, instructions, organizational context, and channel configuration
to create a complete deployable unit. Each deployment has exactly one channel (1:1 relationship).
"""

from typing import Any, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.service_types import DeploymentProvisioningType, DeploymentStatus


class DeploymentConfiguration(BaseModel):
    """Deployment Configuration model.

    The Deployment Configuration is the central composition entity that brings together agent behavior,
    instructions, and organizational context to create a deployable unit. It serves as the primary
    entity that operators interact with when setting up new agent deployments.

    Architecture Context:
        - Central Entity: Primary composition point for all deployment components
        - Managed By: Service Configuration (administrative oversight)
        - Uses: Agent Configuration (N:1), Instruction Configuration (N:1)
        - Associated With: Project (N:1 for organizational grouping)
        - Has: Deployment Channel (1:1 - each deployment exposes through exactly one channel)
        - Pattern: Multi-channel deployments require separate Deployment Configurations per channel

    Provisioning Types:
        - DIRECT: Agent processes interactions directly without additional chains
        - CHAINED: Uses provisioning chain (STT → Agent → TTS) for voice processing

    Deployment Lifecycle:
        - PENDING: Created but not yet activated
        - ACTIVE: Operational and accepting interactions
        - SUSPENDED: Temporarily paused
        - FAILED: Deployment encountered errors

    Attributes:
        id: Unique identifier for the deployment configuration
        project_id: ID of the project this deployment belongs to
        deployment_channel_id: ID of the deployment channel (1:1 relationship)
        deployment_name: Optional human-readable name for administrative identification
        agent_configuration_id: ID of the agent configuration defining core behavior (N:1)
        instruction_configuration_id: ID of the instruction configuration providing guidelines (N:1)
        deployment_status: Current operational status
        provisioning_type: How this deployment processes interactions (DIRECT or CHAINED)
        provisioning_config_chain_id: ID of the provisioning chain for voice processing
        is_active: Whether this deployment is currently active and accepting interactions
        channel: Populated deployment channel configuration (for detail views)
        project: Populated project information (for detail views)
        agent: Populated agent configuration (for detail views)
        instruction: Populated instruction configuration (for detail views)
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        deployment = DeploymentConfiguration(
            id="123",
            project_id="456",
            deployment_channel_id="abc",
            deployment_name="Production Customer Support",
            agent_configuration_id="def",
            instruction_configuration_id="ghi",
            deployment_status=DeploymentStatus.ACTIVE,
            provisioning_type=DeploymentProvisioningType.DIRECT,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    project_id: str = Field(
        ...,
        description="ID of the project this deployment belongs to for organizational grouping, access control, and resource management",
        alias="projectId"
    )
    deployment_channel_id: str = Field(
        ...,
        description="ID of the deployment channel through which this deployment is accessible (1:1 relationship - each deployment has exactly one channel)",
        alias="deploymentChannelId"
    )
    deployment_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the deployment used in administrative interfaces and reporting",
        alias="deploymentName"
    )
    agent_configuration_id: str = Field(
        ...,
        description="ID of the agent configuration that defines the agent's core behavior, capabilities, and LLM model (N:1 relationship - multiple deployments can share an agent)",
        alias="agentConfigurationId"
    )
    instruction_configuration_id: str = Field(
        ...,
        description="ID of the instruction configuration that provides behavioral guidelines, role definition, and conversation patterns for the agent (N:1 relationship)",
        alias="instructionConfigurationId"
    )
    deployment_status: DeploymentStatus = Field(
        ...,
        description="Current operational status of the deployment (PENDING: awaiting activation, ACTIVE: operational, SUSPENDED: temporarily paused, FAILED: encountered errors)",
        alias="deploymentStatus"
    )
    provisioning_type: DeploymentProvisioningType = Field(
        DeploymentProvisioningType.DIRECT,
        description="How this deployment processes interactions: DIRECT for direct agent processing, CHAINED for provisioning chain (STT → Agent → TTS) voice processing",
        alias="provisioningType"
    )
    provisioning_config_chain_id: Optional[str] = Field(
        None,
        description="ID of the provisioning configuration chain for voice processing (required for CHAINED provisioning type, links STT, agent, and TTS models)",
        alias="provisioningConfigChainId"
    )
    is_active: bool = Field(
        False,
        description="Whether this deployment is currently active and accepting user interactions (independent of deploymentStatus for granular control)",
        alias="isActive"
    )
    channel: Optional[Any] = Field(
        None,
        description="Populated deployment channel configuration including type, identifier, and channel-specific settings (null if not loaded, populated for detail views)"
    )
    project: Optional[Any] = Field(
        None,
        description="Populated project information including name and organizational details (null if not loaded, populated for detail views)"
    )
    agent: Optional[Any] = Field(
        None,
        description="Populated agent configuration including model, operational mode, and capabilities (null if not loaded, populated for detail views)"
    )
    instruction: Optional[Any] = Field(
        None,
        description="Populated instruction configuration including role, guidelines, and knowledge sources (null if not loaded, populated for detail views)"
    )


class CreateDeploymentConfiguration(BaseModel):
    """Schema for creating a new deployment configuration.

    Omits auto-generated fields and populated relations. Sets deployment to PENDING status
    with DIRECT provisioning by default.

    This schema enforces required fields for deployment creation while excluding
    fields that are automatically generated or populated by the system.

    Attributes:
        project_id: ID of the project this deployment belongs to
        deployment_channel_id: ID of the deployment channel
        deployment_name: Optional human-readable name
        agent_configuration_id: ID of the agent configuration
        instruction_configuration_id: ID of the instruction configuration
        provisioning_config_chain_id: Optional ID of the provisioning chain
        is_active: Whether deployment is active (default: False)

    Example:
        ```python
        new_deployment = CreateDeploymentConfiguration(
            project_id="456",
            deployment_channel_id="abc",
            deployment_name="Customer Support Line",
            agent_configuration_id="def",
            instruction_configuration_id="ghi",
            is_active=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    project_id: str = Field(
        ...,
        description="ID of the project this deployment belongs to",
        alias="projectId"
    )
    deployment_channel_id: str = Field(
        ...,
        description="ID of the deployment channel",
        alias="deploymentChannelId"
    )
    deployment_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the deployment",
        alias="deploymentName"
    )
    agent_configuration_id: str = Field(
        ...,
        description="ID of the agent configuration",
        alias="agentConfigurationId"
    )
    instruction_configuration_id: str = Field(
        ...,
        description="ID of the instruction configuration",
        alias="instructionConfigurationId"
    )
    provisioning_config_chain_id: Optional[str] = Field(
        None,
        description="Optional ID of the provisioning configuration chain",
        alias="provisioningConfigChainId"
    )
    is_active: bool = Field(
        False,
        description="Whether deployment is active",
        alias="isActive"
    )


class UpdateDeploymentConfiguration(BaseModel):
    """Schema for updating an existing deployment configuration.

    All fields from CreateDeploymentConfiguration are optional (partial),
    with the id field required to identify the deployment to update.

    Supports partial updates - only include the fields you want to modify.
    The id field is mandatory to specify which deployment configuration to update.

    Attributes:
        id: Unique identifier of the deployment to update
        project_id: Optional update to the project association
        deployment_channel_id: Optional update to the deployment channel
        deployment_name: Optional update to the human-readable name
        agent_configuration_id: Optional update to the agent configuration
        instruction_configuration_id: Optional update to the instruction configuration
        deployment_status: Optional update to the deployment status
        provisioning_type: Optional update to the provisioning type
        provisioning_config_chain_id: Optional update to the provisioning chain ID
        is_active: Optional update to the active status

    Example:
        ```python
        update_deployment = UpdateDeploymentConfiguration(
            id="123",
            deployment_name="Updated Support Line",
            is_active=True,
            deployment_status=DeploymentStatus.ACTIVE
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(
        ...,
        description="Unique identifier of the deployment to update"
    )
    project_id: Optional[str] = Field(
        None,
        description="Optional update to the project association",
        alias="projectId"
    )
    deployment_channel_id: Optional[str] = Field(
        None,
        description="Optional update to the deployment channel",
        alias="deploymentChannelId"
    )
    deployment_name: Optional[str] = Field(
        None,
        description="Optional update to the human-readable name",
        alias="deploymentName"
    )
    agent_configuration_id: Optional[str] = Field(
        None,
        description="Optional update to the agent configuration",
        alias="agentConfigurationId"
    )
    instruction_configuration_id: Optional[str] = Field(
        None,
        description="Optional update to the instruction configuration",
        alias="instructionConfigurationId"
    )
    deployment_status: Optional[DeploymentStatus] = Field(
        None,
        description="Optional update to the deployment status",
        alias="deploymentStatus"
    )
    provisioning_type: Optional[DeploymentProvisioningType] = Field(
        None,
        description="Optional update to the provisioning type",
        alias="provisioningType"
    )
    provisioning_config_chain_id: Optional[str] = Field(
        None,
        description="Optional update to the provisioning chain ID",
        alias="provisioningConfigChainId"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Optional update to the active status",
        alias="isActive"
    )
