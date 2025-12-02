"""Knowledge Sources resource for managing knowledge source entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import KnowledgeSource
from wiil.types import PaginatedResult


class KnowledgeSourcesResource:
    """Resource class for managing knowledge sources in the WIIL Platform.

    Provides methods for retrieving and listing knowledge sources.
    Knowledge sources represent repositories of information that AI agents
    can access for context and factual grounding. This is a read-only resource.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/knowledge-sources'

    def get(self, source_id: str) -> KnowledgeSource:
        """Retrieve a knowledge source by ID."""
        return self._http.get(f'{self._base_path}/{source_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[KnowledgeSource]:
        """List knowledge sources with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['KnowledgeSourcesResource']
