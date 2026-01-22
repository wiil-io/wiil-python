"""Tests for Menu Orders resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenuOrdersResource:
    """Test suite for MenuOrdersResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new menu order."""
        input_data = {
            "customer_id": "cust_123",
            "items": [{"item_id": "item_123", "quantity": 2}],
            "total": 25.98,
        }

        mock_response = {
            "id": "order_123",
            "orderNumber": "A-42",
            "type": "takeout",
            "status": "pending",
            "items": [
                {
                    "id": "order_item_1",
                    "menuOrderId": "order_123",
                    "menuItemId": "item_123",
                    "itemName": "Grilled Salmon",
                    "quantity": 2,
                    "unitPrice": 12.99,
                    "totalPrice": 25.98,
                    "specialInstructions": None,
                    "customizations": None,
                    "status": "pending",
                    "preparationTime": None,
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 25.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 25.98,
                "currency": "USD",
            },
            "paymentStatus": "pending",
            "paymentMethod": None,
            "paymentReference": None,
            "orderDate": 1234567890,
            "requestedTime": None,
            "estimatedReadyTime": None,
            "actualReadyTime": None,
            "specialInstructions": None,
            "allergies": None,
            "tableNumber": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/menu-orders",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menu_orders.create(**input_data)

        assert result.id == "order_123"
        assert result.customer_id == "cust_123"
        assert result.total == 25.98

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a menu order by ID."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "A-42",
            "type": "takeout",
            "status": "pending",
            "items": [
                {
                    "id": "order_item_1",
                    "menuOrderId": "order_123",
                    "menuItemId": "item_123",
                    "itemName": "Grilled Salmon",
                    "quantity": 2,
                    "unitPrice": 12.99,
                    "totalPrice": 25.98,
                    "specialInstructions": None,
                    "customizations": None,
                    "status": "pending",
                    "preparationTime": None,
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 25.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 25.98,
                "currency": "USD",
            },
            "paymentStatus": "pending",
            "paymentMethod": None,
            "paymentReference": None,
            "orderDate": 1234567890,
            "requestedTime": None,
            "estimatedReadyTime": None,
            "actualReadyTime": None,
            "specialInstructions": None,
            "allergies": None,
            "tableNumber": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/menu-orders/order_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menu_orders.get("order_123")

        assert result.id == "order_123"
        assert result.status == "pending"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a menu order."""
        update_data = {
            "id": "order_123",
            "status": "confirmed",
        }

        mock_response = {
            "id": "order_123",
            "orderNumber": "A-42",
            "type": "takeout",
            "status": "confirmed",
            "items": [
                {
                    "id": "order_item_1",
                    "menuOrderId": "order_123",
                    "menuItemId": "item_123",
                    "itemName": "Grilled Salmon",
                    "quantity": 2,
                    "unitPrice": 12.99,
                    "totalPrice": 25.98,
                    "specialInstructions": None,
                    "customizations": None,
                    "status": "pending",
                    "preparationTime": None,
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 25.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 25.98,
                "currency": "USD",
            },
            "paymentStatus": "pending",
            "paymentMethod": None,
            "paymentReference": None,
            "orderDate": 1234567890,
            "requestedTime": None,
            "estimatedReadyTime": None,
            "actualReadyTime": None,
            "specialInstructions": None,
            "allergies": None,
            "tableNumber": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/menu-orders",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menu_orders.update(**update_data)

        assert result.status == "confirmed"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu order."""
        mock_api.delete(
            f"{BASE_URL}/menu-orders/order_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.menu_orders.delete("order_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing menu orders with pagination."""
        mock_orders = [
            {
                "id": "order_1",
                "orderNumber": "A-42",
                "type": "takeout",
                "status": "pending",
                "items": [
                    {
                        "id": "order_item_1",
                        "menuOrderId": "order_1",
                        "menuItemId": "item_123",
                        "itemName": "Grilled Salmon",
                        "quantity": 2,
                        "unitPrice": 12.99,
                        "totalPrice": 25.98,
                        "specialInstructions": None,
                        "customizations": None,
                        "status": "pending",
                        "preparationTime": None,
                        "notes": None,
                    }
                ],
                "customerId": "cust_123",
                "customer": None,
                "pricing": {
                    "subtotal": 25.98,
                    "tax": 0.0,
                    "tip": 0.0,
                    "shippingAmount": 0.0,
                    "discount": 0.0,
                    "total": 25.98,
                    "currency": "USD",
                },
                "paymentStatus": "pending",
                "paymentMethod": None,
                "paymentReference": None,
                "orderDate": 1234567890,
                "requestedTime": None,
                "estimatedReadyTime": None,
                "actualReadyTime": None,
                "specialInstructions": None,
                "allergies": None,
                "tableNumber": None,
                "externalOrderId": None,
                "source": "direct",
                "cancelReason": None,
                "notes": None,
                "serviceConversationConfigId": None,
                "deliveryAddress": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "order_2",
                "orderNumber": "A-43",
                "type": "delivery",
                "status": "confirmed",
                "items": [
                    {
                        "id": "order_item_2",
                        "menuOrderId": "order_2",
                        "menuItemId": "item_456",
                        "itemName": "Caesar Salad",
                        "quantity": 1,
                        "unitPrice": 35.50,
                        "totalPrice": 35.50,
                        "specialInstructions": None,
                        "customizations": None,
                        "status": "confirmed",
                        "preparationTime": None,
                        "notes": None,
                    }
                ],
                "customerId": "cust_456",
                "customer": None,
                "pricing": {
                    "subtotal": 35.50,
                    "tax": 0.0,
                    "tip": 0.0,
                    "shippingAmount": 0.0,
                    "discount": 0.0,
                    "total": 35.50,
                    "currency": "USD",
                },
                "paymentStatus": "pending",
                "paymentMethod": None,
                "paymentReference": None,
                "orderDate": 1234567891,
                "requestedTime": None,
                "estimatedReadyTime": None,
                "actualReadyTime": None,
                "specialInstructions": None,
                "allergies": None,
                "tableNumber": None,
                "externalOrderId": None,
                "source": "direct",
                "cancelReason": None,
                "notes": None,
                "serviceConversationConfigId": None,
                "deliveryAddress": None,
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
            f"{BASE_URL}/menu-orders?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menu_orders.list(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving menu orders by customer."""
        mock_orders = [
            {
                "id": "order_1",
                "orderNumber": "A-42",
                "type": "takeout",
                "status": "pending",
                "items": [
                    {
                        "id": "order_item_1",
                        "menuOrderId": "order_1",
                        "menuItemId": "item_123",
                        "itemName": "Grilled Salmon",
                        "quantity": 2,
                        "unitPrice": 12.99,
                        "totalPrice": 25.98,
                        "specialInstructions": None,
                        "customizations": None,
                        "status": "pending",
                        "preparationTime": None,
                        "notes": None,
                    }
                ],
                "customerId": "cust_123",
                "customer": None,
                "pricing": {
                    "subtotal": 25.98,
                    "tax": 0.0,
                    "tip": 0.0,
                    "shippingAmount": 0.0,
                    "discount": 0.0,
                    "total": 25.98,
                    "currency": "USD",
                },
                "paymentStatus": "pending",
                "paymentMethod": None,
                "paymentReference": None,
                "orderDate": 1234567890,
                "requestedTime": None,
                "estimatedReadyTime": None,
                "actualReadyTime": None,
                "specialInstructions": None,
                "allergies": None,
                "tableNumber": None,
                "externalOrderId": None,
                "source": "direct",
                "cancelReason": None,
                "notes": None,
                "serviceConversationConfigId": None,
                "deliveryAddress": None,
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
            f"{BASE_URL}/menu-orders/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menu_orders.get_by_customer("cust_123", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_update_status(self, client: WiilClient, mock_api, api_response):
        """Test updating menu order status."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "A-42",
            "type": "takeout",
            "status": "completed",
            "items": [
                {
                    "id": "order_item_1",
                    "menuOrderId": "order_123",
                    "menuItemId": "item_123",
                    "itemName": "Grilled Salmon",
                    "quantity": 2,
                    "unitPrice": 12.99,
                    "totalPrice": 25.98,
                    "specialInstructions": None,
                    "customizations": None,
                    "status": "pending",
                    "preparationTime": None,
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 25.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 25.98,
                "currency": "USD",
            },
            "paymentStatus": "pending",
            "paymentMethod": None,
            "paymentReference": None,
            "orderDate": 1234567890,
            "requestedTime": None,
            "estimatedReadyTime": None,
            "actualReadyTime": None,
            "specialInstructions": None,
            "allergies": None,
            "tableNumber": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/menu-orders/order_123/status",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menu_orders.update_status("order_123", "completed")

        assert result.status == "completed"
