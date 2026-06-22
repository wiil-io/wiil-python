"""Tests for Service Appointments resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateServiceAppointment,
    UpdateServiceAppointment,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestServiceAppointmentsResource:
    """Test suite for ServiceAppointmentsResource."""

    @staticmethod
    def _appointment_payload(appointment_id: str = 'appt_123'):
        return {
            'id': appointment_id,
            'customerId': 'cust_123',
            'businessServiceId': 'svc_123',
            'providerId': 'provider_123',
            'startTime': 1234567890,
            'endTime': 1234567950,
            'status': 'pending',
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new service appointment."""
        mock_response = self._appointment_payload()

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
            end_time=1234567950,
        ))

        assert result.id == "appt_123"
        assert result.customer_id == "cust_123"
        assert result.business_service_id == "svc_123"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a service appointment by ID."""
        mock_response = self._appointment_payload()
        mock_response['status'] = 'confirmed'

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
            self._appointment_payload('appt_1'),
            self._appointment_payload('appt_2'),
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
        mock_appointments = [self._appointment_payload('appt_1')]

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
            (
                f'{BASE_URL}/service-appointments/by-customer/'
                'cust_123?page=1&pageSize=10'
            ),
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

    def test_get_by_provider(self, client: WiilClient, mock_api, api_response):
        """Test retrieving appointments by provider."""
        mock_response = {
            'data': [self._appointment_payload('appt_1')],
            'meta': {
                'page': 1,
                'pageSize': 20,
                'totalCount': 1,
                'totalPages': 1,
                'hasNextPage': False,
                'hasPreviousPage': False,
            },
        }

        mock_api.add(
            responses.GET,
            (
                f'{BASE_URL}/service-appointments/by-provider/'
                'provider_123?page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.get_by_provider(
            'provider_123',
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].provider_id == 'provider_123'

    def test_get_by_date_range(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test retrieving appointments by date range."""
        mock_response = {
            'data': [self._appointment_payload('appt_1')],
            'meta': {
                'page': 1,
                'pageSize': 20,
                'totalCount': 1,
                'totalPages': 1,
                'hasNextPage': False,
                'hasPreviousPage': False,
            },
        }

        mock_api.add(
            responses.GET,
            (
                f'{BASE_URL}/service-appointments/by-date-range?'
                'startDate=100&endDate=200&page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.get_by_date_range(
            100,
            200,
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a service appointment."""
        mock_response = self._appointment_payload()
        mock_response['duration'] = 60
        mock_response['updatedAt'] = 1234567891

        mock_api.add(
            responses.PATCH,
            f'{BASE_URL}/service-appointments',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.update(UpdateServiceAppointment(
            id='appt_123',
            duration=60,
        ))

        assert result.duration == 60

    def test_cancel(self, client: WiilClient, mock_api, api_response):
        """Test canceling a service appointment."""
        mock_response = self._appointment_payload()
        mock_response['status'] = 'cancelled'

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

        assert result.status == 'cancelled'

    def test_reschedule(self, client: WiilClient, mock_api, api_response):
        """Test rescheduling a service appointment."""
        mock_response = self._appointment_payload()
        mock_response['startTime'] = 1234567999
        mock_response['endTime'] = 1234568099

        mock_api.add(
            responses.POST,
            f'{BASE_URL}/service-appointments/appt_123/reschedule',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.reschedule(
            'appt_123',
            start_time=1234567999,
            end_time=1234568099,
            business_service_id='svc_123',
        )

        assert result.start_time == 1234567999

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        """Test creating appointments in batch."""
        mock_response = {
            'data': [self._appointment_payload('appt_1')],
            'meta': {
                'page': 1,
                'pageSize': 20,
                'totalCount': 1,
                'totalPages': 1,
                'hasNextPage': False,
                'hasPreviousPage': False,
            },
        }

        mock_api.add(
            responses.POST,
            f'{BASE_URL}/service-appointments/batch',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_appointments.create_batch([
            {
                'customerId': 'cust_123',
                'businessServiceId': 'svc_123',
                'startTime': 1234567890,
                'endTime': 1234567950,
            }
        ])

        assert len(result.data) == 1
        assert result.data[0].id == 'appt_1'

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
                start_time=1234567890,
                end_time=1234567950,
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
