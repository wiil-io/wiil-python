"""Dynamic Web Agent resource for managing web agent configurations."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.dynamic_setup import (
    DynamicWebAgentSetup,
    DynamicWebAgentSetupResult,
    UpdateDynamicWebAgent,
)
from wiil.types import PaginatedResult, PaginationRequest


class DynamicWebAgentResource:
    """Resource class for managing dynamic web agents in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    dynamic web agent configurations. Web agents are deployed on web channels
    for customer interactions via chat widgets.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/dynamic-web-agent'

    def create(self, data: DynamicWebAgentSetup) -> DynamicWebAgentSetupResult:
        """Create a new dynamic web agent.

        Args:
            data: Web agent setup data

        Returns:
            The setup result with processing status
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=DynamicWebAgentSetup
        )

    def get(self, agent_id: str) -> DynamicWebAgentSetupResult:
        """Retrieve a dynamic web agent by ID.

        Args:
            agent_id: Web agent ID

        Returns:
            The web agent setup result
        """
        return self._http.get(f'{self._base_path}/{agent_id}')

    def update(self, data: UpdateDynamicWebAgent) -> DynamicWebAgentSetupResult:
        """Update an existing dynamic web agent.

        Args:
            data: Web agent update data (must include id)

        Returns:
            The updated web agent setup result
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateDynamicWebAgent
        )

    def delete(self, agent_id: str) -> bool:
        """Delete a dynamic web agent.

        Args:
            agent_id: Web agent ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/{agent_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DynamicWebAgentSetupResult]:
        """List dynamic web agents with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of web agent setup results
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['DynamicWebAgentResource']
