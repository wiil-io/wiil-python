"""Outbound SMS resource for managing SMS requests."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.conversation import (
    CreateSmsRequest,
    SmsRequest,
    SmsRequestResult,
    UpdateSmsRequest,
)
from wiil.types import PaginatedResult, PaginationRequest, SmsStatus

BATCH_LIMIT = 100


class OutboundSmsResource:
    """Resource class for managing outbound SMS requests in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing outbound SMS
    requests. Supports scheduling, templates, and delivery tracking with retry logic.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/outbound-sms"

    def create(self, data: CreateSmsRequest) -> SmsRequestResult:
        """Create a new outbound SMS request."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateSmsRequest,
            response_model=SmsRequestResult,
        )

    def get(self, sms_id: str) -> SmsRequest:
        """Retrieve an SMS request by ID."""
        return self._http.get(
            f"{self._base_path}/{sms_id}",
            response_model=SmsRequest,
        )

    def get_by_status(
        self,
        status: SmsStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[SmsRequest]:
        """Retrieve SMS requests by status."""
        query_params: Dict[str, Any] = {"status": status}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[SmsRequest],
        )

    def get_by_recipient(
        self,
        phone_number: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[SmsRequest]:
        """Retrieve SMS requests by recipient phone number."""
        query_params: Dict[str, Any] = {"to": phone_number}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-recipient?{urlencode(query_params)}",
            response_model=PaginatedResult[SmsRequest],
        )

    def get_by_template(
        self,
        template_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[SmsRequest]:
        """Retrieve SMS requests by template."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-template/{template_id}{query_string}",
            response_model=PaginatedResult[SmsRequest],
        )

    def get_by_date_range(
        self,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[SmsRequest]:
        """Retrieve SMS requests scheduled within a date range."""
        query_params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[SmsRequest],
        )

    def update(self, data: UpdateSmsRequest) -> SmsRequest:
        """Update an existing SMS request."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateSmsRequest,
            response_model=SmsRequest,
        )

    def cancel(
        self,
        sms_id: str,
        reason: Optional[str] = None,
    ) -> SmsRequest:
        """Cancel an SMS request."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{sms_id}/cancel",
            payload,
            response_model=SmsRequest,
        )

    def retry(self, sms_id: str) -> SmsRequestResult:
        """Retry a failed SMS request."""
        return self._http.post(
            f"{self._base_path}/{sms_id}/retry",
            {},
            response_model=SmsRequestResult,
        )

    def delete(self, sms_id: str) -> bool:
        """Delete an SMS request."""
        return self._http.delete(f"{self._base_path}/{sms_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[SmsRequest]:
        """List SMS requests with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[SmsRequest],
        )

    def create_batch(
        self,
        data: List[Union[CreateSmsRequest, Dict[str, Any]]],
    ) -> PaginatedResult[SmsRequest]:
        """Create multiple SMS requests in a batch.

        Args:
            data: List of SMS requests to create (max 100 items)

        Returns:
            PaginatedResult containing created SMS requests

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
                    validated = CreateSmsRequest.model_validate(item)
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
            response_model=PaginatedResult[SmsRequest],
        )


__all__ = ["OutboundSmsResource"]
