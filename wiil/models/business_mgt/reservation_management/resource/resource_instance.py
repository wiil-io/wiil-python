"""Reservation resource-instance schema definitions."""

from enum import Enum
from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel


class ResourceInstanceStatus(str, Enum):
    """Reservation resource-instance status."""

    AVAILABLE = "available"
    RESERVED = "reserved"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    CLEANING = "cleaning"
    OUT_OF_SERVICE = "out_of_service"


class ResourceInstanceAttribute(BaseModel):
    """Key-value attribute stored on resource instances."""

    key: str
    value: str


class ResourceInstance(EntityModel):
    """Resource instance schema."""

    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_id: str = Field(..., alias="resourceId")
    name: Optional[str] = None
    code: Optional[str] = None
    status: ResourceInstanceStatus = ResourceInstanceStatus.AVAILABLE
    is_available: bool = Field(True, alias="isAvailable")
    attributes: Optional[list[ResourceInstanceAttribute]] = None

    @model_validator(mode="after")
    def validate_availability(self) -> "ResourceInstance":
        if (
            self.status != ResourceInstanceStatus.AVAILABLE
            and self.is_available
        ):
            raise ValueError(
                "isAvailable should be false when status is not available"
            )
        return self


class CreateResourceInstance(BaseModel):
    """Schema for creating resource instances."""

    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    resource_id: str = Field(..., alias="resourceId")
    name: Optional[str] = None
    code: Optional[str] = None
    status: ResourceInstanceStatus = ResourceInstanceStatus.AVAILABLE
    is_available: bool = Field(True, alias="isAvailable")
    attributes: Optional[list[ResourceInstanceAttribute]] = None


class UpdateResourceInstance(BaseModel):
    """Schema for updating resource instances."""

    id: str
    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    resource_id: Optional[str] = Field(None, alias="resourceId")
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[ResourceInstanceStatus] = None
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    attributes: Optional[list[ResourceInstanceAttribute]] = None


class ResourceInstanceFilters(TypedDict, total=False):
    """Filters for resource-instance queries."""

    resourceId: Optional[str]
    locationId: Optional[str]
    status: Optional[list[ResourceInstanceStatus]]
    isAvailable: Optional[bool]


class ResourceInstanceSorting(TypedDict):
    """Sorting options for resource-instance queries."""

    field: Literal["name", "status", "createdAt"]
    direction: Literal["asc", "desc"]


class ResourceInstanceQueryOptions(TypedDict, total=False):
    """Query options for resource-instance retrieval."""

    page: int
    pageSize: int
    filters: Optional[ResourceInstanceFilters]
    sorting: Optional[ResourceInstanceSorting]
