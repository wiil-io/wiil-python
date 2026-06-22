"""Deployment configuration schema definitions.

Deployment Configuration is the central composition entity in the Service Configuration architecture.
It brings together agent behavior, instructions, organizational context, and channel configuration
to create a complete deployable unit. Each deployment has exactly one channel (1:1 relationship).
"""

from typing import Any, Dict, Literal, Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions import DeploymentProvisioningType, DeploymentStatus


class DeploymentConfiguration(EntityModel):
    """Deployment configuration.

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
        - CHAINED: Uses provisioning chain (STT -> Agent -> TTS) for voice processing

    Deployment Lifecycle:
        - PENDING: Created but not yet activated
        - ACTIVE: Operational and accepting interactions
        - SUSPENDED: Temporarily paused
        - FAILED: Deployment encountered errors

    Attributes:
        project_id: ID of the project this deployment belongs to
        deployment_channel_id: ID of the deployment channel (1:1 relationship)
        deployment_name: Optional human-readable name for administrative identification
        agent_configuration_id: ID of the agent configuration defining core behavior
        instruction_configuration_id: ID of the instruction configuration providing behavioral guidelines
        deployment_status: Current operational status
        provisioning_type: How this deployment processes interactions
        provisioning_config_chain_id: ID of the provisioning chain for voice processing
        is_active: Whether this deployment is currently active
        channel: Populated deployment channel configuration
        project: Populated project information
        agent: Populated agent configuration
        instruction: Populated instruction configuration
    """

    project_id: str = Field(
        ...,
        description="ID of the project this deployment belongs to for organizational grouping and access control",
        alias="projectId"
    )
    deployment_channel_id: str = Field(
        ...,
        description="ID of the deployment channel through which this deployment is accessible (1:1 relationship)",
        alias="deploymentChannelId"
    )
    deployment_name: Optional[str] = Field(
        None,
        description="Optional human-readable name for the deployment used in administrative interfaces",
        alias="deploymentName"
    )
    agent_configuration_id: str = Field(
        ...,
        description="ID of the agent configuration that defines the agent's core behavior and capabilities (N:1)",
        alias="agentConfigurationId"
    )
    instruction_configuration_id: str = Field(
        ...,
        description="ID of the instruction configuration that provides behavioral guidelines for the agent (N:1)",
        alias="instructionConfigurationId"
    )
    deployment_status: DeploymentStatus = Field(
        ...,
        description="Current operational status (PENDING, ACTIVE, SUSPENDED, FAILED)",
        alias="deploymentStatus"
    )
    provisioning_type: DeploymentProvisioningType = Field(
        DeploymentProvisioningType.DIRECT,
        description="How this deployment processes interactions: DIRECT for direct agent processing, CHAINED for voice processing pipeline",
        alias="provisioningType"
    )
    provisioning_config_chain_id: Optional[str] = Field(
        None,
        description="ID of the provisioning configuration chain for voice processing (required for CHAINED type)",
        alias="provisioningConfigChainId"
    )
    is_active: bool = Field(
        False,
        description="Whether this deployment is currently active and accepting user interactions",
        alias="isActive"
    )
    channel: Optional[Dict[str, Any]] = Field(
        None,
        description="Populated deployment channel configuration (null if not loaded)"
    )
    project: Optional[Dict[str, Any]] = Field(
        None,
        description="Populated project information (null if not loaded)"
    )
    agent: Optional[Dict[str, Any]] = Field(
        None,
        description="Populated agent configuration (null if not loaded)"
    )
    instruction: Optional[Dict[str, Any]] = Field(
        None,
        description="Populated instruction configuration (null if not loaded)"
    )


class CreateDeploymentConfiguration(BaseModel):
    """Schema for creating a new deployment configuration.

    Omits auto-generated fields and populated relations. Sets deployment to PENDING status
    with DIRECT provisioning by default.
    """

    project_id: str = Field(..., alias="projectId")
    deployment_channel_id: str = Field(..., alias="deploymentChannelId")
    deployment_name: Optional[str] = Field(None, alias="deploymentName")
    agent_configuration_id: str = Field(..., alias="agentConfigurationId")
    instruction_configuration_id: str = Field(..., alias="instructionConfigurationId")
    provisioning_config_chain_id: Optional[str] = Field(None, alias="provisioningConfigChainId")
    is_active: bool = Field(False, alias="isActive")


