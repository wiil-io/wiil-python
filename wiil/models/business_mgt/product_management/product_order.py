"""Product order schema definitions for retail and e-commerce orders."""

from typing import List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.order import OrderAddress, OrderPricing
from wiil.models.type_definitions.business_definitions import ExternalRef
from wiil.types.business_types import OrderStatus, PaymentStatus


class ProductOrderItemBase(BaseModel):
    """Base product order item schema (without productOrderId)."""

    product_id: str = Field(..., alias="productId")
    variant_id: Optional[str] = Field(None, alias="variantId")
    item_name: str = Field(..., alias="itemName")
    sku: Optional[str] = None
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0, alias="unitPrice")
    total_price: float = Field(..., ge=0, alias="totalPrice")
    selected_variant: Optional[str] = Field(None, alias="selectedVariant")
    warranty_info: Optional[str] = Field(None, alias="warrantyInfo")
    status: OrderStatus = OrderStatus.PENDING
    notes: Optional[str] = None


class ProductOrderItem(ProductOrderItemBase):
    """Product order item with IDs for existing items."""

    id: str
    product_order_id: str = Field(..., alias="productOrderId")


class ProductOrder(EntityModel):
    """Product order schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    terminal_id: Optional[str] = Field(None, alias="terminalId")
    operator_id: Optional[str] = Field(None, alias="operatorId")
    order_number: Optional[str] = Field(None, alias="orderNumber")

    status: OrderStatus = OrderStatus.PENDING
    items: List[ProductOrderItem] = Field(..., min_length=1)
    customer_id: str = Field(..., alias="customerId")
    pricing: OrderPricing

    payment_status: PaymentStatus = Field(
        PaymentStatus.PENDING,
        alias="paymentStatus",
    )
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    billing_address: Optional[OrderAddress] = Field(
        None,
        alias="billingAddress",
    )

    order_date: int = Field(..., alias="orderDate")
    requested_delivery_date: Optional[int] = Field(
        None,
        alias="requestedDeliveryDate",
    )
    shipped_date: Optional[int] = Field(None, alias="shippedDate")
    shipping_address: Optional[OrderAddress] = Field(
        None,
        alias="shippingAddress",
    )
    delivered_date: Optional[int] = Field(None, alias="deliveredDate")

    shipping_method: Optional[str] = Field(None, alias="shippingMethod")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    shipping_carrier: Optional[str] = Field(None, alias="shippingCarrier")

    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")
    source: str = "direct"
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
    )


class CreateProductOrder(BaseModel):
    """Schema for creating a product order."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    terminal_id: Optional[str] = Field(None, alias="terminalId")
    operator_id: Optional[str] = Field(None, alias="operatorId")

    status: OrderStatus = OrderStatus.PENDING
    items: List[ProductOrderItemBase] = Field(..., min_length=1)
    customer_id: str = Field(..., alias="customerId")
    pricing: OrderPricing

    payment_status: PaymentStatus = Field(
        PaymentStatus.PENDING,
        alias="paymentStatus",
    )
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    billing_address: Optional[OrderAddress] = Field(
        None,
        alias="billingAddress",
    )

    order_date: int = Field(..., alias="orderDate")
    requested_delivery_date: Optional[int] = Field(
        None,
        alias="requestedDeliveryDate",
    )
    shipping_address: Optional[OrderAddress] = Field(
        None,
        alias="shippingAddress",
    )
    shipping_method: Optional[str] = Field(None, alias="shippingMethod")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    shipping_carrier: Optional[str] = Field(None, alias="shippingCarrier")

    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")
    source: str = "direct"
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None


class UpdateProductOrder(BaseModel):
    """Schema for updating a product order."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    terminal_id: Optional[str] = Field(None, alias="terminalId")
    operator_id: Optional[str] = Field(None, alias="operatorId")

    status: Optional[OrderStatus] = None
    items: Optional[List[ProductOrderItemBase]] = Field(None, min_length=1)
    customer_id: Optional[str] = Field(None, alias="customerId")
    pricing: Optional[OrderPricing] = None

    payment_status: Optional[PaymentStatus] = Field(
        None,
        alias="paymentStatus",
    )
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    billing_address: Optional[OrderAddress] = Field(
        None,
        alias="billingAddress",
    )

    order_date: Optional[int] = Field(None, alias="orderDate")
    requested_delivery_date: Optional[int] = Field(
        None,
        alias="requestedDeliveryDate",
    )
    shipping_address: Optional[OrderAddress] = Field(
        None,
        alias="shippingAddress",
    )

    shipping_method: Optional[str] = Field(None, alias="shippingMethod")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")
    shipping_carrier: Optional[str] = Field(None, alias="shippingCarrier")

    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")
    source: Optional[str] = None
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None


class UpdateProductOrderStatus(BaseModel):
    """Quick status update schema for product orders."""

    id: str
    status: OrderStatus
    shipped_date: Optional[int] = Field(None, alias="shippedDate")
    delivered_date: Optional[int] = Field(None, alias="deliveredDate")
    tracking_number: Optional[str] = Field(None, alias="trackingNumber")


class InventoryAdjustment(BaseModel):
    """Inventory adjustment for a single product."""

    product_id: str = Field(..., alias="productId")
    quantity_used: float = Field(..., alias="quantityUsed")
    reason: Literal["order_fulfillment"] = "order_fulfillment"


class OrderInventoryUpdate(BaseModel):
    """Inventory updates triggered by order fulfillment."""

    order_id: str = Field(..., alias="orderId")
    inventory_adjustments: List[InventoryAdjustment] = Field(
        ...,
        alias="inventoryAdjustments",
    )


class DateRangeFilter(TypedDict, total=False):
    """Date range filter for product-order queries."""

    start: Optional[int]
    end: Optional[int]


class ProductOrderFilters(TypedDict, total=False):
    """Filters for querying product orders."""

    search: Optional[str]
    location_id: Optional[str]
    channel_id: Optional[str]
    terminal_id: Optional[str]
    operator_id: Optional[str]
    status: Optional[List[OrderStatus]]
    payment_status: Optional[List[PaymentStatus]]
    customer_id: Optional[str]
    shipping_method: Optional[str]
    source: Optional[str]
    external_source: Optional[str]
    date_range: Optional[DateRangeFilter]


class ProductOrderSorting(TypedDict):
    """Sorting options for product order queries."""

    field: Literal["order_date", "created_at", "total_amount"]
    direction: Literal["asc", "desc"]


class ProductOrderQueryOptions(TypedDict, total=False):
    """Query options for product order retrieval."""

    page: int
    page_size: int
    filters: Optional[ProductOrderFilters]
    sorting: Optional[ProductOrderSorting]
