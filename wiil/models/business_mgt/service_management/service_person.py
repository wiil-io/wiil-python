"""Service person schema for service-type business records."""

from typing import List, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class ServicePerson(EntityModel):
    """Service person entity for service businesses."""

    location_id: Optional[str] = Field(None, alias="locationId")
    user_account_id: Optional[str] = Field(None, alias="userAccountId")
    name: str = Field(..., min_length=1)
    avatar: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    commission_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        alias="commissionPercent",
    )
    schedule_id: Optional[str] = Field(None, alias="scheduleId")
    bookable_online: bool = Field(True, alias="bookableOnline")
    bookable_by_staff: bool = Field(True, alias="bookableByStaff")
    is_active: bool = Field(True, alias="isActive")


class CreateServicePerson(BaseModel):
    """Schema for creating a service person."""

    location_id: Optional[str] = Field(None, alias="locationId")
    user_account_id: Optional[str] = Field(None, alias="userAccountId")
    name: str = Field(..., min_length=1)
    avatar: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    commission_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        alias="commissionPercent",
    )
    schedule_id: Optional[str] = Field(None, alias="scheduleId")
    bookable_online: bool = Field(True, alias="bookableOnline")
    bookable_by_staff: bool = Field(True, alias="bookableByStaff")
    is_active: bool = Field(True, alias="isActive")


class UpdateServicePerson(BaseModel):
    """Schema for updating a service person."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    user_account_id: Optional[str] = Field(None, alias="userAccountId")
    name: Optional[str] = Field(None, min_length=1)
    avatar: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    commission_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        alias="commissionPercent",
    )
    schedule_id: Optional[str] = Field(None, alias="scheduleId")
    bookable_online: Optional[bool] = Field(None, alias="bookableOnline")
    bookable_by_staff: Optional[bool] = Field(None, alias="bookableByStaff")
    is_active: Optional[bool] = Field(None, alias="isActive")


class ServicePersonFilters(TypedDict, total=False):
    """Filter options for service person queries."""

    name: Optional[str]
    email: Optional[str]


class ServicePersonSorting(TypedDict):
    """Sorting options for service person queries."""

    field: str
    direction: str


class ServicePersonQueryOptions(TypedDict, total=False):
    """Query options for service person retrieval."""

    page: int
    pageSize: int
    filters: Optional[ServicePersonFilters]
    sorting: Optional[ServicePersonSorting]
