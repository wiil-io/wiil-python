"""Business Services resource for managing business service configurations."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    BusinessServiceConfig,
    CreateBusinessService,
    ServiceQRCode,
    UpdateBusinessService,
)
from wiil.types import PaginatedResult, PaginationRequest


class BusinessServicesResource:
    """Resource class for managing business services in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    business services. Business services represent the services offered by a business
    within an organization (e.g., haircut, massage, consultation). Supports QR code
    generation for service appointment booking.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/business-services'

    def create(self, data: CreateBusinessService) -> BusinessServiceConfig:
        """Create a new business service."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessService
        )

    def get(self, service_id: str) -> BusinessServiceConfig:
        """Retrieve a business service by ID."""
        return self._http.get(f'{self._base_path}/{service_id}')

    def update(self, data: UpdateBusinessService) -> BusinessServiceConfig:
        """Update an existing business service."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessService
        )

    def delete(self, service_id: str) -> bool:
        """Delete a business service."""
        return self._http.delete(f'{self._base_path}/{service_id}')

    def list(self, params: Optional[PaginationRequest] = None) -> PaginatedResult[BusinessServiceConfig]:
        """List business services with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def generate_qr_code(self, service_id: Optional[str] = None) -> ServiceQRCode:
        """Generate a QR code for service appointment booking.

        Args:
            service_id: Optional specific service ID for direct appointment booking

        Returns:
            The generated QR code data
        """
        params: Dict[str, Any] = {}
        if service_id is not None:
            params['serviceId'] = service_id

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/qr-code/generate{query_string}')


__all__ = ['BusinessServicesResource']
