"""Provisioning Configurations resource for managing provisioning configuration entities."""

from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    ProvisioningConfigChain,
    TranslationChainConfig,
    CreateProvisioningConfig,
    CreateTranslationChainConfig,
    UpdateProvisioningConfig,
)
from wiil.types import PaginatedResult


class ProvisioningConfigurationsResource:
    """Resource class for managing provisioning configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    provisioning configurations. Provisioning configurations define processing
    chains and translation configurations for AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/provisioning-configurations'

    def create(self, **kwargs: Any) -> ProvisioningConfigChain:
        """Create a new provisioning configuration chain."""
        data = CreateProvisioningConfig(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProvisioningConfig
        )

    def create_translation(self, **kwargs: Any) -> TranslationChainConfig:
        """Create a new translation configuration chain."""
        data = CreateTranslationChainConfig(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTranslationChainConfig
        )

    def get(self, config_id: str) -> Union[ProvisioningConfigChain, TranslationChainConfig]:
        """Retrieve a provisioning configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def get_by_chain_name(self, chain_name: str) -> Union[ProvisioningConfigChain, TranslationChainConfig]:
        """Retrieve a provisioning configuration by chain name."""
        return self._http.get(f'{self._base_path}/by-chain-name/{chain_name}')

    def update(self, **kwargs: Any) -> ProvisioningConfigChain:
        """Update an existing provisioning configuration."""
        data = UpdateProvisioningConfig(**kwargs)
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
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[Union[ProvisioningConfigChain, TranslationChainConfig]]:
        """List all provisioning configurations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if include_deleted is not None:
            params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def list_provisioning_chains(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ProvisioningConfigChain]:
        """List provisioning configuration chains with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/provisioning{query_string}')

    def list_translation_chains(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[TranslationChainConfig]:
        """List translation configuration chains with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/translations{query_string}')


__all__ = ['ProvisioningConfigurationsResource']
