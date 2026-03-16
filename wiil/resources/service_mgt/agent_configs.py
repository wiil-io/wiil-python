"""Agent Configurations resource for managing agent configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    AgentConfiguration,
    CreateAgentConfiguration,
    UpdateAgentConfiguration,
)
from wiil.types import PaginatedResult, PaginationRequest


class AgentConfigurationsResource:
    """Resource class for managing agent configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    agent configurations. Agent configurations define the behavior and settings
    for AI agents in the system.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/agent-configurations'

    def create(self, data: CreateAgentConfiguration) -> AgentConfiguration:
        """Create a new agent configuration.

        Args:
            data: Agent configuration creation data

        Returns:
            The created agent configuration
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateAgentConfiguration,
            response_model=AgentConfiguration
        )

    def get(self, config_id: str) -> AgentConfiguration:
        """Retrieve an agent configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}', response_model=AgentConfiguration)

    def update(self, data: UpdateAgentConfiguration) -> AgentConfiguration:
        """Update an existing agent configuration.

        Args:
            data: Agent configuration update data (must include id)

        Returns:
            The updated agent configuration
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateAgentConfiguration,
            response_model=AgentConfiguration
        )

    def delete(self, config_id: str) -> bool:
        """Delete an agent configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[AgentConfiguration]:
        """List agent configurations with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of agent configurations
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[AgentConfiguration]
        )


__all__ = ['AgentConfigurationsResource']
