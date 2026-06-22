"""Appointment additional info schema for storing dynamic field values."""

from typing import Any, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel

DynamicFieldValue = Any


class AppointmentAdditionalInfo(EntityModel):
    """Stores dynamic field values captured for an appointment."""

    business_service_id: str = Field(..., alias="businessServiceId")
    appointment_id: str = Field(..., alias="appointmentId")
    customer_id: str = Field(..., alias="customerId")
    data: dict[str, DynamicFieldValue] = Field(default_factory=dict)


class CreateAppointmentAdditionalInfo(BaseModel):
    """Schema for creating appointment additional info."""

    business_service_id: str = Field(..., alias="businessServiceId")
    appointment_id: str = Field(..., alias="appointmentId")
    customer_id: str = Field(..., alias="customerId")
    data: dict[str, DynamicFieldValue] = Field(default_factory=dict)


class UpdateAppointmentAdditionalInfo(BaseModel):
    """Schema for updating appointment additional info."""

    id: str
    business_service_id: Optional[str] = Field(None, alias="businessServiceId")
    appointment_id: Optional[str] = Field(None, alias="appointmentId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    data: Optional[dict[str, DynamicFieldValue]] = None


class AppointmentAdditionalInfoFilters(TypedDict, total=False):
    """Filter options for appointment additional info queries."""

    businessServiceId: Optional[str]
    appointmentId: Optional[str]
    customerId: Optional[str]


class AppointmentAdditionalInfoSorting(TypedDict):
    """Sorting options for appointment additional info queries."""

    field: str
    direction: str


class AppointmentAdditionalInfoQueryOptions(TypedDict, total=False):
    """Query options for appointment additional info retrieval."""

    page: int
    pageSize: int
    filters: Optional[AppointmentAdditionalInfoFilters]
    sorting: Optional[AppointmentAdditionalInfoSorting]
