"""Menu order schema definitions for restaurant/food service."""

from typing import List, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.order import OrderPricing
from wiil.models.business_mgt.menu_management.modifier import AppliedModifier
from wiil.models.type_definitions.business_definitions import (
    ExternalRef as ExternalRefModel,
)
from wiil.types.business_types import MenuOrderType, OrderStatus, PaymentStatus


class MenuItemCustomization(BaseModel):
    """Menu item customization with additional cost."""

    name: str
    value: str
    additional_cost: float = Field(0.0, ge=0, alias="additionalCost")


class MenuOrderItemBase(BaseModel):
    """Base menu order item schema (without IDs for creation)."""

    menu_item_id: str = Field(..., alias="menuItemId")
    variant_id: str = Field(..., alias="variantId")
    menu_set_id: Optional[str] = Field(None, alias="menuSetId")
    item_name: str = Field(..., alias="itemName")
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0, alias="unitPrice")
    total_price: float = Field(..., ge=0, alias="totalPrice")
    special_instructions: Optional[str] = Field(
        None,
        alias="specialInstructions",
    )
    customizations: Optional[List[MenuItemCustomization]] = None
    modifiers: Optional[List[AppliedModifier]] = None
    status: OrderStatus = OrderStatus.PENDING
    preparation_time: Optional[int] = Field(
        None,
        gt=0,
        alias="preparationTime",
    )
    notes: Optional[str] = None


class MenuOrderItem(MenuOrderItemBase):
    """Menu order item schema with IDs for existing items."""

    id: str
    menu_order_id: str = Field(..., alias="menuOrderId")


class DeliveryAddress(BaseModel):
    """Delivery address for DELIVERY type orders."""

    street: str
    city: Optional[str] = None
    postal_code: Optional[str] = Field(None, alias="postalCode")


class MenuOrder(EntityModel):
    """Menu order schema for restaurants/food service."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    terminal_id: Optional[str] = Field(None, alias="terminalId")
    operator_id: Optional[str] = Field(None, alias="operatorId")
    order_number: Optional[str] = Field(None, alias="orderNumber")

    type: MenuOrderType
    status: OrderStatus = OrderStatus.PENDING
    items: List[MenuOrderItem] = Field(..., min_length=1)
    customer_id: str = Field(..., alias="customerId")
    pricing: OrderPricing

    payment_status: PaymentStatus = Field(
        PaymentStatus.PENDING,
        alias="paymentStatus",
    )
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")

    order_date: int = Field(..., alias="orderDate")
    requested_time: Optional[int] = Field(None, alias="requestedTime")
    estimated_ready_time: Optional[int] = Field(
        None,
        alias="estimatedReadyTime",
    )
    actual_ready_time: Optional[int] = Field(None, alias="actualReadyTime")

    special_instructions: Optional[str] = Field(
        None,
        alias="specialInstructions",
    )
    allergies: Optional[List[str]] = None
    table_number: Optional[str] = Field(None, alias="tableNumber")

    external_ref: Optional[ExternalRefModel] = Field(None, alias="externalRef")
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
    )
    delivery_address: Optional[DeliveryAddress] = Field(
        None,
        alias="deliveryAddress",
    )
    shipping_address_id: Optional[str] = Field(None, alias="shippingAddressId")
    tip: Optional[float] = Field(None, ge=0)


class CreateMenuOrder(BaseModel):
    """Schema for creating a new menu order."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    terminal_id: Optional[str] = Field(None, alias="terminalId")
    operator_id: Optional[str] = Field(None, alias="operatorId")

    type: MenuOrderType
    status: OrderStatus = OrderStatus.PENDING
    items: List[MenuOrderItemBase] = Field(..., min_length=1)
    customer_id: str = Field(..., alias="customerId")
    pricing: OrderPricing

    payment_status: PaymentStatus = Field(
        PaymentStatus.PENDING,
        alias="paymentStatus",
    )
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")

    order_date: int = Field(..., alias="orderDate")
    requested_time: Optional[int] = Field(None, alias="requestedTime")
    estimated_ready_time: Optional[int] = Field(
        None,
        alias="estimatedReadyTime",
    )

    special_instructions: Optional[str] = Field(
        None,
        alias="specialInstructions",
    )
    allergies: Optional[List[str]] = None
    table_number: Optional[str] = Field(None, alias="tableNumber")

    external_ref: Optional[ExternalRefModel] = Field(None, alias="externalRef")
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None
    delivery_address: Optional[DeliveryAddress] = Field(
        None,
        alias="deliveryAddress",
    )
    shipping_address_id: Optional[str] = Field(None, alias="shippingAddressId")
    tip: Optional[float] = Field(None, ge=0)


