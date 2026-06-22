"""Floor plan sections resource for managing seating sections and table placements."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt.reservation_management import (
    CreateSection,
    CreateTablePlacement,
    Section,
    TablePlacement,
    UpdateSection,
    UpdateTablePlacement,
)
from wiil.types import PaginatedResult, PaginationRequest


class FloorPlanSectionsResource:
    """Resource class for managing floor plan sections in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing floor plan
    sections and their table placements. Sections represent named seating areas
    within a floor plan, containing table positions and capacity information.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/floor-plan-sections"

    def create(self, data: CreateSection) -> Section:
        """Create a new floor plan section."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateSection,
            response_model=Section,
        )

    def get(self, section_id: str) -> Section:
        """Retrieve a section by ID."""
        return self._http.get(
            f"{self._base_path}/{section_id}",
            response_model=Section,
        )

    def get_by_floor_plan(
        self,
        floor_plan_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[Section]:
        """Retrieve sections by floor plan."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-floor-plan/{floor_plan_id}{query_string}",
            response_model=PaginatedResult[Section],
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[Section]:
        """Retrieve sections by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[Section],
        )

    def update(self, data: UpdateSection) -> Section:
        """Update an existing section."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateSection,
            response_model=Section,
        )

    def delete(self, section_id: str) -> bool:
        """Delete a section."""
        return self._http.delete(f"{self._base_path}/{section_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[Section]:
        """List sections with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[Section],
        )

    # ============================================================
    # Table Placement Methods
    # ============================================================

    def add_table_placement(
        self,
        section_id: str,
        data: CreateTablePlacement,
    ) -> TablePlacement:
        """Add a table placement to a section."""
        return self._http.post(
            f"{self._base_path}/{section_id}/tables",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTablePlacement,
            response_model=TablePlacement,
        )

    def get_table_placement(
        self,
        section_id: str,
        placement_id: str,
    ) -> TablePlacement:
        """Retrieve a table placement by ID."""
        return self._http.get(
            f"{self._base_path}/{section_id}/tables/{placement_id}",
            response_model=TablePlacement,
        )

    def update_table_placement(
        self,
        section_id: str,
        data: UpdateTablePlacement,
    ) -> TablePlacement:
        """Update a table placement."""
        return self._http.patch(
            f"{self._base_path}/{section_id}/tables",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateTablePlacement,
            response_model=TablePlacement,
        )

    def remove_table_placement(
        self,
        section_id: str,
        placement_id: str,
    ) -> bool:
        """Remove a table placement from a section."""
        return self._http.delete(
            f"{self._base_path}/{section_id}/tables/{placement_id}"
        )


__all__ = ["FloorPlanSectionsResource"]
