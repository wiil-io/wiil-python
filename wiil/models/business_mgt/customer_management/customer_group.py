"""Customer group schema definitions for business management."""

from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class CustomerGroup(EntityModel):
    """Groups customers for pricing tiers and special terms."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    code: Optional[str] = None
    is_default: bool = Field(False, alias="isDefault")


class CreateCustomerGroup(BaseModel):
    """Schema for creating a new customer group."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    code: Optional[str] = None
    is_default: bool = Field(False, alias="isDefault")


class UpdateCustomerGroup(BaseModel):
    """Schema for updating an existing customer group."""

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    code: Optional[str] = None
    is_default: Optional[bool] = Field(None, alias="isDefault")


class CustomerGroupFilters(TypedDict, total=False):
    """Filters for querying customer groups."""

    search: Optional[str]
    code: Optional[str]
    is_default: Optional[bool]


class CustomerGroupSorting(TypedDict):
    """Sorting options for customer group queries."""

    field: Literal["name", "code", "created_at"]
    direction: Literal["asc", "desc"]


class CustomerGroupQueryOptions(TypedDict, total=False):
    """Query options for customer group retrieval."""

    page: int
    page_size: int
    filters: Optional[CustomerGroupFilters]
    sorting: Optional[CustomerGroupSorting]
