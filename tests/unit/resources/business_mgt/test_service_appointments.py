"""Tests for Service Appointments resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestServiceAppointmentsResource:
    """Test suite for ServiceAppointmentsResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new service appointment."""
        input_data = {
            "customer_id": "cust_123",
            "service_id": "svc_123",
            "start_time": "2024-01-01T10:00:00Z",
            "end_time": "2024-01-01T11:00:00Z",
        }

        mock_response = {
            "id": "appt_123",
            "customerId": "cust_123",
            "serviceId": "svc_123",
            "startTime": "2024-01-01T10:00:00Z",
            "endTime": "2024-01-01T11:00:00Z",
            "status": "pending",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/service-appointments",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.service_appointments.create(**input_data)

        assert result.id == "appt_123"
        assert result.customer_id == "cust_123"
        assert result.service_id == "svc_123"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a service appointment by ID."""
        mock_response = {
            "id": "appt_123",
            "customerId": "cust_123",
            "serviceId": "svc_123",
            "startTime": "2024-01-01T10:00:00Z",
            "endTime": "2024-01-01T11:00:00Z",
            "status": "confirmed",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/service-appointments/appt_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.service_appointments.get("appt_123")

        assert result.id == "appt_123"
        assert result.status == "confirmed"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a service appointment."""
        update_data = {
            "id": "appt_123",
            "status": "confirmed",
        }

        mock_response = {
            "id": "appt_123",
            "customerId": "cust_123",
            "status": "confirmed",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/service-appointments",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.service_appointments.update(**update_data)

        assert result.status == "confirmed"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a service appointment."""
        mock_api.delete(
            f"{BASE_URL}/service-appointments/appt_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.service_appointments.delete("appt_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing service appointments with pagination."""
        mock_appointments = [
            {
                "id": "appt_1",
                "customerId": "cust_123",
                "serviceId": "svc_123",
                "status": "confirmed",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "appt_2",
                "customerId": "cust_456",
                "serviceId": "svc_456",
                "status": "pending",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_appointments,
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
            f"{BASE_URL}/service-appointments?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.service_appointments.list(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving service appointments by customer."""
        mock_appointments = [
            {
                "id": "appt_1",
                "customerId": "cust_123",
                "serviceId": "svc_123",
                "status": "confirmed",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_appointments,
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
            f"{BASE_URL}/service-appointments/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.service_appointments.get_by_customer("cust_123", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_update_status(self, client: WiilClient, mock_api, api_response):
        """Test updating service appointment status."""
        mock_response = {
            "id": "appt_123",
            "customerId": "cust_123",
            "status": "completed",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/service-appointments/appt_123/status",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.service_appointments.update_status("appt_123", "completed")

        assert result.status == "completed"

    def test_get_available_slots(self, client: WiilClient, mock_api, api_response):
        """Test retrieving available appointment slots."""
        mock_slots = [
            {
                "startTime": "2024-01-01T10:00:00Z",
                "endTime": "2024-01-01T11:00:00Z",
                "available": True,
            },
            {
                "startTime": "2024-01-01T11:00:00Z",
                "endTime": "2024-01-01T12:00:00Z",
                "available": True,
            },
        ]

        mock_api.get(
            f"{BASE_URL}/service-appointments/available-slots",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_slots)))

        result = client.service_appointments.get_available_slots()

        assert len(result) == 2
        assert result[0].available is True
