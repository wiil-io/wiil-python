"""Conversation Configurations resource for managing conversation configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.conversation import ServiceConversationConfig
from wiil.types import PaginatedResult


class ConversationConfigurationsResource:
    """Resource class for managing conversation configurations in the WIIL Platform.

    Provides methods for retrieving and listing conversation configurations.
    Conversation configurations define how AI agents manage conversation state,
    context, and flow. This is a read-only resource.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/conversation-configs'

    def get(self, config_id: str) -> ServiceConversationConfig:
        """Retrieve a conversation configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ServiceConversationConfig]:
        """List conversation configurations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['ConversationConfigurationsResource']
