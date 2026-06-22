"""Tests for Customer Groups resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import CreateCustomerGroup, UpdateCustomerGroup
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestCustomerGroupsResource:
    """Test suite for CustomerGroupsResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "grp_123",
            "name": "VIP",
            "description": "Premium customers",
            "code": "VIP",
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/customer-groups",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customer_groups.create(
            CreateCustomerGroup(
                name="VIP",
                description="Premium customers",
                code="VIP",
                is_default=False,
            )
        )

        assert result.id == "grp_123"
        assert result.name == "VIP"

    def test_get(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "grp_123",
            "name": "VIP",
            "description": "Premium customers",
            "code": "VIP",
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customer-groups/grp_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customer_groups.get("grp_123")

        assert result.id == "grp_123"
        assert result.code == "VIP"

    def test_get_by_code(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "grp_123",
            "name": "VIP",
            "description": "Premium customers",
            "code": "VIP",
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customer-groups/code/VIP",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customer_groups.get_by_code("VIP")

        assert result.id == "grp_123"

    def test_get_default(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "grp_default",
            "name": "Retail",
            "description": "Default group",
            "code": "RTL",
            "isDefault": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customer-groups/default",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customer_groups.get_default()

        assert result.id == "grp_default"
        assert result.is_default is True

    def test_update(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "grp_123",
            "name": "Premium VIP",
            "description": "Updated",
            "code": "VIP",
            "isDefault": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/customer-groups/grp_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customer_groups.update(
            "grp_123",
            UpdateCustomerGroup(
                id="grp_123",
                name="Premium VIP",
                is_default=True,
            ),
        )

        assert result.name == "Premium VIP"
        assert result.is_default is True

    def test_delete(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/customer-groups/grp_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.customer_groups.delete("grp_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [
                {
                    "id": "grp_1",
                    "name": "Retail",
                    "description": "Default group",
                    "code": "RTL",
                    "isDefault": True,
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                },
                {
                    "id": "grp_2",
                    "name": "VIP",
                    "description": "Premium",
                    "code": "VIP",
                    "isDefault": False,
                    "createdAt": 1234567891,
                    "updatedAt": 1234567891,
                },
            ],
            "meta": {
                "page": 1,
                "pageSize": 10,
                "totalCount": 2,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customer-groups?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customer_groups.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_create_api_error(
        self,
        client: WiilClient,
        mock_api,
        error_response,
    ):
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/customer-groups",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Name is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.customer_groups.create(CreateCustomerGroup(name="Valid"))

        assert exc_info.value.code == "VALIDATION_ERROR"
