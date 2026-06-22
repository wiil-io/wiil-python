"""Table reservations resource for managing table bookings."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateTableReservation,
    TableReservation,
    UpdateTableReservation,
)
from wiil.models.business_mgt.reservation_management.reservation_slot_query import (  # noqa: E501
    TableReservationSlotQueryRequest,
    TableReservationSlotQueryResponse,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class TableReservationsResource:
    """Resource class for table reservations."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/table-reservations"

    def create(self, data: CreateTableReservation) -> TableReservation:
        """Create a new table reservation."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTableReservation,
            response_model=TableReservation,
        )

    def get(self, reservation_id: str) -> TableReservation:
        """Retrieve a table reservation by ID."""
        return self._http.get(
            f"{self._base_path}/{reservation_id}",
            response_model=TableReservation,
        )

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableReservation]:
        """Retrieve table reservations by customer ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-customer/{customer_id}{query_string}",
            response_model=PaginatedResult[TableReservation],
        )

    def get_by_resource(
        self,
        resource_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableReservation]:
        """Retrieve table reservations by resource ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-resource/{resource_id}{query_string}",
            response_model=PaginatedResult[TableReservation],
        )

    def get_by_date_range(
        self,
        start_time: int,
        end_time: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableReservation]:
        """Retrieve table reservations by date range."""
        query_params: Dict[str, Any] = {
            "startTime": start_time,
            "endTime": end_time,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[TableReservation],
        )

    def update(
        self,
        reservation_id: str,
        data: UpdateTableReservation,
    ) -> TableReservation:
        """Update an existing table reservation."""
        return self._http.patch(
            f"{self._base_path}/{reservation_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateTableReservation,
            response_model=TableReservation,
        )

    def cancel(
        self,
        reservation_id: str,
        reason: Optional[str] = None,
    ) -> TableReservation:
        """Cancel a table reservation."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{reservation_id}/cancel",
            payload,
            response_model=TableReservation,
        )

    def delete(self, reservation_id: str) -> bool:
        """Delete a table reservation."""
        return self._http.delete(f"{self._base_path}/{reservation_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TableReservation]:
        """List table reservations with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[TableReservation],
        )

    def get_available_slots(
        self,
        request: TableReservationSlotQueryRequest,
    ) -> TableReservationSlotQueryResponse:
        """Retrieve available table reservation slots for a given date."""
        query_params = request.model_dump(by_alias=True, exclude_none=True)
        return self._http.get(
            f"{self._base_path}/available-slots?{urlencode(query_params)}",
            response_model=TableReservationSlotQueryResponse,
        )

    def create_batch(
        self,
        data: List[Union[CreateTableReservation, Dict[str, Any]]],
    ) -> PaginatedResult[TableReservation]:
        """Create multiple table reservations in one batch call."""
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
                    validated = CreateTableReservation.model_validate(item)
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
            response_model=PaginatedResult[TableReservation],
        )


__all__ = ["TableReservationsResource"]
