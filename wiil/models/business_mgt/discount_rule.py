"""Discount rule schema definitions for order pricing."""

from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    DiscountCatalogScope,
    DiscountScope,
    DiscountType,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)


class DiscountRule(EntityModel):
    """Discount rule model."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=100)
    code: Optional[str] = None
    scope: DiscountScope = DiscountScope.ORDER
    type: DiscountType = DiscountType.PERCENTAGE
    value: float = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    catalog_scope: DiscountCatalogScope = Field(
        DiscountCatalogScope.ALL,
        alias="catalogScope",
    )
    external_discount_id: Optional[str] = Field(
        None,
        alias="externalDiscountId",
    )
    min_subtotal: Optional[float] = Field(None, ge=0, alias="minSubtotal")
    customer_segment: Optional[str] = Field(None, alias="customerSegment")
    first_order_only: bool = Field(False, alias="firstOrderOnly")
    max_uses: Optional[int] = Field(None, gt=0, alias="maxUses")
    max_uses_per_customer: Optional[int] = Field(
        None,
        gt=0,
        alias="maxUsesPerCustomer",
    )
    is_stackable: bool = Field(True, alias="isStackable")
    priority: int = Field(0, ge=0)
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_discount_rule(self) -> "DiscountRule":
        """Apply percentage and effective-window validation rules."""
        if self.type == DiscountType.PERCENTAGE and self.value > 100:
            raise ValueError(
                "value cannot exceed 100 for percentage discounts"
            )
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to < self.effective_from
        ):
            raise ValueError(
                "effectiveTo must be greater than or equal to effectiveFrom"
            )
        return self


class CreateDiscountRule(BaseModel):
    """Schema for creating a new discount rule."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=100)
    code: Optional[str] = None
    scope: DiscountScope = DiscountScope.ORDER
    type: DiscountType = DiscountType.PERCENTAGE
    value: float = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    catalog_scope: DiscountCatalogScope = Field(
        DiscountCatalogScope.ALL,
        alias="catalogScope",
    )
    external_discount_id: Optional[str] = Field(
        None,
        alias="externalDiscountId",
    )
    min_subtotal: Optional[float] = Field(None, ge=0, alias="minSubtotal")
    customer_segment: Optional[str] = Field(None, alias="customerSegment")
    first_order_only: bool = Field(False, alias="firstOrderOnly")
    max_uses: Optional[int] = Field(None, gt=0, alias="maxUses")
    max_uses_per_customer: Optional[int] = Field(
        None,
        gt=0,
        alias="maxUsesPerCustomer",
    )
    is_stackable: bool = Field(True, alias="isStackable")
    priority: int = Field(0, ge=0)
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None

    @model_validator(mode="after")
    def validate_discount_rule(self) -> "CreateDiscountRule":
        """Apply percentage and effective-window validation rules."""
        if self.type == DiscountType.PERCENTAGE and self.value > 100:
            raise ValueError(
                "value cannot exceed 100 for percentage discounts"
            )
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to < self.effective_from
        ):
            raise ValueError(
                "effectiveTo must be greater than or equal to effectiveFrom"
            )
        return self


class UpdateDiscountRule(BaseModel):
    """Schema for updating an existing discount rule."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = None
    scope: Optional[DiscountScope] = None
    type: Optional[DiscountType] = None
    value: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    catalog_scope: Optional[DiscountCatalogScope] = Field(
        None,
        alias="catalogScope",
    )
    external_discount_id: Optional[str] = Field(
        None,
        alias="externalDiscountId",
    )
    min_subtotal: Optional[float] = Field(None, ge=0, alias="minSubtotal")
    customer_segment: Optional[str] = Field(None, alias="customerSegment")
    first_order_only: Optional[bool] = Field(None, alias="firstOrderOnly")
    max_uses: Optional[int] = Field(None, gt=0, alias="maxUses")
    max_uses_per_customer: Optional[int] = Field(
        None,
        gt=0,
        alias="maxUsesPerCustomer",
    )
    is_stackable: Optional[bool] = Field(None, alias="isStackable")
    priority: Optional[int] = Field(None, ge=0)
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: Optional[bool] = Field(None, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None

    @model_validator(mode="after")
    def validate_discount_rule(self) -> "UpdateDiscountRule":
        """Apply percentage and effective-window validation rules."""
        if self.type == DiscountType.PERCENTAGE and self.value is not None:
            if self.value > 100:
                raise ValueError(
                    "value cannot exceed 100 for percentage discounts"
                )
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to < self.effective_from
        ):
            raise ValueError(
                "effectiveTo must be greater than or equal to effectiveFrom"
            )
        return self


class DiscountRuleFilters(TypedDict, total=False):
    """Filters for querying discount rules."""

    search: Optional[str]
    location_id: Optional[str]
    code: Optional[str]
    scope: Optional[DiscountScope]
    type: Optional[DiscountType]
    catalog_scope: Optional[DiscountCatalogScope]
    is_stackable: Optional[bool]
    is_active: Optional[bool]


class DiscountRuleSorting(TypedDict):
    """Sorting options for discount rule queries."""

    field: Literal["name", "priority", "value", "created_at"]
    direction: Literal["asc", "desc"]


class DiscountRuleQueryOptions(TypedDict, total=False):
    """Query options for discount rule retrieval."""

    page: int
    page_size: int
    filters: Optional[DiscountRuleFilters]
    sorting: Optional[DiscountRuleSorting]
