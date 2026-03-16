"""Tests for translation service."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilValidationError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestTranslationService:
    """Test suite for TranslationService."""

    def test_create_connection_config(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test creating translation connection config."""
        request_payload = {
            "initiatorId": "init_1",
            "participantId": "part_1",
            "initiatorLanguageCode": "en",
            "participantLanguageCode": "es",
            "sessionId": "sess_1",
            "provisioningConfigId": "prov_1",
        }
        response_payload = {
            "sdrtnId": "sdrtn_1",
            "channelIdentifier": "+12065551234",
            "initiatorAccessId": 1001,
            "initiatorToken": "token_i",
            "participantAccessId": 1002,
            "participantToken": "token_p",
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/translation/connect",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(response_payload),
            status=200,
        )

        result = client.translation.create_connection_config(request_payload)

        assert result.sdrtn_id == "sdrtn_1"
        assert result.channel_identifier == "+12065551234"
        assert result.initiator_access_id == 1001

    def test_create_connection_config_invalid_request(
        self,
        client: WiilClient,
    ):
        """Test request validation for translation service."""
        with pytest.raises(WiilValidationError):
            client.translation.create_connection_config(
                {"initiatorId": "init_1"}
            )

    def test_create_connection_config_invalid_response(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test response validation for translation service."""
        request_payload = {
            "initiatorId": "init_1",
            "initiatorLanguageCode": "en",
            "participantLanguageCode": "es",
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/translation/connect",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response({"invalid": "payload"}),
            status=200,
        )

        with pytest.raises(WiilValidationError):
            client.translation.create_connection_config(request_payload)
