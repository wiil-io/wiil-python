"""Telephony Provider resource for managing phone numbers and telephony services.

This module provides methods for retrieving available regions, searching for phone numbers,
and getting pricing information from various telephony providers (SignalWire, Twilio, etc.).
All methods require proper authentication via API key.

Example:
    ```python
    from wiil import WiilClient
    from wiil.types.service_types import ProviderType

    client = WiilClient(api_key='your-api-key')

    # Get available regions for SignalWire
    regions = client.telephony_provider.get_regions(ProviderType.SIGNALWIRE)

    # Search for phone numbers in a specific region
    numbers = client.telephony_provider.get_phone_numbers(
        ProviderType.SIGNALWIRE,
        'US',
        area_code='206'
    )

    # Get pricing for a region
    pricing = client.telephony_provider.get_pricing(ProviderType.SIGNALWIRE, 'US')
    ```
"""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.phone_number import (
    BasePhoneNumberInfo,
    PhoneNumberPricing,
    PhoneProviderRegion,
)
from wiil.types.service_types import ProviderType


class TelephonyProviderResource:
    """Resource class for managing telephony provider services.

    Provides methods for retrieving available regions, searching for phone numbers,
    and getting pricing information from various telephony providers (SignalWire, Twilio, etc.).
    All methods require proper authentication via API key.
    """

    def __init__(self, http: HttpClient):
        """Initialize the TelephonyProviderResource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._resource_path = "/phone-configurations/telephony-provider"

    def get_regions(self, provider: ProviderType) -> List[PhoneProviderRegion]:
        """Retrieve available regions for phone numbers by provider.

        Args:
            provider: Telephony provider (e.g., ProviderType.SIGNALWIRE, ProviderType.TWILIO)

        Returns:
            List of available regions with region information

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            ```python
            regions = client.telephony_provider.get_regions(ProviderType.SIGNALWIRE)
            print(f"Found {len(regions)} regions")
            for region in regions:
                print(f"- {region.region_name} ({region.region_id})")
            ```
        """
        return self._http.get(f"{self._resource_path}/{provider}/regions")

    def get_phone_numbers(
        self,
        provider: ProviderType,
        country_code: str,
        area_code: Optional[str] = None,
        contains: Optional[str] = None,
        postal_code: Optional[str] = None
    ) -> List[BasePhoneNumberInfo]:
        """Retrieve available phone numbers for a specific provider and region.

        Args:
            provider: Telephony provider (e.g., ProviderType.SIGNALWIRE, ProviderType.TWILIO)
            country_code: Country code (e.g., 'US', 'CA')
            area_code: Optional area code filter (e.g., '206', '415')
            contains: Optional number pattern to search for
            postal_code: Optional postal code filter

        Returns:
            List of available phone numbers matching the search criteria

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            ```python
            # Search for phone numbers in US
            numbers = client.telephony_provider.get_phone_numbers(
                ProviderType.SIGNALWIRE,
                'US'
            )

            # Search with area code filter
            seattle_numbers = client.telephony_provider.get_phone_numbers(
                ProviderType.SIGNALWIRE,
                'US',
                area_code='206'
            )

            # Search for specific number pattern
            custom_numbers = client.telephony_provider.get_phone_numbers(
                ProviderType.SIGNALWIRE,
                'US',
                contains='555',
                postal_code='98101'
            )

            for number in numbers:
                print(f"{number.phone_number} - {number.region}")
            ```
        """
        params: Dict[str, Any] = {"countryCode": country_code}

        if area_code:
            params["areaCode"] = area_code
        if contains:
            params["contains"] = contains
        if postal_code:
            params["postalCode"] = postal_code

        query_string = f'?{urlencode(params)}'
        return self._http.get(f"{self._resource_path}/{provider}/numbers{query_string}")

    def get_pricing(
        self,
        provider: ProviderType,
        country_code: str
    ) -> List[PhoneNumberPricing]:
        """Retrieve pricing information for phone numbers by provider and region.

        Args:
            provider: Telephony provider (e.g., ProviderType.SIGNALWIRE, ProviderType.TWILIO)
            country_code: Country code (e.g., 'US', 'CA')

        Returns:
            List of pricing information for phone numbers in the specified region

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            ```python
            pricing = client.telephony_provider.get_pricing(
                ProviderType.SIGNALWIRE,
                'US'
            )
            for price in pricing:
                print(f"Number Type: {price.number_type}")
                print(f"Price: ${price.price}")
            ```
        """
        params: Dict[str, Any] = {"countryCode": country_code}

        query_string = f'?{urlencode(params)}'
        return self._http.get(f"{self._resource_path}/{provider}/pricing{query_string}")


__all__ = ['TelephonyProviderResource']
