"""Tests for Customers resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import CreateCustomer, UpdateCustomer
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestCustomersResource:
    """Test suite for CustomersResource."""

    def test_create_customer(self, client: WiilClient, mock_api, api_response):
        """Test creating a new customer."""
        mock_response = {
            "id": "cust_123",
            "customerId": None,
            "phone_number": "+1234567890",
            "firstname": "John",
            "lastname": "Doe",
            "company": None,
            "timezone": None,
            "email": "john.doe@example.com",
            "preferred_language": "en",
            "call_priority": "medium",
            "preferred_contact_method": "email",
            "best_time_to_call": None,
            "notes": None,
            "tags": None,
            "custom_fields": None,
            "channelId": None,
            "address": None,
            "isValidatedNames": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/customers",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.create(CreateCustomer(
            firstname="John",
            lastname="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890"
        ))

        assert result.id == "cust_123"
        assert result.firstname == "John"
        assert result.email == "john.doe@example.com"

    def test_get_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a customer by ID."""
        mock_response = {
            "id": "cust_123",
            "customerId": None,
            "phone_number": "+1234567890",
            "firstname": "John",
            "lastname": "Doe",
            "company": None,
            "timezone": None,
            "email": "john.doe@example.com",
            "preferred_language": "en",
            "call_priority": "medium",
            "preferred_contact_method": "email",
            "best_time_to_call": None,
            "notes": None,
            "tags": None,
            "custom_fields": None,
            "channelId": None,
            "address": None,
            "isValidatedNames": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers/cust_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.get("cust_123")

        assert result.id == "cust_123"
        assert result.firstname == "John"

    def test_get_customer_by_phone(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a customer by phone number."""
        mock_response = {
            "id": "cust_123",
            "customerId": None,
            "phone_number": "+1234567890",
            "firstname": "John",
            "lastname": "Doe",
            "company": None,
            "timezone": None,
            "email": None,
            "preferred_language": "en",
            "call_priority": "medium",
            "preferred_contact_method": "email",
            "best_time_to_call": None,
            "notes": None,
            "tags": None,
            "custom_fields": None,
            "channelId": None,
            "address": None,
            "isValidatedNames": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        # URL encoding: + becomes %2B
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers/phone/%2B1234567890",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.get_by_phone("+1234567890")

        assert result.id == "cust_123"
        assert result.phone_number == "+1234567890"

    def test_get_customer_by_email(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a customer by email."""
        mock_response = {
            "id": "cust_123",
            "customerId": None,
            "phone_number": None,
            "firstname": "John",
            "lastname": None,
            "company": None,
            "timezone": None,
            "email": "john.doe%40example.com",
            "preferred_language": "en",
            "call_priority": "medium",
            "preferred_contact_method": "email",
            "best_time_to_call": None,
            "notes": None,
            "tags": None,
            "custom_fields": None,
            "channelId": None,
            "address": None,
            "isValidatedNames": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        # URL encoding: @ becomes %40
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers/email/john.doe%40example.com",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.get_by_email("john.doe@example.com")

        assert result.id == "cust_123"

    def test_search_customers(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test searching customers by query."""
        mock_customers = [
            {
                "id": "cust_1",
                "customerId": None,
                "phone_number": None,
                "firstname": "John",
                "lastname": "Doe",
                "company": None,
                "timezone": None,
                "email": "john@example.com",
                "preferred_language": "en",
                "call_priority": "medium",
                "preferred_contact_method": "email",
                "best_time_to_call": None,
                "notes": None,
                "tags": None,
                "custom_fields": None,
                "channelId": None,
                "address": None,
                "isValidatedNames": False,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers/search?query=john&page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.search("john", PaginationRequest(page=1, page_size=10))

        assert len(result.data) == 1
        assert result.data[0].firstname == "John"

    def test_update_customer(self, client: WiilClient, mock_api, api_response):
        """Test updating a customer."""
        mock_response = {
            "id": "cust_123",
            "customerId": None,
            "phone_number": "+1555555555",
            "firstname": "John",
            "lastname": "Doe",
            "company": None,
            "timezone": None,
            "email": "newemail@example.com",
            "preferred_language": "en",
            "call_priority": "medium",
            "preferred_contact_method": "email",
            "best_time_to_call": None,
            "notes": None,
            "tags": None,
            "custom_fields": None,
            "channelId": None,
            "address": None,
            "isValidatedNames": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/customers/cust_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.update("cust_123", UpdateCustomer(
            id="cust_123",
            email="newemail@example.com",
            phone_number="+1555555555"
        ))

        assert result.email == "newemail@example.com"
        assert result.phone_number == "+1555555555"

    def test_delete_customer(self, client: WiilClient, mock_api, api_response):
        """Test deleting a customer."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/customers/cust_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.customers.delete("cust_123")

        assert result is True

    def test_list_customers(self, client: WiilClient, mock_api, api_response):
        """Test listing customers with pagination."""
        mock_customers = [
            {
                "id": "cust_1",
                "customerId": None,
                "phone_number": None,
                "firstname": "John",
                "lastname": "Doe",
                "company": None,
                "timezone": None,
                "email": "john@example.com",
                "preferred_language": "en",
                "call_priority": "medium",
                "preferred_contact_method": "email",
                "best_time_to_call": None,
                "notes": None,
                "tags": None,
                "custom_fields": None,
                "channelId": None,
                "address": None,
                "isValidatedNames": False,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "cust_2",
                "customerId": None,
                "phone_number": None,
                "firstname": "Jane",
                "lastname": "Smith",
                "company": None,
                "timezone": None,
                "email": "jane@example.com",
                "preferred_language": "en",
                "call_priority": "medium",
                "preferred_contact_method": "email",
                "best_time_to_call": None,
                "notes": None,
                "tags": None,
                "custom_fields": None,
                "channelId": None,
                "address": None,
                "isValidatedNames": False,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_list_customers_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing customers with explicit pagination parameters."""
        mock_customers = [
            {
                "id": "cust_3",
                "customerId": None,
                "phone_number": None,
                "firstname": "Bob",
                "lastname": "Wilson",
                "company": None,
                "timezone": None,
                "email": "bob@example.com",
                "preferred_language": "en",
                "call_priority": "medium",
                "preferred_contact_method": "email",
                "best_time_to_call": None,
                "notes": None,
                "tags": None,
                "custom_fields": None,
                "channelId": None,
                "address": None,
                "isValidatedNames": False,
                "createdAt": 1234567892,
                "updatedAt": 1234567892,
            },
        ]

        mock_response = {
            "data": mock_customers,
            "meta": {
                "page": 2,
                "pageSize": 10,
                "totalCount": 11,
                "totalPages": 2,
                "hasNextPage": False,
                "hasPreviousPage": True,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers?page=2&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.customers.list(PaginationRequest(page=2, page_size=10))

        assert len(result.data) == 1
        assert result.meta.page == 2
        assert result.meta.has_previous_page is True

    def test_create_customer_api_error(self, client: WiilClient, mock_api, error_response):
        """Test create customer handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/customers",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Email is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.customers.create(CreateCustomer(
                firstname="John",
                lastname="Doe"
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_customer_not_found(self, client: WiilClient, mock_api, error_response):
        """Test get customer handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/customers/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Customer not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.customers.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
