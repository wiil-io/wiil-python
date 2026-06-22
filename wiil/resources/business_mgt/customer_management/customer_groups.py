"""Customer groups resource for customer segmentation management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote, urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateCustomerGroup,
    CustomerGroup,
    UpdateCustomerGroup,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class CustomerGroupsResource:
    """Resource class for managing customer groups."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/customer-groups"

    def create(self, data: CreateCustomerGroup) -> CustomerGroup:
        """Create a new customer group."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateCustomerGroup,
            response_model=CustomerGroup,
        )

    def get(self, group_id: str) -> CustomerGroup:
        """Retrieve a customer group by ID."""
        return self._http.get(
            f"{self._base_path}/{group_id}",
            response_model=CustomerGroup,
        )

    def get_by_code(self, code: str) -> Optional[CustomerGroup]:
        """Retrieve a customer group by code."""
        return self._http.get(
            f"{self._base_path}/code/{quote(code, safe='')}",
            response_model=CustomerGroup,
        )

    def get_default(self) -> Optional[CustomerGroup]:
        """Retrieve the default customer group."""
        return self._http.get(
            f"{self._base_path}/default",
            response_model=CustomerGroup,
        )

    def update(
        self,
        group_id: str,
        data: UpdateCustomerGroup,
    ) -> CustomerGroup:
        """Update an existing customer group."""
        return self._http.patch(
            f"{self._base_path}/{group_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateCustomerGroup,
            response_model=CustomerGroup,
        )

    def delete(self, group_id: str) -> bool:
        """Delete a customer group."""
        return self._http.delete(f"{self._base_path}/{group_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[CustomerGroup]:
        """List customer groups with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[CustomerGroup],
        )

    def create_batch(
        self,
        data: List[Union[CreateCustomerGroup, Dict[str, Any]]],
    ) -> PaginatedResult[CustomerGroup]:
        """Create multiple customer groups in one batch call."""
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
                    validated = CreateCustomerGroup.model_validate(item)
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
            response_model=PaginatedResult[CustomerGroup],
        )


__all__ = ["CustomerGroupsResource"]
