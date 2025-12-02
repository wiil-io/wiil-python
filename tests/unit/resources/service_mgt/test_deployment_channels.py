"""Tests for Deployment Channels resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestDeploymentChannelsResource:
    """Test suite for DeploymentChannelsResource."""

    def test_create_deployment_channel(self, client: WiilClient, mock_api, api_response):
        """Test creating a new deployment channel."""
        input_data = {
            "channel_type": "CALLS",
            "identifier": "+14155551234",
            "name": "Main Support Line",
            "description": "Primary customer support phone line",
        }

        mock_response = {
            "id": "channel_123",
            "channelType": "CALLS",
            "identifier": "+14155551234",
            "name": "Main Support Line",
            "description": "Primary customer support phone line",
            "status": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/deployment-channels",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.create(**input_data)

        assert result.id == "channel_123"
        assert result.identifier == "+14155551234"

    def test_get_deployment_channel(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a deployment channel by ID."""
        mock_response = {
            "id": "channel_123",
            "channelType": "CALLS",
            "identifier": "+14155551234",
            "name": "Main Support Line",
            "status": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/deployment-channels/channel_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.get("channel_123")

        assert result.id == "channel_123"
        assert result.identifier == "+14155551234"

    def test_get_deployment_channel_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when deployment channel not found."""
        mock_api.get(
            f"{BASE_URL}/deployment-channels/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Deployment channel not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.deployment_channels.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_deployment_channel_by_identifier(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a deployment channel by identifier and type."""
        mock_response = {
            "id": "channel_123",
            "channelType": "CALLS",
            "identifier": "+14155551234",
            "name": "Main Support Line",
            "status": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/deployment-channels/by-identifier/+14155551234?type=CALLS",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.get_by_identifier("+14155551234", "CALLS")

        assert result.id == "channel_123"
        assert result.identifier == "+14155551234"
        assert result.channel_type == "CALLS"

    def test_update_deployment_channel(self, client: WiilClient, mock_api, api_response):
        """Test updating a deployment channel."""
        update_data = {
            "id": "channel_123",
            "name": "Updated Support Line",
            "description": "Updated customer support line",
        }

        mock_response = {
            "id": "channel_123",
            "channelType": "CALLS",
            "identifier": "+14155551234",
            "name": "Updated Support Line",
            "description": "Updated customer support line",
            "status": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/deployment-channels",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.update(**update_data)

        assert result.name == "Updated Support Line"
        assert result.description == "Updated customer support line"

    def test_delete_deployment_channel(self, client: WiilClient, mock_api, api_response):
        """Test deleting a deployment channel."""
        mock_api.delete(
            f"{BASE_URL}/deployment-channels/channel_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.deployment_channels.delete("channel_123")

        assert result is True

    def test_delete_deployment_channel_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when deleting non-existent deployment channel."""
        mock_api.delete(
            f"{BASE_URL}/deployment-channels/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Deployment channel not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.deployment_channels.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_deployment_channels(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment channels with pagination."""
        mock_channels = [
            {
                "id": "channel_1",
                "channelType": "CALLS",
                "identifier": "+14155551234",
                "name": "Channel 1",
                "status": "ACTIVE",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "channel_2",
                "channelType": "SMS",
                "identifier": "+14155555678",
                "name": "Channel 2",
                "status": "ACTIVE",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_channels,
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
            f"{BASE_URL}/deployment-channels",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_deployment_channels_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment channels with custom pagination parameters."""
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
            f"{BASE_URL}/deployment-channels?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.list(page=2, page_size=50)

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True

    def test_list_deployment_channels_by_type(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment channels by type."""
        mock_channels = [
            {
                "id": "channel_1",
                "channelType": "CALLS",
                "identifier": "+14155551234",
                "name": "Call Channel 1",
                "status": "ACTIVE",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_channels,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/deployment-channels/by-type/CALLS",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.list_by_type("CALLS")

        assert len(result.data) == 1
        assert result.data[0].channel_type == "CALLS"

    def test_list_deployment_channels_by_type_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment channels by type with pagination."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 3,
                "pageSize": 10,
                "totalCount": 50,
                "totalPages": 5,
                "hasNextPage": True,
                "hasPreviousPage": True,
            },
        }

        mock_api.get(
            f"{BASE_URL}/deployment-channels/by-type/SMS?page=3&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_channels.list_by_type("SMS", page=3, page_size=10)

        assert result.meta.page == 3
        assert result.meta.page_size == 10
        assert result.meta.has_next_page is True
