"""Menu order schema definitions for restaurant/food service.

This module contains Pydantic models for managing menu orders, order items,
and order status updates for restaurant and food service operations.
"""

from typing import List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.business_mgt.order import OrderCustomer, OrderPricing
from wiil.types.business_types import MenuOrderType, OrderStatus, PaymentStatus


class MenuItemCustomization(PydanticBaseModel):
    """Menu item customization with additional cost.

    Attributes:
        name: Customization option name (e.g., 'Extra Cheese')
        value: Selected customization value or specification
        additional_cost: Extra charge for this customization

    Example:
        ```python
        customization = MenuItemCustomization(
            name="Extra Cheese",
            value="Yes",
            additional_cost=2.50
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., description="Customization option name")
    value: str = Field(..., description="Selected customization value or specification")
    additional_cost: float = Field(
        0.0,
        ge=0,
        description="Extra charge for this customization",
        alias="additionalCost"
    )


class MenuOrderItemBase(PydanticBaseModel):
    """Base menu order item schema (without IDs for creation).

    Order line item for a menu item with quantity, pricing, and customizations.

    Attributes:
        menu_item_id: Menu item ID being ordered
        item_name: Name of the menu item
        quantity: Quantity ordered
        unit_price: Price per unit
        total_price: Total price for this item
        special_instructions: Special preparation instructions
        customizations: Item customizations with additional costs
        status: Item status
        preparation_time: Estimated prep time in minutes
        notes: Additional notes

    Example:
        ```python
        item = MenuOrderItemBase(
            menu_item_id="item_123",
            item_name="Grilled Salmon",
            quantity=2,
            unit_price=24.99,
            total_price=49.98,
            special_instructions="Well done",
            status=OrderStatus.PENDING
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    menu_item_id: str = Field(
        ...,
        description="References MenuItem from menu-config that is being ordered",
        alias="menuItemId"
    )
    item_name: str = Field(
        ...,
        description="Display name of the menu item captured at order time",
        alias="itemName"
    )
    quantity: int = Field(
        ...,
        gt=0,
        description="Number of units ordered for this menu item"
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
        description="Total price for this line item: unitPrice × quantity + customization costs",
        alias="totalPrice"
    )
    special_instructions: Optional[str] = Field(
        None,
        description="Customer's special preparation requests (e.g., 'no onions', 'extra sauce')",
        alias="specialInstructions"
    )
    customizations: Optional[List[MenuItemCustomization]] = Field(
        None,
        description="Item customizations with pricing"
    )
    status: OrderStatus = Field(
        OrderStatus.PENDING,
        description="Current preparation status of this individual item"
    )
    preparation_time: Optional[int] = Field(
        None,
        gt=0,
        description="Estimated preparation time in minutes for this specific item",
        alias="preparationTime"
    )
    notes: Optional[str] = Field(
        None,
        description="Internal notes about this item for kitchen or service staff"
    )


class MenuOrderItem(MenuOrderItemBase):
    """Menu order item schema with IDs (for existing items).

    Extends MenuOrderItemBase with unique identifiers for persisted items.

    Attributes:
        id: Unique identifier for this menu order item instance
        menu_order_id: References parent MenuOrder this item belongs to

    Example:
        ```python
        item = MenuOrderItem(
            id="order_item_123",
            menu_order_id="order_456",
            menu_item_id="item_789",
            item_name="Caesar Salad",
            quantity=1,
            unit_price=12.99,
            total_price=12.99,
            status=OrderStatus.PREPARING
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for this menu order item instance")
    menu_order_id: str = Field(
        ...,
        description="References parent MenuOrder this item belongs to",
        alias="menuOrderId"
    )


class DeliveryAddress(PydanticBaseModel):
    """Delivery address for menu orders.

    Attributes:
        street: Delivery street address
        city: Delivery city
        postal_code: Delivery postal code

    Example:
        ```python
        address = DeliveryAddress(
            street="123 Main St",
            city="San Francisco",
            postal_code="94102"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    street: str = Field(..., description="Delivery street address for DELIVERY type orders")
    city: Optional[str] = Field(None, description="Delivery city for regional routing")
    postal_code: Optional[str] = Field(
        None,
        description="Delivery postal code for address validation",
        alias="postalCode"
    )


class MenuOrder(BaseModel):
    """Menu order schema - for restaurants/food service.

    Complete menu order with items, customer information, pricing, and fulfillment details.

    Attributes:
        order_number: Human-readable order number
        type: Order type (dine-in, takeout, delivery)
        status: Current order status
        items: Items in the order
        customer_id: ID of the customer placing the order
        customer: Customer information
        pricing: Pricing details
        payment_status: Payment status
        payment_method: Payment method used
        payment_reference: Payment reference number
        order_date: Order date as Unix timestamp
        requested_time: Requested pickup/delivery time
        estimated_ready_time: Estimated ready time
        actual_ready_time: Actual ready time
        special_instructions: Special instructions
        allergies: Customer allergies
        table_number: Table number for dine-in
        external_order_id: External order ID for integrations
        source: Order source
        cancel_reason: Reason for cancellation
        notes: Additional notes
        service_conversation_config_id: Service conversation config ID
        delivery_address: Delivery address if applicable

    Example:
        ```python
        order = MenuOrder(
            id="order_123",
            order_number="A-42",
            type=MenuOrderType.DELIVERY,
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
    type: MenuOrderType = Field(
        ...,
        description="Order fulfillment type: DINE_IN, TAKEOUT, or DELIVERY"
    )
    status: OrderStatus = Field(
        OrderStatus.PENDING,
        description="Current order status tracking progression from placement to fulfillment"
    )
    items: List[MenuOrderItem] = Field(
        ...,
        min_length=1,
        description="Menu items in this order with quantities, pricing, and customizations"
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
        description="Complete pricing breakdown including subtotal, tax, tip, and fees"
    )
    payment_status: PaymentStatus = Field(
        PaymentStatus.PENDING,
        description="Payment processing status",
        alias="paymentStatus"
    )
    payment_method: Optional[str] = Field(
        None,
        description="Payment method used (e.g., 'credit_card', 'cash', 'digital_wallet')",
        alias="paymentMethod"
    )
    payment_reference: Optional[str] = Field(
        None,
        description="External payment system reference or transaction ID",
        alias="paymentReference"
    )
    order_date: int = Field(
        ...,
        description="Unix timestamp when order was placed",
        alias="orderDate"
    )
    requested_time: Optional[int] = Field(
        None,
        description="Unix timestamp for customer's requested pickup or delivery time",
        alias="requestedTime"
    )
    estimated_ready_time: Optional[int] = Field(
        None,
        description="Unix timestamp when kitchen estimates order will be ready",
        alias="estimatedReadyTime"
    )
    actual_ready_time: Optional[int] = Field(
        None,
        description="Unix timestamp when order was actually completed and ready",
        alias="actualReadyTime"
    )
    special_instructions: Optional[str] = Field(
        None,
        description="Order-level special instructions from customer",
        alias="specialInstructions"
    )
    allergies: Optional[List[str]] = Field(
        None,
        description="Customer's allergy information for this order"
    )
    table_number: Optional[str] = Field(
        None,
        description="Table number for DINE_IN orders",
        alias="tableNumber"
    )
    external_order_id: Optional[str] = Field(
        None,
        description="Order ID from external system (third-party delivery platform, POS system)",
        alias="externalOrderId"
    )
    source: str = Field(
        "direct",
        description="Order source channel (e.g., 'direct', 'web', 'phone', 'third_party_platform')"
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
    delivery_address: Optional[DeliveryAddress] = Field(
        None,
        description="Delivery address for DELIVERY type orders",
        alias="deliveryAddress"
    )


class CreateMenuOrder(BaseModel):
    """Schema for creating a new menu order.

    Omits auto-generated fields and uses base items without IDs.

    Example:
        ```python
        create_data = CreateMenuOrder(
            type=MenuOrderType.TAKEOUT,
            items=[MenuOrderItemBase(...)],
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

    type: MenuOrderType
    status: OrderStatus = OrderStatus.PENDING
    items: List[MenuOrderItemBase] = Field(..., min_length=1)
    customer_id: str = Field(..., alias="customerId")
    pricing: OrderPricing
    payment_status: PaymentStatus = Field(PaymentStatus.PENDING, alias="paymentStatus")
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    order_date: int = Field(..., alias="orderDate")
    requested_time: Optional[int] = Field(None, alias="requestedTime")
    estimated_ready_time: Optional[int] = Field(None, alias="estimatedReadyTime")
    special_instructions: Optional[str] = Field(None, alias="specialInstructions")
    allergies: Optional[List[str]] = None
    table_number: Optional[str] = Field(None, alias="tableNumber")
    external_order_id: Optional[str] = Field(None, alias="externalOrderId")
    source: str = "direct"
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None
    delivery_address: Optional[DeliveryAddress] = Field(None, alias="deliveryAddress")


class UpdateMenuOrder(BaseModel):
    """Schema for updating an existing menu order.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateMenuOrder(
            id="order_123",
            status=OrderStatus.PREPARING,
            estimated_ready_time=1234567999
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    type: Optional[MenuOrderType] = None
    status: Optional[OrderStatus] = None
    items: Optional[List[MenuOrderItemBase]] = Field(None, min_length=1)
    customer_id: Optional[str] = Field(None, alias="customerId")
    pricing: Optional[OrderPricing] = None
    payment_status: Optional[PaymentStatus] = Field(None, alias="paymentStatus")
    payment_method: Optional[str] = Field(None, alias="paymentMethod")
    payment_reference: Optional[str] = Field(None, alias="paymentReference")
    order_date: Optional[int] = Field(None, alias="orderDate")
    requested_time: Optional[int] = Field(None, alias="requestedTime")
    estimated_ready_time: Optional[int] = Field(None, alias="estimatedReadyTime")
    special_instructions: Optional[str] = Field(None, alias="specialInstructions")
    allergies: Optional[List[str]] = None
    table_number: Optional[str] = Field(None, alias="tableNumber")
    external_order_id: Optional[str] = Field(None, alias="externalOrderId")
    source: Optional[str] = None
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    notes: Optional[str] = None
    delivery_address: Optional[DeliveryAddress] = Field(None, alias="deliveryAddress")


class UpdateMenuOrderStatus(PydanticBaseModel):
    """Quick status update schema for menu orders.

    Simplified schema for updating just the order status and timing fields.

    Attributes:
        id: Unique identifier of the MenuOrder to update
        status: New order status
        estimated_ready_time: Updated Unix timestamp for estimated completion
        actual_ready_time: Unix timestamp when order was actually completed

    Example:
        ```python
        status_update = UpdateMenuOrderStatus(
            id="order_123",
            status=OrderStatus.READY,
            actual_ready_time=1234567999
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier of the MenuOrder to update status for")
    status: OrderStatus = Field(
        ...,
        description="New order status to transition to"
    )
    estimated_ready_time: Optional[int] = Field(
        None,
        description="Updated Unix timestamp for estimated completion",
        alias="estimatedReadyTime"
    )
    actual_ready_time: Optional[int] = Field(
        None,
        description="Unix timestamp when order was actually completed",
        alias="actualReadyTime"
    )
