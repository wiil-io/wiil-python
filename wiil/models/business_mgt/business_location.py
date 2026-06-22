"""Business location schema definitions.

A Business Location is a physical or operational site belonging to an
organization. It carries contact details, operating hours, geographic
coordinates, and lifecycle status, and is referenced by downstream
business-management resources.
"""

from enum import Enum
from typing import Any, Dict, Literal, Optional, TypedDict

from pydantic import EmailStr, Field

from wiil.models.base import Address, BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import WeeklySchedule


class BusinessLocationStatus(str, Enum):
    """Business location lifecycle status."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class GeoCoordinates(BaseModel):
    """Geographic coordinates of a location."""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class BusinessLocation(EntityModel):
    """Business location model.

    Represents a physical or operational site owned by an organization.
    """

    name: str = Field(..., min_length=1)
    code: Optional[str] = None
    external_location_id: Optional[str] = Field(
        None,
        alias="externalLocationId",
    )
    status: BusinessLocationStatus = BusinessLocationStatus.ACTIVE
    is_primary: bool = Field(False, alias="isPrimary")
    timezone: Optional[str] = None
    business_hours: WeeklySchedule = Field(..., alias="businessHours")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    coordinates: Optional[GeoCoordinates] = None
    metadata: Optional[Dict[str, Any]] = None


class CreateBusinessLocation(BaseModel):
    """Schema for creating a new business location.

    Omits auto-generated fields (id, timestamps).
    """

    name: str = Field(..., min_length=1)
    code: Optional[str] = None
    external_location_id: Optional[str] = Field(
        None,
        alias="externalLocationId",
    )
    status: BusinessLocationStatus = BusinessLocationStatus.ACTIVE
    is_primary: bool = Field(False, alias="isPrimary")
    timezone: Optional[str] = None
    business_hours: WeeklySchedule = Field(..., alias="businessHours")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    coordinates: Optional[GeoCoordinates] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateBusinessLocation(BaseModel):
    """Schema for updating an existing business location.

    All fields are optional except id.
    """

    id: str
    name: Optional[str] = Field(None, min_length=1)
    code: Optional[str] = None
    external_location_id: Optional[str] = Field(
        None,
        alias="externalLocationId",
    )
    status: Optional[BusinessLocationStatus] = None
    is_primary: Optional[bool] = Field(None, alias="isPrimary")
    timezone: Optional[str] = None
    business_hours: Optional[WeeklySchedule] = Field(
        None,
        alias="businessHours",
    )
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    coordinates: Optional[GeoCoordinates] = None
    metadata: Optional[Dict[str, Any]] = None


class NearLocationFilter(TypedDict):
    """Radius filter around a geographic point."""

    latitude: float
    longitude: float
    radius_km: float


class BoundingBoxFilter(TypedDict):
    """Geographic bounding box filter."""

    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float


class BusinessLocationFilters(TypedDict, total=False):
    """Filters for querying business locations."""

    status: Optional[BusinessLocationStatus]
    is_primary: Optional[bool]
    search: Optional[str]
    near_location: Optional[NearLocationFilter]
    bounding_box: Optional[BoundingBoxFilter]


class BusinessLocationSorting(TypedDict):
    """Sorting options for business location queries."""

    field: Literal["name", "created_at", "updated_at", "status"]
    direction: Literal["asc", "desc"]


class BusinessLocationQueryOptions(TypedDict, total=False):
    """Query options for business location retrieval."""

    page: int
    page_size: int
    filters: Optional[BusinessLocationFilters]
    sorting: Optional[BusinessLocationSorting]
