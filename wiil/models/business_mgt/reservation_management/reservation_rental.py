"""Rental reservation schema definitions."""

from enum import Enum
from typing import Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    DepositStatus,
    ExternalRef,
)


class RentalReservationStatus(str, Enum):
    """Rental reservation lifecycle status."""

    UPCOMING = "upcoming"
    PICKUP_SOON = "pickup_soon"
    OUT = "out"
    RETURNED = "returned"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class RentalReservationPayment(BaseModel):
    """Payment summary for a rental reservation."""

    rental_charge: float = Field(..., ge=0, alias="rentalCharge")
    security_deposit: float = Field(..., ge=0, alias="securityDeposit")
    deposit_status: DepositStatus = Field(
        ...,
        alias="depositStatus",
    )


class ChecklistCompletion(BaseModel):
    """Checklist completion flags for pickup/return workflows."""

    item_id: str = Field(..., alias="itemId")
    completed: bool = False
    completed_at: Optional[int] = Field(None, alias="completedAt")
    completed_by: Optional[str] = Field(None, alias="completedBy")


class WaiverRef(BaseModel):
    """Waiver reference metadata."""

    waiver_id: str = Field(..., alias="waiverId")
    signed_at: Optional[int] = Field(None, alias="signedAt")
    status: Literal["required", "signed", "waived"] = "required"


class IDRef(BaseModel):
    """Identity verification reference."""

    verification_id: str = Field(..., alias="verificationId")
    provider: Optional[str] = None
    verified_at: Optional[int] = Field(None, alias="verifiedAt")
    status: Literal["required", "verified", "rejected"] = "required"


class RentalReservation(EntityModel):
    """Rental reservation schema."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    customer_id: str = Field(..., alias="customerId")
    resource_id: str = Field(..., alias="resourceId")
    tier_id: str = Field(..., alias="tierId")
    start_at: int = Field(..., alias="startAt")
    end_at: int = Field(..., alias="endAt")
    actual_return_at: Optional[int] = Field(None, alias="actualReturnAt")
    status: RentalReservationStatus = RentalReservationStatus.UPCOMING
    payment: RentalReservationPayment
    checklist_completions: list[ChecklistCompletion] = Field(
        default_factory=list,
        alias="checklistCompletions",
    )
    waiver: Optional[WaiverRef] = None
    id_verification: Optional[IDRef] = Field(None, alias="idVerification")
    notes: Optional[str] = None
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")

    @model_validator(mode="after")
    def validate_dates(self) -> "RentalReservation":
        if self.end_at <= self.start_at:
            raise ValueError("endAt must be greater than startAt")
        if (
            self.actual_return_at is not None
            and self.actual_return_at < self.start_at
        ):
            raise ValueError("actualReturnAt must be >= startAt")
        return self


class CreateRentalReservation(BaseModel):
    """Schema for creating rental reservations."""

    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    customer_id: str = Field(..., alias="customerId")
    resource_id: str = Field(..., alias="resourceId")
    tier_id: str = Field(..., alias="tierId")
    start_at: int = Field(..., alias="startAt")
    end_at: int = Field(..., alias="endAt")
    actual_return_at: Optional[int] = Field(None, alias="actualReturnAt")
    status: RentalReservationStatus = RentalReservationStatus.UPCOMING
    payment: RentalReservationPayment
    checklist_completions: list[ChecklistCompletion] = Field(
        default_factory=list,
        alias="checklistCompletions",
    )
    waiver: Optional[WaiverRef] = None
    id_verification: Optional[IDRef] = Field(None, alias="idVerification")
    notes: Optional[str] = None
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class UpdateRentalReservation(BaseModel):
    """Schema for updating rental reservations."""

    id: str
    location_id: Optional[str] = Field(None, alias="locationId")
    channel_id: Optional[str] = Field(None, alias="channelId")
    customer_id: Optional[str] = Field(None, alias="customerId")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    tier_id: Optional[str] = Field(None, alias="tierId")
    start_at: Optional[int] = Field(None, alias="startAt")
    end_at: Optional[int] = Field(None, alias="endAt")
    actual_return_at: Optional[int] = Field(None, alias="actualReturnAt")
    status: Optional[RentalReservationStatus] = None
    payment: Optional[RentalReservationPayment] = None
    checklist_completions: Optional[list[ChecklistCompletion]] = Field(
        None,
        alias="checklistCompletions",
    )
    waiver: Optional[WaiverRef] = None
    id_verification: Optional[IDRef] = Field(None, alias="idVerification")
    notes: Optional[str] = None
    external_ref: Optional[ExternalRef] = Field(None, alias="externalRef")


class DateRangeFilter(TypedDict, total=False):
    """Date range filter."""

    start: Optional[int]
    end: Optional[int]


class RentalReservationFilters(TypedDict, total=False):
    """Filters for rental reservation queries."""

    search: Optional[str]
    locationId: Optional[str]
    channelId: Optional[str]
    customerId: Optional[str]
    resourceId: Optional[str]
    tierId: Optional[list[str]]
    status: Optional[list[RentalReservationStatus]]
    depositStatus: Optional[list[DepositStatus]]
    dateRange: Optional[DateRangeFilter]
    externalSource: Optional[str]


class RentalReservationSorting(TypedDict):
    """Sorting options for rental reservations."""

    field: Literal["startAt", "endAt", "createdAt"]
    direction: Literal["asc", "desc"]


class RentalReservationQueryOptions(TypedDict, total=False):
    """Query options for rental reservation retrieval."""

    page: int
    pageSize: int
    filters: Optional[RentalReservationFilters]
    sorting: Optional[RentalReservationSorting]
