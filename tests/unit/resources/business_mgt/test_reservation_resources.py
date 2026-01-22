"""Tests for Reservation Resources resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestReservationResourcesResource:
    """Test suite for ReservationResourcesResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new reservation resource."""
        input_data = {
            "name": "Table 1",
            "type": "table",
            "capacity": 4,
            "description": "Window side table",
        }

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

        mock_api.post(
            f"{BASE_URL}/reservation-resources",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservation_resources.create(**input_data)

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

        mock_api.get(
            f"{BASE_URL}/reservation-resources/res_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservation_resources.get("res_123")

        assert result.id == "res_123"
        assert result.name == "Table 1"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a reservation resource."""
        update_data = {
            "id": "res_123",
            "name": "Updated Table 1",
            "capacity": 6,
        }

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

        mock_api.patch(
            f"{BASE_URL}/reservation-resources",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservation_resources.update(**update_data)

        assert result.name == "Updated Table 1"
        assert result.capacity == 6

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a reservation resource."""
        mock_api.delete(
            f"{BASE_URL}/reservation-resources/res_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

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

        mock_api.get(
            f"{BASE_URL}/reservation-resources?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservation_resources.list(page=1, page_size=10)

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

        mock_api.get(
            f"{BASE_URL}/reservation-resources/by-type/table?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservation_resources.get_by_type("table", page=1, page_size=10)

        assert len(result.data) == 2
        assert result.data[0].resource_type == "table"

    def test_get_available(self, client: WiilClient, mock_api, api_response):
        """Test retrieving available reservation resources."""
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
        ]

        mock_api.get(
            f"{BASE_URL}/reservation-resources/available",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_resources)))

        result = client.reservation_resources.get_available()

        assert len(result) == 1
        assert result[0].is_available is True
