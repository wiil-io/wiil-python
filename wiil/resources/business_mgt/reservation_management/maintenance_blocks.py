"""Maintenance blocks resource for managing resource unavailability periods."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt.reservation_management import (
    CreateMaintenanceBlock,
    MaintenanceBlock,
    UpdateMaintenanceBlock,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class MaintenanceBlocksResource:
    """Resource class for managing maintenance blocks in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing maintenance
    blocks. Maintenance blocks represent time periods when a reservable resource
    instance is unavailable for booking (e.g., cleaning, repairs, renovation).
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/maintenance-blocks"

    def create(self, data: CreateMaintenanceBlock) -> MaintenanceBlock:
        """Create a new maintenance block."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMaintenanceBlock,
            response_model=MaintenanceBlock,
        )

    def get(self, block_id: str) -> MaintenanceBlock:
        """Retrieve a maintenance block by ID."""
        return self._http.get(
            f"{self._base_path}/{block_id}",
            response_model=MaintenanceBlock,
        )

    def get_by_resource_instance(
        self,
        resource_instance_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MaintenanceBlock]:
        """Retrieve maintenance blocks by resource instance."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-resource/{resource_instance_id}{query_string}",
            response_model=PaginatedResult[MaintenanceBlock],
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MaintenanceBlock]:
        """Retrieve maintenance blocks by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[MaintenanceBlock],
        )

    def get_by_date_range(
        self,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MaintenanceBlock]:
        """Retrieve maintenance blocks within a date range."""
        query_params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[MaintenanceBlock],
        )

    def update(self, data: UpdateMaintenanceBlock) -> MaintenanceBlock:
        """Update an existing maintenance block."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMaintenanceBlock,
            response_model=MaintenanceBlock,
        )

    def delete(self, block_id: str) -> bool:
        """Delete a maintenance block."""
        return self._http.delete(f"{self._base_path}/{block_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MaintenanceBlock]:
        """List maintenance blocks with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[MaintenanceBlock],
        )

    def create_batch(
        self,
        data: List[Union[CreateMaintenanceBlock, Dict[str, Any]]],
    ) -> PaginatedResult[MaintenanceBlock]:
        """Create multiple maintenance blocks in a batch.

        Args:
            data: List of maintenance blocks to create (max 50 items)

        Returns:
            PaginatedResult containing created maintenance blocks

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
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
                    validated = CreateMaintenanceBlock.model_validate(item)
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
            response_model=PaginatedResult[MaintenanceBlock],
        )


__all__ = ["MaintenanceBlocksResource"]
