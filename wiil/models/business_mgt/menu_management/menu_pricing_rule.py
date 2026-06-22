"""Menu pricing rule schema definitions for menu-specific promotions."""

from typing import List, Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    PricingChannel,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement as CreateDisplayOrderPlacementSchema,
)


class PricingRuleChannelMapping(BaseModel):
    """Per-channel external pricing rule ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_pricing_rule_id: str = Field(..., alias="externalPricingRuleId")


class PricingRuleCommonCondition(BaseModel):
    """Common condition schema for pricing rules."""

    channel: PricingChannel = PricingChannel.ALL
    min_order_amount: Optional[float] = Field(
        None,
        ge=0,
        alias="minOrderAmount",
    )
    max_order_amount: Optional[float] = Field(
        None,
        ge=0,
        alias="maxOrderAmount",
    )
    customer_group_ids: Optional[List[str]] = Field(
        None,
        alias="customerGroupIds",
    )
    day_of_week: Optional[List[int]] = Field(None, alias="dayOfWeek")
    time_start: Optional[str] = Field(None, alias="timeStart")
    time_end: Optional[str] = Field(None, alias="timeEnd")


class MenuPricingRuleCondition(PricingRuleCommonCondition):
    """Menu-specific condition schema for pricing rules."""

    menu_set_id: str = Field(..., min_length=1, alias="menuSetId")
    menu_item_ids: Optional[List[str]] = Field(None, alias="menuItemIds")
    category_ids: Optional[List[str]] = Field(None, alias="categoryIds")


class MenuPricingRule(EntityModel):
    """Menu pricing rule schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None
    channel_mappings: Optional[List[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    discount_id: str = Field(..., min_length=1, alias="discountId")
    menu_set_revision_id: Optional[str] = Field(
        None,
        alias="menuSetRevisionId",
    )
    condition: MenuPricingRuleCondition
    effective_from: Optional[int] = Field(
        None,
        ge=0,
        alias="effectiveFrom",
    )
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_effective_window(self) -> "MenuPricingRule":
        """Ensure effective_to is >= effective_from when both are set."""
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to < self.effective_from
        ):
            raise ValueError(
                "effectiveTo must be greater than or equal to effectiveFrom"
            )
        return self


class CreateMenuPricingRule(BaseModel):
    """Schema for creating a new menu pricing rule."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None
    channel_mappings: Optional[List[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    discount_id: str = Field(..., min_length=1, alias="discountId")
    menu_set_revision_id: Optional[str] = Field(
        None,
        alias="menuSetRevisionId",
    )
    condition: MenuPricingRuleCondition
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacementSchema] = None


class UpdateMenuPricingRule(BaseModel):
    """Schema for updating an existing menu pricing rule."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None
    channel_mappings: Optional[List[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    discount_id: Optional[str] = Field(None, min_length=1, alias="discountId")
    menu_set_revision_id: Optional[str] = Field(
        None,
        alias="menuSetRevisionId",
    )
    condition: Optional[MenuPricingRuleCondition] = None
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    is_active: Optional[bool] = Field(None, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacementSchema] = None


class MenuPricingRuleFilters(TypedDict, total=False):
    """Filters for querying menu pricing rules."""

    search: Optional[str]
    location_id: Optional[str]
    channel: Optional[PricingChannel]
    menu_set_id: Optional[str]
    discount_id: Optional[str]
    is_active: Optional[bool]
    effective_at: Optional[int]


class MenuPricingRuleSorting(TypedDict):
    """Sorting options for menu pricing rule queries."""

    field: Literal["name", "created_at", "display_order"]
    direction: Literal["asc", "desc"]


class MenuPricingRuleQueryOptions(TypedDict, total=False):
    """Query options for menu pricing rule retrieval."""

    page: int
    page_size: int
    filters: Optional[MenuPricingRuleFilters]
    sorting: Optional[MenuPricingRuleSorting]
