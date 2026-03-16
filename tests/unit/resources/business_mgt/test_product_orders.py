"""Tests for Product Orders resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateProductOrder,
    UpdateProductOrder,
    ProductOrderItemBase,
    OrderPricing,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductOrdersResource:
    """Test suite for ProductOrdersResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new product order."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "PO-12345",
            "status": "pending",
            "items": [
                {
                    "id": "order_item_1",
                    "productOrderId": "order_123",
                    "productId": "prod_123",
                    "itemName": "Wireless Mouse",
                    "sku": "WM-001",
                    "quantity": 2,
                    "unitPrice": 29.99,
                    "totalPrice": 59.98,
                    "selectedVariant": None,
                    "warrantyInfo": None,
                    "status": "pending",
                    "notes": None,
                }
            ],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 59.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 59.98,
                "currency": "USD",
            },
            "paymentStatus": "pending",
            "paymentMethod": None,
            "paymentReference": None,
            "billingAddress": None,
            "orderDate": 1234567890,
            "requestedDeliveryDate": None,
            "shippedDate": None,
            "shippingAddress": None,
            "deliveredDate": None,
            "shippingMethod": None,
            "trackingNumber": None,
            "shippingCarrier": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/product-orders",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.product_orders.create(CreateProductOrder(
            customer_id="cust_123",
            items=[ProductOrderItemBase(
                product_id="prod_123",
                item_name="Wireless Mouse",
                quantity=2,
                unit_price=29.99,
                total_price=59.98
            )],
            pricing=OrderPricing(subtotal=59.98, total=59.98),
            order_date=1234567890,
        ))

        assert result.id == "order_123"
        assert result.customer_id == "cust_123"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product order by ID."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "PO-12345",
            "status": "pending",
            "items": [],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 59.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 59.98,
                "currency": "USD",
            },
            "paymentStatus": "pending",
            "paymentMethod": None,
            "paymentReference": None,
            "billingAddress": None,
            "orderDate": 1234567890,
            "requestedDeliveryDate": None,
            "shippedDate": None,
            "shippingAddress": None,
            "deliveredDate": None,
            "shippingMethod": None,
            "trackingNumber": None,
            "shippingCarrier": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-orders/order_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.product_orders.get("order_123")

        assert result.id == "order_123"
        assert result.status == "pending"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a product order."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "PO-12345",
            "status": "shipped",
            "items": [],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 59.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 59.98,
                "currency": "USD",
            },
            "paymentStatus": "paid",
            "paymentMethod": None,
            "paymentReference": None,
            "billingAddress": None,
            "orderDate": 1234567890,
            "requestedDeliveryDate": None,
            "shippedDate": 1234567891,
            "shippingAddress": None,
            "deliveredDate": None,
            "shippingMethod": "Standard",
            "trackingNumber": "TRK123456",
            "shippingCarrier": "UPS",
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-orders",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.product_orders.update(UpdateProductOrder(
            id="order_123",
            status="out_for_delivery",
            tracking_number="TRK123456"
        ))

        assert result.status == "shipped"
        assert result.tracking_number == "TRK123456"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a product order."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-orders/order_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.product_orders.delete("order_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing product orders with pagination."""
        mock_orders = [
            {
                "id": "order_1",
                "orderNumber": "PO-12345",
                "status": "pending",
                "items": [],
                "customerId": "cust_123",
                "customer": None,
                "pricing": {
                    "subtotal": 59.98,
                    "tax": 0.0,
                    "tip": 0.0,
                    "shippingAmount": 0.0,
                    "discount": 0.0,
                    "total": 59.98,
                    "currency": "USD",
                },
                "paymentStatus": "pending",
                "paymentMethod": None,
                "paymentReference": None,
                "billingAddress": None,
                "orderDate": 1234567890,
                "requestedDeliveryDate": None,
                "shippedDate": None,
                "shippingAddress": None,
                "deliveredDate": None,
                "shippingMethod": None,
                "trackingNumber": None,
                "shippingCarrier": None,
                "externalOrderId": None,
                "source": "direct",
                "cancelReason": None,
                "notes": None,
                "serviceConversationConfigId": None,
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
            f"{BASE_URL}/product-orders?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.product_orders.list(PaginationRequest(page=1, page_size=10))

        assert len(result.data) == 1
        assert result.meta.total_count == 1

    def test_update_status(self, client: WiilClient, mock_api, api_response):
        """Test updating product order status."""
        mock_response = {
            "id": "order_123",
            "orderNumber": "PO-12345",
            "status": "delivered",
            "items": [],
            "customerId": "cust_123",
            "customer": None,
            "pricing": {
                "subtotal": 59.98,
                "tax": 0.0,
                "tip": 0.0,
                "shippingAmount": 0.0,
                "discount": 0.0,
                "total": 59.98,
                "currency": "USD",
            },
            "paymentStatus": "paid",
            "paymentMethod": None,
            "paymentReference": None,
            "billingAddress": None,
            "orderDate": 1234567890,
            "requestedDeliveryDate": None,
            "shippedDate": 1234567891,
            "shippingAddress": None,
            "deliveredDate": 1234567892,
            "shippingMethod": None,
            "trackingNumber": None,
            "shippingCarrier": None,
            "externalOrderId": None,
            "source": "direct",
            "cancelReason": None,
            "notes": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567892,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-orders/order_123/status",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.product_orders.update_status("order_123", "delivered")

        assert result.status == "delivered"

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create order handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/product-orders",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Items required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.product_orders.create(CreateProductOrder(
                customer_id="cust_123",
                items=[ProductOrderItemBase(
                    product_id="prod_123",
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
            f"{BASE_URL}/product-orders/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Order not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.product_orders.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
