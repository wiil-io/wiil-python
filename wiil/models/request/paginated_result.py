"""Pagination schema definitions for paginated API responses.

This module mirrors src/request/models/paginated-result.schema.ts
"""

from typing import Any, Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

SortDirection = Literal["asc", "desc"]


class PaginationMeta(BaseModel):
    """Pagination metadata schema.

    Attributes:
        page: Current page number (1-based indexing)
        page_size: Number of items per page - limited to 1000 for performance
        total_count: Total number of items across all pages
        total_pages: Total number of pages available
        has_next_page: Whether there is a next page available for navigation
        has_previous_page: Whether there is a previous page available for navigation
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    page: int = Field(..., gt=0, description="Current page number (1-based indexing)")
    page_size: int = Field(
        ...,
        gt=0,
        le=1000,
        description="Number of items per page - limited to 1000 for performance",
        alias="pageSize"
    )
    total_count: int = Field(
        ...,
        ge=0,
        description="Total number of items across all pages",
        alias="totalCount"
    )
    total_pages: int = Field(
        ...,
        ge=0,
        description="Total number of pages available",
        alias="totalPages"
    )
    has_next_page: bool = Field(
        ...,
        description="Whether there is a next page available for navigation",
        alias="hasNextPage"
    )
    has_previous_page: bool = Field(
        ...,
        description="Whether there is a previous page available for navigation",
        alias="hasPreviousPage"
    )


class BasePaginatedResult(BaseModel):
    """Basic paginated result schema for any data type.

    Use this when you need a flexible paginated result without specific data typing.

    Attributes:
        data: Array of data items for the current page
        meta: Pagination metadata including page info and navigation flags
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    data: List[Any] = Field(..., description="Array of data items for the current page")
    meta: PaginationMeta = Field(
        ...,
        description="Pagination metadata including page info and navigation flags"
    )


class PaginatedResultType(BaseModel, Generic[T]):
    """Generic paginated result type for typed responses.

    Use this with a specific type parameter for typed paginated results.

    Example:
        ```python
        result: PaginatedResultType[Customer] = get_customers(page=1)
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    data: List[T] = Field(..., description="Array of typed data items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")


class PaginatedAccountRequest(BaseModel):
    """Schema for paginated account requests.

    Attributes:
        page: Page number to retrieve (1-based)
        page_size: Number of items per page (max 1000)
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    page: int = Field(
        1,
        gt=0,
        description="Page number to retrieve (1-based)"
    )
    page_size: int = Field(
        20,
        gt=0,
        le=1000,
        description="Number of items per page (max 1000)",
        alias="pageSize"
    )


class PaginationRequest(BaseModel):
    """Generic pagination request schema.

    Attributes:
        page: Page number to retrieve (1-based)
        page_size: Number of items per page (max 1000)
        sort_by: Field name to sort by
        sort_direction: Sort direction - ascending or descending
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    page: int = Field(
        1,
        gt=0,
        description="Page number to retrieve (1-based)"
    )
    page_size: int = Field(
        20,
        gt=0,
        le=1000,
        description="Number of items per page (max 1000)",
        alias="pageSize"
    )
    sort_by: Optional[str] = Field(
        None,
        description="Field name to sort by",
        alias="sortBy"
    )
    sort_direction: SortDirection = Field(
        "asc",
        description="Sort direction - ascending or descending",
        alias="sortDirection"
    )


class SearchablePaginationRequest(PaginationRequest):
    """Schema for search-enabled pagination requests.

    Attributes:
        page: Page number to retrieve
        page_size: Number of items per page
        sort_by: Field name to sort by
        sort_direction: Sort direction
        search: Search query to filter results
        search_fields: Specific fields to search within
    """

    search: Optional[str] = Field(
        None,
        description="Search query to filter results"
    )
    search_fields: Optional[List[str]] = Field(
        None,
        description="Specific fields to search within",
        alias="searchFields"
    )
