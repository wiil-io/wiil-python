# Reservation Management Guide (Python)

This guide covers reservation resources (tables, rooms, rentals) and customer reservations using the WIIL Python SDK.

## Quick Start

```python
from time import time

from wiil import WiilClient
from wiil.models.business_mgt import CreateReservation, CreateResource

client = WiilClient(api_key="your-api-key")
now_ms = int(time() * 1000)

table = client.reservation_resources.create(
    CreateResource(
        resource_type="table",
        name="Table 5",
        description="Window-side table for 4 guests",
        capacity=4,
        is_available=True,
        location="Main dining area",
        amenities=["Window view", "Booth seating"],
        reservation_duration=2,
        reservation_duration_unit="hours",
        sync_enabled=False,
    )
)

reservation = client.reservations.create(
    CreateReservation(
        reservation_type="table",
        resource_id=table.id,
        customer_id="cust_123",
        start_time=now_ms + 3600000,
        end_time=now_ms + 7200000,
        duration=2,
        persons_number=4,
        total_price=0,
        deposit_paid=0,
        notes="Window table preferred",
        is_resource_reservation=True,
    )
)

print("Resource:", table.id)
print("Reservation:", reservation.id)
```

## Reservation Resources

```python
from wiil.models.business_mgt import CreateResource, RoomResource, UpdateResource
from wiil.types import PaginationRequest

room = client.reservation_resources.create(
    CreateResource(
        resource_type="room",
        name="Room 101",
        capacity=2,
        reservation_duration=1,
        reservation_duration_unit="nights",
        room_resource=RoomResource(
            room_number="101",
            room_type="Deluxe King",
            price_per_night=299.99,
            bed_type="King",
            is_smoking=False,
        ),
    )
)

loaded = client.reservation_resources.get(room.id)
rooms = client.reservation_resources.get_by_type("room", PaginationRequest(page=1, page_size=20))

updated = client.reservation_resources.update(
    UpdateResource(id=room.id, is_available=False)
)

print(loaded.name, rooms.meta.total_count, updated.is_available)
```

## Reservations

```python
from wiil.models.business_mgt import CreateReservation, UpdateReservation
from wiil.types import PaginationRequest

reservation = client.reservations.create(
    CreateReservation(
        reservation_type="room",
        resource_id="resource_room101",
        customer_id="cust_456",
        start_time=int(time() * 1000),
        end_time=int(time() * 1000) + 3 * 24 * 60 * 60 * 1000,
        duration=3,
        persons_number=2,
        total_price=899.97,
        deposit_paid=299.99,
        is_resource_reservation=True,
    )
)

loaded = client.reservations.get(reservation.id)
by_customer = client.reservations.get_by_customer("cust_456", PaginationRequest(page=1, page_size=20))
by_resource = client.reservations.get_by_resource("resource_room101", PaginationRequest(page=1, page_size=20))

updated = client.reservations.update(
    UpdateReservation(id=reservation.id, persons_number=3, notes="Updated guest count")
)

status_updated = client.reservations.update_status(reservation.id, "confirmed")
rescheduled = client.reservations.reschedule(
    reservation.id,
    start_time=str(int(time() * 1000) + 48 * 60 * 60 * 1000),
    end_time=str(int(time() * 1000) + 49 * 60 * 60 * 1000),
)

print(loaded.id, by_customer.meta.total_count, by_resource.meta.total_count)
print(updated.persons_number, status_updated.status, rescheduled.start_time)
```
