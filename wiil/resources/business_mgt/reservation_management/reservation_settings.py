"""Reservation settings resource for managing location-level reservation configurations."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt.reservation_management import (
    CreateReservationSettings,
    ReservationSettings,
    UpdateReservationSettings,
)
from wiil.types import PaginatedResult, PaginationRequest


class ReservationSettingsResource:
    """Resource class for managing reservation settings in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing reservation
    settings. Reservation settings define location-level configurations for table,
    room, and rental reservations including durations, booking windows, and policies.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/reservation-settings"

    def create(self, data: CreateReservationSettings) -> ReservationSettings:
        """Create new reservation settings."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateReservationSettings,
            response_model=ReservationSettings,
        )

    def get(self, settings_id: str) -> ReservationSettings:
        """Retrieve reservation settings by ID."""
        return self._http.get(
            f"{self._base_path}/{settings_id}",
            response_model=ReservationSettings,
        )

    def get_by_location(self, location_id: str) -> ReservationSettings:
        """Retrieve reservation settings by location."""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}",
            response_model=ReservationSettings,
        )

    def update(self, data: UpdateReservationSettings) -> ReservationSettings:
        """Update existing reservation settings."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateReservationSettings,
            response_model=ReservationSettings,
        )

    def delete(self, settings_id: str) -> bool:
        """Delete reservation settings."""
        return self._http.delete(f"{self._base_path}/{settings_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ReservationSettings]:
        """List reservation settings with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ReservationSettings],
        )


__all__ = ["ReservationSettingsResource"]
