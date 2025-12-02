"""Service person schema definitions for managing service providers.

This module contains Pydantic models for managing service providers/staff who
perform bookable services.
"""

from typing import Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel


class ServicePerson(BaseModel):
    """Service person schema - Complete service person record.

    Service provider/staff member who performs bookable services.

    Attributes:
        account_id: User account ID of the service person
        description: Description of the service person
        service_id: ID of the service this person provides

    Example:
        ```python
        person = ServicePerson(
            id="person_123",
            account_id="user_456",
            description="Licensed massage therapist with 10 years experience",
            service_id="service_789"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    account_id: str = Field(
        ...,
        description="User account ID linking this service provider to platform identity management",
        alias="accountId"
    )
    description: Optional[str] = Field(
        None,
        description="Professional bio displayed to customers during booking"
    )
    service_id: str = Field(
        ...,
        description="References Business Service from service-config that this person provides",
        alias="serviceId"
    )


class CreateServicePerson(BaseModel):
    """Schema for creating a new service person.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateServicePerson(
            account_id="user_123",
            description="Certified hair stylist specializing in modern cuts",
            service_id="service_456"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    account_id: str = Field(..., alias="accountId")
    description: Optional[str] = None
    service_id: str = Field(..., alias="serviceId")


class UpdateServicePerson(BaseModel):
    """Schema for updating an existing service person.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateServicePerson(
            id="person_123",
            description="Updated bio with new certifications"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    account_id: Optional[str] = Field(None, alias="accountId")
    description: Optional[str] = None
    service_id: Optional[str] = Field(None, alias="serviceId")
