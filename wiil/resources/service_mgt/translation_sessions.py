"""Translation Sessions resource for managing translation session entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.conversation import TranslationServiceLog
from wiil.types import PaginatedResult


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
        return self._http.get(f'{self._base_path}/{session_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[TranslationServiceLog]:
        """List translation sessions with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['TranslationSessionsResource']
