"""Organization-level appointment field configuration schema.

This module mirrors src/core/business-mgt/appointment-field-config.schema.ts

This schema represents the **Organization Level** in the dynamic fields hierarchy:

```
Organization Level (AppointmentFieldConfig) ← THIS SCHEMA
        │
        ▼ inherits via appointmentFieldConfigId
Service Level (ServiceAppointmentFieldConfig)
        │
        ▼ stores values
Appointment Level (AppointmentAdditionalInfo)
```

Defines the base field library that can be reused across multiple services
within an organization.
"""

from typing import List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.type_definitions.dynamic_fields import FieldDefinition, FieldGroup


class AppointmentFieldConfig(BaseModel):
    """Organization-level appointment field configuration.

    Defines the base field library available to all services within an organization.
    Services reference this configuration via `appointment_field_config_id` and can
    selectively inherit, override, or extend the defined fields.

    Attributes:
        id: Unique identifier
        fields: Array of field definitions available at the organization level
        groups: Logical groupings for organizing fields into sections
        reuse_details: Whether captured field data can be reused across appointments
        ensure_email: Whether to ensure an email field is always included
        ensure_phone: Whether to ensure a phone field is always included
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        config = AppointmentFieldConfig(
            id="config-123",
            fields=[
                FieldDefinition(
                    field_key="insurance_number",
                    field_type=DynamicFieldType.TEXT,
                    label="Insurance Number"
                )
            ],
            groups=[
                FieldGroup(
                    group_key="medical",
                    label="Medical Information"
                )
            ],
            reuse_details=True,
            ensure_email=True,
            ensure_phone=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    fields: List[FieldDefinition] = Field(
        default_factory=list,
        description="Array of field definitions available at the organization level"
    )
    groups: List[FieldGroup] = Field(
        default_factory=list,
        description="Logical groupings for organizing fields into sections"
    )
    reuse_details: bool = Field(
        False,
        description="Whether captured field data can be reused across appointments for the same customer",
        alias="reuseDetails"
    )
    ensure_email: bool = Field(
        False,
        description="Whether to ensure an email field is always included",
        alias="ensureEmail"
    )
    ensure_phone: bool = Field(
        False,
        description="Whether to ensure a phone field is always included",
        alias="ensurePhone"
    )


class CreateAppointmentFieldConfig(PydanticBaseModel):
    """Schema for creating appointment field configuration.

    Omits auto-generated timestamp fields but allows id for explicit setting.

    Example:
        ```python
        create_data = CreateAppointmentFieldConfig(
            fields=[...],
            groups=[...],
            reuse_details=True,
            ensure_email=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: Optional[str] = None
    fields: List[FieldDefinition] = Field(default_factory=list)
    groups: List[FieldGroup] = Field(default_factory=list)
    reuse_details: bool = Field(False, alias="reuseDetails")
    ensure_email: bool = Field(False, alias="ensureEmail")
    ensure_phone: bool = Field(False, alias="ensurePhone")


class UpdateAppointmentFieldConfig(PydanticBaseModel):
    """Schema for updating appointment field configuration.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateAppointmentFieldConfig(
            id="config-123",
            reuse_details=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    fields: Optional[List[FieldDefinition]] = None
    groups: Optional[List[FieldGroup]] = None
    reuse_details: Optional[bool] = Field(None, alias="reuseDetails")
    ensure_email: Optional[bool] = Field(None, alias="ensureEmail")
    ensure_phone: Optional[bool] = Field(None, alias="ensurePhone")
