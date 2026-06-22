"""Service provider time-off schema and query definitions."""

from typing import Annotated, List, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    ServiceProviderTimeOffStatus,
    ServiceProviderTimeOffType,
)

DayOfWeek = Annotated[str, Field(pattern=r"^[0-6]$")]


class ServiceProviderTimeOffRecurrence(BaseModel):
    """Recurrence rule for recurring time-off."""

    day_of_week: List[DayOfWeek] = Field(..., min_length=1, alias="dayOfWeek")


class ServiceTimeOff(EntityModel):
    """Time-off block for a service provider."""

    provider_id: str = Field(..., alias="providerId")
    type: ServiceProviderTimeOffType
    start_date: int = Field(..., gt=0, alias="startDate")
    end_date: int = Field(..., gt=0, alias="endDate")
    reason: Optional[str] = None
    status: ServiceProviderTimeOffStatus = ServiceProviderTimeOffStatus.PENDING
    recurrence: Optional[ServiceProviderTimeOffRecurrence] = None


class CreateServiceTimeOff(BaseModel):
    """Schema for creating service time-off."""

    provider_id: str = Field(..., alias="providerId")
    type: ServiceProviderTimeOffType
    start_date: int = Field(..., gt=0, alias="startDate")
    end_date: int = Field(..., gt=0, alias="endDate")
    reason: Optional[str] = None
    status: ServiceProviderTimeOffStatus = ServiceProviderTimeOffStatus.PENDING
    recurrence: Optional[ServiceProviderTimeOffRecurrence] = None


class UpdateServiceTimeOff(BaseModel):
    """Schema for updating service time-off."""

    id: str
    provider_id: Optional[str] = Field(None, alias="providerId")
    type: Optional[ServiceProviderTimeOffType] = None
    start_date: Optional[int] = Field(None, gt=0, alias="startDate")
    end_date: Optional[int] = Field(None, gt=0, alias="endDate")
    reason: Optional[str] = None
    status: Optional[ServiceProviderTimeOffStatus] = None
    recurrence: Optional[ServiceProviderTimeOffRecurrence] = None


class ServiceTimeOffFilters(TypedDict, total=False):
    """Filter options for service time-off queries."""

    serviceProviderId: Optional[str]
    type: Optional[ServiceProviderTimeOffType]
    status: Optional[ServiceProviderTimeOffStatus]


class ServiceTimeOffSorting(TypedDict):
    """Sorting options for service time-off queries."""

    field: str
    direction: str


class ServiceTimeOffQueryOptions(TypedDict, total=False):
    """Query options for service time-off retrieval."""

    page: int
    pageSize: int
    filters: Optional[ServiceTimeOffFilters]
    sorting: Optional[ServiceTimeOffSorting]
