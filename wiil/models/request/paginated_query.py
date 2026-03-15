"""Timestamp-based query schema definitions for filtering records.

This module mirrors src/request/models/paginated-quest.schema.ts
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TimestampQuery(BaseModel):
    """Schema for queries based on a specific timestamp.

    Attributes:
        from_timestamp: Unix timestamp to filter records
            (e.g., for fetching updates since this time)
        to_timestamp: Optional end Unix timestamp to filter records up to this time
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
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
        1,
        ge=1,
        description="Page number for pagination, starting from 1"
    )
    page_size: int = Field(
        20,
        ge=1,
        le=100,
        description="Number of records per page, max 100",
        alias="pageSize"
    )
