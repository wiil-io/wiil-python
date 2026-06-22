"""Business service configuration schema definitions."""

from enum import Enum
from typing import Optional

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.business_mgt.bookings_shared import (
    ServiceBookingRules,
    ServiceDepositStrategy,
)
from wiil.models.type_definitions.business_definitions import (
    SimpleWeeklySchedule,
    validate_simple_weekly_schedule,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)
from wiil.models.type_definitions.dynamic_fields import (
    FieldDefinition,
    FieldOverride,
)


class ServicePriceMode(str, Enum):
    """Service pricing mode options."""

    FIXED = "FIXED"
    STARTS_AT = "STARTS_AT"
    VARIABLE = "VARIABLE"


class ServiceGratuityMode(str, Enum):
    """Service gratuity mode options."""

    NONE = "NONE"
    OPTIONAL = "OPTIONAL"
    REQUIRED = "REQUIRED"


class ServiceAvailabilityMode(str, Enum):
    """Service availability mode options."""

    ALWAYS = "ALWAYS"
    SCHEDULED = "SCHEDULED"
    INHERIT = "INHERIT"


class ServiceCategoryChannelMapping(BaseModel):
    """Per-channel service category ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_category_id: str = Field(..., alias="externalCategoryId")


class ServiceChannelMapping(BaseModel):
    """Per-channel service ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_service_id: str = Field(..., alias="externalServiceId")
    external_category_id: Optional[str] = Field(
        None,
        alias="externalCategoryId",
    )


class ServiceDurationSegments(BaseModel):
    """Service duration segments for different phases."""

    prep: int = Field(0, ge=0)
    active: int = Field(60, gt=0)
    processing: int = Field(0, ge=0)
    finish: int = Field(0, ge=0)
    turnover: int = Field(0, ge=0)


class ServiceDateRange(BaseModel):
    """Date range for service availability or exclusion."""

    start_date: str = Field(..., alias="startDate")
    end_date: str = Field(..., alias="endDate")
    is_exclusion: bool = Field(False, alias="isExclusion")


class ServiceAvailability(BaseModel):
    """Service availability configuration."""

    mode: ServiceAvailabilityMode = ServiceAvailabilityMode.INHERIT
    weekly_schedule: Optional[SimpleWeeklySchedule] = Field(
        None,
        alias="weeklySchedule",
    )
    date_ranges: Optional[list[ServiceDateRange]] = Field(
        None,
        alias="dateRanges",
    )

    @model_validator(mode="after")
    def validate_scheduled_mode(self) -> "ServiceAvailability":
        """Require weekly schedule in SCHEDULED mode."""
        if (
            self.mode == ServiceAvailabilityMode.SCHEDULED
            and self.weekly_schedule is None
        ):
            raise ValueError(
                "weeklySchedule is required when mode is SCHEDULED"
            )

        if self.weekly_schedule is not None:
            validate_simple_weekly_schedule(self.weekly_schedule)

        return self


class ServiceAppointmentFieldConfig(BaseModel):
    """Service-level appointment field configuration."""

    inherited_field_keys: list[str] = Field(
        default_factory=list,
        alias="inheritedFieldKeys",
    )
    field_overrides: list[FieldOverride] = Field(
        default_factory=list,
        alias="fieldOverrides",
    )
    additional_fields: list[FieldDefinition] = Field(
        default_factory=list,
        alias="additionalFields",
    )
    is_active: bool = Field(True, alias="isActive")
    reuse_details: bool = Field(False, alias="reuseDetails")


