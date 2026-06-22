"""Generic reservation schema definitions for compatibility."""

from typing import Optional

from pydantic import Field

from wiil.models.base import BaseModel
from wiil.models.type_definitions.business_definitions import ResourceType
from wiil.types.business_types import AppointmentStatus


class Reservation(BaseModel):
    """Generic reservation schema."""

    reservation_type: ResourceType = Field(..., alias="reservationType")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    customer_id: str = Field(..., alias="customerId")
    start_time: int = Field(..., alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[float] = Field(None, ge=0)
    persons_number: Optional[int] = Field(None, ge=0, alias="personsNumber")
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    deposit_paid: float = Field(0.0, ge=0, alias="depositPaid")
    status: AppointmentStatus = AppointmentStatus.PENDING
    notes: Optional[str] = None
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    is_resource_reservation: bool = Field(False, alias="isResourceReservation")


class CreateReservation(BaseModel):
    """Schema for creating generic reservations."""

    reservation_type: ResourceType = Field(..., alias="reservationType")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    customer_id: str = Field(..., alias="customerId")
    start_time: int = Field(..., alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[float] = Field(None, ge=0)
    persons_number: Optional[int] = Field(None, ge=0, alias="personsNumber")
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    deposit_paid: float = Field(0.0, ge=0, alias="depositPaid")
    notes: Optional[str] = None
    is_resource_reservation: bool = Field(False, alias="isResourceReservation")


class UpdateReservation(BaseModel):
    """Schema for updating generic reservations."""

    id: str
    reservation_type: Optional[ResourceType] = Field(
        None,
        alias="reservationType",
    )
    resource_id: Optional[str] = Field(None, alias="resourceId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    start_time: Optional[int] = Field(None, alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    duration: Optional[float] = Field(None, ge=0)
    persons_number: Optional[int] = Field(None, ge=0, alias="personsNumber")
    total_price: Optional[float] = Field(None, ge=0, alias="totalPrice")
    deposit_paid: Optional[float] = Field(None, ge=0, alias="depositPaid")
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    cancel_reason: Optional[str] = Field(None, alias="cancelReason")
    is_resource_reservation: Optional[bool] = Field(
        None,
        alias="isResourceReservation",
    )
