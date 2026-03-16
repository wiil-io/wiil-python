"""Tests for Phone Configurations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.service_mgt import UpdatePhoneConfiguration
from wiil.types import PaginationRequest


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestPhoneConfigurationsResource:
    """Test suite for PhoneConfigurationsResource."""

    def test_get_phone_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a phone configuration by ID."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "providerPhoneNumberId": "PN123abc",
            "phoneRequestId": "REQ456",
            "friendlyName": "Support Line",
            "regionId": "us-ca",
            "monthlyPrice": 1.00,
            "regionOrCountryName": "California, United States",
            "countryCode": "US",
            "providerType": "signalwire",
            "isImported": False,
            "status": "active",
            "isPorted": False,
            "markedForRelease": False,
            "metadata": None,
            "voiceChannelId": None,
            "smsChannelId": None,
            "voiceChannel": None,
            "smsChannel": None,
            "isUSSMSPermitted": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/phone_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.phone_configs.get("phone_123")

        assert result.id == "phone_123"
        assert result.phone_number == "+14155551234"

    def test_get_phone_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when phone configuration not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Phone configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.phone_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_phone_configuration_by_phone_number(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a phone configuration by phone number."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "providerPhoneNumberId": "PN123abc",
            "phoneRequestId": "REQ456",
            "friendlyName": "Support Line",
            "regionId": "us-ca",
            "monthlyPrice": 1.00,
            "regionOrCountryName": "California, United States",
            "countryCode": "US",
            "providerType": "signalwire",
            "isImported": False,
            "status": "active",
            "isPorted": False,
            "markedForRelease": False,
            "metadata": None,
            "voiceChannelId": None,
            "smsChannelId": None,
            "voiceChannel": None,
            "smsChannel": None,
            "isUSSMSPermitted": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/by-phone-number/+14155551234",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.phone_configs.get_by_phone_number("+14155551234")

        assert result.id == "phone_123"
        assert result.phone_number == "+14155551234"

    def test_get_phone_configuration_by_request_id(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a phone configuration by request ID."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "providerPhoneNumberId": "PN123abc",
            "phoneRequestId": "req_123",
            "friendlyName": "Support Line",
            "regionId": "us-ca",
            "monthlyPrice": 1.00,
            "regionOrCountryName": "California, United States",
            "countryCode": "US",
            "providerType": "signalwire",
            "isImported": False,
            "status": "active",
            "isPorted": False,
            "markedForRelease": False,
            "metadata": None,
            "voiceChannelId": None,
            "smsChannelId": None,
            "voiceChannel": None,
            "smsChannel": None,
            "isUSSMSPermitted": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/by-request/req_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.phone_configs.get_by_request_id("req_123")

        assert result.id == "phone_123"
        assert result.phone_request_id == "req_123"

    def test_update_phone_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a phone configuration."""
        mock_response = {
            "id": "phone_123",
            "phoneNumber": "+14155551234",
            "providerPhoneNumberId": "PN123abc",
            "phoneRequestId": "REQ456",
            "friendlyName": "Updated Support Line",
            "regionId": "us-ca",
            "monthlyPrice": 1.00,
            "regionOrCountryName": "California, United States",
            "countryCode": "US",
            "providerType": "signalwire",
            "isImported": False,
            "status": "active",
            "isPorted": False,
            "markedForRelease": False,
            "metadata": None,
            "voiceChannelId": None,
            "smsChannelId": None,
            "voiceChannel": None,
            "smsChannel": None,
            "isUSSMSPermitted": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/phone-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.phone_configs.update(UpdatePhoneConfiguration(
            id="phone_123",
            friendly_name="Updated Support Line"
        ))

        assert result.friendly_name == "Updated Support Line"
        assert result.updated_at == 1234567891

    def test_delete_phone_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a phone configuration."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/phone-configurations/phone_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.phone_configs.delete("phone_123")

        assert result is True

    def test_delete_phone_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when deleting non-existent phone config."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/phone-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Phone configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.phone_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_phone_configurations(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing phone configurations with pagination."""
        mock_configs = [
            {
                "id": "phone_1",
                "phoneNumber": "+14155551234",
                "providerPhoneNumberId": "PN123abc",
                "phoneRequestId": "REQ001",
                "friendlyName": "Phone 1",
                "regionId": "us-ca",
                "monthlyPrice": 1.00,
                "regionOrCountryName": "California, United States",
                "countryCode": "US",
                "providerType": "signalwire",
                "providerAccountId": None,
                "isImported": False,
                "status": "active",
                "isPorted": False,
                "markedForRelease": False,
                "metadata": None,
                "voiceChannelId": None,
                "smsChannelId": None,
                "voiceChannel": None,
                "smsChannel": None,
                "isUSSMSPermitted": True,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "phone_2",
                "phoneNumber": "+14155555678",
                "providerPhoneNumberId": "PN456def",
                "phoneRequestId": "REQ002",
                "friendlyName": "Phone 2",
                "regionId": "us-ca",
                "monthlyPrice": 1.00,
                "regionOrCountryName": "California, United States",
                "countryCode": "US",
                "providerType": "signalwire",
                "providerAccountId": None,
                "isImported": False,
                "status": "active",
                "isPorted": False,
                "markedForRelease": False,
                "metadata": None,
                "voiceChannelId": None,
                "smsChannelId": None,
                "voiceChannel": None,
                "smsChannel": None,
                "isUSSMSPermitted": True,
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
            f"{BASE_URL}/phone-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.phone_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_phone_configurations_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing phone configs with custom pagination parameters."""
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
            f"{BASE_URL}/phone-configurations?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.phone_configs.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
