"""Business locations resource for managing business location configurations."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    BusinessLocation,
    BusinessLocationFilters,
    CreateBusinessLocation,
    UpdateBusinessLocation,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class BusinessLocationsResource:
    """Resource class for managing business locations."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/business-locations"

    def create(self, data: CreateBusinessLocation) -> BusinessLocation:
        """Create a new business location."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessLocation,
            response_model=BusinessLocation,
        )

    def get(self, location_id: str) -> BusinessLocation:
        """Retrieve a business location by ID."""
        return self._http.get(
            f"{self._base_path}/{location_id}",
            response_model=BusinessLocation,
        )

    def get_by_code(self, code: str) -> Optional[BusinessLocation]:
        """Retrieve a business location by code."""
        return self._http.get(
            f"{self._base_path}/code/{code}",
            response_model=BusinessLocation,
        )

    def update(self, data: UpdateBusinessLocation) -> BusinessLocation:
        """Update an existing business location."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessLocation,
            response_model=BusinessLocation,
        )

    def delete(self, location_id: str) -> bool:
        """Delete a business location."""
        return self._http.delete(f"{self._base_path}/{location_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
        filters: Optional[BusinessLocationFilters] = None,
    ) -> PaginatedResult[BusinessLocation]:
        """List business locations with optional pagination and filters."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size
        if filters:
            status = filters.get("status")
            if status is not None:
                query_params["status"] = (
                    status.value if hasattr(status, "value") else status
                )
            is_primary = filters.get("is_primary")
            if is_primary is not None:
                query_params["isPrimary"] = "true" if is_primary else "false"
            search = filters.get("search")
            if search is not None:
                query_params["search"] = search

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[BusinessLocation],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[BusinessLocation]:
        """Retrieve active business locations."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[BusinessLocation],
        )

    def get_primary(self) -> Optional[BusinessLocation]:
        """Retrieve the primary business location for the organization."""
        return self._http.get(
            f"{self._base_path}/primary",
            response_model=BusinessLocation,
        )

    def create_batch(
        self,
        data: List[Union[CreateBusinessLocation, Dict[str, Any]]],
    ) -> PaginatedResult[BusinessLocation]:
        """Create multiple business locations in one batch call."""
        if len(data) > BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {BATCH_LIMIT}",
                details=[
                    {
                        "path": ["data"],
                        "message": (
                            f"Array length {len(data)} exceeds "
                            f"maximum of {BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateBusinessLocation.model_validate(item)
                    payload.append(
                        validated.model_dump(by_alias=True, exclude_none=True)
                    )
                elif isinstance(item, BaseModel):
                    payload.append(
                        item.model_dump(by_alias=True, exclude_none=True)
                    )
                else:
                    raise WiilValidationError(
                        f"Invalid item type at index {i}",
                        details=[
                            {
                                "path": ["data", i],
                                "message": "Expected dict or Pydantic model",
                            }
                        ],
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f"Validation failed for item at index {i}",
                    details=e.errors(),
                )

        return self._http.post(
            f"{self._base_path}/batch",
            payload,
            response_model=PaginatedResult[BusinessLocation],
        )


__all__ = ["BusinessLocationsResource"]