class UpdateMenuOrder(BaseModel):
    """Schema for updating an existing menu order."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    terminal_id: Optional[str] = Field(None, alias="terminalId")
    operator_id: Optional[str] = Field(None, alias="operatorId")

    type: Optional[MenuOrderType] = None
    status: Optional[OrderStatus] = None
    items: Optional[List[MenuOrderItemBase]] = Field(None, min_length=1)
    customer_id: Optional[str] = Field(None, alias="customerId")
    pricing: Optional[OrderPricing] = None

    payment_status: Optional[PaymentStatus] = Field(
        None,
        alias="paymentStatus",
    )
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")

    order_date: Optional[int] = Field(None, alias="orderDate")
    requested_time: Optional[int] = Field(None, alias="requestedTime")
    estimated_ready_time: Optional[int] = Field(
        None,
        alias="estimatedReadyTime",
    )

    special_instructions: Optional[str] = Field(
        None,
        alias="specialInstructions",
    )
    allergies: Optional[List[str]] = None
    table_number: Optional[str] = Field(None, alias="tableNumber")

    external_ref: Optional[ExternalRefModel] = Field(None, alias="externalRef")
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None
    delivery_address: Optional[DeliveryAddress] = Field(
        None,
        alias="deliveryAddress",
    )
    shipping_address_id: Optional[str] = Field(None, alias="shippingAddressId")
    tip: Optional[float] = Field(None, ge=0)


class UpdateMenuOrderStatus(BaseModel):
    """Quick status update schema for menu orders."""

    id: str
    status: OrderStatus
    estimated_ready_time: Optional[int] = Field(
        None,
        alias="estimatedReadyTime",
    )
    actual_ready_time: Optional[int] = Field(None, alias="actualReadyTime")


class MenuOrderPricingPreview(BaseModel):
    """Validation/preview result for menu-order pricing calculations."""

    success: bool
    items: List[MenuOrderItemBase]
    pricing: Optional[OrderPricing]
    errors: List[str]
    warnings: List[str]


class DateRangeFilter(TypedDict, total=False):
    """Date range filter for menu order queries."""

    start: Optional[int]
    end: Optional[int]


class MenuOrderFilters(TypedDict, total=False):
    """Filters for querying menu orders."""

    search: Optional[str]
    location_id: Optional[str]
    channel_id: Optional[str]
    terminal_id: Optional[str]
    operator_id: Optional[str]
    type: Optional[List[MenuOrderType]]
    status: Optional[List[OrderStatus]]
    payment_status: Optional[List[PaymentStatus]]
    customer_id: Optional[str]
    table_number: Optional[str]
    external_source: Optional[str]
    date_range: Optional[DateRangeFilter]


class MenuOrderSorting(TypedDict):
    """Sorting options for menu order queries."""

    field: Literal["order_date", "created_at", "total_amount"]
    direction: Literal["asc", "desc"]


class MenuOrderQueryOptions(TypedDict, total=False):
    """Query options for menu order retrieval."""

    page: int
    page_size: int
    filters: Optional[MenuOrderFilters]
    sorting: Optional[MenuOrderSorting]
