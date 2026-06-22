"""Table assignment schema definitions."""

from enum import Enum
from typing import Literal, Optional, TypedDict

from pydantic import Field

from wiil.models.base import EntityModel


class TableAssignmentType(str, Enum):
    """Table assignment type."""

    SOFT = "soft"
    HARD = "hard"


class TableAssignmentStatus(str, Enum):
    """Table assignment status."""

    ASSIGNED = "assigned"
    REASSIGNED = "reassigned"
    RELEASED = "released"


class TableAssignment(EntityModel):
    """Table assignment schema."""

    reservation_id: str = Field(..., alias="reservationId")
    slot_start: int = Field(..., gt=0, alias="slotStart")
    slot_end: int = Field(..., gt=0, alias="slotEnd")
    table_instance_id: str = Field(..., alias="tableInstanceId")
    floor_plan_id: str = Field(..., alias="floorPlanId")
    floor_plan_section_id: Optional[str] = Field(
        None,
        alias="floorPlanSectionId",
    )
    assignment_type: TableAssignmentType = Field(
        TableAssignmentType.SOFT,
        alias="assignmentType",
    )
    status: TableAssignmentStatus = TableAssignmentStatus.ASSIGNED
    assigned_by: Optional[str] = Field(None, alias="assignedBy")
    assigned_at: int = Field(..., gt=0, alias="assignedAt")
    released_at: Optional[int] = Field(None, gt=0, alias="releasedAt")
    released_by: Optional[str] = Field(None, alias="releasedBy")
    notes: Optional[str] = None
    location_id: Optional[str] = Field(None, alias="locationId")


class TableAssignmentFilters(TypedDict, total=False):
    """Filters for table-assignment queries."""

    reservationId: Optional[str]
    tableInstanceId: Optional[str]
    status: Optional[list[TableAssignmentStatus]]
    assignedBy: Optional[str]
    locationId: Optional[str]


class TableAssignmentSorting(TypedDict):
    """Sorting options for table-assignment queries."""

    field: Literal["assignedAt", "releasedAt", "createdAt"]
    direction: Literal["asc", "desc"]


class TableAssignmentQueryOptions(TypedDict, total=False):
    """Query options for table-assignment retrieval."""

    page: int
    pageSize: int
    filters: Optional[TableAssignmentFilters]
    sorting: Optional[TableAssignmentSorting]
