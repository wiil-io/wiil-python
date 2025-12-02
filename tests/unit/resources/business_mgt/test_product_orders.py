"""Tests for Product Orders resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductOrdersResource:
    """Test suite for ProductOrdersResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new product order."""
        input_data = {
            "customer_id": "cust_123",
            "items": [{"product_id": "prod_123", "quantity": 2}],
            "total": 59.98,
        }

        mock_response = {
            "id": "order_123",
            "customerId": "cust_123",
            "items": [{"productId": "prod_123", "quantity": 2}],
            "total": 59.98,
            "status": "pending",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/product-orders",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.product_orders.create(**input_data)

        assert result.id == "order_123"
        assert result.customer_id == "cust_123"
        assert result.total == 59.98

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product order by ID."""
        mock_response = {
            "id": "order_123",
            "customerId": "cust_123",
            "items": [{"productId": "prod_123", "quantity": 2}],
            "total": 59.98,
            "status": "pending",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/product-orders/order_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.product_orders.get("order_123")

        assert result.id == "order_123"
        assert result.status == "pending"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a product order."""
        update_data = {
            "id": "order_123",
            "status": "confirmed",
        }

        mock_response = {
            "id": "order_123",
            "customerId": "cust_123",
            "status": "confirmed",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/product-orders",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.product_orders.update(**update_data)

        assert result.status == "confirmed"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a product order."""
        mock_api.delete(
            f"{BASE_URL}/product-orders/order_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.product_orders.delete("order_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing product orders with pagination."""
        mock_orders = [
            {
                "id": "order_1",
                "customerId": "cust_123",
                "total": 59.98,
                "status": "pending",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "order_2",
                "customerId": "cust_456",
                "total": 99.99,
                "status": "confirmed",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_orders,
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
            f"{BASE_URL}/product-orders?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.product_orders.list(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving product orders by customer."""
        mock_orders = [
            {
                "id": "order_1",
                "customerId": "cust_123",
                "total": 59.98,
                "status": "pending",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_orders,
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
            f"{BASE_URL}/product-orders/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.product_orders.get_by_customer("cust_123", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_update_status(self, client: WiilClient, mock_api, api_response):
        """Test updating product order status."""
        mock_response = {
            "id": "order_123",
            "customerId": "cust_123",
            "status": "completed",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/product-orders/order_123/status",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.product_orders.update_status("order_123", "completed")

        assert result.status == "completed"
