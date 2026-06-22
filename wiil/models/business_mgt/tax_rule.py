"""Tax rule schema definitions for order pricing."""

from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    TaxCatalogScope,
    TaxRateType,
    TaxScope,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)


class TaxRule(EntityModel):
    """Tax rule model."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=100)
    scope: TaxScope = TaxScope.ORDER
    rate_type: TaxRateType = Field(TaxRateType.PERCENTAGE, alias="rateType")
    rate_value: float = Field(..., ge=0, alias="rateValue")
    currency: str = Field("USD", min_length=3, max_length=3)
    catalog_scope: TaxCatalogScope = Field(
        TaxCatalogScope.ALL,
        alias="catalogScope",
    )
    external_tax_id: Optional[str] = Field(None, alias="externalTaxId")
    is_inclusive: bool = Field(False, alias="isInclusive")
    priority: int = Field(0, ge=0)
    is_compound: bool = Field(False, alias="isCompound")
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_tax_rule(self) -> "TaxRule":
        """Apply percentage and effective-window validation rules."""
        if self.rate_type == TaxRateType.PERCENTAGE and self.rate_value > 100:
            raise ValueError(
                "rateValue cannot exceed 100 for percentage taxes"
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


class CreateTaxRule(BaseModel):
    """Schema for creating a new tax rule."""

    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1, max_length=100)
    scope: TaxScope = TaxScope.ORDER
    rate_type: TaxRateType = Field(TaxRateType.PERCENTAGE, alias="rateType")
    rate_value: float = Field(..., ge=0, alias="rateValue")
    currency: str = Field("USD", min_length=3, max_length=3)
    catalog_scope: TaxCatalogScope = Field(
        TaxCatalogScope.ALL,
        alias="catalogScope",
    )
    external_tax_id: Optional[str] = Field(None, alias="externalTaxId")
    is_inclusive: bool = Field(False, alias="isInclusive")
    priority: int = Field(0, ge=0)
    is_compound: bool = Field(False, alias="isCompound")
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: bool = Field(True, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None

    @model_validator(mode="after")
    def validate_tax_rule(self) -> "CreateTaxRule":
        """Apply percentage and effective-window validation rules."""
        if self.rate_type == TaxRateType.PERCENTAGE and self.rate_value > 100:
            raise ValueError(
                "rateValue cannot exceed 100 for percentage taxes"
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


class UpdateTaxRule(BaseModel):
    """Schema for updating an existing tax rule."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    scope: Optional[TaxScope] = None
    rate_type: Optional[TaxRateType] = Field(None, alias="rateType")
    rate_value: Optional[float] = Field(None, ge=0, alias="rateValue")
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    catalog_scope: Optional[TaxCatalogScope] = Field(
        None,
        alias="catalogScope",
    )
    external_tax_id: Optional[str] = Field(None, alias="externalTaxId")
    is_inclusive: Optional[bool] = Field(None, alias="isInclusive")
    priority: Optional[int] = Field(None, ge=0)
    is_compound: Optional[bool] = Field(None, alias="isCompound")
    effective_from: Optional[int] = Field(None, ge=0, alias="effectiveFrom")
    effective_to: Optional[int] = Field(None, ge=0, alias="effectiveTo")
    is_active: Optional[bool] = Field(None, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None

    @model_validator(mode="after")
    def validate_tax_rule(self) -> "UpdateTaxRule":
        """Apply percentage and effective-window validation rules."""
        if (
            self.rate_type == TaxRateType.PERCENTAGE
            and self.rate_value is not None
        ):
            if self.rate_value > 100:
                raise ValueError(
                    "rateValue cannot exceed 100 for percentage taxes"
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


class TaxRuleFilters(TypedDict, total=False):
    """Filters for querying tax rules."""

    search: Optional[str]
    location_id: Optional[str]
    scope: Optional[TaxScope]
    rate_type: Optional[TaxRateType]
    catalog_scope: Optional[TaxCatalogScope]
    is_inclusive: Optional[bool]
    is_active: Optional[bool]


class TaxRuleSorting(TypedDict):
    """Sorting options for tax rule queries."""

    field: Literal["name", "priority", "rate_value", "created_at"]
    direction: Literal["asc", "desc"]


class TaxRuleQueryOptions(TypedDict, total=False):
    """Query options for tax rule retrieval."""

    page: int
    page_size: int
    filters: Optional[TaxRuleFilters]
    sorting: Optional[TaxRuleSorting]
