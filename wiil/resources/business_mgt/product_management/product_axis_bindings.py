"""Product axis bindings resource for linking products to variant axes."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateProductAxisBinding,
    ProductAxisBinding,
    UpdateProductAxisBinding,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 100


class ProductAxisBindingsResource:
    """Resource class for product axis bindings."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/product-management/axis-bindings"

    def create(self, data: CreateProductAxisBinding) -> ProductAxisBinding:
        """Create a new product axis binding."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductAxisBinding,
            response_model=ProductAxisBinding,
        )

    def get(self, binding_id: str) -> ProductAxisBinding:
        """Retrieve a product axis binding by ID."""
        return self._http.get(
            f"{self._base_path}/{binding_id}",
            response_model=ProductAxisBinding,
        )

    def get_by_product(
        self,
        product_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductAxisBinding]:
        """Retrieve bindings by product ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-product/{product_id}{query_string}",
            response_model=PaginatedResult[ProductAxisBinding],
        )

    def get_by_axis(
        self,
        axis_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductAxisBinding]:
        """Retrieve bindings by variant axis ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-axis/{axis_id}{query_string}",
            response_model=PaginatedResult[ProductAxisBinding],
        )

    def update(
        self,
        binding_id: str,
        data: UpdateProductAxisBinding,
    ) -> ProductAxisBinding:
        """Update an existing product axis binding."""
        return self._http.patch(
            f"{self._base_path}/{binding_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductAxisBinding,
            response_model=ProductAxisBinding,
        )

    def delete(self, binding_id: str) -> bool:
        """Delete a product axis binding."""
        return self._http.delete(f"{self._base_path}/{binding_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductAxisBinding]:
        """List product axis bindings with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ProductAxisBinding],
        )

    def create_batch(
        self,
        data: List[Union[CreateProductAxisBinding, Dict[str, Any]]],
    ) -> PaginatedResult[ProductAxisBinding]:
        """Create multiple bindings in one batch call."""
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
                    validated = CreateProductAxisBinding.model_validate(item)
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
            response_model=PaginatedResult[ProductAxisBinding],
        )


__all__ = ["ProductAxisBindingsResource"]
