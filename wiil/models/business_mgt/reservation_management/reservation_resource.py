"""Generic reservation-resource compatibility schema definitions."""

from typing import Optional

from pydantic import Field

from wiil.models.base import BaseModel
from wiil.models.business_mgt.reservation_management.resource.resource import (
    CreateResource,
    Resource,
    UpdateResource,
)


class RoomResource(BaseModel):
    """Room-specific compatibility resource payload."""

    room_number: Optional[str] = Field(None, alias="roomNumber")
    room_type: Optional[str] = Field(None, alias="roomType")
    price_per_night: Optional[float] = Field(None, ge=0, alias="pricePerNight")


class RentalResource(BaseModel):
    """Rental-specific compatibility resource payload."""

    item_type: Optional[str] = Field(None, alias="itemType")
    price_per_hour: Optional[float] = Field(None, ge=0, alias="pricePerHour")


__all__ = [
    "RoomResource",
    "RentalResource",
    "Resource",
    "CreateResource",
    "UpdateResource",
]
