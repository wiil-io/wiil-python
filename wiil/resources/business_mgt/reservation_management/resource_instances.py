"""Resource instances resource for managing physical reservation units."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt.reservation_management import (
    CreateResourceInstance,
    ResourceInstance,
    UpdateResourceInstance,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 100


class ResourceInstancesResource:
    """Resource class for managing resource instances in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    resource instances. Resource instances represent physical reservable units
    such as specific tables, rooms, or rental equipment with operational status
    tracking and availability management.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/resource-instances"

    def create(self, data: CreateResourceInstance) -> ResourceInstance:
        """Create a new resource instance."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateResourceInstance,
            response_model=ResourceInstance,
        )

    def get(self, instance_id: str) -> ResourceInstance:
        """Retrieve a resource instance by ID."""
        return self._http.get(
            f"{self._base_path}/{instance_id}",
            response_model=ResourceInstance,
        )

    def get_by_resource(
        self,
        resource_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceInstance]:
        """Retrieve resource instances by parent resource ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-resource/{resource_id}{query_string}",
            response_model=PaginatedResult[ResourceInstance],
        )

    def get_by_status(
        self,
        status: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceInstance]:
        """Retrieve resource instances by operational status."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-status/{status}{query_string}",
            response_model=PaginatedResult[ResourceInstance],
        )

    def get_available(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceInstance]:
        """Retrieve available resource instances."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/available{query_string}",
            response_model=PaginatedResult[ResourceInstance],
        )

    def update(
        self,
        instance_id: str,
        data: UpdateResourceInstance,
    ) -> ResourceInstance:
        """Update an existing resource instance."""
        return self._http.patch(
            f"{self._base_path}/{instance_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateResourceInstance,
            response_model=ResourceInstance,
        )

    def update_status(
        self,
        instance_id: str,
        status: str,
    ) -> ResourceInstance:
        """Update the operational status of a resource instance."""
        return self._http.patch(
            f"{self._base_path}/{instance_id}/status",
            {"status": status},
            response_model=ResourceInstance,
        )

    def delete(self, instance_id: str) -> bool:
        """Delete a resource instance."""
        return self._http.delete(f"{self._base_path}/{instance_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ResourceInstance]:
        """List resource instances with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ResourceInstance],
        )

    def create_batch(
        self,
        data: List[Union[CreateResourceInstance, Dict[str, Any]]],
    ) -> PaginatedResult[ResourceInstance]:
        """Create multiple resource instances in a batch.

        Args:
            data: List of instances to create (max 100 items)

        Returns:
            PaginatedResult containing created instances

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
                    validated = CreateResourceInstance.model_validate(item)
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
            response_model=PaginatedResult[ResourceInstance],
        )


__all__ = ["ResourceInstancesResource"]
