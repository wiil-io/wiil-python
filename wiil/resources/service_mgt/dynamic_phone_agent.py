"""Dynamic Phone Agent resource for managing phone agent configurations."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.dynamic_setup import (
    DynamicPhoneAgentSetup,
    DynamicPhoneAgentSetupResult,
    UpdateDynamicPhoneAgent,
)
from wiil.types import PaginatedResult, PaginationRequest


class DynamicPhoneAgentResource:
    """Resource class for managing dynamic phone agents in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    dynamic phone agent configurations. Phone agents are deployed on telephony
    channels for voice-based customer interactions.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/dynamic-phone-agent'

    def create(
        self,
        data: DynamicPhoneAgentSetup
    ) -> DynamicPhoneAgentSetupResult:
        """Create a new dynamic phone agent.

        Args:
            data: Phone agent setup data

        Returns:
            The setup result with processing status
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=DynamicPhoneAgentSetup
        )

    def get(self, agent_id: str) -> DynamicPhoneAgentSetupResult:
        """Retrieve a dynamic phone agent by ID.

        Args:
            agent_id: Phone agent ID

        Returns:
            The phone agent setup result
        """
        return self._http.get(f'{self._base_path}/{agent_id}')

    def update(
        self,
        data: UpdateDynamicPhoneAgent
    ) -> DynamicPhoneAgentSetupResult:
        """Update an existing dynamic phone agent.

        Args:
            data: Phone agent update data (must include id)

        Returns:
            The updated phone agent setup result
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateDynamicPhoneAgent
        )

    def delete(self, agent_id: str) -> bool:
        """Delete a dynamic phone agent.

        Args:
            agent_id: Phone agent ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/{agent_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DynamicPhoneAgentSetupResult]:
        """List dynamic phone agents with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of phone agent setup results
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['DynamicPhoneAgentResource']
