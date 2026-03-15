"""Tests for OTT service."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilValidationError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestOttService:
    """Test suite for OttService."""

    def test_get_chat_connection_configuration(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test fetching OTT chat connection configuration."""
        mock_payload = {
            "connection_url": "wss://example.com/chat",
            "channel_token": "token_123",
            "channel_identifier": "channel_123",
        }

        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/chat-service-config/config_123"
                "?email=user%40example.com&phone=%2B12065551234"
            ),
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_payload),
            status=200,
        )

        result = client.ott.get_chat_connection_configuration(
            {
                "configId": "config_123",
                "contact": {
                    "email": "user@example.com",
                    "phone": "+12065551234",
                },
            }
        )

        assert result.channel_identifier == "channel_123"
        assert result.connection_url == "wss://example.com/chat"

    def test_get_voice_connection_configuration(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test fetching OTT voice connection configuration."""
        mock_payload = {
            "sdrtn_id": "sdrtn_123",
            "channel_identifier": "channel_abc",
            "channel_token": "voice_token",
            "platform_user_id": 42,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/commission-service-agent/config_abc",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_payload),
            status=200,
        )

        result = client.ott.get_voice_connection_configuration(
            {
                "configId": "config_abc",
            }
        )

        assert result.sdrtn_id == "sdrtn_123"
        assert result.platform_user_id == 42

    def test_get_chat_connection_configuration_invalid_request(
        self,
        client: WiilClient,
    ):
        """Test request validation on OTT chat config API."""
        with pytest.raises(WiilValidationError):
            client.ott.get_chat_connection_configuration({})

    def test_get_voice_connection_configuration_invalid_response(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test response validation on OTT voice config API."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/commission-service-agent/config_invalid",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response({"bad": "payload"}),
            status=200,
        )

        with pytest.raises(WiilValidationError):
            client.ott.get_voice_connection_configuration(
                {"configId": "config_invalid"}
            )
