"""Service provider join schema for service-to-provider assignments."""

from typing import Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class ServiceProvider(EntityModel):
    """Join record linking a service to a provider with optional overrides."""

    service_id: str = Field(..., alias="serviceId")
    provider_id: str = Field(..., alias="providerId")
    price_override: Optional[float] = Field(
        None,
        ge=0,
        alias="priceOverride",
    )
    duration_override: Optional[int] = Field(
        None,
        gt=0,
        alias="durationOverride",
    )
    active: bool = True


class CreateServiceProvider(BaseModel):
    """Schema for creating a service provider assignment."""

    service_id: str = Field(..., alias="serviceId")
    provider_id: str = Field(..., alias="providerId")
    price_override: Optional[float] = Field(
        None,
        ge=0,
        alias="priceOverride",
    )
    duration_override: Optional[int] = Field(
        None,
        gt=0,
        alias="durationOverride",
    )
    active: bool = True


class UpdateServiceProvider(BaseModel):
    """Schema for updating a service provider assignment."""

    id: str
    service_id: Optional[str] = Field(None, alias="serviceId")
    provider_id: Optional[str] = Field(None, alias="providerId")
    price_override: Optional[float] = Field(
        None,
        ge=0,
        alias="priceOverride",
    )
    duration_override: Optional[int] = Field(
        None,
        gt=0,
        alias="durationOverride",
    )
    active: Optional[bool] = None


class ServiceProviderFilters(TypedDict, total=False):
    """Filter options for service provider queries."""

    serviceId: Optional[str]
    active: Optional[bool]


class ServiceProviderSorting(TypedDict):
    """Sorting options for service provider queries."""

    field: str
    direction: str


class ServiceProviderQueryOptions(TypedDict, total=False):
    """Query options for service provider retrieval."""

    page: int
    pageSize: int
    filters: Optional[ServiceProviderFilters]
    sorting: Optional[ServiceProviderSorting]
