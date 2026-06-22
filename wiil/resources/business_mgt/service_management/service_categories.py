"""Service categories resource for category grouping management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateServiceCategory,
    ServiceCategory,
    UpdateServiceCategory,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ServiceCategoriesResource:
    """Resource class for service categories."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/service-categories"

    def create(self, data: CreateServiceCategory) -> ServiceCategory:
        """Create a new service category."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServiceCategory,
            response_model=ServiceCategory,
        )

    def get(self, category_id: str) -> ServiceCategory:
        """Retrieve a service category by ID."""
        return self._http.get(
            f"{self._base_path}/{category_id}",
            response_model=ServiceCategory,
        )

    def update(self, data: UpdateServiceCategory) -> ServiceCategory:
        """Update an existing service category."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateServiceCategory,
            response_model=ServiceCategory,
        )

    def toggle_active(self, category_id: str) -> ServiceCategory:
        """Toggle the active status of a service category."""
        return self._http.post(
            f"{self._base_path}/{category_id}/toggle-active",
            {},
            response_model=ServiceCategory,
        )

    def delete(self, category_id: str) -> bool:
        """Delete a service category."""
        return self._http.delete(f"{self._base_path}/{category_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServiceCategory]:
        """List service categories with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ServiceCategory],
        )

    def create_batch(
        self,
        data: List[Union[CreateServiceCategory, Dict[str, Any]]],
    ) -> PaginatedResult[ServiceCategory]:
        """Create multiple service categories in one batch call."""
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
                    validated = CreateServiceCategory.model_validate(item)
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
            response_model=PaginatedResult[ServiceCategory],
        )


__all__ = ["ServiceCategoriesResource"]
