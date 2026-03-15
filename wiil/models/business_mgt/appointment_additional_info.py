"""Appointment Additional Info schema for storing dynamic field values.

This module mirrors src/core/business-mgt/appointment-additional-info.schema.ts

This schema represents the **Appointment Level** in the dynamic fields hierarchy:

```
Organization Level (AppointmentFieldConfig)
        │
        ▼ inherits via appointmentFieldConfigId
Service Level (ServiceAppointmentFieldConfig)
        │
        ▼ stores values
Appointment Level (AppointmentAdditionalInfo) ← THIS SCHEMA
```

Stores the actual captured field values for a specific appointment instance.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel


class AppointmentAdditionalInfo(BaseModel):
    """Appointment additional info for storing dynamic field values.

    Links captured data to the organization, service, appointment, and customer.
    The `data` property contains key-value pairs where keys correspond to `field_key`
    values defined in the organization and service-level field configurations.

    Attributes:
        id: Unique identifier
        organization_id: Reference to the organization
        business_service_id: Reference to the business service
        appointment_id: Reference to the appointment instance
        customer_id: Reference to the customer who provided the information
        data: Key-value store of captured field values
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        info = AppointmentAdditionalInfo(
            id="info-123",
            organization_id="org-456",
            business_service_id="svc-789",
            appointment_id="apt-101",
            customer_id="cust-202",
            data={
                "preferred_time": "morning",
                "special_requirements": "wheelchair accessible",
                "insurance_number": "INS-12345"
            }
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    organization_id: str = Field(
        ...,
        description="Reference to the organization that owns this appointment data",
        alias="organizationId"
    )
    business_service_id: str = Field(
        ...,
        description="Reference to the business service for this appointment",
        alias="businessServiceId"
    )
    appointment_id: str = Field(
        ...,
        description="Reference to the appointment instance these field values belong to",
        alias="appointmentId"
    )
    customer_id: str = Field(
        ...,
        description="Reference to the customer who provided this information",
        alias="customerId"
    )
    data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value store of captured field values"
    )


class CreateAppointmentAdditionalInfo(PydanticBaseModel):
    """Schema for creating appointment additional info.

    Omits auto-generated fields (id, timestamps).

    Example:
        ```python
        create_data = CreateAppointmentAdditionalInfo(
            organization_id="org-456",
            business_service_id="svc-789",
            appointment_id="apt-101",
            customer_id="cust-202",
            data={"preferred_time": "morning"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    organization_id: str = Field(..., alias="organizationId")
    business_service_id: str = Field(..., alias="businessServiceId")
    appointment_id: str = Field(..., alias="appointmentId")
    customer_id: str = Field(..., alias="customerId")
    data: Dict[str, Any] = Field(default_factory=dict)


class UpdateAppointmentAdditionalInfo(PydanticBaseModel):
    """Schema for updating appointment additional info.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateAppointmentAdditionalInfo(
            id="info-123",
            data={"preferred_time": "afternoon", "notes": "Updated"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    organization_id: Optional[str] = Field(None, alias="organizationId")
    business_service_id: Optional[str] = Field(None, alias="businessServiceId")
    appointment_id: Optional[str] = Field(None, alias="appointmentId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    data: Optional[Dict[str, Any]] = None
