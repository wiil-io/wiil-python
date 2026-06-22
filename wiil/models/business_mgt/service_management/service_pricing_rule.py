"""Service pricing rule schema with conditions and actions."""

from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.pricing_rule_shared import (
    PricingRuleAction,
    PricingRuleChannelMapping,
    PricingRuleCommonCondition,
)
from wiil.models.type_definitions.business_definitions import (
    PricingChannel,
    PricingRuleApplyLevel,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)


class ServicePricingRuleCondition(PricingRuleCommonCondition):
    """Condition shape specific to service pricing rules."""

    all_services: bool = Field(False, alias="allServices")
    service_ids_any: list[str] = Field(
        default_factory=list,
        alias="serviceIdsAny",
    )
    service_ids_all: list[str] = Field(
        default_factory=list,
        alias="serviceIdsAll",
    )


class ServicePricingRule(EntityModel):
    """Pricing rule for service appointments."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=120)
    apply_level: PricingRuleApplyLevel = Field(
        PricingRuleApplyLevel.ORDER,
        alias="applyLevel",
    )
    is_stackable: bool = Field(True, alias="isStackable")
    priority: int = Field(0, ge=0)
    channel_mappings: Optional[list[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    condition: ServicePricingRuleCondition = Field(
        default_factory=ServicePricingRuleCondition
    )
    action: PricingRuleAction
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")


class CreateServicePricingRule(BaseModel):
    """Schema for creating a service pricing rule."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=120)
    apply_level: PricingRuleApplyLevel = Field(
        PricingRuleApplyLevel.ORDER,
        alias="applyLevel",
    )
    is_stackable: bool = Field(True, alias="isStackable")
    priority: int = Field(0, ge=0)
    channel_mappings: Optional[list[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    condition: ServicePricingRuleCondition = Field(
        default_factory=ServicePricingRuleCondition
    )
    action: PricingRuleAction
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateServicePricingRule(BaseModel):
    """Schema for updating a service pricing rule."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    apply_level: Optional[PricingRuleApplyLevel] = Field(
        None,
        alias="applyLevel",
    )
    is_stackable: Optional[bool] = Field(None, alias="isStackable")
    priority: Optional[int] = Field(None, ge=0)
    channel_mappings: Optional[list[PricingRuleChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    condition: Optional[ServicePricingRuleCondition] = None
    action: Optional[PricingRuleAction] = None
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: Optional[bool] = Field(None, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None


class ServicePricingRuleFilters(TypedDict, total=False):
    """Filter options for service pricing rule queries."""

    search: Optional[str]
    location_id: Optional[str]
    apply_level: Optional[PricingRuleApplyLevel]
    channel: Optional[PricingChannel]
    is_stackable: Optional[bool]
    is_active: Optional[bool]


class ServicePricingRuleSorting(TypedDict):
    """Sorting options for service pricing rule queries."""

    field: Literal["name", "priority", "created_at"]
    direction: Literal["asc", "desc"]


class ServicePricingRuleQueryOptions(TypedDict, total=False):
    """Query options for service pricing rule retrieval."""

    page: int
    page_size: int
    filters: Optional[ServicePricingRuleFilters]
    sorting: Optional[ServicePricingRuleSorting]
