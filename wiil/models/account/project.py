"""Project schema definitions for account management."""

from typing import Any, Dict, List, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.account_types import ServiceStatus


class Project(BaseModel):
    """Project entity.

    Represents a project within an organization, providing environment
    isolation and configuration management.

    Attributes:
        id: Unique identifier for the project
        name: Project name
        region_id: Geographic region ID for this project
        description: Optional description of the project's purpose
        compliance: Array of compliance standards this project adheres to
        current_subscription_id: ID of the current subscription plan
        is_default: Whether this is the default project for the organization
        service_status: Current service status
        metadata: Additional custom metadata for the project
        created_at: Timestamp when the project was created
        updated_at: Timestamp when the project was last updated

    Example:
        ```python
        project = Project(
            id='UEIW#@EWW123',
            name='Production Environment',
            region_id='us-west-2',
            description='Main production deployment',
            compliance=['SOC2', 'HIPAA'],
            is_default=True,
            service_status=ServiceStatus.ACTIVE,
            current_subscription_id='789',
            metadata={'environment': 'production'},
            created_at=1234567890,
            updated_at=1234567890
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        min_length=2,
        description="Project name (minimum 2 characters)"
    )
    region_id: Optional[str] = Field(
        None,
        description="Geographic region ID for this project (optional, can inherit from organization)",
        alias="regionId"
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the project's purpose"
    )
    compliance: Optional[List[str]] = Field(
        None,
        description="Array of compliance standards this project adheres to (e.g., SOC2, HIPAA)"
    )
    current_subscription_id: Optional[str] = Field(
        None,
        description="ID of the current subscription plan for this project",
        alias="currentSubscriptionId"
    )
    is_default: bool = Field(
        ...,
        description="Whether this is the default project for the organization (system-managed flag, set automatically on creation)",
        alias="isDefault"
    )
    service_status: ServiceStatus = Field(
        ServiceStatus.ACTIVE,
        description="Current service status of the project",
        alias="serviceStatus"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom metadata for the project"
    )


class CreateProject(BaseModel):
    """Schema for creating a new project.

    Omits auto-generated fields (id, timestamps) and system-managed fields (isDefault).

    Attributes:
        name: Project name
        region_id: Geographic region ID for this project
        description: Optional description of the project's purpose
        compliance: Array of compliance standards this project adheres to
        current_subscription_id: ID of the current subscription plan
        service_status: Current service status
        metadata: Additional custom metadata for the project

    Example:
        ```python
        create_data = CreateProject(
            name='Production Environment',
            region_id='us-west-2',
            description='Main production deployment',
            compliance=['SOC2', 'HIPAA'],
            service_status=ServiceStatus.ACTIVE,
            metadata={'environment': 'production'}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        min_length=2,
        description="Project name (minimum 2 characters)"
    )
    region_id: Optional[str] = Field(
        None,
        description="Geographic region ID for this project (optional, can inherit from organization)",
        alias="regionId"
    )
    description: Optional[str] = Field(
        None,
        description="Optional description of the project's purpose"
    )
    compliance: Optional[List[str]] = Field(
        None,
        description="Array of compliance standards this project adheres to (e.g., SOC2, HIPAA)"
    )
    current_subscription_id: Optional[str] = Field(
        None,
        description="ID of the current subscription plan for this project",
        alias="currentSubscriptionId"
    )
    service_status: Optional[ServiceStatus] = Field(
        None,
        description="Current service status of the project",
        alias="serviceStatus"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom metadata for the project"
    )


class UpdateProject(BaseModel):
    """Schema for updating an existing project.

    All CreateProject fields are optional (partial), with id required to identify the project.

    Attributes:
        id: Unique identifier for the project to update
        name: Updated project name
        region_id: Updated geographic region ID
        description: Updated description
        compliance: Updated compliance standards array
        current_subscription_id: Updated subscription plan ID
        service_status: Updated service status
        metadata: Updated metadata

    Example:
        ```python
        update_data = UpdateProject(
            id='proj_123',
            name='Production Environment v2',
            description='Updated production deployment',
            compliance=['SOC2', 'HIPAA', 'GDPR']
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for the project to update")
    name: Optional[str] = Field(
        None,
        min_length=2,
        description="Updated project name"
    )
    region_id: Optional[str] = Field(
        None,
        description="Updated geographic region ID",
        alias="regionId"
    )
    description: Optional[str] = Field(
        None,
        description="Updated description"
    )
    compliance: Optional[List[str]] = Field(
        None,
        description="Updated array of compliance standards"
    )
    current_subscription_id: Optional[str] = Field(
        None,
        description="Updated subscription plan ID",
        alias="currentSubscriptionId"
    )
    service_status: Optional[ServiceStatus] = Field(
        None,
        description="Updated service status",
        alias="serviceStatus"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Updated metadata"
    )
