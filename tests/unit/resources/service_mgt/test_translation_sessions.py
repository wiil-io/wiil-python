"""Tests for Translation Sessions resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestTranslationSessionsResource:
    """Test suite for TranslationSessionsResource."""

    def test_get_translation_session(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a translation session by ID."""
        mock_response = {
            "id": "session_123",
            "organizationId": "org_456",
            "projectId": "proj_789",
            "partnerInitiatorId": "initiator_001",
            "partnerSessionId": "sess_abc",
            "sdrtId": None,
            "translationConfigId": "config_123",
            "participants": ["participant_1", "participant_2"],
            "durationInSeconds": 120,
            "status": "completed",
            "direction": "bidirectional",
            "transcribedConversationLog": None,
            "logTranscriptionInParticipantRecords": False,
            "translationSummary": None,
            "createdDay": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/translation-sessions/session_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.translation_sessions.get("session_123")

        assert result.id == "session_123"
        assert result.organization_id == "org_456"
        assert result.status == "completed"

    def test_get_translation_session_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when translation session not found."""
        mock_api.get(
            f"{BASE_URL}/translation-sessions/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Translation session not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.translation_sessions.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_list_translation_sessions(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing translation sessions with pagination."""
        mock_sessions = [
            {
                "id": "session_1",
                "organizationId": "org_456",
                "projectId": "proj_789",
                "partnerInitiatorId": "initiator_001",
                "partnerSessionId": "sess_1",
                "sdrtId": None,
                "translationConfigId": "config_123",
                "participants": ["participant_1", "participant_2"],
                "durationInSeconds": 90,
                "status": "completed",
                "direction": "bidirectional",
                "transcribedConversationLog": None,
                "logTranscriptionInParticipantRecords": False,
                "translationSummary": None,
                "createdDay": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "session_2",
                "organizationId": "org_456",
                "projectId": "proj_789",
                "partnerInitiatorId": "initiator_002",
                "partnerSessionId": "sess_2",
                "sdrtId": None,
                "translationConfigId": "config_123",
                "participants": ["participant_3", "participant_4"],
                "durationInSeconds": 150,
                "status": "completed",
                "direction": "bidirectional",
                "transcribedConversationLog": None,
                "logTranscriptionInParticipantRecords": False,
                "translationSummary": None,
                "createdDay": None,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_sessions,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 2,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/translation-sessions",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.translation_sessions.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_translation_sessions_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing translation sessions with pagination parameters."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 2,
                "pageSize": 50,
                "totalCount": 100,
                "totalPages": 2,
                "hasNextPage": False,
                "hasPreviousPage": True,
            },
        }

        mock_api.get(
            f"{BASE_URL}/translation-sessions?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.translation_sessions.list(page=2, page_size=50)

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
