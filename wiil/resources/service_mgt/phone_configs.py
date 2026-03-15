"""Phone Configurations resource for managing phone configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    PhoneConfiguration,
    UpdatePhoneConfiguration,
)
from wiil.types import PaginatedResult, PaginationRequest


class PhoneConfigurationsResource:
    """Resource class for managing phone configurations in the WIIL Platform.

    Provides methods for retrieving, updating, deleting, and listing
    phone configurations. Phone configurations manage phone numbers and telephony
    settings for voice-based AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/phone-configurations'

    def get(self, config_id: str) -> PhoneConfiguration:
        """Retrieve a phone configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def get_by_phone_number(self, phone_number: str) -> PhoneConfiguration:
        """Retrieve a phone configuration by phone number."""
        return self._http.get(f'{self._base_path}/by-phone-number/{phone_number}')

    def get_by_request_id(self, request_id: str) -> PhoneConfiguration:
        """Retrieve a phone configuration by request ID."""
        return self._http.get(f'{self._base_path}/by-request/{request_id}')

    def update(self, data: UpdatePhoneConfiguration) -> PhoneConfiguration:
        """Update an existing phone configuration.

        Args:
            data: Phone configuration update data (must include id)

        Returns:
            The updated phone configuration
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdatePhoneConfiguration
        )

    def delete(self, config_id: str) -> bool:
        """Delete a phone configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[PhoneConfiguration]:
        """List phone configurations with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of phone configurations
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['PhoneConfigurationsResource']
