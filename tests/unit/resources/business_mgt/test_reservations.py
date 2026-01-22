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
            "start_time": 1234567890,
            "party_size": 4,
        }

        mock_response = {
            "id": "rsv_123",
            "reservationType": "table",
            "resourceId": "res_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": None,
            "duration": None,
            "personsNumber": 4,
            "totalPrice": None,
            "depositPaid": 0.0,
            "status": "pending",
            "notes": None,
            "cancelReason": None,
            "isResourceReservation": False,
            "serviceConversationConfigId": None,
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

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a reservation by ID."""
        mock_response = {
            "id": "rsv_123",
            "reservationType": "table",
            "resourceId": "res_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": None,
            "duration": None,
            "personsNumber": 4,
            "totalPrice": None,
            "depositPaid": 0.0,
            "status": "confirmed",
            "notes": None,
            "cancelReason": None,
            "isResourceReservation": False,
            "serviceConversationConfigId": None,
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
            "reservationType": "table",
            "resourceId": "res_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": None,
            "duration": None,
            "personsNumber": 6,
            "totalPrice": None,
            "depositPaid": 0.0,
            "status": "confirmed",
            "notes": None,
            "cancelReason": None,
            "isResourceReservation": False,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/reservations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.reservations.update(**update_data)

        assert result.persons_number == 6
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
                "reservationType": "table",
                "resourceId": "res_123",
                "customerId": "cust_123",
                "customerName": None,
                "customerEmail": None,
                "startTime": 1234567890,
                "endTime": None,
                "duration": None,
                "personsNumber": 4,
                "totalPrice": None,
                "depositPaid": 0.0,
                "status": "confirmed",
                "notes": None,
                "cancelReason": None,
                "isResourceReservation": False,
                "serviceConversationConfigId": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "rsv_2",
                "reservationType": "table",
                "resourceId": "res_456",
                "customerId": "cust_456",
                "customerName": None,
                "customerEmail": None,
                "startTime": 1234567891,
                "endTime": None,
                "duration": None,
                "personsNumber": 2,
                "totalPrice": None,
                "depositPaid": 0.0,
                "status": "pending",
                "notes": None,
                "cancelReason": None,
                "isResourceReservation": False,
                "serviceConversationConfigId": None,
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
                "reservationType": "table",
                "resourceId": "res_123",
                "customerId": "cust_123",
                "customerName": None,
                "customerEmail": None,
                "startTime": 1234567890,
                "endTime": None,
                "duration": None,
                "personsNumber": 4,
                "totalPrice": None,
                "depositPaid": 0.0,
                "status": "confirmed",
                "notes": None,
                "cancelReason": None,
                "isResourceReservation": False,
                "serviceConversationConfigId": None,
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
