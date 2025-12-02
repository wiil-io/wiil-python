"""Business service configuration schema definitions.

This module contains Pydantic models for managing business service configurations
and QR codes for appointment booking.
"""

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel


class BusinessServiceConfig(BaseModel):
    """Business service configuration schema.

    Service offered by the business with scheduling, pricing, and availability settings.

    Attributes:
        name: Name of the service offered
        description: Detailed description of the service
        duration: Service duration in minutes (max 8 hours)
        buffer_time: Buffer time between appointments in minutes
        is_bookable: Whether this service can be booked online
        price: Service price in account currency
        is_active: Whether the service is currently available
        display_order: Display order in service listings

    Example:
        ```python
        service = BusinessServiceConfig(
            id="service_123",
            name="Massage Therapy",
            description="60-minute relaxation massage",
            duration=60,
            buffer_time=15,
            is_bookable=True,
            price=90.00,
            is_active=True,
            display_order=1
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        min_length=1,
        description="Display name of the service offered"
    )
    description: Optional[str] = Field(
        None,
        description="Detailed description of the service including what's included"
    )
    duration: int = Field(
        60,
        gt=0,
        le=480,
        description="Service duration in minutes with maximum of 480 minutes (8 hours)"
    )
    buffer_time: int = Field(
        0,
        ge=0,
        description="Buffer time in minutes between consecutive appointments",
        alias="bufferTime"
    )
    is_bookable: bool = Field(
        True,
        description="Whether this service can be booked online through AI Powered Services",
        alias="isBookable"
    )
    price: Optional[float] = Field(
        0.0,
        ge=0,
        description="Service price in the account's currency"
    )
    is_active: bool = Field(
        True,
        description="Whether the service is currently active and available for booking",
        alias="isActive"
    )
    display_order: Optional[int] = Field(
        None,
        description="Display order in service listings and booking interfaces",
        alias="displayOrder"
    )


class ServiceQRCode(PydanticBaseModel):
    """Service QR code schema for appointment booking.

    QR code configuration for accessing service appointment booking interface.

    Attributes:
        id: Unique identifier for the QR code
        appointment_url: Direct link to the appointment page
        qr_code_image: Base64 encoded QR code image
        service_id: Specific service ID for direct appointment

    Example:
        ```python
        qr_code = ServiceQRCode(
            id="qr_123",
            appointment_url="https://book.example.com/services",
            service_id="service_456"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str = Field(..., description="Unique identifier for this QR code instance")
    appointment_url: str = Field(
        ...,
        description="URL to the appointment booking interface accessed by scanning",
        alias="appointmentUrl"
    )
    qr_code_image: Optional[str] = Field(
        None,
        description="Base64 encoded QR code image for printing or digital display",
        alias="qrCodeImage"
    )
    service_id: Optional[str] = Field(
        None,
        description="Optional specific Business Service ID for direct appointment booking",
        alias="serviceId"
    )


class CreateBusinessService(BaseModel):
    """Schema for creating a new business service.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateBusinessService(
            name="Hair Cut",
            description="Professional hair cutting service",
            duration=30,
            buffer_time=10,
            is_bookable=True,
            price=35.00,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    duration: int = Field(60, gt=0, le=480)
    buffer_time: int = Field(0, ge=0, alias="bufferTime")
    is_bookable: bool = Field(True, alias="isBookable")
    price: Optional[float] = Field(0.0, ge=0)
    is_active: bool = Field(True, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdateBusinessService(BaseModel):
    """Schema for updating an existing business service.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateBusinessService(
            id="service_123",
            price=40.00,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    duration: Optional[int] = Field(None, gt=0, le=480)
    buffer_time: Optional[int] = Field(None, ge=0, alias="bufferTime")
    is_bookable: Optional[bool] = Field(None, alias="isBookable")
    price: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = Field(None, alias="isActive")
    display_order: Optional[int] = Field(None, alias="displayOrder")
