"""Resource categories resource for managing reservation resource groupings."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt.reservation_management import (
    CreateResourceCategory,
    ResourceCategory,
    UpdateResourceCategory,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ResourceCategoriesResource:
    """Resource class for managing resource categories in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    resource categories. Resource categories group reservation resources by type,
    location, and display order for organized resource management.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/resource-categories"

    def create(self, data: CreateResourceCategory) -> ResourceCategory:
        """Create a new resource category."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateResourceCategory,
            response_model=ResourceCategory,
        )

    def get(self, category_id: str) -> ResourceCategory:
        """Retrieve a resource category by ID."""
        return self._http.get(
            f"{self._base_path}/{category_id}",
            response_model=ResourceCategory,
        )

    def get_by_resource_type(
        self,
        resource_type: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceCategory]:
        """Retrieve resource categories by resource type."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-type/{resource_type}{query_string}",
            response_model=PaginatedResult[ResourceCategory],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceCategory]:
        """Retrieve active resource categories."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[ResourceCategory],
        )

    def update(
        self,
        category_id: str,
        data: UpdateResourceCategory,
    ) -> ResourceCategory:
        """Update an existing resource category."""
        return self._http.patch(
            f"{self._base_path}/{category_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateResourceCategory,
            response_model=ResourceCategory,
        )

    def delete(self, category_id: str) -> bool:
        """Delete a resource category."""
        return self._http.delete(f"{self._base_path}/{category_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceCategory]:
        """List resource categories with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ResourceCategory],
        )

    def create_batch(
        self,
        data: List[Union[CreateResourceCategory, Dict[str, Any]]],
    ) -> PaginatedResult[ResourceCategory]:
        """Create multiple resource categories in a batch.

        Args:
            data: List of categories to create (max 50 items)

        Returns:
            PaginatedResult containing created categories

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
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
                    validated = CreateResourceCategory.model_validate(item)
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
            response_model=PaginatedResult[ResourceCategory],
        )


__all__ = ["ResourceCategoriesResource"]
