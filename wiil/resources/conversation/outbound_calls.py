"""Outbound calls resource for managing AI-powered voice call requests."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.conversation import (
    BusinessCallRequest,
    CallRequestResult,
    CreateCallRequest,
    UpdateCallRequest,
)
from wiil.types import CallRequestStatus, PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class OutboundCallsResource:
    """Resource class for managing outbound call requests in the WIIL Platform.

    Provides methods for creating, retrieving, updating, canceling, and listing
    outbound call requests. Supports scheduling, retry logic, and calling hours
    compliance for AI-powered voice calls.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/outbound-calls"

    def create(self, data: CreateCallRequest) -> CallRequestResult:
        """Create a new outbound call request."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateCallRequest,
            response_model=CallRequestResult,
        )

    def get(self, call_id: str) -> BusinessCallRequest:
        """Retrieve a call request by ID."""
        return self._http.get(
            f"{self._base_path}/{call_id}",
            response_model=BusinessCallRequest,
        )

    def get_by_agent(
        self,
        agent_configuration_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[BusinessCallRequest]:
        """Retrieve call requests by agent configuration."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-agent/{agent_configuration_id}{query_string}",
            response_model=PaginatedResult[BusinessCallRequest],
        )

    def get_by_status(
        self,
        status: CallRequestStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[BusinessCallRequest]:
        """Retrieve call requests by status."""
        query_params: Dict[str, Any] = {"status": status.value}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[BusinessCallRequest],
        )

    def get_by_date_range(
        self,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[BusinessCallRequest]:
        """Retrieve call requests scheduled within a date range."""
        query_params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[BusinessCallRequest],
        )

    def update(self, data: UpdateCallRequest) -> BusinessCallRequest:
        """Update an existing call request."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateCallRequest,
            response_model=BusinessCallRequest,
        )

    def update_status(
        self,
        call_id: str,
        status: CallRequestStatus,
    ) -> BusinessCallRequest:
        """Update call request status."""
        return self._http.patch(
            f"{self._base_path}/{call_id}/status",
            {"status": status.value},
            response_model=BusinessCallRequest,
        )

    def cancel(
        self,
        call_id: str,
        reason: Optional[str] = None,
    ) -> BusinessCallRequest:
        """Cancel a call request."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{call_id}/cancel",
            payload,
            response_model=BusinessCallRequest,
        )

    def retry(self, call_id: str) -> CallRequestResult:
        """Retry a failed call request."""
        return self._http.post(
            f"{self._base_path}/{call_id}/retry",
            {},
            response_model=CallRequestResult,
        )

    def delete(self, call_id: str) -> bool:
        """Delete a call request."""
        return self._http.delete(f"{self._base_path}/{call_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[BusinessCallRequest]:
        """List call requests with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[BusinessCallRequest],
        )

    def create_batch(
        self,
        data: List[Union[CreateCallRequest, Dict[str, Any]]],
    ) -> PaginatedResult[BusinessCallRequest]:
        """Create multiple call requests in a batch.

        Args:
            data: List of call requests to create (max 50 items)

        Returns:
            PaginatedResult containing created call requests

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
                    validated = CreateCallRequest.model_validate(item)
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
            response_model=PaginatedResult[BusinessCallRequest],
        )


__all__ = ["OutboundCallsResource"]
