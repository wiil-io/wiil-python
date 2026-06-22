"""Shipping addresses resource for customer delivery address management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateShippingAddress,
    ShippingAddress,
    UpdateShippingAddress,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ShippingAddressesResource:
    """Resource class for managing shipping addresses."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/shipping-addresses"

    def create(self, data: CreateShippingAddress) -> ShippingAddress:
        """Create a new shipping address."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateShippingAddress,
            response_model=ShippingAddress,
        )

    def get(self, address_id: str) -> ShippingAddress:
        """Retrieve a shipping address by ID."""
        return self._http.get(
            f"{self._base_path}/{address_id}",
            response_model=ShippingAddress,
        )

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ShippingAddress]:
        """Retrieve shipping addresses by customer ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-customer/{customer_id}{query_string}",
            response_model=PaginatedResult[ShippingAddress],
        )

    def get_primary(self, customer_id: str) -> Optional[ShippingAddress]:
        """Retrieve a customer's primary shipping address."""
        return self._http.get(
            f"{self._base_path}/primary/{customer_id}",
            response_model=ShippingAddress,
        )

    def update(
        self,
        address_id: str,
        data: UpdateShippingAddress,
    ) -> ShippingAddress:
        """Update an existing shipping address."""
        return self._http.patch(
            f"{self._base_path}/{address_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateShippingAddress,
            response_model=ShippingAddress,
        )

    def set_primary(self, address_id: str) -> ShippingAddress:
        """Set a shipping address as primary for its customer."""
        return self._http.post(
            f"{self._base_path}/{address_id}/set-primary",
            {},
            response_model=ShippingAddress,
        )

    def delete(self, address_id: str) -> bool:
        """Delete a shipping address."""
        return self._http.delete(f"{self._base_path}/{address_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ShippingAddress]:
        """List shipping addresses with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ShippingAddress],
        )

    def create_batch(
        self,
        data: List[Union[CreateShippingAddress, Dict[str, Any]]],
    ) -> PaginatedResult[ShippingAddress]:
        """Create multiple shipping addresses in one batch call."""
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
                    validated = CreateShippingAddress.model_validate(item)
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
            response_model=PaginatedResult[ShippingAddress],
        )


__all__ = ["ShippingAddressesResource"]
