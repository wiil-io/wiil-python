"""Service providers resource for service/provider assignment management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateServiceProvider,
    ServiceProvider,
    UpdateServiceProvider,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 100


class ServiceProvidersResource:
    """Resource class for service provider assignments."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/service-providers/bindings"

    def create(self, data: CreateServiceProvider) -> ServiceProvider:
        """Create a new service provider assignment."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServiceProvider,
            response_model=ServiceProvider,
        )

    def get(self, assignment_id: str) -> ServiceProvider:
        """Retrieve a service provider assignment by ID."""
        return self._http.get(
            f"{self._base_path}/{assignment_id}",
            response_model=ServiceProvider,
        )

    def get_by_service(
        self,
        service_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceProvider]:
        """Retrieve assignments by service ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-service/{service_id}{query_string}",
            response_model=PaginatedResult[ServiceProvider],
        )

    def get_by_provider(
        self,
        provider_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceProvider]:
        """Retrieve assignments by provider ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-provider/{provider_id}{query_string}",
            response_model=PaginatedResult[ServiceProvider],
        )

    def update(self, data: UpdateServiceProvider) -> ServiceProvider:
        """Update an existing service provider assignment."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateServiceProvider,
            response_model=ServiceProvider,
        )

    def delete(self, assignment_id: str) -> bool:
        """Delete a service provider assignment."""
        return self._http.delete(f"{self._base_path}/{assignment_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceProvider]:
        """List service provider assignments with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ServiceProvider],
        )

    def create_batch(
        self,
        data: List[Union[CreateServiceProvider, Dict[str, Any]]],
    ) -> PaginatedResult[ServiceProvider]:
        """Create multiple assignments in one batch call."""
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
                    validated = CreateServiceProvider.model_validate(item)
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
            response_model=PaginatedResult[ServiceProvider],
        )


__all__ = ["ServiceProvidersResource"]
