"""Tests for Customers resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestCustomersResource:
    """Test suite for CustomersResource."""

    def test_create_customer(self, client: WiilClient, mock_api, api_response):
        """Test creating a new customer."""
        input_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
        }

        mock_response = {
            "id": "cust_123",
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/customers",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.create(**input_data)

        assert result.id == "cust_123"
        assert result.firstname == "John"
        assert result.email == "john.doe@example.com"

    def test_get_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a customer by ID."""
        mock_response = {
            "id": "cust_123",
            "firstname": "John",
            "lastname": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/customers/cust_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.get("cust_123")

        assert result.id == "cust_123"
        assert result.firstname == "John"

    def test_get_customer_by_phone(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a customer by phone number."""
        mock_response = {
            "id": "cust_123",
            "firstname": "John",
            "lastname": "Doe",
            "phone_number": "+1234567890",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        # URL encoding: + becomes %2B
        mock_api.get(
            f"{BASE_URL}/customers/phone/%2B1234567890",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.get_by_phone("+1234567890")

        assert result.id == "cust_123"
        assert result.phone_number == "+1234567890"

    def test_get_customer_by_email(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a customer by email."""
        mock_response = {
            "id": "cust_123",
            "firstname": "John",
            "email": "john.doe%40example.com",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        # URL encoding: @ becomes %40
        mock_api.get(
            f"{BASE_URL}/customers/email/john.doe%40example.com",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.get_by_email("john.doe@example.com")

        assert result.id == "cust_123"

    def test_search_customers(self, client: WiilClient, mock_api, api_response):
        """Test searching customers by query."""
        mock_customers = [
            {
                "id": "cust_1",
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@example.com",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_customers,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/customers/search?query=john&page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.search("john", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].firstname == "John"

    def test_update_customer(self, client: WiilClient, mock_api, api_response):
        """Test updating a customer.

        NOTE: This tests the corrected signature update(customer_id, **kwargs).
        """
        update_data = {
            "email": "newemail@example.com",
            "phone_number": "+1555555555",
        }

        mock_response = {
            "id": "cust_123",
            "firstname": "John",
            "lastname": "Doe",
            "email": "newemail@example.com",
            "phone_number": "+1555555555",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/customers/cust_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.update("cust_123", **update_data)

        assert result.email == "newemail@example.com"
        assert result.phone_number == "+1555555555"

    def test_delete_customer(self, client: WiilClient, mock_api, api_response):
        """Test deleting a customer."""
        mock_api.delete(
            f"{BASE_URL}/customers/cust_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.customers.delete("cust_123")

        assert result is True

    def test_list_customers(self, client: WiilClient, mock_api, api_response):
        """Test listing customers with pagination."""
        mock_customers = [
            {
                "id": "cust_1",
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@example.com",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "cust_2",
                "firstname": "Jane",
                "lastname": "Smith",
                "email": "jane@example.com",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_customers,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 2,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/customers",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.customers.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
