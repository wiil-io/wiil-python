"""Shared booking schema definitions for services and reservations."""

from enum import Enum

from pydantic import Field

from wiil.models.base import BaseModel


class ServiceDepositStrategy(str, Enum):
    """Service deposit strategy options."""

    NONE = "NONE"
    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"


class ReservationType(str, Enum):
    """Reservation type options."""

    TABLE = "TABLE"
    ROOM = "ROOM"
    RENTAL = "RENTAL"
    OTHER = "OTHER"


class ServiceBookingRules(BaseModel):
    """Service booking rules configuration."""

    online_enabled: bool = Field(True, alias="onlineEnabled")
    existing_only: bool = Field(False, alias="existingOnly")
    requires_consult: bool = Field(False, alias="requiresConsult")
    max_days_out: int = Field(30, gt=0, alias="maxDaysOut")
    min_notice_hours: int = Field(0, ge=0, alias="minNoticeHours")
    late_cancel_hours: int = Field(24, ge=0, alias="lateCancelHours")
