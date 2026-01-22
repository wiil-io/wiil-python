"""Reservation resource schema definitions for various resource types.

This module contains Pydantic models for managing reservable resources including
rooms, rentals, and other bookable items with type-specific attributes.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.business_types import ResourceReservationDurationUnit, ResourceType


class RoomResource(PydanticBaseModel):
    """Room resource schema for hotel/accommodation bookings.

    Room-specific attributes for hotel and accommodation reservations.

    Attributes:
        room_number: Room number or identifier
        room_type: Type of room (e.g., Standard Queen, Deluxe King)
        price_per_night: Price per night for the room
        view: Room view (e.g., City View, Ocean View)
        bed_type: Type of bed (e.g., Queen, King, Twin)
        is_smoking: Whether smoking is allowed
        accessibility_features: Accessibility features available

    Example:
        ```python
        room = RoomResource(
            room_number="101",
            room_type="Deluxe King",
            price_per_night=150.00,
            view="Ocean View",
            bed_type="King",
            is_smoking=False,
            accessibility_features="Roll-in shower, grab bars"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    room_number: str = Field(
        ...,
        description="Unique room identifier or number (e.g., '101', 'Penthouse A')",
        alias="roomNumber"
    )
    room_type: str = Field(
        ...,
        description="Room category or class (e.g., 'Standard Queen', 'Deluxe King')",
        alias="roomType"
    )
    price_per_night: float = Field(
        ...,
        ge=0,
        description="Nightly rate for this room in the account's currency",
        alias="pricePerNight"
    )
    view: Optional[str] = Field(
        None,
        description="Room view classification (e.g., 'City View', 'Ocean View')"
    )
    bed_type: Optional[str] = Field(
        None,
        description="Bed configuration (e.g., 'Queen', 'King', 'Twin', '2 Double')",
        alias="bedType"
    )
    is_smoking: bool = Field(
        False,
        description="Whether smoking is permitted in this room",
        alias="isSmoking"
    )
    accessibility_features: Optional[str] = Field(
        None,
        description="ADA/accessibility accommodations available",
        alias="accessibilityFeatures"
    )


class RentalResource(PydanticBaseModel):
    """Rental resource schema for hourly rentals.

    Rental-specific attributes for hourly or time-based rentals.

    Attributes:
        item_type: Type of rental item (e.g., Game Room, Conference Room)
        price_per_hour: Hourly rate for this rental

    Example:
        ```python
        rental = RentalResource(
            item_type="Conference Room A",
            price_per_hour=50.00
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    item_type: str = Field(
        ...,
        description="Rental category or equipment type (e.g., 'Game Room', 'Conference Room')",
        alias="itemType"
    )
    price_per_hour: float = Field(
        ...,
        ge=0,
        description="Hourly rental rate in the account's currency",
        alias="pricePerHour"
    )


class Resource(BaseModel):
    """Main resource schema for managing reservable resources.

    Complete resource definition with type-specific attributes and availability tracking.

    Attributes:
        resource_type: Type of resource
        name: Name of the resource (table, room, etc.)
        description: Description of the resource
        capacity: Maximum capacity (e.g., number of people)
        is_available: Whether the resource is available for reservation
        location: Physical location of the resource
        amenities: Available amenities
        reservation_duration: Default reservation duration
        reservation_duration_unit: Unit of the default reservation duration
        calendar_id: Calendar ID for availability sync
        sync_enabled: Whether calendar sync is enabled
        last_sync_at: Last sync timestamp
        room_resource: Room-specific fields
        rental_resource: Rental-specific fields
        metadata: Additional metadata for other resource types

    Example:
        ```python
        resource = Resource(
            id="res_123",
            resource_type=ResourceType.TABLE,
            name="Table 5",
            description="Window table with ocean view",
            capacity=4,
            is_available=True,
            location="Main dining area",
            amenities=["Window view", "Booth seating"],
            reservation_duration=2,
            reservation_duration_unit=ResourceReservationDurationUnit.HOURS
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    resource_type: ResourceType = Field(
        ...,
        description="Category of reservable resource: ROOM, TABLE, RENTAL, or OTHER",
        alias="resourceType"
    )
    name: str = Field(
        ...,
        description="Display name of the resource (e.g., 'Table 5', 'Conference Room A')"
    )
    description: Optional[str] = Field(
        None,
        description="Detailed description of the resource including features and characteristics"
    )
    capacity: Optional[int] = Field(
        None,
        gt=0,
        description="Maximum occupancy or party size for this resource"
    )
    is_available: bool = Field(
        True,
        description="Whether this resource is currently active and available for reservations",
        alias="isAvailable"
    )
    location: Optional[str] = Field(
        None,
        description="Physical location or placement (e.g., 'Window side', 'Third floor')"
    )
    amenities: List[str] = Field(
        default_factory=list,
        description="List of available features or amenities"
    )
    reservation_duration: Optional[int] = Field(
        None,
        gt=0,
        description="Default or standard reservation length in specified units",
        alias="reservationDuration"
    )
    reservation_duration_unit: Optional[ResourceReservationDurationUnit] = Field(
        None,
        description="Time unit for reservationDuration: HOURS, DAYS, or MINUTES",
        alias="reservationDurationUnit"
    )
    calendar_id: Optional[str] = Field(
        None,
        description="External calendar system ID for real-time availability synchronization",
        alias="calendarId"
    )
    sync_enabled: Optional[bool] = Field(
        False,
        description="Whether automatic calendar synchronization is active for this resource",
        alias="syncEnabled"
    )
    last_sync_at: Optional[int] = Field(
        None,
        description="Unix timestamp of most recent calendar synchronization",
        alias="lastSyncAt"
    )
    room_resource: Optional[RoomResource] = Field(
        None,
        description="Hotel/accommodation-specific fields. Only populated when resourceType is ROOM",
        alias="roomResource"
    )
    rental_resource: Optional[RentalResource] = Field(
        None,
        description="Hourly rental-specific fields. Only populated when resourceType is RENTAL",
        alias="rentalResource"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Extensible key-value storage for custom resource attributes"
    )


class CreateResource(BaseModel):
    """Schema for creating a new resource.

    Omits auto-generated fields (id, created_at, updated_at).

    Example:
        ```python
        create_data = CreateResource(
            resource_type=ResourceType.ROOM,
            name="Room 101",
            description="Standard room with city view",
            capacity=2,
            is_available=True,
            room_resource=RoomResource(
                room_number="101",
                room_type="Standard",
                price_per_night=120.00,
                bed_type="Queen"
            )
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    resource_type: ResourceType = Field(..., alias="resourceType")
    name: str
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    is_available: bool = Field(True, alias="isAvailable")
    location: Optional[str] = None
    amenities: List[str] = Field(default_factory=list)
    reservation_duration: Optional[int] = Field(None, gt=0, alias="reservationDuration")
    reservation_duration_unit: Optional[ResourceReservationDurationUnit] = Field(
        None,
        alias="reservationDurationUnit"
    )
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    room_resource: Optional[RoomResource] = Field(None, alias="roomResource")
    rental_resource: Optional[RentalResource] = Field(None, alias="rentalResource")
    metadata: Optional[Dict[str, Any]] = None


class UpdateResource(BaseModel):
    """Schema for updating an existing resource.

    All fields are optional except id.

    Example:
        ```python
        update_data = UpdateResource(
            id="res_123",
            is_available=False,
            notes="Under maintenance until next week"
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    resource_type: Optional[ResourceType] = Field(None, alias="resourceType")
    name: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    location: Optional[str] = None
    amenities: Optional[List[str]] = None
    reservation_duration: Optional[int] = Field(None, gt=0, alias="reservationDuration")
    reservation_duration_unit: Optional[ResourceReservationDurationUnit] = Field(
        None,
        alias="reservationDurationUnit"
    )
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    sync_enabled: Optional[bool] = Field(None, alias="syncEnabled")
    last_sync_at: Optional[int] = Field(None, alias="lastSyncAt")
    room_resource: Optional[RoomResource] = Field(None, alias="roomResource")
    rental_resource: Optional[RentalResource] = Field(None, alias="rentalResource")
    metadata: Optional[Dict[str, Any]] = None
