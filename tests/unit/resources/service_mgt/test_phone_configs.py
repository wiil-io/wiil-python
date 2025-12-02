"""Tests for Phone Configurations resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestPhoneConfigurationsResource:
    """Test suite for PhoneConfigurationsResource."""

    def test_purchase_phone_number(self, client: WiilClient, mock_api, api_response):
        """Test purchasing a new phone number."""
        input_data = {
            "phone_number": "+14155551234",
            "area_code": "415",
            "country_code": "US",
            "friendly_name": "Support Line",
        }

        mock_response = {
            "requestId": "req_123",
            "phoneNumber": "+14155551234",
            "friendlyName": "Support Line",
            "status": "PENDING",
            "purchaseDate": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/phone-configurations/purchase",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.purchase(**input_data)

        assert result.request_id == "req_123"
        assert result.phone_number == "+14155551234"

    def test_get_phone_configuration(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a phone configuration by ID."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "friendlyName": "Support Line",
            "status": "ACTIVE",
            "capabilities": ["voice", "sms"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/phone-configurations/phone_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.get("phone_123")

        assert result.id == "phone_123"
        assert result.phone_number == "+14155551234"

    def test_get_phone_configuration_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when phone configuration not found."""
        mock_api.get(
            f"{BASE_URL}/phone-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Phone configuration not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.phone_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_phone_configuration_by_phone_number(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a phone configuration by phone number."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "friendlyName": "Support Line",
            "status": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/phone-configurations/by-phone-number/+14155551234",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.get_by_phone_number("+14155551234")

        assert result.id == "phone_123"
        assert result.phone_number == "+14155551234"

    def test_get_phone_configuration_by_request_id(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a phone configuration by request ID."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "friendlyName": "Support Line",
            "status": "ACTIVE",
            "requestId": "req_123",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/phone-configurations/by-request/req_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.get_by_request_id("req_123")

        assert result.id == "phone_123"
        assert result.request_id == "req_123"

    def test_update_phone_configuration(self, client: WiilClient, mock_api, api_response):
        """Test updating a phone configuration."""
        update_data = {
            "id": "phone_123",
            "friendly_name": "Updated Support Line",
            "status": "INACTIVE",
        }

        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "friendlyName": "Updated Support Line",
            "status": "INACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/phone-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.update(**update_data)

        assert result.friendly_name == "Updated Support Line"
        assert result.status == "INACTIVE"

    def test_delete_phone_configuration(self, client: WiilClient, mock_api, api_response):
        """Test deleting a phone configuration."""
        mock_api.delete(
            f"{BASE_URL}/phone-configurations/phone_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.phone_configs.delete("phone_123")

        assert result is True

    def test_delete_phone_configuration_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when deleting non-existent phone configuration."""
        mock_api.delete(
            f"{BASE_URL}/phone-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Phone configuration not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.phone_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_phone_configurations(self, client: WiilClient, mock_api, api_response):
        """Test listing phone configurations with pagination."""
        mock_configs = [
            {
                "id": "phone_1",
                "phoneNumber": "+14155551234",
                "friendlyName": "Phone 1",
                "status": "ACTIVE",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "phone_2",
                "phoneNumber": "+14155555678",
                "friendlyName": "Phone 2",
                "status": "ACTIVE",
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

        mock_api.get(
            f"{BASE_URL}/phone-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_phone_configurations_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing phone configurations with custom pagination parameters."""
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
            f"{BASE_URL}/phone-configurations?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.phone_configs.list(page=2, page_size=50)

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
