"""Product order schema definitions for retail/product sales.

This module contains Pydantic models for managing product orders, order items,
and inventory updates for retail and e-commerce operations.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.business_mgt.order import OrderAddress, OrderCustomer, OrderPricing
from wiil.types.business_types import OrderStatus, PaymentStatus


class ProductOrderItemBase(PydanticBaseModel):
    """Base product order item schema (without productOrderId for creation).

    Order line item for a product with quantity, pricing, and variant selection.

    Attributes:
        product_id: Product ID being ordered
        item_name: Name of the product
        sku: Product SKU
        quantity: Quantity ordered
        unit_price: Price per unit
        total_price: Total price for this item
        selected_variant: Selected variant (size, color, etc.)
        warranty_info: Warranty information
        status: Item status
        notes: Additional notes

    Example:
        ```python
        item = ProductOrderItemBase(
            product_id="prod_123",
            item_name="Wireless Mouse",
            sku="WM-001",
            quantity=2,
            unit_price=29.99,
            total_price=59.98,
            status=OrderStatus.PENDING
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    product_id: str = Field(
        ...,
        description="References Product from product-config being ordered",
        alias="productId"
    )
    item_name: str = Field(
        ...,
        description="Display name of the product captured at order time",
        alias="itemName"
    )
    sku: Optional[str] = Field(
        None,
        description="Stock Keeping Unit identifier captured at order time"
    )
    quantity: int = Field(
        ...,
        gt=0,
        description="Number of units ordered for this product"
    )
    unit_price: float = Field(
        ...,
        ge=0,
        description="Price per unit at the time of order",
        alias="unitPrice"
    )
    total_price: float = Field(
        ...,
        ge=0,
        description="Total price for this line item: unitPrice × quantity",
        alias="totalPrice"
    )
    selected_variant: Optional[str] = Field(
        None,
        description="Selected product variant specification (e.g., 'Large/Blue', 'XL', '128GB')",
        alias="selectedVariant"
    )
    warranty_info: Optional[str] = Field(
        None,
        description="Warranty terms and coverage details captured at purchase time",
        alias="warrantyInfo"
    )
    status: OrderStatus = Field(
        OrderStatus.PENDING,
        description="Current fulfillment status of this individual item"
    )
    notes: Optional[str] = Field(
        None,
        description="Internal notes about this item for warehouse or fulfillment staff"
    )


class ProductOrderItem(ProductOrderItemBase):
    """Product order item schema with IDs (for existing items).

    Extends ProductOrderItemBase with unique identifiers for persisted items.

    Attributes:
        id: Unique identifier for this product order item instance
        product_order_id: References parent ProductOrder this item belongs to

    Example:
        ```python
        item = ProductOrderItem(
            id="order_item_123",
            product_order_id="order_456",
            product_id="prod_789",
            item_name="Wireless Keyboard",
            quantity=1,
            unit_price=79.99,
            total_price=79.99,
            status=OrderStatus.PROCESSING
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for this product order item instance")
    product_order_id: str = Field(
        ...,
        description="References parent ProductOrder this item belongs to",
        alias="productOrderId"
    )


class ProductOrder(BaseModel):
    """Product order schema - for retail/product sales.

    Complete product order with items, customer information, pricing, and shipping details.

    Attributes:
        order_number: Human-readable order number
        status: Order status
        items: Items in the order
        customer_id: Customer ID
        customer: Customer information
        pricing: Pricing details
        payment_status: Payment status
        payment_method: Payment method
        payment_reference: Payment reference
        billing_address: Billing address
        order_date: Order date
        requested_delivery_date: Requested delivery date
        shipped_date: Shipped date
        shipping_address: Shipping address
        delivered_date: Delivered date
        shipping_method: Shipping method
        tracking_number: Tracking number
        shipping_carrier: Shipping carrier
        external_order_id: External order ID
        source: Order source
        cancel_reason: Cancellation reason
        notes: Additional notes
        service_conversation_config_id: Service conversation config ID

    Example:
        ```python
        order = ProductOrder(
            id="order_123",
            order_number="ORD-12345",
            status=OrderStatus.PENDING,
            items=[...],
            customer_id="cust_123",
            pricing=OrderPricing(...),
            payment_status=PaymentStatus.PENDING,
            order_date=1234567890
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    order_number: Optional[str] = Field(
        None,
        description="Human-readable order number displayed to customers and staff",
        alias="orderNumber"
    )
    status: OrderStatus = Field(
        OrderStatus.PENDING,
        description="Current order status tracking progression from placement through fulfillment"
    )
    items: List[ProductOrderItem] = Field(
        ...,
        min_length=1,
        description="Products in this order with quantities, pricing, and variants"
    )
    customer_id: str = Field(
        ...,
        description="References Customer who placed this order",
        alias="customerId"
    )
    customer: Optional[OrderCustomer] = Field(
        None,
        description="Populated customer information for convenient access"
    )
    pricing: OrderPricing = Field(
        ...,
        description="Complete pricing breakdown including subtotal, tax, shipping fees, and discounts"
    )
    payment_status: PaymentStatus = Field(
        PaymentStatus.PENDING,
        description="Payment processing status",
        alias="paymentStatus"
    )
    payment_method: Optional[str] = Field(
        None,
        description="Payment method used (e.g., 'credit_card', 'paypal', 'bank_transfer')",
        alias="paymentMethod"
    )
    payment_reference: Optional[str] = Field(
        None,
        description="External payment system reference or transaction ID",
        alias="paymentReference"
    )
    billing_address: Optional[OrderAddress] = Field(
        None,
        description="Billing address for payment processing and invoicing",
        alias="billingAddress"
    )
    order_date: int = Field(
        ...,
        description="Unix timestamp when order was placed",
        alias="orderDate"
    )
    requested_delivery_date: Optional[int] = Field(
        None,
        description="Unix timestamp for customer's requested delivery date",
        alias="requestedDeliveryDate"
    )
    shipped_date: Optional[int] = Field(
        None,
        description="Unix timestamp when order was shipped",
        alias="shippedDate"
    )
    shipping_address: Optional[OrderAddress] = Field(
        None,
        description="Delivery address for shipment",
        alias="shippingAddress"
    )
    delivered_date: Optional[int] = Field(
        None,
        description="Unix timestamp when order was delivered to customer",
        alias="deliveredDate"
    )
    shipping_method: Optional[str] = Field(
        None,
        description="Shipping service level (e.g., 'Standard', 'Express', 'Overnight')",
        alias="shippingMethod"
    )
    tracking_number: Optional[str] = Field(
        None,
        description="Carrier tracking number for shipment monitoring",
        alias="trackingNumber"
    )
    shipping_carrier: Optional[str] = Field(
        None,
        description="Shipping carrier name (e.g., 'UPS', 'FedEx', 'USPS')",
        alias="shippingCarrier"
    )
    external_order_id: Optional[str] = Field(
        None,
        description="Order ID from external system (e-commerce platform, marketplace, ERP)",
        alias="externalOrderId"
    )
    source: str = Field(
        "direct",
        description="Order source channel (e.g., 'direct', 'web', 'marketplace', 'wholesale')"
    )
    cancel_reason: Optional[str] = Field(
        None,
        description="Reason provided when order is cancelled",
        alias="cancelReason"
    )
    notes: Optional[str] = Field(
        None,
        description="Internal operational notes about this order"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        description="References the AI Powered Services conversation configuration",
        alias="serviceConversationConfigId"
    )


class CreateProductOrder(BaseModel):
    """Schema for creating a new product order.

    Omits auto-generated fields and uses base items without IDs.

    Example:
        ```python
        create_data = CreateProductOrder(
            items=[ProductOrderItemBase(...)],
            customer_id="cust_123",
            pricing=OrderPricing(...),
            order_date=1234567890
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    status: OrderStatus = OrderStatus.PENDING
    items: List[ProductOrderItemBase] = Field(..., min_length=1)
    customer_id: str = Field(..., alias="customerId")
    pricing: OrderPricing
    payment_status: PaymentStatus = Field(PaymentStatus.PENDING, alias="paymentStatus")
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    billing_address: Optional[OrderAddress] = Field(None, alias="billingAddress")
    order_date: int = Field(..., alias="orderDate")
    requested_delivery_date: Optional[int] = Field(None, alias="requestedDeliveryDate")
    shipping_address: Optional[OrderAddress] = Field(None, alias="shippingAddress")
    shipping_method: Optional[str] = Field(None, alias="shippingMethod")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    shipping_carrier: Optional[str] = Field(None, alias="shippingCarrier")
    external_order_id: Optional[str] = Field(None, alias="externalOrderId")
    source: str = "direct"
    notes: Optional[str] = None


class UpdateProductOrder(BaseModel):
    """Schema for updating an existing product order.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateProductOrder(
            id="order_123",
            status=OrderStatus.SHIPPED,
            shipped_date=1234567999,
            tracking_number="1Z999AA10123456784"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    status: Optional[OrderStatus] = None
    items: Optional[List[ProductOrderItemBase]] = Field(None, min_length=1)
    customer_id: Optional[str] = Field(None, alias="customerId")
    pricing: Optional[OrderPricing] = None
    payment_status: Optional[PaymentStatus] = Field(None, alias="paymentStatus")
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    billing_address: Optional[OrderAddress] = Field(None, alias="billingAddress")
    order_date: Optional[int] = Field(None, alias="orderDate")
    requested_delivery_date: Optional[int] = Field(None, alias="requestedDeliveryDate")
    shipped_date: Optional[int] = Field(None, alias="shippedDate")
    shipping_address: Optional[OrderAddress] = Field(None, alias="shippingAddress")
    delivered_date: Optional[int] = Field(None, alias="deliveredDate")
    shipping_method: Optional[str] = Field(None, alias="shippingMethod")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    shipping_carrier: Optional[str] = Field(None, alias="shippingCarrier")
    external_order_id: Optional[str] = Field(None, alias="externalOrderId")
    source: Optional[str] = None
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None


class UpdateProductOrderStatus(PydanticBaseModel):
    """Quick status update schema for product orders.

    Simplified schema for updating just the order status and related timing fields.

    Attributes:
        id: Unique identifier of the ProductOrder to update
        status: New order status
        shipped_date: Unix timestamp when order was shipped
        delivered_date: Unix timestamp when order was delivered
        tracking_number: Carrier tracking number

    Example:
        ```python
        status_update = UpdateProductOrderStatus(
            id="order_123",
            status=OrderStatus.DELIVERED,
            delivered_date=1234567999
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier of the ProductOrder to update status for")
    status: OrderStatus = Field(
        ...,
        description="New order status to transition to"
    )
    shipped_date: Optional[int] = Field(
        None,
        description="Unix timestamp when order was shipped",
        alias="shippedDate"
    )
    delivered_date: Optional[int] = Field(
        None,
        description="Unix timestamp when order was delivered",
        alias="deliveredDate"
    )
    tracking_number: Optional[str] = Field(
        None,
        description="Carrier tracking number added when order ships",
        alias="trackingNumber"
    )


class InventoryAdjustment(PydanticBaseModel):
    """Inventory adjustment for a single product.

    Attributes:
        product_id: References Product to deduct inventory from
        quantity_used: Quantity to deduct from Product stock
        reason: Fixed reason code for inventory adjustment

    Example:
        ```python
        adjustment = InventoryAdjustment(
            product_id="prod_123",
            quantity_used=5,
            reason="order_fulfillment"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    product_id: str = Field(
        ...,
        description="References Product from product-config to deduct inventory from",
        alias="productId"
    )
    quantity_used: float = Field(
        ...,
        description="Quantity to deduct from Product stock quantity",
        alias="quantityUsed"
    )
    reason: Literal["order_fulfillment"] = Field(
        "order_fulfillment",
        description="Fixed reason code for inventory adjustment"
    )


class OrderInventoryUpdate(PydanticBaseModel):
    """Schema for inventory updates triggered by order fulfillment.

    Attributes:
        order_id: References ProductOrder that triggered this inventory update
        inventory_adjustments: Array of inventory deductions required

    Example:
        ```python
        inventory_update = OrderInventoryUpdate(
            order_id="order_123",
            inventory_adjustments=[
                InventoryAdjustment(
                    product_id="prod_456",
                    quantity_used=2,
                    reason="order_fulfillment"
                )
            ]
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    order_id: str = Field(
        ...,
        description="References ProductOrder that triggered this inventory update",
        alias="orderId"
    )
    inventory_adjustments: List[InventoryAdjustment] = Field(
        ...,
        description="Array of inventory deductions required to fulfill this Product Order",
        alias="inventoryAdjustments"
    )
