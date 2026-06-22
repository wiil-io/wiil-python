"""Product variant axes resource for variant dimensions."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote, urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateVariantAxis,
    UpdateVariantAxis,
    VariantAxis,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ProductVariantAxesResource:
    """Resource class for product variant axes."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/product-variant-axes"

    def create(self, data: CreateVariantAxis) -> VariantAxis:
        """Create a new variant axis."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateVariantAxis,
            response_model=VariantAxis,
        )

    def get(self, axis_id: str) -> VariantAxis:
        """Retrieve a variant axis by ID."""
        return self._http.get(
            f"{self._base_path}/{axis_id}",
            response_model=VariantAxis,
        )

    def get_by_name(self, name: str) -> Optional[VariantAxis]:
        """Retrieve a variant axis by name."""
        return self._http.get(
            f"{self._base_path}/by-name/{quote(name, safe='')}",
            response_model=VariantAxis,
        )

    def update(self, axis_id: str, data: UpdateVariantAxis) -> VariantAxis:
        """Update an existing variant axis."""
        return self._http.patch(
            f"{self._base_path}/{axis_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateVariantAxis,
            response_model=VariantAxis,
        )

    def delete(self, axis_id: str) -> bool:
        """Delete a variant axis."""
        return self._http.delete(f"{self._base_path}/{axis_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[VariantAxis]:
        """List variant axes with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[VariantAxis],
        )

    def create_batch(
        self,
        data: List[Union[CreateVariantAxis, Dict[str, Any]]],
    ) -> PaginatedResult[VariantAxis]:
        """Create multiple variant axes in one batch call."""
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
                    validated = CreateVariantAxis.model_validate(item)
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
            response_model=PaginatedResult[VariantAxis],
        )


__all__ = ["ProductVariantAxesResource"]
