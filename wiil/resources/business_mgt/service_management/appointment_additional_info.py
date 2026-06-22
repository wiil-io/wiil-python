"""Appointment additional info resource for dynamic field value management."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    AppointmentAdditionalInfo,
    CreateAppointmentAdditionalInfo,
    UpdateAppointmentAdditionalInfo,
)
from wiil.types import PaginatedResult, PaginationRequest


class AppointmentAdditionalInfoResource:
    """Resource class for appointment additional info."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/appointment-additional-info"

    def create(
        self, data: CreateAppointmentAdditionalInfo
    ) -> AppointmentAdditionalInfo:
        """Create new appointment additional info."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateAppointmentAdditionalInfo,
            response_model=AppointmentAdditionalInfo,
        )

    def get(self, info_id: str) -> AppointmentAdditionalInfo:
        """Retrieve appointment additional info by ID."""
        return self._http.get(
            f"{self._base_path}/{info_id}",
            response_model=AppointmentAdditionalInfo,
        )

    def get_by_appointment(
        self, appointment_id: str
    ) -> AppointmentAdditionalInfo:
        """Retrieve appointment additional info by appointment."""
        return self._http.get(
            f"{self._base_path}/by-appointment/{appointment_id}",
            response_model=AppointmentAdditionalInfo,
        )

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentAdditionalInfo]:
        """Retrieve appointment additional info by customer with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-customer/{customer_id}{query_string}",
            response_model=PaginatedResult[AppointmentAdditionalInfo],
        )

    def get_by_business_service(
        self,
        business_service_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentAdditionalInfo]:
        """Retrieve appointment additional info by business service."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-business-service/"
            f"{business_service_id}{query_string}",
            response_model=PaginatedResult[AppointmentAdditionalInfo],
        )

    def update(
        self, data: UpdateAppointmentAdditionalInfo
    ) -> AppointmentAdditionalInfo:
        """Update existing appointment additional info."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateAppointmentAdditionalInfo,
            response_model=AppointmentAdditionalInfo,
        )

    def delete(self, info_id: str) -> bool:
        """Delete appointment additional info."""
        return self._http.delete(f"{self._base_path}/{info_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentAdditionalInfo]:
        """List appointment additional info with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[AppointmentAdditionalInfo],
        )


__all__ = ["AppointmentAdditionalInfoResource"]
