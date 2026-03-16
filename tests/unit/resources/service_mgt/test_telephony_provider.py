"""Tests for Telephony Provider resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestTelephonyProviderResource:
    """Test suite for TelephonyProviderResource."""

    def test_get_regions_not_exposed(self, client: WiilClient):
        """Ensure the unsupported regions API is not exposed."""
        assert not hasattr(client.telephony_provider, "get_regions")

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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/numbers?countryCode=US",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_numbers),
            status=200,
        )

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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/numbers?countryCode=US&areaCode=206&contains=555&postalCode=98101",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_numbers),
            status=200,
        )

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
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/numbers?countryCode=XX",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "No phone numbers available"),
            status=404,
        )

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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/pricing?countryCode=US",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_pricing),
            status=200,
        )

        result = client.telephony_provider.get_pricing("signalwire", "US")

        assert len(result) == 2
        assert result[0].number_type == "local"
        assert result[0].price == 1.00
        assert result[1].number_type == "toll_free"
        assert result[1].price == 2.00

    def test_get_pricing_error(self, client: WiilClient, mock_api, error_response):
        """Test API error when getting pricing."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/signalwire/pricing?countryCode=XX",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Pricing not available for region"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.telephony_provider.get_pricing("signalwire", "XX")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_purchase_status(self, client: WiilClient, mock_api, api_response):
        """Test retrieving phone number purchase status by request id."""
        mock_purchase = {
            "id": "req_123",
            "friendlyName": "Customer Support",
            "phoneNumber": "+12065551234",
            "countryCode": "US",
            "chargedCredits": 1.0,
            "status": "completed",
            "numberType": "local",
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/purchase-request/req_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_purchase),
            status=200,
        )

        result = client.telephony_provider.get_purchase_status("req_123")

        assert result["id"] == "req_123"
        assert result["status"] == "completed"

    def test_purchase_returns_terminal_status_immediately(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test purchase returns immediately when initial state is terminal."""
        purchase_payload = {
            "phoneNumber": "+12065551234",
            "friendlyName": "Customer Support",
        }
        completed_purchase = {
            "id": "req_234",
            "friendlyName": "Customer Support",
            "phoneNumber": "+12065551234",
            "countryCode": "US",
            "chargedCredits": 1.0,
            "status": "completed",
            "numberType": "local",
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/phone-configurations/telephony-provider/purchase",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(completed_purchase),
            status=200,
        )

        result = client.telephony_provider.purchase(purchase_payload)

        assert result["id"] == "req_234"
        assert result["status"] == "completed"

    def test_purchase_polls_until_completed(
        self,
        client: WiilClient,
        mock_api,
        api_response,
        monkeypatch,
    ):
        """Test purchase polling flow until it reaches a terminal status."""
        purchase_payload = {
            "phoneNumber": "+12065551234",
            "friendlyName": "Customer Support",
        }
        pending_purchase = {
            "id": "req_345",
            "friendlyName": "Customer Support",
            "phoneNumber": "+12065551234",
            "countryCode": "US",
            "chargedCredits": 1.0,
            "status": "pending",
            "numberType": "local",
        }
        completed_purchase = {
            "id": "req_345",
            "friendlyName": "Customer Support",
            "phoneNumber": "+12065551234",
            "countryCode": "US",
            "chargedCredits": 1.0,
            "status": "completed",
            "numberType": "local",
        }

        monkeypatch.setattr(
            client.telephony_provider,
            "_POLL_INTERVAL_SECONDS",
            0,
        )
        monkeypatch.setattr(
            client.telephony_provider,
            "_POLL_TIMEOUT_SECONDS",
            2,
        )

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/phone-configurations/telephony-provider/purchase",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(pending_purchase),
            status=200,
        )

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/purchase-request/req_345",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(pending_purchase),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/phone-configurations/telephony-provider/purchase-request/req_345",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(completed_purchase),
            status=200,
        )

        result = client.telephony_provider.purchase(purchase_payload)

        assert result["id"] == "req_345"
        assert result["status"] == "completed"

    def test_purchase_timeout(self, client: WiilClient, mock_api, api_response, monkeypatch):
        """Test purchase polling timeout."""
        purchase_payload = {
            "phoneNumber": "+12065551234",
            "friendlyName": "Customer Support",
        }
        pending_purchase = {
            "id": "req_456",
            "friendlyName": "Customer Support",
            "phoneNumber": "+12065551234",
            "countryCode": "US",
            "chargedCredits": 1.0,
            "status": "pending",
            "numberType": "local",
        }

        monkeypatch.setattr(
            client.telephony_provider,
            "_POLL_INTERVAL_SECONDS",
            0,
        )
        monkeypatch.setattr(
            client.telephony_provider,
            "_POLL_TIMEOUT_SECONDS",
            0,
        )

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/phone-configurations/telephony-provider/purchase",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(pending_purchase),
            status=200,
        )

        with pytest.raises(TimeoutError):
            client.telephony_provider.purchase(purchase_payload)
