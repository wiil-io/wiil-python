"""Reservation resource-versioning schema definitions."""

from enum import Enum
from typing import Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class ResourceRevisionStatus(str, Enum):
    """Resource revision status."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ResourceRevisionDeriveStrategy(str, Enum):
    """Resource revision derive strategy."""

    COPY_CURRENT = "copy_current"
    EMPTY = "empty"


class ResourceDefinition(EntityModel):
    """Resource definition schema."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    is_active: bool = Field(True, alias="isActive")


class ResourceRevision(EntityModel):
    """Resource revision schema."""

    resource_id: str = Field(..., alias="resourceId")
    label: Optional[str] = None
    status: ResourceRevisionStatus = ResourceRevisionStatus.DRAFT
    derived_from_revision_id: Optional[str] = Field(
        None,
        alias="derivedFromRevisionId",
    )
    published_at: Optional[int] = Field(None, gt=0, alias="publishedAt")


class CreateResourceDefinition(BaseModel):
    """Schema for creating a resource definition."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    is_active: bool = Field(True, alias="isActive")


class UpdateResourceDefinition(BaseModel):
    """Schema for updating a resource definition."""

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    is_active: Optional[bool] = Field(None, alias="isActive")


class CreateResourceRevision(BaseModel):
    """Schema for creating a resource revision."""

    resource_id: str = Field(..., alias="resourceId")
    label: Optional[str] = None
    status: ResourceRevisionStatus = ResourceRevisionStatus.DRAFT
    derived_from_revision_id: Optional[str] = Field(
        None,
        alias="derivedFromRevisionId",
    )
    published_at: Optional[int] = Field(None, gt=0, alias="publishedAt")


class UpdateResourceRevision(BaseModel):
    """Schema for updating a resource revision."""

    id: str
    resource_id: Optional[str] = Field(None, alias="resourceId")
    label: Optional[str] = None
    status: Optional[ResourceRevisionStatus] = None
    derived_from_revision_id: Optional[str] = Field(
        None,
        alias="derivedFromRevisionId",
    )
    published_at: Optional[int] = Field(None, gt=0, alias="publishedAt")


class DeriveResourceRevisionRequest(BaseModel):
    """Request schema for deriving a resource revision."""

    resource_id: str = Field(..., alias="resourceId")
    source_revision_id: Optional[str] = Field(None, alias="sourceRevisionId")
    strategy: ResourceRevisionDeriveStrategy = (
        ResourceRevisionDeriveStrategy.COPY_CURRENT
    )
    label: Optional[str] = None


class DeriveResourceRevisionResult(BaseModel):
    """Result schema for derive-resource-revision operations."""

    resource_id: str = Field(..., alias="resourceId")
    resource_revision_id: str = Field(..., alias="resourceRevisionId")


class ResourceRevisionContext(BaseModel):
    """Context schema identifying an active resource revision."""

    resource_id: str = Field(..., alias="resourceId")
    resource_revision_id: str = Field(..., alias="resourceRevisionId")
