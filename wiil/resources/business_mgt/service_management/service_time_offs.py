"""Service time offs resource for provider unavailability management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateServiceTimeOff,
    ServiceTimeOff,
    UpdateServiceTimeOff,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ServiceTimeOffsResource:
    """Resource class for service provider time off records."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/service-providers/time-off"

    def create(self, data: CreateServiceTimeOff) -> ServiceTimeOff:
        """Create a new service time off record."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServiceTimeOff,
            response_model=ServiceTimeOff,
        )

    def get(self, time_off_id: str) -> ServiceTimeOff:
        """Retrieve a service time off record by ID."""
        return self._http.get(
            f"{self._base_path}/{time_off_id}",
            response_model=ServiceTimeOff,
        )

    def get_by_provider(
        self,
        provider_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceTimeOff]:
        """Retrieve time off records by provider ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-provider/{provider_id}{query_string}",
            response_model=PaginatedResult[ServiceTimeOff],
        )

    def get_by_date_range(
        self,
        provider_id: str,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceTimeOff]:
        """Retrieve time off records by date range for a specific provider."""
        query_params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range/{provider_id}"
            f"?{urlencode(query_params)}",
            response_model=PaginatedResult[ServiceTimeOff],
        )

    def update(self, data: UpdateServiceTimeOff) -> ServiceTimeOff:
        """Update an existing service time off record."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateServiceTimeOff,
            response_model=ServiceTimeOff,
        )

    def approve(self, time_off_id: str) -> ServiceTimeOff:
        """Approve a pending time off request."""
        return self._http.post(
            f"{self._base_path}/{time_off_id}/approve",
            {},
            response_model=ServiceTimeOff,
        )

    def reject(
        self,
        time_off_id: str,
        reason: Optional[str] = None,
    ) -> ServiceTimeOff:
        """Reject a pending time off request."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{time_off_id}/reject",
            payload,
            response_model=ServiceTimeOff,
        )

    def delete(self, time_off_id: str) -> bool:
        """Delete a service time off record."""
        return self._http.delete(f"{self._base_path}/{time_off_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceTimeOff]:
        """List service time off records with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ServiceTimeOff],
        )

    def create_batch(
        self,
        data: List[Union[CreateServiceTimeOff, Dict[str, Any]]],
    ) -> PaginatedResult[ServiceTimeOff]:
        """Create multiple time off records in one batch call."""
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
                    validated = CreateServiceTimeOff.model_validate(item)
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
            response_model=PaginatedResult[ServiceTimeOff],
        )


__all__ = ["ServiceTimeOffsResource"]
