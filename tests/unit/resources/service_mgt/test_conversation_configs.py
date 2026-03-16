"""Tests for Conversation Configurations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestConversationConfigurationsResource:
    """Test suite for ConversationConfigurationsResource."""

    def test_get_conversation_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a conversation configuration by ID."""
        mock_response = {
            "id": "conv_123",
            "channelId": "channel_456",
            "organizationId": "org_789",
            "projectId": "proj_012",
            "deploymentConfigId": "deploy_345",
            "channelIdentifier": "+12125551234",
            "conversationType": "TELEPHONY_CALL",
            "status": "active",
            "durationInSeconds": 120,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/conversation-configs/conv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.conversation_configs.get("conv_123")

        assert result.id == "conv_123"
        assert result.channel_id == "channel_456"
        assert result.organization_id == "org_789"
        assert result.conversation_type == "TELEPHONY_CALL"

    def test_get_conversation_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when conversation configuration not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/conversation-configs/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Conversation configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.conversation_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_list_conversation_configurations(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing conversation configurations with pagination."""
        mock_configs = [
            {
                "id": "conv_1",
                "channelId": "channel_101",
                "organizationId": "org_789",
                "projectId": "proj_012",
                "deploymentConfigId": "deploy_345",
                "channelIdentifier": "+12125551111",
                "conversationType": "OTT_CHAT",
                "status": "active",
                "durationInSeconds": 45,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "conv_2",
                "channelId": "channel_102",
                "organizationId": "org_789",
                "projectId": "proj_012",
                "deploymentConfigId": "deploy_345",
                "channelIdentifier": "+12125552222",
                "conversationType": "SMS",
                "status": "ended",
                "durationInSeconds": 90,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_configs,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 2,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/conversation-configs",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.conversation_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1
        assert result.data[0].id == "conv_1"
        assert result.data[0].conversation_type == "OTT_CHAT"
        assert result.data[1].id == "conv_2"
        assert result.data[1].conversation_type == "SMS"

    def test_list_conversation_configurations_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing conversation configurations with custom pagination parameters."""
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/conversation-configs?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.conversation_configs.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
