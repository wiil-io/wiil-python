"""Outbound emails resource for managing email requests and delivery tracking."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.conversation import (
    CreateEmailRequest,
    EmailRecord,
    EmailRequest,
    EmailRequestResult,
    UpdateEmailRequest,
)
from wiil.types import EmailStatus, PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class OutboundEmailsResource:
    """Resource class for managing outbound email requests in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing outbound email
    requests. Supports scheduling, templates, attachments, and delivery tracking
    with retry logic.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/outbound-emails"

    def create(self, data: CreateEmailRequest) -> EmailRequestResult:
        """Create a new outbound email request."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateEmailRequest,
            response_model=EmailRequestResult,
        )

    def get(self, email_id: str) -> EmailRequest:
        """Retrieve an email request by ID."""
        return self._http.get(
            f"{self._base_path}/{email_id}",
            response_model=EmailRequest,
        )

    def get_by_status(
        self,
        status: EmailStatus,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[EmailRequest]:
        """Retrieve email requests by status."""
        query_params: Dict[str, Any] = {"status": status}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-status?{urlencode(query_params)}",
            response_model=PaginatedResult[EmailRequest],
        )

    def get_by_template(
        self,
        template_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[EmailRequest]:
        """Retrieve email requests by template."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-template/{template_id}{query_string}",
            response_model=PaginatedResult[EmailRequest],
        )

    def get_by_date_range(
        self,
        start_date: int,
        end_date: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[EmailRequest]:
        """Retrieve email requests scheduled within a date range."""
        query_params: Dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[EmailRequest],
        )

    def update(self, data: UpdateEmailRequest) -> EmailRequest:
        """Update an existing email request."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateEmailRequest,
            response_model=EmailRequest,
        )

    def cancel(
        self,
        email_id: str,
        reason: Optional[str] = None,
    ) -> EmailRequest:
        """Cancel an email request."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{email_id}/cancel",
            payload,
            response_model=EmailRequest,
        )

    def retry(self, email_id: str) -> EmailRequestResult:
        """Retry a failed email request."""
        return self._http.post(
            f"{self._base_path}/{email_id}/retry",
            {},
            response_model=EmailRequestResult,
        )

    def get_records(
        self,
        email_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[EmailRecord]:
        """Retrieve delivery records for an email request."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/{email_id}/records{query_string}",
            response_model=PaginatedResult[EmailRecord],
        )

    def delete(self, email_id: str) -> bool:
        """Delete an email request."""
        return self._http.delete(f"{self._base_path}/{email_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[EmailRequest]:
        """List email requests with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[EmailRequest],
        )

    def create_batch(
        self,
        data: List[Union[CreateEmailRequest, Dict[str, Any]]],
    ) -> PaginatedResult[EmailRequest]:
        """Create multiple email requests in a batch.

        Args:
            data: List of email requests to create (max 50 items)

        Returns:
            PaginatedResult containing created email requests

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
                    validated = CreateEmailRequest.model_validate(item)
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
            response_model=PaginatedResult[EmailRequest],
        )


__all__ = ["OutboundEmailsResource"]
