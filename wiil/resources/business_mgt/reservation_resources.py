"""Reservation Resources resource for managing reservation resources."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateResource,
    Resource,
    UpdateResource,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


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
            schema=CreateResource,
            response_model=Resource
        )

    def get(self, resource_id: str) -> Resource:
        """Retrieve a reservation resource by ID."""
        return self._http.get(
            f'{self._base_path}/{resource_id}',
            response_model=Resource
        )

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
        return self._http.get(
            f'{self._base_path}/by-type/{resource_type}{query_string}',
            response_model=PaginatedResult[Resource]
        )

    def update(self, data: UpdateResource) -> Resource:
        """Update an existing reservation resource."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateResource,
            response_model=Resource
        )

    def delete(self, resource_id: str) -> bool:
        """Delete a reservation resource."""
        return self._http.delete(f'{self._base_path}/{resource_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[Resource]:
        """List reservation resources with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[Resource]
        )

    def create_batch(
        self,
        data: List[Union[CreateResource, Dict[str, Any]]]
    ) -> PaginatedResult[Resource]:
        """Create multiple reservation resources in a batch.

        Args:
            data: List of resources to create (max 50 items)

        Returns:
            PaginatedResult containing created resources

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
        if len(data) > BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': f'Array length {len(data)} exceeds maximum of {BATCH_LIMIT}'
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateResource.model_validate(item)
                    payload.append(validated.model_dump(by_alias=True, exclude_none=True))
                elif isinstance(item, BaseModel):
                    payload.append(item.model_dump(by_alias=True, exclude_none=True))
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
            response_model=PaginatedResult[Resource]
        )


__all__ = ['ReservationResourcesResource']
