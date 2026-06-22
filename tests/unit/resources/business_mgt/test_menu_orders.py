"""Tests for Menu Orders resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateMenuOrder,
    UpdateMenuOrder,
    MenuOrderItemBase,
    OrderPricing,
)
from wiil.types import PaginationRequest
from wiil.types.business_types import MenuOrderType, OrderStatus

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenuOrdersResource:
    """Test suite for MenuOrdersResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new menu order."""
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
                    "variantId": "variant_123",
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
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-orders",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.create(CreateMenuOrder(
            type=MenuOrderType.TAKEOUT,
            customer_id="cust_123",
            items=[MenuOrderItemBase(
                menu_item_id="item_123",
                variant_id="variant_123",
                item_name="Grilled Salmon",
                quantity=2,
                unit_price=12.99,
                total_price=25.98
            )],
            pricing=OrderPricing(subtotal=25.98, total=25.98),
            order_date=1234567890,
        ))

        assert result.id == "order_123"
        assert result.customer_id == "cust_123"

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
                    "variantId": "variant_123",
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
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-orders/order_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.get("order_123")

        assert result.id == "order_123"
        assert result.type == "takeout"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a menu order."""
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
                    "variantId": "variant_123",
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
            "tableNumber": "5",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/menu-orders",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.update(UpdateMenuOrder(
            id="order_123",
            status=OrderStatus.CONFIRMED,
            table_number="5"
        ))

        assert result.status == "confirmed"
        assert result.table_number == "5"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu order."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/menu-orders/order_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

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
                        "variantId": "variant_123",
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-orders?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.meta.total_count == 1

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
                    "variantId": "variant_123",
                    "itemName": "Grilled Salmon",
                    "quantity": 2,
                    "unitPrice": 12.99,
                    "totalPrice": 25.98,
                    "specialInstructions": None,
                    "customizations": None,
                    "status": "completed",
                    "preparationTime": None,
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
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
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/menu-orders/order_123/status",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.update_status("order_123", "completed")

        assert result.status == "completed"

    def test_get_by_customer(self, client: WiilClient, mock_api, api_response):
        """Test retrieving menu orders by customer."""
        mock_response = {
            "data": [
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
                            "variantId": "variant_123",
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
                    "cancelReason": None,
                    "notes": None,
                    "serviceConversationConfigId": None,
                    "deliveryAddress": None,
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
            f"{BASE_URL}/menu-orders/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_cancel(self, client: WiilClient, mock_api, api_response):
        """Test canceling a menu order."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "A-42",
            "type": "takeout",
            "status": "cancelled",
            "items": [
                {
                    "id": "order_item_1",
                    "menuOrderId": "order_123",
                    "menuItemId": "item_123",
                    "variantId": "variant_123",
                    "itemName": "Grilled Salmon",
                    "quantity": 2,
                    "unitPrice": 12.99,
                    "totalPrice": 25.98,
                    "specialInstructions": None,
                    "customizations": None,
                    "status": "cancelled",
                    "preparationTime": None,
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
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
            "cancelReason": "Customer request",
            "notes": None,
            "serviceConversationConfigId": None,
            "deliveryAddress": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-orders/order_123/cancel",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_orders.cancel(
            "order_123",
            reason="Customer request",
        )

        assert result.status == "cancelled"
        assert result.cancel_reason == "Customer request"

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create order handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-orders",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Items required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.menu_orders.create(CreateMenuOrder(
                type=MenuOrderType.TAKEOUT,
                customer_id="cust_123",
                items=[MenuOrderItemBase(
                    menu_item_id="item_123",
                    variant_id="variant_123",
                    item_name="Test",
                    quantity=1,
                    unit_price=10.0,
                    total_price=10.0
                )],
                pricing=OrderPricing(subtotal=10.0, total=10.0),
                order_date=1234567890,
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get order handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-orders/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Order not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.menu_orders.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
