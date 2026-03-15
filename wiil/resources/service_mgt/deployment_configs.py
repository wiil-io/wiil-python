"""Deployment Configurations resource for managing deployment configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    DeploymentConfiguration,
    CreateDeploymentConfiguration,
    UpdateDeploymentConfiguration,
)
from wiil.types import PaginatedResult, PaginationRequest


class DeploymentConfigurationsResource:
    """Resource class for managing deployment configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    deployment configurations. Deployment configurations link agents, instructions,
    and channels together to create complete AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/deployment-configurations'

    def create(self, data: CreateDeploymentConfiguration) -> DeploymentConfiguration:
        """Create a new deployment configuration.

        Args:
            data: Deployment configuration creation data

        Returns:
            The created deployment configuration
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateDeploymentConfiguration
        )

    def get(self, config_id: str) -> DeploymentConfiguration:
        """Retrieve a deployment configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def get_by_channel(self, channel_id: str) -> DeploymentConfiguration:
        """Retrieve a deployment configuration by channel ID."""
        return self._http.get(f'{self._base_path}/by-channel/{channel_id}')

    def update(self, data: UpdateDeploymentConfiguration) -> DeploymentConfiguration:
        """Update an existing deployment configuration.

        Args:
            data: Deployment configuration update data (must include id)

        Returns:
            The updated deployment configuration
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateDeploymentConfiguration
        )

    def delete(self, config_id: str) -> bool:
        """Delete a deployment configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DeploymentConfiguration]:
        """List deployment configurations with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of deployment configurations
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def list_by_project(
        self,
        project_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DeploymentConfiguration]:
        """List deployment configurations by project ID.

        Args:
            project_id: Project ID
            params: Pagination parameters

        Returns:
            Paginated list of deployment configurations for the project
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/by-project/{project_id}{query_string}')

    def list_by_agent(
        self,
        agent_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DeploymentConfiguration]:
        """List deployment configurations by agent configuration ID.

        Args:
            agent_id: Agent configuration ID
            params: Pagination parameters

        Returns:
            Paginated list of deployment configurations using the agent
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/by-agent/{agent_id}{query_string}')

    def list_by_instruction(
        self,
        instruction_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DeploymentConfiguration]:
        """List deployment configurations by instruction configuration ID.

        Args:
            instruction_id: Instruction configuration ID
            params: Pagination parameters

        Returns:
            Paginated list of deployment configurations using the instruction
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/by-instruction/{instruction_id}{query_string}')


__all__ = ['DeploymentConfigurationsResource']
