"""Room reservations resource for managing room bookings."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateRoomReservation,
    RoomReservation,
    UpdateRoomReservation,
)
from wiil.models.business_mgt.reservation_management.reservation_slot_query import (  # noqa: E501
    RoomReservationSlotQueryRequest,
    RoomReservationSlotQueryResponse,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class RoomReservationsResource:
    """Resource class for room reservations."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/room-reservations"

    def create(self, data: CreateRoomReservation) -> RoomReservation:
        """Create a new room reservation."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateRoomReservation,
            response_model=RoomReservation,
        )

    def get(self, reservation_id: str) -> RoomReservation:
        """Retrieve a room reservation by ID."""
        return self._http.get(
            f"{self._base_path}/{reservation_id}",
            response_model=RoomReservation,
        )

    def get_by_guest(
        self,
        guest_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomReservation]:
        """Retrieve room reservations by guest ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-guest/{guest_id}{query_string}",
            response_model=PaginatedResult[RoomReservation],
        )

    def get_by_resource(
        self,
        resource_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomReservation]:
        """Retrieve room reservations by resource ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-resource/{resource_id}{query_string}",
            response_model=PaginatedResult[RoomReservation],
        )

    def get_by_check_in_range(
        self,
        check_in_start: int,
        check_in_end: int,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomReservation]:
        """Retrieve room reservations by check-in date range."""
        query_params: Dict[str, Any] = {
            "checkInStart": check_in_start,
            "checkInEnd": check_in_end,
        }
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-check-in-range?{urlencode(query_params)}",
            response_model=PaginatedResult[RoomReservation],
        )

    def update(
        self,
        reservation_id: str,
        data: UpdateRoomReservation,
    ) -> RoomReservation:
        """Update an existing room reservation."""
        return self._http.patch(
            f"{self._base_path}/{reservation_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateRoomReservation,
            response_model=RoomReservation,
        )

    def cancel(
        self,
        reservation_id: str,
        reason: Optional[str] = None,
    ) -> RoomReservation:
        """Cancel a room reservation."""
        payload: Dict[str, Any] = {}
        if reason is not None:
            payload["reason"] = reason

        return self._http.post(
            f"{self._base_path}/{reservation_id}/cancel",
            payload,
            response_model=RoomReservation,
        )

    def delete(self, reservation_id: str) -> bool:
        """Delete a room reservation."""
        return self._http.delete(f"{self._base_path}/{reservation_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[RoomReservation]:
        """List room reservations with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[RoomReservation],
        )

    def get_available_slots(
        self,
        request: RoomReservationSlotQueryRequest,
    ) -> RoomReservationSlotQueryResponse:
        """Retrieve available room reservation slots for a check-in date."""
        query_params = request.model_dump(by_alias=True, exclude_none=True)
        return self._http.get(
            f"{self._base_path}/available-slots?{urlencode(query_params)}",
            response_model=RoomReservationSlotQueryResponse,
        )

    def create_batch(
        self,
        data: List[Union[CreateRoomReservation, Dict[str, Any]]],
    ) -> PaginatedResult[RoomReservation]:
        """Create multiple room reservations in one batch call."""
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
                    validated = CreateRoomReservation.model_validate(item)
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
            response_model=PaginatedResult[RoomReservation],
        )


__all__ = ["RoomReservationsResource"]
