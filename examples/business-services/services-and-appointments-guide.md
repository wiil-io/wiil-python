# Business Services and Appointments Guide (Python)

Manage services and schedule appointments for service-based businesses using the WIIL Python SDK.

## Prerequisites

- Python 3.9+
- `wiil` package installed
- WIIL API key

```python
from wiil import WiilClient

client = WiilClient(api_key="your-api-key")
```

## Quick Start

```python
from time import time

from wiil.models.business_mgt import CreateBusinessService, CreateServiceAppointment

service = client.business_services.create(
    CreateBusinessService(
        name="Professional Haircut",
        description="Premium haircut service with styling",
        duration=45,
        buffer_time=15,
        price=50.00,
        is_bookable=True,
        is_active=True,
    )
)

start_time = int(time() * 1000) + 24 * 60 * 60 * 1000
appointment = client.service_appointments.create(
    CreateServiceAppointment(
        business_service_id=service.id,
        customer_id="cust_123",
        start_time=start_time,
        end_time=start_time + (45 * 60 * 1000),
        duration=45,
        total_price=50.00,
        deposit_paid=0,
    )
)

confirmed = client.service_appointments.update_status(appointment.id, "confirmed")
print(service.id, appointment.id, confirmed.status)
```

## Business Services

```python
from wiil.models.business_mgt import CreateBusinessService, UpdateBusinessService
from wiil.types import PaginationRequest

service = client.business_services.create(
    CreateBusinessService(
        name="Massage Therapy",
        description="60-minute therapeutic massage",
        duration=60,
        buffer_time=10,
        price=80.00,
        display_order=2,
    )
)

loaded = client.business_services.get(service.id)
services = client.business_services.list(PaginationRequest(page=1, page_size=20))

updated = client.business_services.update(
    UpdateBusinessService(id=service.id, name="Premium Massage Therapy", price=90.00)
)

qr = client.business_services.generate_qr_code(service_id=updated.id)
deleted = client.business_services.delete(updated.id)

print(loaded.name, services.meta.total_count, qr.appointment_url, deleted)
```

## Service Appointments

```python
from time import time

from wiil.models.business_mgt import CreateServiceAppointment
from wiil.types import PaginationRequest

start_ms = int(time() * 1000) + 3600000
appointment = client.service_appointments.create(
    CreateServiceAppointment(
        business_service_id="service_123",
        customer_id="cust_456",
        start_time=start_ms,
        end_time=start_ms + 60 * 60 * 1000,
        duration=60,
        total_price=80.00,
        deposit_paid=20.00,
    )
)

loaded = client.service_appointments.get(appointment.id)
customer_appointments = client.service_appointments.get_by_customer(
    "cust_456", PaginationRequest(page=1, page_size=20)
)
service_appointments = client.service_appointments.get_by_service(
    "service_123", PaginationRequest(page=1, page_size=20)
)

rescheduled = client.service_appointments.reschedule(
    appointment.id,
    start_time=str(int(time() * 1000) + 48 * 60 * 60 * 1000),
    end_time=str(int(time() * 1000) + 49 * 60 * 60 * 1000),
)

cancelled = client.service_appointments.cancel(appointment.id, reason="Customer requested cancellation")

print(loaded.id)
print(customer_appointments.meta.total_count, service_appointments.meta.total_count)
print(rescheduled.start_time, cancelled.status)
```

## Batch Operations

Create multiple business services in a single request.

### Create Services in Batch

```python
from wiil.models.business_mgt import CreateBusinessService

services = client.business_services.create_batch([
    CreateBusinessService(
        name="30-Minute Massage",
        description="Relaxation massage",
        duration=30,
        price=50.00,
        is_bookable=True,
    ),
    CreateBusinessService(
        name="60-Minute Massage",
        description="Deep tissue massage",
        duration=60,
        price=80.00,
        is_bookable=True,
    ),
    CreateBusinessService(
        name="90-Minute Massage",
        description="Full body therapeutic massage",
        duration=90,
        price=110.00,
        is_bookable=True,
    ),
])

print(f"Created {len(services.data)} services")
for service in services.data:
    print(f"  - {service.name}: ${service.price}")
```

**Limits:** Maximum 50 services per batch

### Handling Batch Errors

Batch operations validate each item and report errors with index information:

```python
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import CreateBusinessService

try:
    services = client.business_services.create_batch([
        CreateBusinessService(name="Valid Service", duration=30, price=25.00),
        CreateBusinessService(name="", duration=30, price=25.00),  # Invalid: empty name
    ])
except WiilValidationError as e:
    print(f"Validation error: {e.message}")
    for detail in e.details:
        print(f"  - {detail}")
```

## Common Status Values

- Appointments: `"pending"`, `"confirmed"`, `"completed"`, `"cancelled"`, `"no_show"`
- Reservations: `"pending"`, `"confirmed"`, `"cancelled"`, `"completed"`
- Orders: `"pending"`, `"confirmed"`, `"preparing"`, `"completed"`, `"cancelled"`
