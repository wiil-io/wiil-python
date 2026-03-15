"""Tests for Reservation Resources resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateResource,
    UpdateResource,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestReservationResourcesResource:
    """Test suite for ReservationResourcesResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new reservation resource."""
        mock_response = {
            "id": "res_123",
            "resourceType": "table",
            "name": "Table 1",
            "description": "Window side table",
            "capacity": 4,
            "isAvailable": True,
            "location": None,
            "amenities": [],
            "reservationDuration": None,
            "reservationDurationUnit": None,
            "calendarId": None,
            "syncEnabled": False,
            "lastSyncAt": None,
            "roomResource": None,
            "rentalResource": None,
            "metadata": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/reservation-resources",
            json=api_response(mock_response),
            status=200
        )

        result = client.reservation_resources.create(CreateResource(
            name="Table 1",
            resource_type="table",
            capacity=4,
            description="Window side table"
        ))

        assert result.id == "res_123"
        assert result.name == "Table 1"
        assert result.capacity == 4

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a reservation resource by ID."""
        mock_response = {
            "id": "res_123",
            "resourceType": "table",
            "name": "Table 1",
            "description": "Window side table",
            "capacity": 4,
            "isAvailable": True,
            "location": None,
            "amenities": [],
            "reservationDuration": None,
            "reservationDurationUnit": None,
            "calendarId": None,
            "syncEnabled": False,
            "lastSyncAt": None,
            "roomResource": None,
            "rentalResource": None,
            "metadata": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/reservation-resources/res_123",
            json=api_response(mock_response),
            status=200
        )

        result = client.reservation_resources.get("res_123")

        assert result.id == "res_123"
        assert result.name == "Table 1"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a reservation resource."""
        mock_response = {
            "id": "res_123",
            "resourceType": "table",
            "name": "Updated Table 1",
            "description": "Window side table",
            "capacity": 6,
            "isAvailable": True,
            "location": None,
            "amenities": [],
            "reservationDuration": None,
            "reservationDurationUnit": None,
            "calendarId": None,
            "syncEnabled": False,
            "lastSyncAt": None,
            "roomResource": None,
            "rentalResource": None,
            "metadata": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/reservation-resources",
            json=api_response(mock_response),
            status=200
        )

        result = client.reservation_resources.update(UpdateResource(
            id="res_123",
            name="Updated Table 1",
            capacity=6
        ))

        assert result.name == "Updated Table 1"
        assert result.capacity == 6

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a reservation resource."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/reservation-resources/res_123",
            json=api_response(True),
            status=200
        )

        result = client.reservation_resources.delete("res_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing reservation resources with pagination."""
        mock_resources = [
            {
                "id": "res_1",
                "resourceType": "table",
                "name": "Table 1",
                "description": None,
                "capacity": 4,
                "isAvailable": True,
                "location": None,
                "amenities": [],
                "reservationDuration": None,
                "reservationDurationUnit": None,
                "calendarId": None,
                "syncEnabled": False,
                "lastSyncAt": None,
                "roomResource": None,
                "rentalResource": None,
                "metadata": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "res_2",
                "resourceType": "room",
                "name": "Conference Room A",
                "description": None,
                "capacity": 10,
                "isAvailable": True,
                "location": None,
                "amenities": [],
                "reservationDuration": None,
                "reservationDurationUnit": None,
                "calendarId": None,
                "syncEnabled": False,
                "lastSyncAt": None,
                "roomResource": None,
                "rentalResource": None,
                "metadata": None,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_resources,
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
            f"{BASE_URL}/reservation-resources?page=1&pageSize=10",
            json=api_response(mock_response),
            status=200
        )

        result = client.reservation_resources.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_type(self, client: WiilClient, mock_api, api_response):
        """Test retrieving reservation resources by type."""
        mock_resources = [
            {
                "id": "res_1",
                "resourceType": "table",
                "name": "Table 1",
                "description": None,
                "capacity": 4,
                "isAvailable": True,
                "location": None,
                "amenities": [],
                "reservationDuration": None,
                "reservationDurationUnit": None,
                "calendarId": None,
                "syncEnabled": False,
                "lastSyncAt": None,
                "roomResource": None,
                "rentalResource": None,
                "metadata": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "res_2",
                "resourceType": "table",
                "name": "Table 2",
                "description": None,
                "capacity": 6,
                "isAvailable": True,
                "location": None,
                "amenities": [],
                "reservationDuration": None,
                "reservationDurationUnit": None,
                "calendarId": None,
                "syncEnabled": False,
                "lastSyncAt": None,
                "roomResource": None,
                "rentalResource": None,
                "metadata": None,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_resources,
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
            f"{BASE_URL}/reservation-resources/by-type/table?page=1&pageSize=10",
            json=api_response(mock_response),
            status=200
        )

        result = client.reservation_resources.get_by_type(
            "table",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.data[0].resource_type == "table"

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create resource handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/reservation-resources",
            json=error_response("VALIDATION_ERROR", "Name is required"),
            status=400
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.reservation_resources.create(CreateResource(
                name="",
                resource_type="table"
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get resource handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/reservation-resources/nonexistent",
            json=error_response("NOT_FOUND", "Resource not found"),
            status=404
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.reservation_resources.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
