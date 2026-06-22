"""Tests for Shipping Addresses resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateShippingAddress,
    UpdateShippingAddress,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestShippingAddressesResource:
    """Test suite for ShippingAddressesResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "addr_123",
            "customerId": "cust_123",
            "street": "123 Main St",
            "street2": "Apt 4B",
            "city": "New York",
            "state": "NY",
            "postalCode": "10001",
            "country": "US",
            "recipientName": "John Doe",
            "phoneNumber": "+12125551234",
            "instructions": "Leave at front door",
            "isPrimary": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/shipping-addresses",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.create(
            CreateShippingAddress(
                customer_id="cust_123",
                street="123 Main St",
                city="New York",
                state="NY",
                postal_code="10001",
                country="US",
                recipient_name="John Doe",
                phone_number="+12125551234",
                instructions="Leave at front door",
                is_primary=True,
            )
        )

        assert result.id == "addr_123"
        assert result.customer_id == "cust_123"

    def test_get(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "addr_123",
            "customerId": "cust_123",
            "street": "123 Main St",
            "street2": None,
            "city": "New York",
            "state": "NY",
            "postalCode": "10001",
            "country": "US",
            "recipientName": None,
            "phoneNumber": None,
            "instructions": None,
            "isPrimary": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/shipping-addresses/addr_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.get("addr_123")

        assert result.id == "addr_123"
        assert result.is_primary is True

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [
                {
                    "id": "addr_1",
                    "customerId": "cust_123",
                    "street": "123 Main St",
                    "street2": None,
                    "city": "New York",
                    "state": "NY",
                    "postalCode": "10001",
                    "country": "US",
                    "recipientName": None,
                    "phoneNumber": None,
                    "instructions": None,
                    "isPrimary": True,
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                }
            ],
            "meta": {
                "page": 1,
                "pageSize": 10,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/shipping-addresses/by-customer/"
                "cust_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_get_primary(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "addr_1",
            "customerId": "cust_123",
            "street": "123 Main St",
            "street2": None,
            "city": "New York",
            "state": "NY",
            "postalCode": "10001",
            "country": "US",
            "recipientName": None,
            "phoneNumber": None,
            "instructions": None,
            "isPrimary": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/shipping-addresses/primary/cust_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.get_primary("cust_123")

        assert result.id == "addr_1"
        assert result.is_primary is True

    def test_update(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "addr_123",
            "customerId": "cust_123",
            "street": "456 Oak Ave",
            "street2": None,
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "90001",
            "country": "US",
            "recipientName": "John Doe",
            "phoneNumber": "+12125551234",
            "instructions": "Ring twice",
            "isPrimary": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/shipping-addresses/addr_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.update(
            "addr_123",
            UpdateShippingAddress(
                id="addr_123",
                street="456 Oak Ave",
                city="Los Angeles",
                state="CA",
                postal_code="90001",
                country="US",
                is_primary=True,
            ),
        )

        assert result.street == "456 Oak Ave"
        assert result.city == "Los Angeles"

    def test_set_primary(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "id": "addr_123",
            "customerId": "cust_123",
            "street": "456 Oak Ave",
            "street2": None,
            "city": "Los Angeles",
            "state": "CA",
            "postalCode": "90001",
            "country": "US",
            "recipientName": None,
            "phoneNumber": None,
            "instructions": None,
            "isPrimary": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/shipping-addresses/addr_123/set-primary",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.set_primary("addr_123")

        assert result.id == "addr_123"
        assert result.is_primary is True

    def test_delete(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/shipping-addresses/addr_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.shipping_addresses.delete("addr_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [
                {
                    "id": "addr_1",
                    "customerId": "cust_123",
                    "street": "123 Main St",
                    "street2": None,
                    "city": "New York",
                    "state": "NY",
                    "postalCode": "10001",
                    "country": "US",
                    "recipientName": None,
                    "phoneNumber": None,
                    "instructions": None,
                    "isPrimary": True,
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                }
            ],
            "meta": {
                "page": 1,
                "pageSize": 10,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/shipping-addresses?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.shipping_addresses.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.meta.total_count == 1

    def test_get_not_found(
        self,
        client: WiilClient,
        mock_api,
        error_response,
    ):
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/shipping-addresses/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Shipping address not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.shipping_addresses.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
