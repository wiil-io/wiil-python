"""Organization-level appointment field configuration schema."""

from typing import Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions import BusinessSupportServices
from wiil.models.type_definitions.dynamic_fields import (
    FieldDefinition,
    FieldGroup,
)


class AppointmentFieldConfig(EntityModel):
    """Organization-level appointment field library."""

    fields: list[FieldDefinition] = Field(default_factory=list)
    groups: list[FieldGroup] = Field(default_factory=list)
    reuse_details: bool = Field(False, alias="reuseDetails")
    ensure_email: bool = Field(False, alias="ensureEmail")
    ensure_phone: bool = Field(False, alias="ensurePhone")
    support_service: Optional[BusinessSupportServices] = Field(
        None,
        alias="supportService",
        description=(
            "Business support service this field configuration applies to "
            "(e.g., appointment management)."
        ),
    )


class CreateAppointmentFieldConfig(BaseModel):
    """Schema for creating appointment field config."""

    fields: list[FieldDefinition] = Field(default_factory=list)
    groups: list[FieldGroup] = Field(default_factory=list)
    reuse_details: bool = Field(False, alias="reuseDetails")
    ensure_email: bool = Field(False, alias="ensureEmail")
    ensure_phone: bool = Field(False, alias="ensurePhone")
    support_service: Optional[BusinessSupportServices] = Field(
        None,
        alias="supportService",
        description=(
            "Business support service this field configuration applies to "
            "(e.g., appointment management)."
        ),
    )


class UpdateAppointmentFieldConfig(BaseModel):
    """Schema for updating appointment field config."""

    id: str
    fields: Optional[list[FieldDefinition]] = None
    groups: Optional[list[FieldGroup]] = None
    reuse_details: Optional[bool] = Field(None, alias="reuseDetails")
    ensure_email: Optional[bool] = Field(None, alias="ensureEmail")
    ensure_phone: Optional[bool] = Field(None, alias="ensurePhone")
    support_service: Optional[BusinessSupportServices] = Field(
        None,
        alias="supportService",
        description=(
            "Business support service this field configuration applies to "
            "(e.g., appointment management)."
        ),
    )


class AppointmentFieldConfigFilters(TypedDict, total=False):
    """Filter options for appointment field config queries."""

    reuseDetails: Optional[bool]
    ensureEmail: Optional[bool]
    ensurePhone: Optional[bool]


class AppointmentFieldConfigSorting(TypedDict):
    """Sorting options for appointment field config queries."""

    field: str
    direction: str


class AppointmentFieldConfigQueryOptions(TypedDict, total=False):
    """Query options for appointment field config retrieval."""

    page: int
    pageSize: int
    filters: Optional[AppointmentFieldConfigFilters]
    sorting: Optional[AppointmentFieldConfigSorting]
