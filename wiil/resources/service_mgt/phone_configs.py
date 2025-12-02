"""Phone Configurations resource for managing phone configuration entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    PhoneConfiguration,
    PhoneNumberPurchase,
    CreatePhoneNumberPurchase,
    UpdatePhoneConfiguration,
)
from wiil.types import PaginatedResult


class PhoneConfigurationsResource:
    """Resource class for managing phone configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    phone configurations. Phone configurations manage phone numbers and telephony
    settings for voice-based AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/phone-configurations'

    def purchase(self, **kwargs: Any) -> PhoneNumberPurchase:
        """Purchase a new phone number and create a phone configuration."""
        data = CreatePhoneNumberPurchase(**kwargs)
        return self._http.post(
            f'{self._base_path}/purchase',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreatePhoneNumberPurchase
        )

    def get(self, config_id: str) -> PhoneConfiguration:
        """Retrieve a phone configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def get_by_phone_number(self, phone_number: str) -> PhoneConfiguration:
        """Retrieve a phone configuration by phone number."""
        return self._http.get(f'{self._base_path}/by-phone-number/{phone_number}')

    def get_by_request_id(self, request_id: str) -> PhoneConfiguration:
        """Retrieve a phone configuration by request ID."""
        return self._http.get(f'{self._base_path}/by-request/{request_id}')

    def update(self, **kwargs: Any) -> PhoneConfiguration:
        """Update an existing phone configuration."""
        data = UpdatePhoneConfiguration(**kwargs)
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
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[PhoneConfiguration]:
        """List phone configurations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['PhoneConfigurationsResource']
