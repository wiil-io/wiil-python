"""Service persons resource for provider/staff management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateServicePerson,
    ServicePerson,
    UpdateServicePerson,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ServicePersonsResource:
    """Resource class for service persons."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/service-providers/persons"

    def create(self, data: CreateServicePerson) -> ServicePerson:
        """Create a new service person."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServicePerson,
            response_model=ServicePerson,
        )

    def get(self, person_id: str) -> ServicePerson:
        """Retrieve a service person by ID."""
        return self._http.get(
            f"{self._base_path}/{person_id}",
            response_model=ServicePerson,
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServicePerson]:
        """Retrieve service persons by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[ServicePerson],
        )

    def update(self, data: UpdateServicePerson) -> ServicePerson:
        """Update an existing service person."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateServicePerson,
            response_model=ServicePerson,
        )

    def delete(self, person_id: str) -> bool:
        """Delete a service person."""
        return self._http.delete(f"{self._base_path}/{person_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServicePerson]:
        """List service persons with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ServicePerson],
        )

    def create_batch(
        self,
        data: List[Union[CreateServicePerson, Dict[str, Any]]],
    ) -> PaginatedResult[ServicePerson]:
        """Create multiple service persons in one batch call."""
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
                    validated = CreateServicePerson.model_validate(item)
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
            response_model=PaginatedResult[ServicePerson],
        )


__all__ = ["ServicePersonsResource"]
