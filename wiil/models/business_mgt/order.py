"""Shared order schema definitions used across menu and product orders.

This module contains common Pydantic models for order customer information,
pricing, and address details shared between menu and product orders.
"""

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, EmailStr, Field

from wiil.models.base import Address


class OrderAddress(Address):
    """Order address schema extending base address with delivery instructions.

    Extends the base Address model with delivery-specific instructions for
    couriers and delivery personnel.

    Attributes:
        delivery_instructions: Special delivery instructions (gate code, building entrance)

    Example:
        ```python
        address = OrderAddress(
            street="123 Main St",
            city="San Francisco",
            state="CA",
            postal_code="94102",
            country="USA",
            delivery_instructions="Ring doorbell, leave at front door"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    delivery_instructions: Optional[str] = Field(
        None,
        description="Special delivery instructions (gate code, building entrance, drop-off location)",
        alias="deliveryInstructions"
    )


class OrderCustomer(PydanticBaseModel):
    """Shared customer schema for orders.

    Customer information specific to an order, including contact details and
    optional customer ID reference.

    Attributes:
        customer_id: Customer ID if registered in the system
        name: Customer's full name
        phone: Customer's phone number
        email: Customer's email address
        address: Customer address for delivery/billing

    Example:
        ```python
        customer = OrderCustomer(
            customer_id="cust_123",
            name="John Doe",
            phone="+14155552671",
            email="john.doe@example.com",
            address=OrderAddress(
                street="456 Oak Ave",
                city="Oakland",
                state="CA",
                postal_code="94601",
                country="USA"
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    customer_id: Optional[str] = Field(
        None,
        description="References Customer ID if customer is registered in the system",
        alias="customerId"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="Customer's full name for order identification and communication"
    )
    phone: Optional[str] = Field(
        None,
        description="Customer's contact phone for order updates and delivery coordination"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Customer's email for digital receipts and order confirmations"
    )
    address: Optional[OrderAddress] = Field(
        None,
        description="Customer address for delivery or billing purposes"
    )


class OrderPricing(PydanticBaseModel):
    """Shared pricing schema for orders.

    Complete pricing breakdown including subtotal, taxes, fees, and discounts.

    Attributes:
        subtotal: Subtotal before tax and fees
        tax: Tax amount
        tip: Tip/gratuity amount
        shipping_amount: Shipping amount if applicable
        discount: Discount amount applied
        total: Final total amount
        currency: Currency code (ISO 4217 format)

    Example:
        ```python
        pricing = OrderPricing(
            subtotal=50.00,
            tax=4.50,
            tip=10.00,
            shipping_amount=5.00,
            discount=5.00,
            total=64.50,
            currency="USD"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    subtotal: float = Field(
        ...,
        ge=0,
        description="Sum of all item prices before tax, fees, or discounts"
    )
    tax: float = Field(
        0.0,
        ge=0,
        description="Calculated tax amount based on applicable tax rates"
    )
    tip: float = Field(
        0.0,
        ge=0,
        description="Gratuity amount for service staff (common in food service)"
    )
    shipping_amount: float = Field(
        0.0,
        ge=0,
        description="Shipping or delivery fee for product/menu orders",
        alias="shippingAmount"
    )
    discount: float = Field(
        0.0,
        ge=0,
        description="Total discount applied from promotions, coupons, or loyalty programs"
    )
    total: float = Field(
        ...,
        ge=0,
        description="Final amount due: subtotal + tax + tip + shipping - discount"
    )
    currency: str = Field(
        "USD",
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code (e.g., 'USD', 'EUR', 'GBP')"
    )
