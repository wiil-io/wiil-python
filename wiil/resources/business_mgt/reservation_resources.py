"""Reservation Resources resource for managing reservation resources."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    ReservationResource,
    CreateReservationResource,
    UpdateReservationResource,
)
from wiil.types import PaginatedResult


class ReservationResourcesResource:
    """Resource class for managing reservation resources in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    reservation resources. Reservation resources represent bookable items such as
    tables, rooms, equipment, or staff that can be reserved by customers.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/reservation-resources'

    def create(self, **kwargs: Any) -> ReservationResource:
        """Create a new reservation resource."""
        data = CreateReservationResource(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateReservationResource
        )

    def get(self, resource_id: str) -> ReservationResource:
        """Retrieve a reservation resource by ID."""
        return self._http.get(f'{self._base_path}/{resource_id}')

    def get_by_type(
        self,
        resource_type: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ReservationResource]:
        """Retrieve reservation resources by type."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-type/{resource_type}{query_string}')

    def update(self, **kwargs: Any) -> ReservationResource:
        """Update an existing reservation resource."""
        data = UpdateReservationResource(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateReservationResource
        )

    def delete(self, resource_id: str) -> bool:
        """Delete a reservation resource."""
        return self._http.delete(f'{self._base_path}/{resource_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ReservationResource]:
        """List reservation resources with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['ReservationResourcesResource']
