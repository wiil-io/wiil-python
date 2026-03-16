"""Tests for Business Services resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import CreateBusinessService, UpdateBusinessService
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestBusinessServicesResource:
    """Test suite for BusinessServicesResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new business service."""
        mock_response = {
            "id": "svc_123",
            "name": "Haircut",
            "description": "Professional haircut service",
            "duration": 30,
            "bufferTime": 10,
            "isBookable": True,
            "price": 25.00,
            "isActive": True,
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/business-services",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.create(CreateBusinessService(
            name="Haircut",
            description="Professional haircut service",
            duration=30,
            buffer_time=10,
            is_bookable=True,
            price=25.00,
            is_active=True,
            display_order=1
        ))

        assert result.id == "svc_123"
        assert result.name == "Haircut"
        assert result.price == 25.00

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a business service by ID."""
        mock_response = {
            "id": "svc_123",
            "name": "Haircut",
            "description": "Professional haircut service",
            "duration": 30,
            "bufferTime": 10,
            "isBookable": True,
            "price": 25.00,
            "isActive": True,
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/business-services/svc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.get("svc_123")

        assert result.id == "svc_123"
        assert result.name == "Haircut"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a business service."""
        mock_response = {
            "id": "svc_123",
            "name": "Premium Haircut",
            "description": "Professional haircut service",
            "duration": 30,
            "bufferTime": 10,
            "isBookable": True,
            "price": 35.00,
            "isActive": True,
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/business-services",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.update(UpdateBusinessService(
            id="svc_123",
            name="Premium Haircut",
            price=35.00
        ))

        assert result.name == "Premium Haircut"
        assert result.price == 35.00

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a business service."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/business-services/svc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.business_services.delete("svc_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing business services with pagination."""
        mock_services = [
            {
                "id": "svc_1",
                "name": "Haircut",
                "description": "Professional haircut service",
                "duration": 30,
                "bufferTime": 10,
                "isBookable": True,
                "price": 25.00,
                "isActive": True,
                "displayOrder": 1,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "svc_2",
                "name": "Massage",
                "description": "Relaxing massage therapy",
                "duration": 60,
                "bufferTime": 15,
                "isBookable": True,
                "price": 80.00,
                "isActive": True,
                "displayOrder": 2,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/business-services?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_generate_qr_code(self, client: WiilClient, mock_api, api_response):
        """Test generating QR code for service booking."""
        mock_response = {
            "id": "qr_123",
            "appointmentUrl": "https://book.example.com/services/svc_123",
            "qrCodeImage": None,
            "serviceId": "svc_123",
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/business-services/qr-code/generate?serviceId=svc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.generate_qr_code(service_id="svc_123")

        assert result.id == "qr_123"
        assert result.service_id == "svc_123"

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create service handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/business-services",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Name is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.business_services.create(CreateBusinessService(name="Valid Service"))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get service handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/business-services/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Service not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.business_services.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
