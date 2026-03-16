"""Conversation Configurations resource for managing conversation configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.conversation import ServiceConversationConfig
from wiil.types import PaginatedResult, PaginationRequest


class ConversationConfigurationsResource:
    """Resource class for managing conversation configurations in the WIIL Platform.

    Provides methods for retrieving and listing conversation configurations.
    Conversation configurations define how AI agents manage conversation state,
    context, and flow. This is a read-only resource.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/conversation-configurations'

    def get(self, config_id: str) -> ServiceConversationConfig:
        """Retrieve a conversation configuration by ID."""
        return self._http.get(
            f'{self._base_path}/{config_id}',
            response_model=ServiceConversationConfig
        )

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ServiceConversationConfig]:
        """List conversation configurations with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of conversation configurations
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[ServiceConversationConfig]
        )


__all__ = ['ConversationConfigurationsResource']
