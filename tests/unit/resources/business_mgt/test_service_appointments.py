"""Tests for Service Appointments resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import CreateServiceAppointment
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestServiceAppointmentsResource:
    """Test suite for ServiceAppointmentsResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new service appointment."""
        mock_response = {
            "id": "appt_123",
            "businessServiceId": "svc_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": 1234567950,
            "duration": 30,
            "totalPrice": 0.0,
            "depositPaid": 0.0,
            "status": "pending",
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/service-appointments",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.create(CreateServiceAppointment(
            customer_id="cust_123",
            business_service_id="svc_123",
            start_time=1234567890,
            end_time=1234567950
        ))

        assert result.id == "appt_123"
        assert result.customer_id == "cust_123"
        assert result.business_service_id == "svc_123"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a service appointment by ID."""
        mock_response = {
            "id": "appt_123",
            "businessServiceId": "svc_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": 1234567950,
            "duration": 30,
            "totalPrice": 0.0,
            "depositPaid": 0.0,
            "status": "confirmed",
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/service-appointments/appt_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.get("appt_123")

        assert result.id == "appt_123"
        assert result.status == "confirmed"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a service appointment."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/service-appointments/appt_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.service_appointments.delete("appt_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing service appointments with pagination."""
        mock_appointments = [
            {
                "id": "appt_1",
                "businessServiceId": "svc_123",
                "customerId": "cust_123",
                "customerName": None,
                "customerEmail": None,
                "startTime": 1234567890,
                "endTime": 1234567950,
                "duration": 30,
                "totalPrice": 0.0,
                "depositPaid": 0.0,
                "status": "confirmed",
                "assignedUserAccountId": None,
                "calendarId": None,
                "calendarEventId": None,
                "calendarProvider": None,
                "cancelReason": None,
                "serviceConversationConfigId": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "appt_2",
                "businessServiceId": "svc_456",
                "customerId": "cust_456",
                "customerName": None,
                "customerEmail": None,
                "startTime": 1234567891,
                "endTime": 1234567951,
                "duration": 30,
                "totalPrice": 0.0,
                "depositPaid": 0.0,
                "status": "pending",
                "assignedUserAccountId": None,
                "calendarId": None,
                "calendarEventId": None,
                "calendarProvider": None,
                "cancelReason": None,
                "serviceConversationConfigId": None,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/service-appointments?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving service appointments by customer."""
        mock_appointments = [
            {
                "id": "appt_1",
                "businessServiceId": "svc_123",
                "customerId": "cust_123",
                "customerName": None,
                "customerEmail": None,
                "startTime": 1234567890,
                "endTime": 1234567950,
                "duration": 30,
                "totalPrice": 0.0,
                "depositPaid": 0.0,
                "status": "confirmed",
                "assignedUserAccountId": None,
                "calendarId": None,
                "calendarEventId": None,
                "calendarProvider": None,
                "cancelReason": None,
                "serviceConversationConfigId": None,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/service-appointments/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_update_status(self, client: WiilClient, mock_api, api_response):
        """Test updating service appointment status."""
        mock_response = {
            "id": "appt_123",
            "businessServiceId": "svc_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": 1234567950,
            "duration": 30,
            "totalPrice": 0.0,
            "depositPaid": 0.0,
            "status": "completed",
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/service-appointments/appt_123/status",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.update_status("appt_123", "completed")

        assert result.status == "completed"

    def test_cancel(self, client: WiilClient, mock_api, api_response):
        """Test canceling a service appointment."""
        mock_response = {
            "id": "appt_123",
            "businessServiceId": "svc_123",
            "customerId": "cust_123",
            "customerName": None,
            "customerEmail": None,
            "startTime": 1234567890,
            "endTime": 1234567950,
            "duration": 30,
            "totalPrice": 0.0,
            "depositPaid": 0.0,
            "status": "cancelled",
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": "Customer request",
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/service-appointments/appt_123/cancel",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.cancel(
            "appt_123",
            reason="Customer request"
        )

        assert result.status == "cancelled"
        assert result.cancel_reason == "Customer request"

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create appointment handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/service-appointments",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Service ID is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.service_appointments.create(CreateServiceAppointment(
                customer_id="cust_123",
                business_service_id="svc_123",
                start_time=1234567890
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get appointment handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/service-appointments/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Appointment not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.service_appointments.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
