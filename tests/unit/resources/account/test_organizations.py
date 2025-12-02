"""Tests for Organizations resource."""

import pytest
import respx
from httpx import Response

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
            "businessVerticalId": "bv_456",
            "platformEmail": "admin@acme.com",
            "serviceStatus": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/organizations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.organizations.get()

        assert result.id == "org_123"
        assert result.company_name == "Acme Corporation"
        assert result.business_vertical_id == "bv_456"
        assert result.platform_email == "admin@acme.com"
        assert result.service_status == "ACTIVE"

    def test_get_organization_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when organization not found."""
        mock_api.get(
            f"{BASE_URL}/organizations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Organization not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.organizations.get()

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_organization_unauthorized(self, client: WiilClient, mock_api, error_response):
        """Test API error when API key is unauthorized."""
        mock_api.get(
            f"{BASE_URL}/organizations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            401,
            json=error_response("UNAUTHORIZED", "Invalid API key")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.organizations.get()

        assert exc_info.value.status_code == 401
        assert exc_info.value.code == "UNAUTHORIZED"
