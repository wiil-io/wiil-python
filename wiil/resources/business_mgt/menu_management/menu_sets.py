"""Menu sets resource for bundled and selector-based menu set management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote, urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import CreateMenuSet, MenuSet, UpdateMenuSet
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class MenuSetsResource:
    """Resource class for menu sets."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/menu-sets"

    def create(self, data: CreateMenuSet) -> MenuSet:
        """Create a new menu set."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMenuSet,
            response_model=MenuSet,
        )

    def get(self, menu_set_id: str) -> MenuSet:
        """Retrieve a menu set by ID."""
        return self._http.get(
            f"{self._base_path}/{menu_set_id}",
            response_model=MenuSet,
        )

    def get_by_code(self, code: str) -> Optional[MenuSet]:
        """Retrieve a menu set by code."""
        return self._http.get(
            f"{self._base_path}/code/{quote(code, safe='')}",
            response_model=MenuSet,
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MenuSet]:
        """Retrieve active menu sets with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[MenuSet],
        )

    def update(self, menu_set_id: str, data: UpdateMenuSet) -> MenuSet:
        """Update an existing menu set."""
        return self._http.patch(
            f"{self._base_path}/{menu_set_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMenuSet,
            response_model=MenuSet,
        )

    def delete(self, menu_set_id: str) -> bool:
        """Delete a menu set."""
        return self._http.delete(f"{self._base_path}/{menu_set_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MenuSet]:
        """List menu sets with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[MenuSet],
        )

    def create_batch(
        self,
        data: List[Union[CreateMenuSet, Dict[str, Any]]],
    ) -> PaginatedResult[MenuSet]:
        """Create multiple menu sets in a batch."""
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
                    validated = CreateMenuSet.model_validate(item)
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
            response_model=PaginatedResult[MenuSet],
        )


__all__ = ["MenuSetsResource"]
