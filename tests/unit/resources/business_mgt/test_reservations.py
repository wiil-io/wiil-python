"""Tests for Reservations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import CreateReservation, UpdateReservation
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestReservationsResource:
    """Test suite for ReservationsResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new reservation."""
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

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/reservations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.reservations.create(CreateReservation(
            reservation_type="table",
            customer_id="cust_123",
            resource_id="res_123",
            start_time=1234567890,
            persons_number=4
        ))

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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/reservations/rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.reservations.get("rsv_123")

        assert result.id == "rsv_123"
        assert result.status == "confirmed"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a reservation."""
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

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/reservations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.reservations.update(UpdateReservation(
            id="rsv_123",
            persons_number=6,
            status="confirmed"
        ))

        assert result.persons_number == 6
        assert result.status == "confirmed"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a reservation."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/reservations/rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/reservations?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.reservations.list(PaginationRequest(page=1, page_size=10))

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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/reservations/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.reservations.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_cancel(self, client: WiilClient, mock_api, api_response):
        """Test canceling a reservation."""
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
            "status": "cancelled",
            "notes": None,
            "cancelReason": "Customer request",
            "isResourceReservation": False,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567892,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/reservations/rsv_123/cancel",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.reservations.cancel("rsv_123", reason="Customer request")

        assert result.status == "cancelled"
        assert result.cancel_reason == "Customer request"

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create reservation handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/reservations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Customer ID is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.reservations.create(CreateReservation(
                reservation_type="table",
                customer_id="cust_123",
                start_time=1234567890
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get reservation handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/reservations/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Reservation not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.reservations.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
