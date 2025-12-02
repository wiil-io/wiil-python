"""Deployment Configurations resource for managing deployment configuration entities."""

from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    DeploymentConfigurationResult,
    CreateDeploymentConfiguration,
    CreateChainDeploymentConfiguration,
    UpdateDeploymentConfiguration,
)
from wiil.types import PaginatedResult


class DeploymentConfigurationsResource:
    """Resource class for managing deployment configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    deployment configurations. Deployment configurations link agents, instructions,
    and channels together to create complete AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/deployment-configurations'

    def create(self, **kwargs: Any) -> DeploymentConfigurationResult:
        """Create a new deployment configuration."""
        data = CreateDeploymentConfiguration(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateDeploymentConfiguration
        )

    def create_chain(self, **kwargs: Any) -> DeploymentConfigurationResult:
        """Create a chained deployment configuration."""
        data = CreateChainDeploymentConfiguration(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateChainDeploymentConfiguration
        )

    def get(self, config_id: str) -> DeploymentConfigurationResult:
        """Retrieve a deployment configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def get_by_channel(self, channel_id: str) -> DeploymentConfigurationResult:
        """Retrieve a deployment configuration by channel ID."""
        return self._http.get(f'{self._base_path}/by-channel/{channel_id}')

    def update(self, **kwargs: Any) -> DeploymentConfigurationResult:
        """Update an existing deployment configuration."""
        data = UpdateDeploymentConfiguration(**kwargs)
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
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[DeploymentConfigurationResult]:
        """List deployment configurations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def list_by_project(
        self,
        project_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[DeploymentConfigurationResult]:
        """List deployment configurations by project ID."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-project/{project_id}{query_string}')

    def list_by_agent(
        self,
        agent_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[DeploymentConfigurationResult]:
        """List deployment configurations by agent configuration ID."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-agent/{agent_id}{query_string}')

    def list_by_instruction(
        self,
        instruction_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[DeploymentConfigurationResult]:
        """List deployment configurations by instruction configuration ID."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-instruction/{instruction_id}{query_string}')


__all__ = ['DeploymentConfigurationsResource']
