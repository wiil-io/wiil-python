"""Service Appointments resource for managing service appointments."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateServiceAppointment,
    ServiceAppointment,
    ServiceSlotQueryRequest,
    ServiceSlotQueryResponse,
    UpdateServiceAppointment,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ServiceAppointmentsResource:
    """Resource class for managing service appointments in the WIIL Platform.

    Provides methods for creating, retrieving, updating, canceling, and listing
    service appointments. Service appointments represent scheduled sessions for
    business services with customers.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/service-appointments'

    def create(self, data: CreateServiceAppointment) -> ServiceAppointment:
        """Create a new service appointment."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServiceAppointment,
            response_model=ServiceAppointment
        )

    def get(self, appointment_id: str) -> ServiceAppointment:
        """Retrieve a service appointment by ID."""
        return self._http.get(
            f'{self._base_path}/{appointment_id}',
            response_model=ServiceAppointment,
        )

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ServiceAppointment]:
        """Retrieve service appointments by customer."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-customer/{customer_id}{query_string}',
            response_model=PaginatedResult[ServiceAppointment]
        )

    def get_by_service(
        self,
        service_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ServiceAppointment]:
        """Retrieve service appointments by service."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-service/{service_id}{query_string}',
            response_model=PaginatedResult[ServiceAppointment]
        )

    def get_by_provider(
        self,
        provider_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceAppointment]:
        """Retrieve service appointments by provider."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-provider/{provider_id}{query_string}',
            response_model=PaginatedResult[ServiceAppointment],
        )

    def get_by_date_range(
        self,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceAppointment]:
        """Retrieve service appointments by date range."""
        query_params: Dict[str, Any] = {
            'startDate': start_date,
            'endDate': end_date,
        }
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        return self._http.get(
            f'{self._base_path}/by-date-range?{urlencode(query_params)}',
            response_model=PaginatedResult[ServiceAppointment],
        )

    def get_available_slots(
        self,
        request: ServiceSlotQueryRequest,
    ) -> ServiceSlotQueryResponse:
        """Retrieve available appointment slots for a service.

        Returns:
            The available slot query response payload
        """
        query_params: Dict[str, Any] = {
            'serviceId': request.service_id,
            'localDate': request.local_date,
            'providerId': request.provider_id,
        }
        if request.location_id is not None:
            query_params['locationId'] = request.location_id
        if request.max_results is not None:
            query_params['maxResults'] = request.max_results

        return self._http.get(
            f'{self._base_path}/available-slots?{urlencode(query_params)}',
            response_model=ServiceSlotQueryResponse,
        )

    def update(self, data: UpdateServiceAppointment) -> ServiceAppointment:
        """Update an existing service appointment."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateServiceAppointment,
            response_model=ServiceAppointment,
        )

    def update_status(
        self,
        appointment_id: str,
        status: str,
    ) -> ServiceAppointment:
        """Update appointment status."""
        return self._http.patch(
            f'{self._base_path}/{appointment_id}/status',
            {'status': status},
            response_model=ServiceAppointment
        )

    def cancel(
        self,
        appointment_id: str,
        reason: Optional[str] = None,
    ) -> ServiceAppointment:
        """Cancel a service appointment."""
        data: Dict[str, Any] = {}
        if reason is not None:
            data['cancelReason'] = reason
        return self._http.post(
            f'{self._base_path}/{appointment_id}/cancel',
            data,
            response_model=ServiceAppointment
        )

    def reschedule(
        self,
        appointment_id: str,
        start_time: int,
        end_time: Optional[int] = None,
        business_service_id: Optional[str] = None,
    ) -> ServiceAppointment:
        """Reschedule a service appointment."""
        data: Dict[str, Any] = {
            'startTime': start_time,
        }
        if end_time is not None:
            data['endTime'] = end_time
        if business_service_id is not None:
            data['businessServiceId'] = business_service_id
        return self._http.post(
            f'{self._base_path}/{appointment_id}/reschedule',
            data,
            response_model=ServiceAppointment
        )

    def delete(self, appointment_id: str) -> bool:
        """Delete a service appointment."""
        return self._http.delete(f'{self._base_path}/{appointment_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceAppointment]:
        """List service appointments with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[ServiceAppointment]
        )

    def create_batch(
        self,
        data: List[Union[CreateServiceAppointment, Dict[str, Any]]],
    ) -> PaginatedResult[ServiceAppointment]:
        """Create multiple service appointments in a batch."""
        if len(data) > BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': (
                        f'Array length {len(data)} exceeds maximum '
                        f'of {BATCH_LIMIT}'
                    ),
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateServiceAppointment.model_validate(item)
                    payload.append(
                        validated.model_dump(by_alias=True, exclude_none=True)
                    )
                elif isinstance(item, BaseModel):
                    payload.append(
                        item.model_dump(by_alias=True, exclude_none=True)
                    )
                else:
                    raise WiilValidationError(
                        f'Invalid item type at index {i}',
                        details=[{
                            'path': ['data', i],
                            'message': 'Expected dict or Pydantic model'
                        }]
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f'Validation failed for item at index {i}',
                    details=e.errors()
                )

        return self._http.post(
            f'{self._base_path}/batch',
            payload,
            response_model=PaginatedResult[ServiceAppointment],
        )


__all__ = ['ServiceAppointmentsResource']
