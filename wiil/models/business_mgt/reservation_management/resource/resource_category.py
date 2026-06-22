"""Reservation resource-category schema definitions."""

from typing import Any, Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import ResourceType
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)


class ResourceCategoryChannelMapping(BaseModel):
    """Per-channel external resource-category mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_category_id: str = Field(..., alias="externalCategoryId")


class ResourceCategory(EntityModel):
    """Resource category schema."""

    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[list[ResourceCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    resource_type: Optional[ResourceType] = Field(None, alias="resourceType")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")
    metadata: Optional[dict[str, Any]] = None


class CreateResourceCategory(BaseModel):
    """Schema for creating resource categories."""

    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[list[ResourceCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    resource_type: Optional[ResourceType] = Field(None, alias="resourceType")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")
    metadata: Optional[dict[str, Any]] = None
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdateResourceCategory(BaseModel):
    """Schema for updating resource categories."""

    id: str
    resource_revision_id: Optional[str] = Field(
        None,
        alias="resourceRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    channel_mappings: Optional[list[ResourceCategoryChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    resource_type: Optional[ResourceType] = Field(None, alias="resourceType")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_active: Optional[bool] = Field(None, alias="isActive")
    metadata: Optional[dict[str, Any]] = None
    placement: Optional[CreateDisplayOrderPlacement] = None


class ResourceCategoryFilters(TypedDict, total=False):
    """Filters for resource-category queries."""

    search: Optional[str]
    locationId: Optional[str]
    resourceType: Optional[list[ResourceType]]
    isActive: Optional[bool]


class ResourceCategorySorting(TypedDict):
    """Sorting options for resource-category queries."""

    field: Literal["name", "displayOrder", "createdAt"]
    direction: Literal["asc", "desc"]


class ResourceCategoryQueryOptions(TypedDict, total=False):
    """Query options for resource-category retrieval."""

    page: int
    pageSize: int
    filters: Optional[ResourceCategoryFilters]
    sorting: Optional[ResourceCategorySorting]
