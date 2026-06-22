"""Room assignments resource for managing room-to-reservation assignments."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt.reservation_management import (
    RoomAssignment,
    RoomAssignmentStatus,
)
from wiil.types import PaginatedResult, PaginationRequest


class RoomAssignmentsResource:
    """Resource class for reading room assignments in the WIIL Platform.

    Provides read-only methods for retrieving and listing room assignments.
    Room assignments are managed by the platform as part of reservation
    workflows and record the physical room instance assigned to a room
    reservation.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/room-assignments"

    def get(self, assignment_id: str) -> RoomAssignment:
        """Retrieve a room assignment by ID."""
        return self._http.get(
            f"{self._base_path}/{assignment_id}",
            response_model=RoomAssignment,
        )

    def get_by_reservation(
        self,
        reservation_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomAssignment]:
        """Retrieve room assignments by reservation."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-reservation/{reservation_id}{query_string}",
            response_model=PaginatedResult[RoomAssignment],
        )

    def get_by_room_instance(
        self,
        room_instance_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomAssignment]:
        """Retrieve room assignments by room instance."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-room/{room_instance_id}{query_string}",
            response_model=PaginatedResult[RoomAssignment],
        )

    def get_by_status(
        self,
        status: RoomAssignmentStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomAssignment]:
        """Retrieve room assignments by status."""
        query_params: Dict[str, Any] = {"status": status}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[RoomAssignment],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomAssignment]:
        """Retrieve active room assignments."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[RoomAssignment],
        )

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomAssignment]:
        """List room assignments with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[RoomAssignment],
        )


__all__ = ["RoomAssignmentsResource"]
