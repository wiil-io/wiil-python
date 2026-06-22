"""Table assignments resource for managing table-to-reservation assignments."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt.reservation_management import (
    TableAssignment,
    TableAssignmentStatus,
)
from wiil.types import PaginatedResult, PaginationRequest


class TableAssignmentsResource:
    """Resource class for reading table assignments in the WIIL Platform.

    Provides read-only methods for retrieving and listing table assignments.
    Table assignments are managed by the platform as part of reservation
    workflows and record the physical table instance assigned to a table
    reservation.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/table-assignments"

    def get(self, assignment_id: str) -> TableAssignment:
        """Retrieve a table assignment by ID."""
        return self._http.get(
            f"{self._base_path}/{assignment_id}",
            response_model=TableAssignment,
        )

    def get_by_reservation(
        self,
        reservation_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableAssignment]:
        """Retrieve table assignments by reservation."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-reservation/{reservation_id}{query_string}",
            response_model=PaginatedResult[TableAssignment],
        )

    def get_by_table_instance(
        self,
        table_instance_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableAssignment]:
        """Retrieve table assignments by table instance."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-table/{table_instance_id}{query_string}",
            response_model=PaginatedResult[TableAssignment],
        )

    def get_by_status(
        self,
        status: TableAssignmentStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableAssignment]:
        """Retrieve table assignments by status."""
        query_params: Dict[str, Any] = {"status": status}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[TableAssignment],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableAssignment]:
        """Retrieve active table assignments."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[TableAssignment],
        )

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableAssignment]:
        """List table assignments with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[TableAssignment],
        )


__all__ = ["TableAssignmentsResource"]
