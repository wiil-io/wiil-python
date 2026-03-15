"""Reservation Resources resource for managing reservation resources."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    CreateResource,
    Resource,
    UpdateResource,
)
from wiil.types import PaginatedResult, PaginationRequest


class ReservationResourcesResource:
    """Resource class for managing reservation resources in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    reservation resources. Reservation resources represent bookable items such as
    tables, rooms, equipment, or staff that can be reserved by customers.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/reservation-resources'

    def create(self, data: CreateResource) -> Resource:
        """Create a new reservation resource."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateResource
        )

    def get(self, resource_id: str) -> Resource:
        """Retrieve a reservation resource by ID."""
        return self._http.get(f'{self._base_path}/{resource_id}')

    def get_by_type(
        self,
        resource_type: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[Resource]:
        """Retrieve reservation resources by type."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/by-type/{resource_type}{query_string}')

    def update(self, data: UpdateResource) -> Resource:
        """Update an existing reservation resource."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateResource
        )

    def delete(self, resource_id: str) -> bool:
        """Delete a reservation resource."""
        return self._http.delete(f'{self._base_path}/{resource_id}')

    def list(self, params: Optional[PaginationRequest] = None) -> PaginatedResult[Resource]:
        """List reservation resources with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['ReservationResourcesResource']
