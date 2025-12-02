"""Reservations resource for managing customer reservations."""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    Reservation,
    CreateReservation,
    UpdateReservation,
    ReservationSettings,
    CreateReservationSettings,
    UpdateReservationSettings,
)
from wiil.types import PaginatedResult


class ReservationsResource:
    """Resource class for managing reservations in the WIIL Platform.

    Provides comprehensive methods for creating, retrieving, updating, canceling,
    and rescheduling reservations. Supports filtering by customer and resource.
    Includes reservation settings management.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/reservations'

    def create(self, **kwargs: Any) -> Reservation:
        """Create a new reservation."""
        data = CreateReservation(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateReservation
        )

    def get(self, reservation_id: str) -> Reservation:
        """Retrieve a reservation by ID."""
        return self._http.get(f'{self._base_path}/{reservation_id}')

    def get_by_customer(
        self,
        customer_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[Reservation]:
        """Retrieve reservations by customer."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-customer/{customer_id}{query_string}')

    def get_by_resource(
        self,
        resource_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[Reservation]:
        """Retrieve reservations by resource."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-resource/{resource_id}{query_string}')

    def update(self, **kwargs: Any) -> Reservation:
        """Update an existing reservation."""
        data = UpdateReservation(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateReservation
        )

    def update_status(self, reservation_id: str, status: str) -> Reservation:
        """Update reservation status."""
        return self._http.patch(
            f'{self._base_path}/{reservation_id}/status',
            {'status': status}
        )

    def cancel(self, reservation_id: str, reason: Optional[str] = None) -> Reservation:
        """Cancel a reservation."""
        data: Dict[str, Any] = {}
        if reason is not None:
            data['reason'] = reason
        return self._http.post(f'{self._base_path}/{reservation_id}/cancel', data)

    def reschedule(
        self,
        reservation_id: str,
        start_time: str,
        end_time: str,
        resource_id: Optional[str] = None
    ) -> Reservation:
        """Reschedule a reservation."""
        data: Dict[str, Any] = {
            'startTime': start_time,
            'endTime': end_time
        }
        if resource_id is not None:
            data['resourceId'] = resource_id
        return self._http.post(f'{self._base_path}/{reservation_id}/reschedule', data)

    def delete(self, reservation_id: str) -> bool:
        """Delete a reservation."""
        return self._http.delete(f'{self._base_path}/{reservation_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[Reservation]:
        """List reservations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    # =============== Reservation Settings Methods ===============

    def get_settings(self) -> List[ReservationSettings]:
        """Retrieve reservation settings for the organization."""
        return self._http.get(f'{self._base_path}/settings')

    def create_settings(self, **kwargs: Any) -> ReservationSettings:
        """Create reservation settings."""
        data = CreateReservationSettings(**kwargs)
        return self._http.post(
            f'{self._base_path}/settings',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateReservationSettings
        )

    def update_settings(self, **kwargs: Any) -> ReservationSettings:
        """Update reservation settings."""
        data = UpdateReservationSettings(**kwargs)
        return self._http.patch(
            f'{self._base_path}/settings',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateReservationSettings
        )

    def delete_settings(self, settings_id: str) -> bool:
        """Delete reservation settings."""
        return self._http.delete(f'{self._base_path}/settings/{settings_id}')


__all__ = ['ReservationsResource']
