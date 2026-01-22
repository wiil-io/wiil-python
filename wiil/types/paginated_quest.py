"""Timestamp-based query schema definitions for filtering records.

This module provides Pydantic models for timestamp-based queries and paginated
timestamp queries used across the WIIL Platform API.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TimestampQuery(BaseModel):
    """Schema for queries based on a specific timestamp.

    Attributes:
        from_timestamp: Unix timestamp to filter records (e.g., for fetching updates since this time)
        to_timestamp: Optional end Unix timestamp to filter records up to this time
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    from_timestamp: int = Field(
        ...,
        description="Unix timestamp to filter records (e.g., for fetching updates since this time)",
        alias="fromTimestamp"
    )
    to_timestamp: Optional[int] = Field(
        None,
        description="Optional end Unix timestamp to filter records up to this time",
        alias="toTimestamp"
    )


class AccountPaginatedTimestampQuery(TimestampQuery):
    """Schema for paginated queries based on a specific timestamp.

    Attributes:
        from_timestamp: Unix timestamp to filter records
        to_timestamp: Optional end Unix timestamp
        page: Page number for pagination, starting from 1
        page_size: Number of records per page, max 100
    """

    page: int = Field(
        default=1,
        ge=1,
        description="Page number for pagination, starting from 1"
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of records per page, max 100",
        alias="pageSize"
    )


__all__ = [
    'TimestampQuery',
    'AccountPaginatedTimestampQuery',
]
