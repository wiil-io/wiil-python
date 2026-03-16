"""Translation Sessions resource for managing translation session entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.conversation import TranslationServiceLog
from wiil.types import PaginatedResult, PaginationRequest


class TranslationSessionsResource:
    """Resource class for managing translation sessions in the WIIL Platform.

    Provides methods for retrieving and listing translation sessions.
    Translation sessions represent logs and records of translation operations
    performed by the AI system.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/translation-sessions'

    def get(self, session_id: str) -> TranslationServiceLog:
        """Retrieve a translation session by ID."""
        return self._http.get(
            f'{self._base_path}/{session_id}',
            response_model=TranslationServiceLog
        )

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[TranslationServiceLog]:
        """List translation sessions with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of translation sessions
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[TranslationServiceLog]
        )


__all__ = ['TranslationSessionsResource']
