"""Product sets resource for bundled products and selector sets."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote, urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateProductSet,
    ProductSet,
    UpdateProductSet,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ProductSetsResource:
    """Resource class for product sets."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/product-sets"

    def create(self, data: CreateProductSet) -> ProductSet:
        """Create a new product set."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductSet,
            response_model=ProductSet,
        )

    def get(self, product_set_id: str) -> ProductSet:
        """Retrieve a product set by ID."""
        return self._http.get(
            f"{self._base_path}/{product_set_id}",
            response_model=ProductSet,
        )

    def get_by_code(self, code: str) -> Optional[ProductSet]:
        """Retrieve a product set by code."""
        return self._http.get(
            f"{self._base_path}/code/{quote(code, safe='')}",
            response_model=ProductSet,
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductSet]:
        """Retrieve active product sets with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[ProductSet],
        )

    def update(
        self,
        product_set_id: str,
        data: UpdateProductSet,
    ) -> ProductSet:
        """Update an existing product set."""
        return self._http.patch(
            f"{self._base_path}/{product_set_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductSet,
            response_model=ProductSet,
        )

    def delete(self, product_set_id: str) -> bool:
        """Delete a product set."""
        return self._http.delete(f"{self._base_path}/{product_set_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductSet]:
        """List product sets with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ProductSet],
        )

    def create_batch(
        self,
        data: List[Union[CreateProductSet, Dict[str, Any]]],
    ) -> PaginatedResult[ProductSet]:
        """Create multiple product sets in one batch call."""
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
                    validated = CreateProductSet.model_validate(item)
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
            response_model=PaginatedResult[ProductSet],
        )


__all__ = ["ProductSetsResource"]
