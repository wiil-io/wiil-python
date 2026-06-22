"""Service slot query schemas for appointment availability lookups.

These are transient request/response query objects, not persisted database
models. They back the appointment slot-availability lookup endpoint.
"""

from typing import Optional

from pydantic import Field

from wiil.models.base import BaseModel


class ServiceSlotQueryRequest(BaseModel):
    """Request payload for querying available service appointment slots."""

    service_id: str = Field(..., alias="serviceId")
    local_date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        alias="localDate",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    provider_id: str = Field(..., alias="providerId")
    max_results: int = Field(10, gt=0, le=1000, alias="maxResults")


class ServiceCandidateSlot(BaseModel):
    """An available candidate time slot for booking."""

    provider_id: str = Field(..., alias="providerId")
    service_provider_id: Optional[str] = Field(
        None,
        alias="serviceProviderId",
    )
    start_time_of_day: str = Field(
        ...,
        pattern=r"^(0?[1-9]|1[0-2]):[0-5]\d\s?(AM|PM)$",
        alias="startTimeOfDay",
    )
    start_minute_of_day: int = Field(
        ...,
        ge=0,
        le=1439,
        alias="startMinuteOfDay",
    )
    end_minute_of_day: int = Field(
        ...,
        ge=1,
        le=1440,
        alias="endMinuteOfDay",
    )
    start_time_utc_sec: int = Field(..., alias="startTimeUtcSec")
    end_time_utc_sec: int = Field(..., alias="endTimeUtcSec")


class ServiceSlotQueryResponse(BaseModel):
    """Response payload containing available slots for the requested date."""

    local_date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        alias="localDate",
    )
    timezone: str = Field(..., min_length=1)
    generated_at: int = Field(..., alias="generatedAt")
    slots: list[ServiceCandidateSlot]
