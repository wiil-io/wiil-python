"""Tests for Telephony Provider resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestTelephonyProviderResource:
    """Test suite for TelephonyProviderResource."""

    def test_get_regions(self, client: WiilClient, mock_api, api_response):
        """Test retrieving available regions for a provider."""
        mock_regions = [
            {
                "regionId": "us-west",
                "regionName": "US West",
                "countryCode": "US",
                "countryName": "United States",
                "providerType": "signalwire"
            },
            {
                "regionId": "us-east",
                "regionName": "US East",
                "countryCode": "US",
                "countryName": "United States",
                "providerType": "signalwire"
            }
        ]

        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/regions",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_regions)))

        result = client.telephony_provider.get_regions("signalwire")

        assert len(result) == 2
        assert result[0].region_id == "us-west"
        assert result[0].region_name == "US West"
        assert result[1].region_id == "us-east"

    def test_get_regions_error(self, client: WiilClient, mock_api, error_response):
        """Test API error when getting regions."""
        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/invalid/regions",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            400,
            json=error_response("INVALID_PROVIDER", "Invalid provider type")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.telephony_provider.get_regions("invalid")

        assert exc_info.value.status_code == 400
        assert exc_info.value.code == "INVALID_PROVIDER"

    def test_get_phone_numbers(self, client: WiilClient, mock_api, api_response):
        """Test retrieving available phone numbers."""
        mock_numbers = [
            {
                "friendlyName": "Seattle Number",
                "phoneNumber": "+12065551234",
                "lata": None,
                "rateCenter": "Seattle",
                "region": "WA",
                "postalCode": "98101",
                "countryCode": "US",
                "capabilities": {
                    "voice": True,
                    "SMS": True,
                    "MMS": False
                },
                "beta": False,
                "numberType": "local"
            }
        ]

        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/numbers?countryCode=US",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_numbers)))

        result = client.telephony_provider.get_phone_numbers("signalwire", "US")

        assert len(result) == 1
        assert result[0].phone_number == "+12065551234"
        assert result[0].region == "WA"

    def test_get_phone_numbers_with_filters(self, client: WiilClient, mock_api, api_response):
        """Test retrieving phone numbers with search filters."""
        mock_numbers = [
            {
                "friendlyName": "Seattle 206 Number",
                "phoneNumber": "+12065551234",
                "lata": None,
                "rateCenter": "Seattle",
                "region": "WA",
                "postalCode": "98101",
                "countryCode": "US",
                "capabilities": {
                    "voice": True,
                    "SMS": True,
                    "MMS": False
                },
                "beta": False,
                "numberType": "local"
            }
        ]

        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/numbers?countryCode=US&areaCode=206&contains=555&postalCode=98101",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_numbers)))

        result = client.telephony_provider.get_phone_numbers(
            "signalwire",
            "US",
            area_code="206",
            contains="555",
            postal_code="98101"
        )

        assert len(result) == 1
        assert result[0].phone_number == "+12065551234"

    def test_get_phone_numbers_not_found(self, client: WiilClient, mock_api, error_response):
        """Test when no phone numbers are available."""
        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/numbers?countryCode=XX",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "No phone numbers available")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.telephony_provider.get_phone_numbers("signalwire", "XX")

        assert exc_info.value.status_code == 404

    def test_get_pricing(self, client: WiilClient, mock_api, api_response):
        """Test retrieving pricing information."""
        mock_pricing = [
            {
                "number_type": "local",
                "country": "United States",
                "countryCode": "US",
                "phoneNumberPrices": [
                    {
                        "base_price": "1.00",
                        "current_price": "1.00"
                    }
                ],
                "price": 1.00,
                "priceUnit": "per month",
                "providerType": "signalwire",
                "currency": "USD"
            },
            {
                "number_type": "toll_free",
                "country": "United States",
                "countryCode": "US",
                "phoneNumberPrices": [
                    {
                        "base_price": "2.00",
                        "current_price": "2.00"
                    }
                ],
                "price": 2.00,
                "priceUnit": "per month",
                "providerType": "signalwire",
                "currency": "USD"
            }
        ]

        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/pricing?countryCode=US",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_pricing)))

        result = client.telephony_provider.get_pricing("signalwire", "US")

        assert len(result) == 2
        assert result[0].number_type == "local"
        assert result[0].price == 1.00
        assert result[1].number_type == "toll_free"
        assert result[1].price == 2.00

    def test_get_pricing_error(self, client: WiilClient, mock_api, error_response):
        """Test API error when getting pricing."""
        mock_api.get(
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/pricing?countryCode=XX",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Pricing not available for region")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.telephony_provider.get_pricing("signalwire", "XX")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"
