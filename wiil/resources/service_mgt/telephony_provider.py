"""Telephony Provider resource for managing phone numbers and telephony services.

This module provides methods for searching available phone numbers,
getting pricing information, purchasing phone numbers, and checking
purchase status. All methods require proper authentication via API key.

Example:
    ```python
    from wiil import WiilClient

    client = WiilClient(api_key='your-api-key')

    # Search for phone numbers
    numbers = client.telephony_provider.get_phone_numbers()

    # Search with area code filter
    seattle_numbers = client.telephony_provider.get_phone_numbers(
        area_code='206'
    )

    # Get pricing
    pricing = client.telephony_provider.get_pricing()
    ```
"""

import time
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.phone_number import (
    BasePhoneNumberInfo,
    BusinessPhoneNumberPurchaseRequest,
    PhoneNumberPricing,
    PhoneNumberPurchase,
)
from wiil.types import PaginatedResult


class TelephonyProviderResource:
    """Resource class for managing telephony provider services.

    Provides methods for searching for phone numbers, getting pricing information,
    purchasing phone numbers, and checking purchase status.
    All methods require proper authentication via API key.
    """

    _POLL_INTERVAL_SECONDS = 5
    _POLL_TIMEOUT_SECONDS = 120
    _TERMINAL_PURCHASE_STATES = {"completed", "failed", "cancelled"}

    def __init__(self, http: HttpClient):
        """Initialize the TelephonyProviderResource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._resource_path = "/phone-configurations/telephony-provider"

    def get_phone_numbers(
        self,
        area_code: Optional[str] = None,
        contains: Optional[str] = None,
        postal_code: Optional[str] = None
    ) -> PaginatedResult[BasePhoneNumberInfo]:
        """Retrieve available phone numbers.

        Args:
            area_code: Optional area code filter (e.g., '206', '415')
            contains: Optional number pattern to search for
            postal_code: Optional postal code filter

        Returns:
            Paginated list of available phone numbers matching the search criteria

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            ```python
            # Search for phone numbers
            numbers = client.telephony_provider.get_phone_numbers()

            # Search with area code filter
            seattle_numbers = client.telephony_provider.get_phone_numbers(
                area_code='206'
            )

            for number in numbers:
                print(f"{number.phone_number} - {number.region}")
            ```
        """
        params: Dict[str, Any] = {}

        if area_code:
            params["areaCode"] = area_code
        if contains:
            params["contains"] = contains
        if postal_code:
            params["postalCode"] = postal_code

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(
            f"{self._resource_path}/numbers{query_string}",
            response_model=PaginatedResult[BasePhoneNumberInfo]
        )

    def get_pricing(self) -> PaginatedResult[PhoneNumberPricing]:
        """Retrieve pricing information for phone numbers.

        Returns:
            Paginated list of pricing information for phone numbers

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            ```python
            pricing = client.telephony_provider.get_pricing()
            for price in pricing:
                print(f"Number Type: {price.number_type}")
                print(f"Price: ${price.price}")
            ```
        """
        return self._http.get(
            f"{self._resource_path}/pricing",
            response_model=PaginatedResult[PhoneNumberPricing]
        )

    def purchase(
        self,
        data: Union[BusinessPhoneNumberPurchaseRequest, Dict[str, Any]]
    ) -> PhoneNumberPurchase:
        """Purchase a phone number and poll until terminal state.

        Args:
            data: Purchase request payload

        Returns:
            Final purchase result after polling completes

        Raises:
            TimeoutError: If purchase does not reach terminal status in time
        """
        payload = (
            data.model_dump(by_alias=True, exclude_none=True)
            if isinstance(data, BusinessPhoneNumberPurchaseRequest)
            else data
        )

        initial_result = self._http.post(
            f"{self._resource_path}/purchase",
            payload,
            schema=BusinessPhoneNumberPurchaseRequest,
            response_model=PhoneNumberPurchase
        )

        initial_status = self._normalize_status(initial_result)
        if initial_status in self._TERMINAL_PURCHASE_STATES:
            return initial_result

        request_id = self._extract_field(initial_result, "id")
        if not request_id:
            raise TimeoutError("Purchase polling failed: missing purchase request id")

        start = time.monotonic()
        while (time.monotonic() - start) < self._POLL_TIMEOUT_SECONDS:
            time.sleep(self._POLL_INTERVAL_SECONDS)
            status_result = self.get_purchase_status(request_id)
            status = self._normalize_status(status_result)

            if status in self._TERMINAL_PURCHASE_STATES:
                return status_result

        raise TimeoutError(
            "Phone number purchase timed out after "
            f"{self._POLL_TIMEOUT_SECONDS}s. Last status: {initial_status}"
        )

    def get_purchase_status(self, request_id: str) -> PhoneNumberPurchase:
        """Get current status for a phone purchase request."""
        return self._http.get(
            f"{self._resource_path}/purchase-request/{request_id}",
            response_model=PhoneNumberPurchase
        )

    @staticmethod
    def _extract_field(payload: Any, field_name: str) -> Optional[Any]:
        """Read a field from either model objects or plain dictionaries."""
        if isinstance(payload, dict):
            return payload.get(field_name)
        return getattr(payload, field_name, None)

    @classmethod
    def _normalize_status(cls, payload: Any) -> str:
        """Normalize status values to lowercase text for comparisons."""
        status = cls._extract_field(payload, "status")
        if status is None:
            return ""
        status = getattr(status, "value", status)
        return str(status).lower()


__all__ = ['TelephonyProviderResource']
