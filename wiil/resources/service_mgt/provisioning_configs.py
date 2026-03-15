"""Provisioning Configurations resource for managing provisioning configuration entities."""

from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    ProvisioningConfigChain,
    UpdateProvisioningConfig,
)
from wiil.types import PaginatedResult, PaginationRequest


class ProvisioningConfigurationsResource:
    """Resource class for managing provisioning configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    provisioning configurations. Provisioning configurations define processing
    chains and translation configurations for AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/provisioning-configurations'

    def create(self, data: CreateProvisioningConfig) -> ProvisioningConfigChain:
        """Create a new provisioning configuration chain.

        Args:
            data: Provisioning configuration creation data

        Returns:
            The created provisioning configuration chain
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProvisioningConfig
        )

    def get(self, config_id: str) -> ProvisioningConfigChain:
        """Retrieve a provisioning configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def get_by_chain_name(self, chain_name: str) -> ProvisioningConfigChain:
        """Retrieve a provisioning configuration by chain name."""
        return self._http.get(f'{self._base_path}/by-chain-name/{chain_name}')

    def update(self, data: UpdateProvisioningConfig) -> ProvisioningConfigChain:
        """Update an existing provisioning configuration.

        Args:
            data: Provisioning configuration update data (must include id)

        Returns:
            The updated provisioning configuration chain
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProvisioningConfig
        )

    def delete(self, config_id: str) -> bool:
        """Delete a provisioning configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[ProvisioningConfigChain]:
        """List all provisioning configurations with pagination.

        Args:
            params: Pagination parameters
            include_deleted: Include deleted configurations

        Returns:
            Paginated list of provisioning configurations
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size
        if include_deleted is not None:
            query_params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def list_provisioning_chains(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ProvisioningConfigChain]:
        """List provisioning configuration chains with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of provisioning configuration chains
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/provisioning{query_string}')


__all__ = ['ProvisioningConfigurationsResource']
