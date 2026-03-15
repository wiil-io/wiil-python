"""Tests for Organizations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestOrganizationsResource:
    """Test suite for OrganizationsResource."""

    def test_get_organization(self, client: WiilClient, mock_api, api_response):
        """Test retrieving the organization that owns the API key."""
        mock_response = {
            "id": "org_123",
            "companyName": "Acme Corporation",
            "businessVerticalId": "technology",
            "platformEmail": "admin@acme.com",
            "serviceStatus": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/organizations",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.organizations.get()

        assert result.id == "org_123"
        assert result.company_name == "Acme Corporation"
        assert result.business_vertical_id == "technology"
        assert result.platform_email == "admin@acme.com"

    def test_get_organization_unauthorized(
        self,
        client: WiilClient,
        mock_api,
        error_response
    ):
        """Test API error when request fails with unauthorized."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/organizations",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response("UNAUTHORIZED", "Invalid API key"),
            status=401,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.organizations.get()

        assert exc_info.value.status_code == 401
        assert exc_info.value.code == "UNAUTHORIZED"

    def test_get_organization_server_error(
        self,
        client: WiilClient,
        mock_api,
        error_response
    ):
        """Test API error on server error."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/organizations",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response("INTERNAL_ERROR", "Internal server error"),
            status=500,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.organizations.get()

        assert exc_info.value.status_code == 500
        assert exc_info.value.code == "INTERNAL_ERROR"
