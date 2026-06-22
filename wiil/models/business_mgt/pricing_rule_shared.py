"""Shared pricing-rule schema definitions for menu and product pricing."""

from typing import List, Optional

from pydantic import Field, model_validator

from wiil.models.base import BaseModel
from wiil.models.type_definitions.business_definitions import (
    PricingChannel,
    PricingRuleAdjustmentType,
)


class PricingRuleChannelMapping(BaseModel):
    """Per-channel external pricing rule ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_pricing_rule_id: str = Field(..., alias="externalPricingRuleId")


class PricingRuleCommonCondition(BaseModel):
    """Common condition schema for pricing rules."""

    days_of_week: List[int] = Field(default_factory=list, alias="daysOfWeek")
    start_minute: Optional[int] = Field(
        None,
        ge=0,
        le=1439,
        alias="startMinute",
    )
    end_minute: Optional[int] = Field(
        None,
        ge=0,
        le=1439,
        alias="endMinute",
    )
    customer_segment_ids: Optional[List[str]] = Field(
        None,
        alias="customerSegmentIds",
    )
    channel: PricingChannel = PricingChannel.ALL

    @model_validator(mode="after")
    def validate_minute_window(self) -> "PricingRuleCommonCondition":
        """Ensure end_minute >= start_minute when both are provided."""
        if (
            self.start_minute is not None
            and self.end_minute is not None
            and self.end_minute < self.start_minute
        ):
            raise ValueError(
                "endMinute must be greater than or equal to startMinute"
            )
        return self


class PricingRuleAction(BaseModel):
    """Pricing-rule action schema."""

    adjustment_type: PricingRuleAdjustmentType = Field(
        ...,
        alias="adjustmentType",
    )
    adjustment_value: float = Field(..., ge=0, alias="adjustmentValue")
    currency: str = Field("USD", min_length=3, max_length=3)
    max_adjustment_amount: Optional[float] = Field(
        None,
        ge=0,
        alias="maxAdjustmentAmount",
    )
