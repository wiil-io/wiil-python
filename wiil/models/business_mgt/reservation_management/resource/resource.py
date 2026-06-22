"""Reservation resource schema definitions."""

from typing import Any, Literal, Optional, TypedDict, Union

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.bookings_shared import (
    ServiceBookingRules,
    ServiceDepositStrategy,
)
from wiil.models.business_mgt.reservation_management.resource.resource_instance import (  # noqa: E501
    ResourceInstanceAttribute,
    ResourceInstanceStatus,
)
from wiil.models.type_definitions.business_definitions import (
    ResourceReservationDurationUnit,
    ResourceType,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)


class ResourceChannelMapping(BaseModel):
    """Per-channel external resource mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_resource_id: str = Field(..., alias="externalResourceId")


class ResourceCapacityRange(BaseModel):
    """Range-based capacity config (tables)."""

    kind: Literal["range"] = "range"
    min: int = Field(..., gt=0)
    max: int = Field(..., gt=0)


class ResourceCapacityOccupancy(BaseModel):
    """Occupancy-based capacity config (rooms)."""

    kind: Literal["occupancy"] = "occupancy"
    standard: int = Field(..., gt=0)
    max: int = Field(..., gt=0)
    extra_fee: Optional[float] = Field(None, ge=0, alias="extraFee")


class ResourceCapacitySingle(BaseModel):
    """Single capacity config (rentals)."""

    kind: Literal["single"] = "single"
    value: int = Field(..., gt=0)
    weight_limit: Optional[float] = Field(None, gt=0, alias="weightLimit")
    skill_level: Optional[str] = Field(None, alias="skillLevel")


ResourceCapacity = Union[
    ResourceCapacityRange,
    ResourceCapacityOccupancy,
    ResourceCapacitySingle,
]


class ResourcePricingNone(BaseModel):
    """No-pricing strategy (tables)."""

    kind: Literal["none"] = "none"
    hold_policy: Optional[str] = Field(None, alias="holdPolicy")


class ResourceDayOfWeekRates(BaseModel):
    """Weekday rates for day-of-week pricing."""

    mon: float = Field(..., ge=0)
    tue: float = Field(..., ge=0)
    wed: float = Field(..., ge=0)
    thu: float = Field(..., ge=0)
    fri: float = Field(..., ge=0)
    sat: float = Field(..., ge=0)
    sun: float = Field(..., ge=0)


class ResourcePricingDayOfWeek(BaseModel):
    """Day-of-week pricing strategy (rooms)."""

    kind: Literal["dayOfWeek"] = "dayOfWeek"
    rates: ResourceDayOfWeekRates


class ResourcePricingTier(BaseModel):
    """Tier row used by tiered pricing strategy."""

    from_value: float = Field(..., ge=0, alias="from")
    to: Optional[float] = Field(None, ge=0)
    price: float = Field(..., ge=0)


class ResourcePricingTiered(BaseModel):
    """Tiered pricing strategy (rentals)."""

    kind: Literal["tiered"] = "tiered"
    tiers: list[ResourcePricingTier] = Field(..., min_length=1)


ResourcePricingStrategy = Union[
    ResourcePricingNone,
    ResourcePricingDayOfWeek,
    ResourcePricingTiered,
]


class ResourceAttribute(BaseModel):
    """Key-value attribute on resources."""

    key: str
    value: str


class ChecklistTemplateItem(BaseModel):
    """Checklist item used by resource workflows."""

    id: str
    label: str
    required: bool = True
    phase: Literal["pickup", "return", "both"] = "both"


class CreateResourceInstanceInput(BaseModel):
    """Inline instance input used when creating or updating a resource."""

    code: Optional[str] = None
    status: ResourceInstanceStatus = ResourceInstanceStatus.AVAILABLE
    name: Optional[str] = None
    location_id: Optional[str] = Field(None, alias="locationId")
    is_available: bool = Field(True, alias="isAvailable")
    attributes: Optional[list[ResourceInstanceAttribute]] = None
    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )


class Resource(EntityModel):
    """Reservation resource schema."""

    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_type: ResourceType = Field(..., alias="resourceType")
    category_id: Optional[str] = Field(None, alias="categoryId")
    name: str
    description: Optional[str] = None
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    capacity: Optional[int] = Field(None, gt=0)
    capacity_config: Optional[ResourceCapacity] = Field(
        None,
        alias="capacityConfig",
    )
    is_available: bool = Field(True, alias="isAvailable")
    channel_mappings: Optional[list[ResourceChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    location: Optional[str] = None
    amenities: list[str] = Field(default_factory=list)
    instances: Optional[list[str]] = None
    pricing: Optional[ResourcePricingStrategy] = None
    turnover_minutes: Optional[int] = Field(
        None,
        ge=0,
        alias="turnoverMinutes",
    )
    attributes: Optional[list[ResourceAttribute]] = None
    booking_rules: Optional[ServiceBookingRules] = Field(
        None,
        alias="bookingRules",
    )
    deposit_strategy: Optional[ServiceDepositStrategy] = Field(
        None,
        alias="depositStrategy",
    )
    reservation_duration: Optional[int] = Field(
        None,
        gt=0,
        alias="reservationDuration",
    )
    reservation_duration_unit: Optional[
        ResourceReservationDurationUnit
    ] = Field(
        None,
        alias="reservationDurationUnit",
    )
    checklist_template: list[ChecklistTemplateItem] = Field(
        default_factory=list,
        alias="checklistTemplate",
    )
    applicable_tier_ids: list[str] = Field(
        default_factory=list,
        alias="applicableTierIds",
    )
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    metadata: Optional[dict[str, Any]] = None

    @model_validator(mode="after")
    def validate_resource_configs(self) -> "Resource":
        if (
            self.capacity_config is not None
            and self.capacity_config.kind == "range"
            and self.capacity_config.max < self.capacity_config.min
        ):
            raise ValueError(
                "capacityConfig.max must be greater than or equal to "
                "capacityConfig.min"
            )
        if (
            self.capacity_config is not None
            and self.capacity_config.kind == "occupancy"
            and self.capacity_config.max < self.capacity_config.standard
        ):
            raise ValueError(
                "capacityConfig.max must be greater than or equal to "
                "capacityConfig.standard"
            )

        if self.resource_type == ResourceType.TABLE:
            if (
                self.capacity_config is not None
                and self.capacity_config.kind != "range"
            ):
                raise ValueError(
                    "Table resources must use capacityConfig.kind 'range'"
                )
            if self.pricing is not None and self.pricing.kind != "none":
                raise ValueError(
                    "Table resources must use pricing.kind 'none'"
                )

        if self.resource_type == ResourceType.ROOM:
            if (
                self.capacity_config is not None
                and self.capacity_config.kind != "occupancy"
            ):
                raise ValueError(
                    "Room resources must use capacityConfig.kind "
                    "'occupancy'"
                )
            if self.pricing is not None and self.pricing.kind != "dayOfWeek":
                raise ValueError(
                    "Room resources must use pricing.kind 'dayOfWeek'"
                )

        if self.resource_type == ResourceType.RENTAL:
            if (
                self.capacity_config is not None
                and self.capacity_config.kind != "single"
            ):
                raise ValueError(
                    "Rental resources must use capacityConfig.kind 'single'"
                )
            if self.pricing is not None and self.pricing.kind != "tiered":
                raise ValueError(
                    "Rental resources must use pricing.kind 'tiered'"
                )
        return self


class CreateResource(BaseModel):
    """Schema for creating resources."""

    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_type: ResourceType = Field(..., alias="resourceType")
    category_id: Optional[str] = Field(None, alias="categoryId")
    name: str
    description: Optional[str] = None
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    capacity: Optional[int] = Field(None, gt=0)
    capacity_config: Optional[ResourceCapacity] = Field(
        None,
        alias="capacityConfig",
    )
    is_available: bool = Field(True, alias="isAvailable")
    channel_mappings: Optional[list[ResourceChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    location: Optional[str] = None
    amenities: list[str] = Field(default_factory=list)
    instances: list[CreateResourceInstanceInput] = Field(
        default_factory=list,
    )
    pricing: Optional[ResourcePricingStrategy] = None
    turnover_minutes: Optional[int] = Field(
        None,
        ge=0,
        alias="turnoverMinutes",
    )
    attributes: Optional[list[ResourceAttribute]] = None
    booking_rules: Optional[ServiceBookingRules] = Field(
        None,
        alias="bookingRules",
    )
    deposit_strategy: Optional[ServiceDepositStrategy] = Field(
        None,
        alias="depositStrategy",
    )
    reservation_duration: Optional[int] = Field(
        None,
        gt=0,
        alias="reservationDuration",
    )
    reservation_duration_unit: Optional[
        ResourceReservationDurationUnit
    ] = Field(
        None,
        alias="reservationDurationUnit",
    )
    checklist_template: list[ChecklistTemplateItem] = Field(
        default_factory=list,
        alias="checklistTemplate",
    )
    applicable_tier_ids: list[str] = Field(
        default_factory=list,
        alias="applicableTierIds",
    )
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    metadata: Optional[dict[str, Any]] = None
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateResource(BaseModel):
    """Schema for updating resources."""

    id: str
    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_type: Optional[ResourceType] = Field(None, alias="resourceType")
    category_id: Optional[str] = Field(None, alias="categoryId")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")
    capacity: Optional[int] = Field(None, gt=0)
    capacity_config: Optional[ResourceCapacity] = Field(
        None,
        alias="capacityConfig",
    )
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    channel_mappings: Optional[list[ResourceChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    location: Optional[str] = None
    amenities: Optional[list[str]] = None
    instances: Optional[list[CreateResourceInstanceInput]] = None
    pricing: Optional[ResourcePricingStrategy] = None
    turnover_minutes: Optional[int] = Field(
        None,
        ge=0,
        alias="turnoverMinutes",
    )
    attributes: Optional[list[ResourceAttribute]] = None
    booking_rules: Optional[ServiceBookingRules] = Field(
        None,
        alias="bookingRules",
    )
    deposit_strategy: Optional[ServiceDepositStrategy] = Field(
        None,
        alias="depositStrategy",
    )
    reservation_duration: Optional[int] = Field(
        None,
        gt=0,
        alias="reservationDuration",
    )
    reservation_duration_unit: Optional[
        ResourceReservationDurationUnit
    ] = Field(
        None,
        alias="reservationDurationUnit",
    )
    checklist_template: Optional[list[ChecklistTemplateItem]] = Field(
        None,
        alias="checklistTemplate",
    )
    applicable_tier_ids: Optional[list[str]] = Field(
        None,
        alias="applicableTierIds",
    )
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    metadata: Optional[dict[str, Any]] = None
    placement: Optional[CreateDisplayOrderPlacement] = None


class ResourceInstanceRef(BaseModel):
    """Reference to a concrete resource instance."""

    id: str
    name: str


BusinessResourceCatalog = list[Resource]


class CapacityRangeFilter(TypedDict, total=False):
    """Capacity range filter."""

    min: Optional[int]
    max: Optional[int]


class PriceRangeFilter(TypedDict, total=False):
    """Price range filter."""

    min: Optional[float]
    max: Optional[float]


class ResourceFilters(TypedDict, total=False):
    """Filters for resource queries."""

    search: Optional[str]
    locationId: Optional[str]
    resourceType: Optional[list[ResourceType]]
    categoryId: Optional[str]
    isAvailable: Optional[bool]
    capacityRange: Optional[CapacityRangeFilter]
    location: Optional[str]
    amenities: Optional[list[str]]
    priceRange: Optional[PriceRangeFilter]


class ResourceSorting(TypedDict):
    """Sorting options for resource queries."""

    field: Literal["name", "capacity", "createdAt"]
    direction: Literal["asc", "desc"]


class ResourceQueryOptions(TypedDict, total=False):
    """Query options for resource retrieval."""

    page: int
    pageSize: int
    filters: Optional[ResourceFilters]
    sorting: Optional[ResourceSorting]
