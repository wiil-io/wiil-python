"""Rental assignment schema definitions."""

from enum import Enum
from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel


class RentalAssignmentStatus(str, Enum):
    """Rental assignment status."""

    ASSIGNED = "assigned"
    REASSIGNED = "reassigned"
    RELEASED = "released"


class RentalAssignmentType(str, Enum):
    """Rental assignment type."""

    SOFT = "soft"
    HARD = "hard"


class RentalUnitCondition(BaseModel):
    """Condition metadata captured for assigned rental units."""

    recorded_at: int = Field(..., gt=0, alias="recordedAt")
    recorded_by: str = Field(..., alias="recordedBy")
    notes: Optional[str] = None
    damage_reported: bool = Field(False, alias="damageReported")
    image_urls: Optional[list[str]] = Field(None, alias="imageUrls")


class RentalAssignment(EntityModel):
    """Rental assignment schema."""

    reservation_id: str = Field(..., alias="reservationId")
    slot_start: int = Field(..., gt=0, alias="slotStart")
    slot_end: int = Field(..., gt=0, alias="slotEnd")
    rental_instance_id: str = Field(..., alias="rentalInstanceId")
    assignment_type: RentalAssignmentType = Field(
        RentalAssignmentType.SOFT,
        alias="assignmentType",
    )
    status: RentalAssignmentStatus = RentalAssignmentStatus.ASSIGNED
    assigned_by: Optional[str] = Field(None, alias="assignedBy")
    assigned_at: int = Field(..., gt=0, alias="assignedAt")
    released_at: Optional[int] = Field(None, gt=0, alias="releasedAt")
    released_by: Optional[str] = Field(None, alias="releasedBy")
    condition_at_pickup: Optional[RentalUnitCondition] = Field(
        None,
        alias="conditionAtPickup",
    )
    condition_at_return: Optional[RentalUnitCondition] = Field(
        None,
        alias="conditionAtReturn",
    )
    notes: Optional[str] = None
    location_id: Optional[str] = Field(None, alias="locationId")


class RentalAssignmentFilters(TypedDict, total=False):
    """Filters for rental-assignment queries."""

    reservationId: Optional[str]
    rentalInstanceId: Optional[str]
    status: Optional[list[RentalAssignmentStatus]]
    assignmentType: Optional[RentalAssignmentType]
    assignedBy: Optional[str]
    locationId: Optional[str]
    damageReported: Optional[bool]


class RentalAssignmentSorting(TypedDict):
    """Sorting options for rental-assignment queries."""

    field: Literal["assignedAt", "releasedAt", "createdAt"]
    direction: Literal["asc", "desc"]


class RentalAssignmentQueryOptions(TypedDict, total=False):
    """Query options for rental-assignment retrieval."""

    page: int
    pageSize: int
    filters: Optional[RentalAssignmentFilters]
    sorting: Optional[RentalAssignmentSorting]
