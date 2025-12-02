"""Tests for Reservations resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestReservationsResource:
    """Test suite for ReservationsResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new reservation."""
        input_data = {
            "customer_id": "cust_123",
            "resource_id": "res_123",
            "start_time": "2024-01-01T10:00:00Z",
            "end_time": "2024-01-01T12:00:00Z",
            "party_size": 4,
        }

        mock_response = {
            "id": "rsv_123",
            "customerId": "cust_123",
            "resourceId": "res_123",
            "startTime": "2024-01-01T10:00:00Z",
            "endTime": "2024-01-01T12:00:00Z",
            "partySize": 4,
            "status": "pending",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/reservations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.create(**input_data)

        assert result.id == "rsv_123"
        assert result.customer_id == "cust_123"
        assert result.party_size == 4

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a reservation by ID."""
        mock_response = {
            "id": "rsv_123",
            "customerId": "cust_123",
            "resourceId": "res_123",
            "startTime": "2024-01-01T10:00:00Z",
            "endTime": "2024-01-01T12:00:00Z",
            "partySize": 4,
            "status": "confirmed",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/reservations/rsv_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.get("rsv_123")

        assert result.id == "rsv_123"
        assert result.status == "confirmed"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a reservation."""
        update_data = {
            "id": "rsv_123",
            "party_size": 6,
            "status": "confirmed",
        }

        mock_response = {
            "id": "rsv_123",
            "customerId": "cust_123",
            "partySize": 6,
            "status": "confirmed",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/reservations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.update(**update_data)

        assert result.party_size == 6
        assert result.status == "confirmed"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a reservation."""
        mock_api.delete(
            f"{BASE_URL}/reservations/rsv_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.reservations.delete("rsv_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing reservations with pagination."""
        mock_reservations = [
            {
                "id": "rsv_1",
                "customerId": "cust_123",
                "resourceId": "res_123",
                "partySize": 4,
                "status": "confirmed",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "rsv_2",
                "customerId": "cust_456",
                "resourceId": "res_456",
                "partySize": 2,
                "status": "pending",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_reservations,
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
            f"{BASE_URL}/reservations?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.list(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving reservations by customer."""
        mock_reservations = [
            {
                "id": "rsv_1",
                "customerId": "cust_123",
                "resourceId": "res_123",
                "partySize": 4,
                "status": "confirmed",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_reservations,
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
            f"{BASE_URL}/reservations/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.get_by_customer("cust_123", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_update_status(self, client: WiilClient, mock_api, api_response):
        """Test updating reservation status."""
        mock_response = {
            "id": "rsv_123",
            "customerId": "cust_123",
            "status": "completed",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/reservations/rsv_123/status",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.update_status("rsv_123", "completed")

        assert result.status == "completed"

    def test_get_available_slots(self, client: WiilClient, mock_api, api_response):
        """Test retrieving available reservation slots."""
        mock_slots = [
            {
                "startTime": "2024-01-01T10:00:00Z",
                "endTime": "2024-01-01T12:00:00Z",
                "available": True,
            },
            {
                "startTime": "2024-01-01T12:00:00Z",
                "endTime": "2024-01-01T14:00:00Z",
                "available": True,
            },
        ]

        mock_api.get(
            f"{BASE_URL}/reservations/available-slots",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_slots)))

        result = client.reservations.get_available_slots()

        assert len(result) == 2
        assert result[0].available is True
