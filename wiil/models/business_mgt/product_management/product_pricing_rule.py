"""Product pricing-rule schema definitions."""

from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.pricing_rule_shared import (
    PricingRuleChannelMapping,
    PricingRuleCommonCondition,
)
from wiil.models.type_definitions.business_definitions import PricingChannel
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)


class ProductPricingRuleCondition(PricingRuleCommonCondition):
    """Common pricing condition extended with product set targeting."""

    product_set_id: str = Field(..., min_length=1, alias="productSetId")


class ProductPricingRule(EntityModel):
    """Product pricing rule schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=120)
    channel_mappings: Optional[list[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    discount_id: str = Field(..., min_length=1, alias="discountId")
    product_set_revision_id: Optional[str] = Field(
        None,
        alias="productSetRevisionId",
    )
    condition: ProductPricingRuleCondition
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_effective_window(self) -> "ProductPricingRule":
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


class CreateProductPricingRule(BaseModel):
    """Schema for creating a product pricing rule."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=120)
    channel_mappings: Optional[list[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    discount_id: str = Field(..., min_length=1, alias="discountId")
    product_set_revision_id: Optional[str] = Field(
        None,
        alias="productSetRevisionId",
    )
    condition: ProductPricingRuleCondition
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateProductPricingRule(BaseModel):
    """Schema for updating a product pricing rule."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    channel_mappings: Optional[list[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    discount_id: Optional[str] = Field(None, min_length=1, alias="discountId")
    product_set_revision_id: Optional[str] = Field(
        None,
        alias="productSetRevisionId",
    )
    condition: Optional[ProductPricingRuleCondition] = None
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: Optional[bool] = Field(None, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None


class ProductPricingRuleFilters(TypedDict, total=False):
    """Filters for querying product pricing rules."""

    search: Optional[str]
    location_id: Optional[str]
    channel: Optional[PricingChannel]
    is_active: Optional[bool]


class ProductPricingRuleSorting(TypedDict):
    """Sorting options for product pricing rule queries."""

    field: Literal["name", "created_at"]
    direction: Literal["asc", "desc"]


class ProductPricingRuleQueryOptions(TypedDict, total=False):
    """Query options for product pricing rule retrieval."""

    page: int
    page_size: int
    filters: Optional[ProductPricingRuleFilters]
    sorting: Optional[ProductPricingRuleSorting]
