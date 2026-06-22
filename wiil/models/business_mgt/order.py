"""Shared order schema definitions used across business order models."""

import re
from typing import List, Optional

from pydantic import EmailStr, Field, field_validator

from wiil.models.base import Address, BaseModel
from wiil.models.type_definitions.business_definitions import (
    DiscountScope,
    DiscountType,
    PricingRuleAdjustmentType,
    PricingRuleApplyLevel,
    TaxRateType,
    TaxScope,
)

_TIME_PATTERN = re.compile(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
_DAY_PATTERN = re.compile(r"^[0-6]$")


class OrderAddress(Address):
    """Order address schema with delivery instructions."""

    delivery_instructions: Optional[str] = Field(
        None,
        alias="deliveryInstructions",
    )


class OrderCustomer(BaseModel):
    """Customer details associated with an order."""

    customer_id: Optional[str] = Field(None, alias="customerId")
    name: str = Field(..., min_length=1)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[OrderAddress] = None


class AppliedDiscount(BaseModel):
    """Applied discount breakdown entry."""

    discount_rule_id: Optional[str] = Field(None, alias="discountRuleId")
    external_discount_id: Optional[str] = Field(
        None,
        alias="externalDiscountId",
    )
    name: str = Field(..., min_length=1)
    code: Optional[str] = None
    scope: DiscountScope = DiscountScope.ORDER
    type: DiscountType
    value: float = Field(..., ge=0)
    discountable_amount: float = Field(..., ge=0, alias="discountableAmount")
    discount_amount: float = Field(..., ge=0, alias="discountAmount")
    is_stacked: bool = Field(False, alias="isStacked")


class AppliedPricingRule(BaseModel):
    """Applied pricing-rule breakdown entry."""

    pricing_rule_id: Optional[str] = Field(None, alias="pricingRuleId")
    external_pricing_rule_id: Optional[str] = Field(
        None,
        alias="externalPricingRuleId",
    )
    name: str = Field(..., min_length=1)
    apply_level: PricingRuleApplyLevel = Field(
        PricingRuleApplyLevel.ORDER,
        alias="applyLevel",
    )
    adjustment_type: PricingRuleAdjustmentType = Field(
        ...,
        alias="adjustmentType",
    )
    adjustment_value: float = Field(..., ge=0, alias="adjustmentValue")
    base_amount: float = Field(..., ge=0, alias="baseAmount")
    adjusted_amount: float = Field(..., ge=0, alias="adjustedAmount")
    delta_amount: float = Field(..., alias="deltaAmount")
    applied_at: Optional[int] = Field(None, ge=0, alias="appliedAt")


class AppliedTax(BaseModel):
    """Applied tax breakdown entry."""

    tax_rule_id: Optional[str] = Field(None, alias="taxRuleId")
    external_tax_id: Optional[str] = Field(None, alias="externalTaxId")
    name: str = Field(..., min_length=1)
    scope: TaxScope = TaxScope.ORDER
    rate_type: TaxRateType = Field(..., alias="rateType")
    rate_value: float = Field(..., ge=0, alias="rateValue")
    taxable_amount: float = Field(..., ge=0, alias="taxableAmount")
    tax_amount: float = Field(..., ge=0, alias="taxAmount")
    is_inclusive: bool = Field(False, alias="isInclusive")


class OrderPricing(BaseModel):
    """Comprehensive order pricing breakdown."""

    subtotal_before_tax: Optional[float] = Field(
        None,
        ge=0,
        alias="subtotalBeforeTax",
    )
    subtotal: float = Field(..., ge=0)
    applied_pricing_rules: List[AppliedPricingRule] = Field(
        default_factory=list,
        alias="appliedPricingRules",
    )
    total_pricing_adjustment_amount: float = Field(
        0,
        alias="totalPricingAdjustmentAmount",
    )
    subtotal_after_pricing_rules: Optional[float] = Field(
        None,
        ge=0,
        alias="subtotalAfterPricingRules",
    )
    applied_discounts: List[AppliedDiscount] = Field(
        default_factory=list,
        alias="appliedDiscounts",
    )
    total_discount_amount: float = Field(0, ge=0, alias="totalDiscountAmount")
    subtotal_after_discount: Optional[float] = Field(
        None,
        ge=0,
        alias="subtotalAfterDiscount",
    )
    applied_taxes: List[AppliedTax] = Field(
        default_factory=list,
        alias="appliedTaxes",
    )
    total_tax_amount: float = Field(0, ge=0, alias="totalTaxAmount")
    tax: float = Field(0, ge=0)
    tip: float = Field(0, ge=0)
    shipping_amount: float = Field(0, ge=0, alias="shippingAmount")
    discount: float = Field(0, ge=0)
    subtotal_after_tax: Optional[float] = Field(
        None,
        ge=0,
        alias="subtotalAfterTax",
    )
    total: float = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)


class MenuItemDaypart(BaseModel):
    """Time-based menu availability window."""

    name: str = Field(..., min_length=1)
    start_time: str = Field(..., alias="startTime")
    end_time: str = Field(..., alias="endTime")
    days_of_week: Optional[List[str]] = Field(None, alias="daysOfWeek")

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_time(cls, value: str) -> str:
        """Validate HH:MM time format."""
        if not _TIME_PATTERN.fullmatch(value):
            raise ValueError("Invalid time format (HH:MM)")
        return value

    @field_validator("days_of_week")
    @classmethod
    def validate_days_of_week(
        cls,
        value: Optional[List[str]],
    ) -> Optional[List[str]]:
        """Validate day strings are in the 0-6 range."""
        if value is None:
            return value
        for day in value:
            if not _DAY_PATTERN.fullmatch(day):
                raise ValueError("Day must be 0-6")
        return value


DEFAULT_MENU_ITEM_DAYPARTS: List[MenuItemDaypart] = [
    MenuItemDaypart(name="Breakfast", startTime="06:00", endTime="11:00"),
    MenuItemDaypart(name="Lunch", startTime="11:00", endTime="16:00"),
    MenuItemDaypart(name="Dinner", startTime="16:00", endTime="22:00"),
    MenuItemDaypart(name="Happy hour", startTime="15:00", endTime="18:00"),
]
