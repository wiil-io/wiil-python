"""Rental reservations resource for managing rental bookings."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateRentalReservation,
    RentalReservation,
    UpdateRentalReservation,
)
from wiil.models.business_mgt.reservation_management.reservation_slot_query import (  # noqa: E501
    RentalReservationSlotQueryRequest,
    RentalReservationSlotQueryResponse,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class RentalReservationsResource:
    """Resource class for rental reservations."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/rental-reservations"

    def create(self, data: CreateRentalReservation) -> RentalReservation:
        """Create a new rental reservation."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateRentalReservation,
            response_model=RentalReservation,
        )

    def get(self, reservation_id: str) -> RentalReservation:
        """Retrieve a rental reservation by ID."""
        return self._http.get(
            f"{self._base_path}/{reservation_id}",
            response_model=RentalReservation,
        )

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalReservation]:
        """Retrieve rental reservations by customer ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-customer/{customer_id}{query_string}",
            response_model=PaginatedResult[RentalReservation],
        )

    def get_by_resource(
        self,
        resource_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalReservation]:
        """Retrieve rental reservations by resource ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-resource/{resource_id}{query_string}",
            response_model=PaginatedResult[RentalReservation],
        )

    def get_by_tier(
        self,
        tier_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalReservation]:
        """Retrieve rental reservations by tier ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-tier/{tier_id}{query_string}",
            response_model=PaginatedResult[RentalReservation],
        )

    def get_by_date_range(
        self,
        start_at: int,
        end_at: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalReservation]:
        """Retrieve rental reservations by date range."""
        query_params: Dict[str, Any] = {
            "startAt": start_at,
            "endAt": end_at,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-date-range?{urlencode(query_params)}",
            response_model=PaginatedResult[RentalReservation],
        )

    def update(
        self,
        reservation_id: str,
        data: UpdateRentalReservation,
    ) -> RentalReservation:
        """Update an existing rental reservation."""
        return self._http.patch(
            f"{self._base_path}/{reservation_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateRentalReservation,
            response_model=RentalReservation,
        )

    def record_return(
        self,
        reservation_id: str,
        actual_return_at: int,
    ) -> RentalReservation:
        """Record the actual return time for a rental reservation."""
        return self._http.post(
            f"{self._base_path}/{reservation_id}/return",
            {"actualReturnAt": actual_return_at},
            response_model=RentalReservation,
        )

    def cancel(
        self,
        reservation_id: str,
        reason: Optional[str] = None,
    ) -> RentalReservation:
        """Cancel a rental reservation."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{reservation_id}/cancel",
            payload,
            response_model=RentalReservation,
        )

    def delete(self, reservation_id: str) -> bool:
        """Delete a rental reservation."""
        return self._http.delete(f"{self._base_path}/{reservation_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RentalReservation]:
        """List rental reservations with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[RentalReservation],
        )

    def get_available_slots(
        self,
        request: RentalReservationSlotQueryRequest,
    ) -> RentalReservationSlotQueryResponse:
        """Retrieve available rental reservation slots for a given date."""
        query_params = request.model_dump(by_alias=True, exclude_none=True)
        return self._http.get(
            f"{self._base_path}/available-slots?{urlencode(query_params)}",
            response_model=RentalReservationSlotQueryResponse,
        )

    def create_batch(
        self,
        data: List[Union[CreateRentalReservation, Dict[str, Any]]],
    ) -> PaginatedResult[RentalReservation]:
        """Create multiple rental reservations in one batch call."""
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
                    validated = CreateRentalReservation.model_validate(item)
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
            response_model=PaginatedResult[RentalReservation],
        )


__all__ = ["RentalReservationsResource"]
