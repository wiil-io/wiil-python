"""Agent Configurations resource for managing agent configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    AgentConfiguration,
    CreateAgentConfiguration,
    UpdateAgentConfiguration,
)
from wiil.types import PaginatedResult


class AgentConfigurationsResource:
    """Resource class for managing agent configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    agent configurations. Agent configurations define the behavior and settings
    for AI agents in the system.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/agent-configurations'

    def create(self, **kwargs: Any) -> AgentConfiguration:
        """Create a new agent configuration."""
        data = CreateAgentConfiguration(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateAgentConfiguration
        )

    def get(self, config_id: str) -> AgentConfiguration:
        """Retrieve an agent configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def update(self, **kwargs: Any) -> AgentConfiguration:
        """Update an existing agent configuration."""
        data = UpdateAgentConfiguration(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateAgentConfiguration
        )

    def delete(self, config_id: str) -> bool:
        """Delete an agent configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[AgentConfiguration]:
        """List agent configurations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['AgentConfigurationsResource']
