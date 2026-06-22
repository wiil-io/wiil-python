"""Room assignment schema definitions."""

from enum import Enum
from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import EntityModel


class RoomAssignmentStatus(str, Enum):
    """Room assignment status."""

    ASSIGNED = "assigned"
    REASSIGNED = "reassigned"
    RELEASED = "released"


class RoomAssignmentType(str, Enum):
    """Room assignment type."""

    SOFT = "soft"
    HARD = "hard"


class RoomAssignment(EntityModel):
    """Room assignment schema."""

    reservation_id: str = Field(..., alias="reservationId")
    slot_start: int = Field(..., gt=0, alias="slotStart")
    slot_end: int = Field(..., gt=0, alias="slotEnd")
    room_instance_id: str = Field(..., alias="roomInstanceId")
    assignment_type: RoomAssignmentType = Field(
        RoomAssignmentType.SOFT,
        alias="assignmentType",
    )
    status: RoomAssignmentStatus = RoomAssignmentStatus.ASSIGNED
    assigned_by: Optional[str] = Field(None, alias="assignedBy")
    assigned_at: int = Field(..., gt=0, alias="assignedAt")
    released_at: Optional[int] = Field(None, gt=0, alias="releasedAt")
    released_by: Optional[str] = Field(None, alias="releasedBy")
    housekeeping_notes: Optional[str] = Field(
        None,
        alias="housekeepingNotes",
    )
    notes: Optional[str] = None
    location_id: Optional[str] = Field(None, alias="locationId")


class RoomAssignmentFilters(TypedDict, total=False):
    """Filters for room-assignment queries."""

    reservationId: Optional[str]
    roomInstanceId: Optional[str]
    status: Optional[list[RoomAssignmentStatus]]
    assignmentType: Optional[RoomAssignmentType]
    assignedBy: Optional[str]
    locationId: Optional[str]


class RoomAssignmentSorting(TypedDict):
    """Sorting options for room-assignment queries."""

    field: Literal["assignedAt", "releasedAt", "createdAt"]
    direction: Literal["asc", "desc"]


class RoomAssignmentQueryOptions(TypedDict, total=False):
    """Query options for room-assignment retrieval."""

    page: int
    pageSize: int
    filters: Optional[RoomAssignmentFilters]
    sorting: Optional[RoomAssignmentSorting]
