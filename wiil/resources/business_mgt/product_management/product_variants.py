"""Product variants resource for SKU-level variant management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateProductVariant,
    ProductVariant,
    UpdateProductVariant,
)
from wiil.types import PaginatedResult

BATCH_LIMIT = 100


class ProductVariantsResource:
    """Resource class for product variants."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/product-management/variants"

    def create(self, data: CreateProductVariant) -> ProductVariant:
        """Create a new product variant."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductVariant,
            response_model=ProductVariant,
        )

    def get(self, variant_id: str) -> ProductVariant:
        """Retrieve a product variant by ID."""
        return self._http.get(
            f"{self._base_path}/{variant_id}",
            response_model=ProductVariant,
        )

    def get_by_sku(self, sku: str) -> Optional[ProductVariant]:
        """Retrieve a variant by SKU."""
        return self._http.get(
            f"{self._base_path}/by-sku/{quote(sku, safe='')}",
            response_model=ProductVariant,
        )

    def get_default(self, product_id: str) -> Optional[ProductVariant]:
        """Retrieve the default variant for a product."""
        return self._http.get(
            f"{self._base_path}/default/{product_id}",
            response_model=ProductVariant,
        )

    def update(
        self,
        variant_id: str,
        data: UpdateProductVariant,
    ) -> ProductVariant:
        """Update an existing product variant."""
        return self._http.patch(
            f"{self._base_path}/{variant_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductVariant,
            response_model=ProductVariant,
        )

    def delete(self, variant_id: str) -> bool:
        """Delete a product variant."""
        return self._http.delete(f"{self._base_path}/{variant_id}")

    def create_batch(
        self,
        data: List[Union[CreateProductVariant, Dict[str, Any]]],
    ) -> PaginatedResult[ProductVariant]:
        """Create multiple product variants in one batch call."""
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
                    validated = CreateProductVariant.model_validate(item)
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
            response_model=PaginatedResult[ProductVariant],
        )


__all__ = ["ProductVariantsResource"]
