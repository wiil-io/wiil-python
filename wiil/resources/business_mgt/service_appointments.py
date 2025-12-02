"""Service Appointments resource for managing service appointments."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    ServiceAppointment,
    CreateServiceAppointment,
)
from wiil.types import PaginatedResult


class ServiceAppointmentsResource:
    """Resource class for managing service appointments in the WIIL Platform.

    Provides methods for creating, retrieving, updating, canceling, and listing
    service appointments. Service appointments represent scheduled sessions for
    business services with customers.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/service-appointments'

    def create(self, **kwargs: Any) -> ServiceAppointment:
        """Create a new service appointment."""
        data = CreateServiceAppointment(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServiceAppointment
        )

    def get(self, appointment_id: str) -> ServiceAppointment:
        """Retrieve a service appointment by ID."""
        return self._http.get(f'{self._base_path}/{appointment_id}')

    def get_by_customer(
        self,
        customer_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ServiceAppointment]:
        """Retrieve service appointments by customer."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-customer/{customer_id}{query_string}')

    def get_by_service(
        self,
        service_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ServiceAppointment]:
        """Retrieve service appointments by service."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-service/{service_id}{query_string}')

    def update_status(self, appointment_id: str, status: str) -> ServiceAppointment:
        """Update appointment status."""
        return self._http.patch(
            f'{self._base_path}/{appointment_id}/status',
            {'status': status}
        )

    def cancel(self, appointment_id: str, reason: Optional[str] = None) -> ServiceAppointment:
        """Cancel a service appointment."""
        data: Dict[str, Any] = {}
        if reason is not None:
            data['reason'] = reason
        return self._http.post(f'{self._base_path}/{appointment_id}/cancel', data)

    def reschedule(
        self,
        appointment_id: str,
        start_time: str,
        end_time: str,
        service_id: Optional[str] = None
    ) -> ServiceAppointment:
        """Reschedule a service appointment."""
        data: Dict[str, Any] = {
            'startTime': start_time,
            'endTime': end_time
        }
        if service_id is not None:
            data['serviceId'] = service_id
        return self._http.post(f'{self._base_path}/{appointment_id}/reschedule', data)

    def delete(self, appointment_id: str) -> bool:
        """Delete a service appointment."""
        return self._http.delete(f'{self._base_path}/{appointment_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ServiceAppointment]:
        """List service appointments with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['ServiceAppointmentsResource']