class ServiceCategory(EntityModel):
    """Service category schema."""

    service_revision_id: Optional[str] = Field(
        None,
        alias="serviceRevisionId",
    )
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    channel_mappings: Optional[list[ServiceCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")


class CreateServiceCategory(BaseModel):
    """Schema for creating a service category."""

    service_revision_id: Optional[str] = Field(
        None,
        alias="serviceRevisionId",
    )
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    channel_mappings: Optional[list[ServiceCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateServiceCategory(BaseModel):
    """Schema for updating a service category."""

    id: str
    service_revision_id: Optional[str] = Field(
        None,
        alias="serviceRevisionId",
    )
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    channel_mappings: Optional[list[ServiceCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: Optional[bool] = Field(None, alias="isActive")
    placement: Optional[CreateDisplayOrderPlacement] = None


class BusinessServiceConfig(EntityModel):
    """Business service configuration schema."""

    service_revision_id: Optional[str] = Field(
        None,
        alias="serviceRevisionId",
    )
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    category_id: Optional[str] = Field(None, alias="categoryId")
    booking_code: Optional[str] = Field(None, alias="bookingCode")
    duration: int = Field(60, gt=0, le=480)
    duration_segments: Optional[ServiceDurationSegments] = Field(
        None,
        alias="durationSegments",
    )
    buffer_before: int = Field(0, ge=0, alias="bufferBefore")
    buffer_after: int = Field(0, ge=0, alias="bufferAfter")
    is_bookable: bool = Field(True, alias="isBookable")
    allows_processing_chair_swap: Optional[bool] = Field(
        None,
        alias="allowsProcessingChairSwap",
    )
    service_availability: Optional[ServiceAvailability] = Field(
        None,
        alias="serviceAvailability",
    )
    max_concurrent_bookings: Optional[int] = Field(
        None,
        gt=0,
        alias="maxConcurrentBookings",
    )
    base_price: float = Field(0, ge=0, alias="basePrice")
    price_mode: Optional[ServicePriceMode] = Field(None, alias="priceMode")
    gratuity_mode: Optional[ServiceGratuityMode] = Field(
        None,
        alias="gratuityMode",
    )
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[list[ServiceChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    primary_service_user_account_id: Optional[str] = Field(
        None,
        alias="primaryServiceUserAccountId",
    )
    required_resources: list[str] = Field(
        default_factory=list,
        alias="requiredResources",
    )
    booking_rules: Optional[ServiceBookingRules] = Field(
        None,
        alias="bookingRules",
    )
    deposit_strategy: Optional[ServiceDepositStrategy] = Field(
        None,
        alias="depositStrategy",
    )
    deposit_value: Optional[float] = Field(None, ge=0, alias="depositValue")
    late_cancel_fee_percent: float = Field(
        0,
        ge=0,
        le=100,
        alias="lateCancelFeePercent",
    )
    no_show_fee_percent: float = Field(
        0,
        ge=0,
        le=100,
        alias="noShowFeePercent",
    )
    required_datafield_config: Optional[ServiceAppointmentFieldConfig] = Field(
        None,
        alias="requiredDatafieldConfig",
    )


class CreateBusinessService(BaseModel):
    """Schema for creating a business service."""

    service_revision_id: Optional[str] = Field(
        None,
        alias="serviceRevisionId",
    )
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    category_id: Optional[str] = Field(None, alias="categoryId")
    booking_code: Optional[str] = Field(None, alias="bookingCode")
    duration: int = Field(60, gt=0, le=480)
    duration_segments: Optional[ServiceDurationSegments] = Field(
        None,
        alias="durationSegments",
    )
    buffer_before: int = Field(0, ge=0, alias="bufferBefore")
    buffer_after: int = Field(0, ge=0, alias="bufferAfter")
    is_bookable: bool = Field(True, alias="isBookable")
    allows_processing_chair_swap: Optional[bool] = Field(
        None,
        alias="allowsProcessingChairSwap",
    )
    service_availability: Optional[ServiceAvailability] = Field(
        None,
        alias="serviceAvailability",
    )
    max_concurrent_bookings: Optional[int] = Field(
        None,
        gt=0,
        alias="maxConcurrentBookings",
    )
    base_price: float = Field(0, ge=0, alias="basePrice")
    price_mode: Optional[ServicePriceMode] = Field(None, alias="priceMode")
    gratuity_mode: Optional[ServiceGratuityMode] = Field(
        None,
        alias="gratuityMode",
    )
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[list[ServiceChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    primary_service_user_account_id: Optional[str] = Field(
        None,
        alias="primaryServiceUserAccountId",
    )
    required_resources: list[str] = Field(
        default_factory=list,
        alias="requiredResources",
    )
    booking_rules: Optional[ServiceBookingRules] = Field(
        None,
        alias="bookingRules",
    )
    deposit_strategy: Optional[ServiceDepositStrategy] = Field(
        None,
        alias="depositStrategy",
    )
    deposit_value: Optional[float] = Field(None, ge=0, alias="depositValue")
    late_cancel_fee_percent: float = Field(
        0,
        ge=0,
        le=100,
        alias="lateCancelFeePercent",
    )
    no_show_fee_percent: float = Field(
        0,
        ge=0,
        le=100,
        alias="noShowFeePercent",
    )
    required_datafield_config: Optional[ServiceAppointmentFieldConfig] = Field(
        None,
        alias="requiredDatafieldConfig",
    )
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateBusinessService(BaseModel):
    """Schema for updating an existing business service."""

    id: str
    service_revision_id: Optional[str] = Field(
        None,
        alias="serviceRevisionId",
    )
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")
    category_id: Optional[str] = Field(None, alias="categoryId")
    booking_code: Optional[str] = Field(None, alias="bookingCode")
    duration: Optional[int] = Field(None, gt=0, le=480)
    duration_segments: Optional[ServiceDurationSegments] = Field(
        None,
        alias="durationSegments",
    )
    buffer_before: Optional[int] = Field(None, ge=0, alias="bufferBefore")
    buffer_after: Optional[int] = Field(None, ge=0, alias="bufferAfter")
    is_bookable: Optional[bool] = Field(None, alias="isBookable")
    allows_processing_chair_swap: Optional[bool] = Field(
        None,
        alias="allowsProcessingChairSwap",
    )
    service_availability: Optional[ServiceAvailability] = Field(
        None,
        alias="serviceAvailability",
    )
    max_concurrent_bookings: Optional[int] = Field(
        None,
        gt=0,
        alias="maxConcurrentBookings",
    )
    base_price: Optional[float] = Field(None, ge=0, alias="basePrice")
    price_mode: Optional[ServicePriceMode] = Field(None, alias="priceMode")
    gratuity_mode: Optional[ServiceGratuityMode] = Field(
        None,
        alias="gratuityMode",
    )
    is_active: Optional[bool] = Field(None, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    channel_mappings: Optional[list[ServiceChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    primary_service_user_account_id: Optional[str] = Field(
        None,
        alias="primaryServiceUserAccountId",
    )
    required_resources: Optional[list[str]] = Field(
        None,
        alias="requiredResources",
    )
    booking_rules: Optional[ServiceBookingRules] = Field(
        None,
        alias="bookingRules",
    )
    deposit_strategy: Optional[ServiceDepositStrategy] = Field(
        None,
        alias="depositStrategy",
    )
    deposit_value: Optional[float] = Field(None, ge=0, alias="depositValue")
    late_cancel_fee_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        alias="lateCancelFeePercent",
    )
    no_show_fee_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        alias="noShowFeePercent",
    )
    required_datafield_config: Optional[ServiceAppointmentFieldConfig] = Field(
        None,
        alias="requiredDatafieldConfig",
    )
    placement: Optional[CreateDisplayOrderPlacement] = None


class ServiceCatalog(BaseModel):
    """Service catalog entry with category and services."""

    service_category: ServiceCategory = Field(..., alias="serviceCategory")
    services: list[BusinessServiceConfig]


BusinessServiceCatalog = list[ServiceCatalog]


__all__ = [
    "ServicePriceMode",
    "ServiceGratuityMode",
    "ServiceAvailabilityMode",
    "ServiceCategoryChannelMapping",
    "ServiceChannelMapping",
    "ServiceDurationSegments",
    "ServiceDateRange",
    "ServiceAvailability",
    "ServiceAppointmentFieldConfig",
    "ServiceCategory",
    "CreateServiceCategory",
    "UpdateServiceCategory",
    "BusinessServiceConfig",
    "CreateBusinessService",
    "UpdateBusinessService",
    "ServiceCatalog",
    "BusinessServiceCatalog",
]