class CreateChainDeploymentConfiguration(BaseModel):
    """Schema for creating a chained deployment configuration.

    Similar to CreateDeploymentConfiguration but requires a provisioningConfigChainId
    and sets provisioningType to CHAINED by default.
    """

    project_id: str = Field(..., alias="projectId")
    deployment_channel_id: str = Field(..., alias="deploymentChannelId")
    deployment_name: Optional[str] = Field(None, alias="deploymentName")
    agent_configuration_id: str = Field(..., alias="agentConfigurationId")
    instruction_configuration_id: str = Field(..., alias="instructionConfigurationId")
    provisioning_config_chain_id: str = Field(..., alias="provisioningConfigChainId")
    deployment_status: Literal[DeploymentStatus.PENDING] = Field(
        DeploymentStatus.PENDING,
        alias="deploymentStatus"
    )
    provisioning_type: DeploymentProvisioningType = Field(
        DeploymentProvisioningType.CHAINED,
        alias="provisioningType"
    )
    is_active: bool = Field(False, alias="isActive")


class UpdateDeploymentConfiguration(BaseModel):
    """Schema for updating an existing deployment configuration.

    All fields from CreateDeploymentConfiguration are optional (partial),
    with the id field required to identify the deployment to update.
    """

    id: str
    project_id: Optional[str] = Field(None, alias="projectId")
    deployment_channel_id: Optional[str] = Field(None, alias="deploymentChannelId")
    deployment_name: Optional[str] = Field(None, alias="deploymentName")
    agent_configuration_id: Optional[str] = Field(None, alias="agentConfigurationId")
    instruction_configuration_id: Optional[str] = Field(None, alias="instructionConfigurationId")
    provisioning_config_chain_id: Optional[str] = Field(None, alias="provisioningConfigChainId")
    is_active: Optional[bool] = Field(None, alias="isActive")


class DeploymentConfigurationResult(EntityModel):
    """Deployment configuration result (lightweight version).

    Omits populated relation fields (channel, project, agent, instruction) to provide
    a lighter payload suitable for list views and search results.
    """

    project_id: str = Field(..., alias="projectId")
    deployment_channel_id: str = Field(..., alias="deploymentChannelId")
    deployment_name: Optional[str] = Field(None, alias="deploymentName")
    agent_configuration_id: str = Field(..., alias="agentConfigurationId")
    instruction_configuration_id: str = Field(..., alias="instructionConfigurationId")
    deployment_status: DeploymentStatus = Field(..., alias="deploymentStatus")
    provisioning_type: DeploymentProvisioningType = Field(
        DeploymentProvisioningType.DIRECT,
        alias="provisioningType"
    )
    provisioning_config_chain_id: Optional[str] = Field(None, alias="provisioningConfigChainId")
    is_active: bool = Field(False, alias="isActive")


class DeploymentConfigurationDetails(EntityModel):
    """Deployment configuration details (full version with all relations).

    Extends the base schema by requiring all relation fields to be fully populated.
    Ideal for detail views where complete information is needed.
    """

    project_id: str = Field(..., alias="projectId")
    deployment_channel_id: str = Field(..., alias="deploymentChannelId")
    deployment_name: Optional[str] = Field(None, alias="deploymentName")
    agent_configuration_id: str = Field(..., alias="agentConfigurationId")
    instruction_configuration_id: str = Field(..., alias="instructionConfigurationId")
    deployment_status: DeploymentStatus = Field(..., alias="deploymentStatus")
    provisioning_type: DeploymentProvisioningType = Field(
        DeploymentProvisioningType.DIRECT,
        alias="provisioningType"
    )
    provisioning_config_chain_id: Optional[str] = Field(None, alias="provisioningConfigChainId")
    is_active: bool = Field(False, alias="isActive")
    channel: Dict[str, Any] = Field(..., description="Populated deployment channel configuration")
    project: Dict[str, Any] = Field(..., description="Populated project information")
    agent: Dict[str, Any] = Field(..., description="Populated agent configuration")
    instruction: Dict[str, Any] = Field(..., description="Populated instruction configuration")
