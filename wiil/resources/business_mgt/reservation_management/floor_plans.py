"""Floor plans resource for managing table layout canvases."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt.reservation_management import (
    CreateFloorPlan,
    CreateFloorPlanDefinition,
    FloorPlan,
    FloorPlanDefinition,
    UpdateFloorPlan,
)
from wiil.types import PaginatedResult, PaginationRequest


class FloorPlansResource:
    """Resource class for managing floor plans in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing floor plans.
    Floor plans represent table layout canvases for reservable business locations,
    defining the coordinate space for section and table placement.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/floor-plans"
        self._definition_path = "/floor-plans-definitions"

    def create_definition(
        self,
        data: CreateFloorPlanDefinition,
    ) -> FloorPlanDefinition:
        """Atomically create a floor plan with its sections and tables."""
        return self._http.post(
            self._definition_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateFloorPlanDefinition,
            response_model=FloorPlanDefinition,
        )

    def get_definition(self, floor_plan_id: str) -> FloorPlanDefinition:
        """Retrieve a fully hydrated floor plan definition by ID."""
        return self._http.get(
            f"{self._definition_path}/{floor_plan_id}",
            response_model=FloorPlanDefinition,
        )

    def list_definitions(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[FloorPlanDefinition]:
        """List floor plan definitions with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._definition_path}{query_string}",
            response_model=PaginatedResult[FloorPlanDefinition],
        )

    def create(self, data: CreateFloorPlan) -> FloorPlan:
        """Create a new floor plan."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateFloorPlan,
            response_model=FloorPlan,
        )

    def get(self, floor_plan_id: str) -> FloorPlan:
        """Retrieve a floor plan by ID."""
        return self._http.get(
            f"{self._base_path}/{floor_plan_id}",
            response_model=FloorPlan,
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[FloorPlan]:
        """Retrieve floor plans by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[FloorPlan],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[FloorPlan]:
        """Retrieve active floor plans."""
        query_params: Dict[str, Any] = {"isActive": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/active?{urlencode(query_params)}",
            response_model=PaginatedResult[FloorPlan],
        )

    def update(self, data: UpdateFloorPlan) -> FloorPlan:
        """Update an existing floor plan."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateFloorPlan,
            response_model=FloorPlan,
        )

    def delete(self, floor_plan_id: str) -> bool:
        """Delete a floor plan."""
        return self._http.delete(f"{self._base_path}/{floor_plan_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[FloorPlan]:
        """List floor plans with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[FloorPlan],
        )


__all__ = ["FloorPlansResource"]
