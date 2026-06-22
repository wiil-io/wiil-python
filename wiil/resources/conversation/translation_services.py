"""Translation services resource for managing real-time translation sessions."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.conversation import (
    CreateTranslationParticipant,
    CreateTranslationServiceLog,
    CreateTranslationServiceRequest,
    TranslationConversationConfig,
    TranslationParticipant,
    TranslationServiceLog,
    UpdateTranslationParticipant,
    UpdateTranslationServiceLog,
)
from wiil.types import ConversationStatus, PaginatedResult, PaginationRequest


class TranslationServicesResource:
    """Resource class for managing translation services in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing translation
    service logs and participants. Translation services enable real-time language
    translation for cross-language communication.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/translation-services"

    def initiate(
        self,
        data: CreateTranslationServiceRequest,
    ) -> TranslationConversationConfig:
        """Initiate a new translation session."""
        return self._http.post(
            f"{self._base_path}/initiate",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTranslationServiceRequest,
            response_model=TranslationConversationConfig,
        )

    def create(self, data: CreateTranslationServiceLog) -> TranslationServiceLog:
        """Create a new translation service log."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTranslationServiceLog,
            response_model=TranslationServiceLog,
        )

    def get(self, session_id: str) -> TranslationServiceLog:
        """Retrieve a translation service log by ID."""
        return self._http.get(
            f"{self._base_path}/{session_id}",
            response_model=TranslationServiceLog,
        )

    def get_by_organization(
        self,
        organization_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TranslationServiceLog]:
        """Retrieve translation service logs by organization."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-organization/{organization_id}{query_string}",
            response_model=PaginatedResult[TranslationServiceLog],
        )

    def get_by_project(
        self,
        project_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TranslationServiceLog]:
        """Retrieve translation service logs by project."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-project/{project_id}{query_string}",
            response_model=PaginatedResult[TranslationServiceLog],
        )

    def get_by_status(
        self,
        status: ConversationStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TranslationServiceLog]:
        """Retrieve translation service logs by status."""
        query_params: Dict[str, Any] = {"status": status}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[TranslationServiceLog],
        )

    def get_by_date_range(
        self,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TranslationServiceLog]:
        """Retrieve translation service logs within a date range."""
        query_params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[TranslationServiceLog],
        )

    def update(self, data: UpdateTranslationServiceLog) -> TranslationServiceLog:
        """Update an existing translation service log."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateTranslationServiceLog,
            response_model=TranslationServiceLog,
        )

    def update_status(
        self,
        session_id: str,
        status: ConversationStatus,
    ) -> TranslationServiceLog:
        """Update translation session status."""
        return self._http.patch(
            f"{self._base_path}/{session_id}/status",
            {"status": status},
            response_model=TranslationServiceLog,
        )

    def end(self, session_id: str) -> TranslationServiceLog:
        """End a translation session."""
        return self._http.post(
            f"{self._base_path}/{session_id}/end",
            {},
            response_model=TranslationServiceLog,
        )

    def generate_summary(self, session_id: str) -> TranslationServiceLog:
        """Generate a summary for a translation session."""
        return self._http.post(
            f"{self._base_path}/{session_id}/generate-summary",
            {},
            response_model=TranslationServiceLog,
        )

    def get_participants(
        self,
        session_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TranslationParticipant]:
        """Retrieve participants for a translation session."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/{session_id}/participants{query_string}",
            response_model=PaginatedResult[TranslationParticipant],
        )

    def add_participant(
        self,
        session_id: str,
        data: CreateTranslationParticipant,
    ) -> TranslationParticipant:
        """Add a participant to a translation session."""
        return self._http.post(
            f"{self._base_path}/{session_id}/participants",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTranslationParticipant,
            response_model=TranslationParticipant,
        )

    def update_participant(
        self,
        session_id: str,
        data: UpdateTranslationParticipant,
    ) -> TranslationParticipant:
        """Update a participant in a translation session."""
        return self._http.patch(
            f"{self._base_path}/{session_id}/participants",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateTranslationParticipant,
            response_model=TranslationParticipant,
        )

    def remove_participant(
        self,
        session_id: str,
        participant_id: str,
    ) -> bool:
        """Remove a participant from a translation session."""
        return self._http.delete(
            f"{self._base_path}/{session_id}/participants/{participant_id}"
        )

    def delete(self, session_id: str) -> bool:
        """Delete a translation service log."""
        return self._http.delete(f"{self._base_path}/{session_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TranslationServiceLog]:
        """List translation service logs with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[TranslationServiceLog],
        )


__all__ = ["TranslationServicesResource"]
