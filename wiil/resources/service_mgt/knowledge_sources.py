"""Knowledge Sources resource for managing knowledge source entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import KnowledgeSource
from wiil.types import PaginatedResult, PaginationRequest


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
        return self._http.get(f'{self._base_path}/{source_id}', response_model=KnowledgeSource)

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[KnowledgeSource]:
        """List knowledge sources with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of knowledge sources
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[KnowledgeSource]
        )


__all__ = ['KnowledgeSourcesResource']
