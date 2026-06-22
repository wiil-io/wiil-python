"""Rental assignments resource for managing rental-to-reservation assignments."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt.reservation_management import (
    RentalAssignment,
    RentalAssignmentStatus,
)
from wiil.types import PaginatedResult, PaginationRequest


class RentalAssignmentsResource:
    """Resource class for reading rental assignments in the WIIL Platform.

    Provides read-only methods for retrieving and listing rental assignments.
    Rental assignments are managed by the platform as part of reservation
    workflows and record the physical rental unit assigned to a rental
    reservation, including condition tracking at pickup and return.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/rental-assignments"

    def get(self, assignment_id: str) -> RentalAssignment:
        """Retrieve a rental assignment by ID."""
        return self._http.get(
            f"{self._base_path}/{assignment_id}",
            response_model=RentalAssignment,
        )

    def get_by_reservation(
        self,
        reservation_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalAssignment]:
        """Retrieve rental assignments by reservation."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-reservation/{reservation_id}{query_string}",
            response_model=PaginatedResult[RentalAssignment],
        )

    def get_by_rental_instance(
        self,
        rental_instance_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalAssignment]:
        """Retrieve rental assignments by rental instance."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-rental/{rental_instance_id}{query_string}",
            response_model=PaginatedResult[RentalAssignment],
        )

    def get_by_status(
        self,
        status: RentalAssignmentStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalAssignment]:
        """Retrieve rental assignments by status."""
        query_params: Dict[str, Any] = {"status": status}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[RentalAssignment],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalAssignment]:
        """Retrieve active rental assignments."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[RentalAssignment],
        )

    def get_with_damage(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalAssignment]:
        """Retrieve rental assignments with damage reported."""
        query_params: Dict[str, Any] = {"damageReported": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/with-damage?{urlencode(query_params)}",
            response_model=PaginatedResult[RentalAssignment],
        )

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalAssignment]:
        """List rental assignments with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[RentalAssignment],
        )


__all__ = ["RentalAssignmentsResource"]
