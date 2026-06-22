"""Appointment field configs resource for organization-level field libraries."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    AppointmentFieldConfig,
    CreateAppointmentFieldConfig,
    UpdateAppointmentFieldConfig,
)
from wiil.types import PaginatedResult, PaginationRequest


class AppointmentFieldConfigsResource:
    """Resource class for appointment field configurations.

    Provides methods for creating, retrieving, updating, deleting, and listing
    appointment field configurations. These define organization-level field
    libraries for appointment booking forms, including field definitions,
    groupings, and customer data reuse settings.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/appointment-field-configs"

    def create(
        self, data: CreateAppointmentFieldConfig
    ) -> AppointmentFieldConfig:
        """Create a new appointment field configuration."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateAppointmentFieldConfig,
            response_model=AppointmentFieldConfig,
        )

    def get(self, config_id: str) -> AppointmentFieldConfig:
        """Retrieve an appointment field configuration by ID."""
        return self._http.get(
            f"{self._base_path}/{config_id}",
            response_model=AppointmentFieldConfig,
        )

    def get_with_email_required(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentFieldConfig]:
        """List appointment field configurations that require email."""
        query_params: Dict[str, Any] = {"ensureEmail": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/with-email-required?{urlencode(query_params)}",
            response_model=PaginatedResult[AppointmentFieldConfig],
        )

    def get_with_phone_required(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentFieldConfig]:
        """List appointment field configurations that require phone."""
        query_params: Dict[str, Any] = {"ensurePhone": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/with-phone-required?{urlencode(query_params)}",
            response_model=PaginatedResult[AppointmentFieldConfig],
        )

    def get_with_reuse_enabled(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentFieldConfig]:
        """List appointment field configurations with reuse details enabled."""
        query_params: Dict[str, Any] = {"reuseDetails": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/with-reuse-enabled?{urlencode(query_params)}",
            response_model=PaginatedResult[AppointmentFieldConfig],
        )

    def update(
        self, data: UpdateAppointmentFieldConfig
    ) -> AppointmentFieldConfig:
        """Update an existing appointment field configuration."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateAppointmentFieldConfig,
            response_model=AppointmentFieldConfig,
        )

    def delete(self, config_id: str) -> bool:
        """Delete an appointment field configuration."""
        return self._http.delete(f"{self._base_path}/{config_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[AppointmentFieldConfig]:
        """List appointment field configurations with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[AppointmentFieldConfig],
        )


__all__ = ["AppointmentFieldConfigsResource"]
