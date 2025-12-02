"""Tests for Business Services resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestBusinessServicesResource:
    """Test suite for BusinessServicesResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new business service."""
        input_data = {
            "name": "Haircut",
            "category": "Hair Services",
            "duration": 30,
            "price": 25.00,
            "description": "Professional haircut service",
        }

        mock_response = {
            "id": "svc_123",
            "name": "Haircut",
            "category": "Hair Services",
            "duration": 30,
            "price": 25.00,
            "description": "Professional haircut service",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/business-services",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.business_services.create(**input_data)

        assert result.id == "svc_123"
        assert result.name == "Haircut"
        assert result.price == 25.00

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a business service by ID."""
        mock_response = {
            "id": "svc_123",
            "name": "Haircut",
            "category": "Hair Services",
            "duration": 30,
            "price": 25.00,
            "description": "Professional haircut service",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/business-services/svc_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.business_services.get("svc_123")

        assert result.id == "svc_123"
        assert result.name == "Haircut"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a business service."""
        update_data = {
            "id": "svc_123",
            "name": "Premium Haircut",
            "price": 35.00,
        }

        mock_response = {
            "id": "svc_123",
            "name": "Premium Haircut",
            "price": 35.00,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/business-services",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.business_services.update(**update_data)

        assert result.name == "Premium Haircut"
        assert result.price == 35.00

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a business service."""
        mock_api.delete(
            f"{BASE_URL}/business-services/svc_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.business_services.delete("svc_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing business services with pagination."""
        mock_services = [
            {
                "id": "svc_1",
                "name": "Haircut",
                "category": "Hair Services",
                "duration": 30,
                "price": 25.00,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "svc_2",
                "name": "Massage",
                "category": "Spa Services",
                "duration": 60,
                "price": 80.00,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_services,
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
            f"{BASE_URL}/business-services?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.business_services.list(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving business services by category."""
        mock_services = [
            {
                "id": "svc_1",
                "name": "Haircut",
                "category": "Hair Services",
                "duration": 30,
                "price": 25.00,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "svc_2",
                "name": "Hair Coloring",
                "category": "Hair Services",
                "duration": 90,
                "price": 75.00,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_api.get(
            f"{BASE_URL}/business-services/by-category/Hair%20Services",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_services)))

        result = client.business_services.get_by_category("Hair Services")

        assert len(result) == 2
        assert result[0].category == "Hair Services"
