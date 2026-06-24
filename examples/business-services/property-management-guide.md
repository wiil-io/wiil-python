# Property Management Guide (Python)

This guide covers managing real-estate property data and customer inquiries using the WIIL Python SDK.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateProperty,
    CreatePropertyAddress,
    CreatePropertyCategory,
)

client = WiilClient(api_key="your-api-key")
property_config = client.property_config
property_inquiry = client.property_inquiry

category = property_config.create_category(
    CreatePropertyCategory(
        name="Luxury Homes",
        description="High-end residential listings",
        property_type="residential",
        display_order=1,
    )
)

address = property_config.create_address(
    CreatePropertyAddress(
        street="123 Ocean View Drive",
        city="Miami",
        state="FL",
        postal_code="33139",
        country="USA",
    )
)

property_listing = property_config.create(
    CreateProperty(
        category_id=category.id,
        address_id=address.id,
        title="Stunning Oceanfront Villa",
        description="Luxury 5-bedroom villa with panoramic ocean views",
        property_type="residential",
        property_sub_type="villa",
        listing_type="sale",
        listing_status="active",
        sale_price=2500000,
        sale_price_currency="USD",
        is_active=True,
    )
)

print("Property created:", property_listing.id)
```

## Categories and Addresses

```python
from wiil.models.business_mgt import (
    CreatePropertyAddress,
    CreatePropertyCategory,
    UpdatePropertyAddress,
    UpdatePropertyCategory,
)
from wiil.types import PaginationRequest

category = property_config.create_category(
    CreatePropertyCategory(name="Commercial", property_type="commercial")
)

categories = property_config.list_categories(PaginationRequest(page=1, page_size=20))
category = property_config.get_category(category.id)

category = property_config.update_category(
    UpdatePropertyCategory(id=category.id, name="Premium Commercial")
)

address = property_config.create_address(
    CreatePropertyAddress(
        street="456 Park Avenue",
        city="New York",
        state="NY",
        postal_code="10022",
        country="USA",
        is_verified=False,
    )
)

address = property_config.verify_address(address.id)
address = property_config.update_address(
    UpdatePropertyAddress(id=address.id, neighborhood="Midtown East")
)

print(categories.meta.total_count, category.name, address.is_verified)
```

## Properties and Search

```python
from wiil.models.business_mgt import CreateProperty, UpdateProperty
from wiil.types import PaginationRequest

prop = property_config.create(
    CreateProperty(
        category_id="cat_123",
        address_id="addr_123",
        title="Downtown Office Suite",
        property_type="commercial",
        property_sub_type="office",
        listing_type="rent",
        rental_price=4500,
        rental_period="monthly",
    )
)

loaded = property_config.get(prop.id)
all_properties = property_config.list(PaginationRequest(page=1, page_size=20))
category_properties = property_config.get_by_category("cat_123", PaginationRequest(page=1, page_size=20))
search_results = property_config.search("office", PaginationRequest(page=1, page_size=20))

updated = property_config.update(
    UpdateProperty(id=prop.id, listing_status="under_offer", is_featured=True)
)

deleted = property_config.delete(updated.id)
print(loaded.title, all_properties.meta.total_count, category_properties.meta.total_count, search_results.meta.total_count, deleted)
```

## Property Inquiries

```python
from wiil.models.business_mgt import (
    CreatePropertyInquiry,
    UpdatePropertyInquiry,
    UpdatePropertyInquiryStatus,
)
from wiil.models.type_definitions import PropertyInquiryType, PropertyInquiryStatus
from wiil.types import PaginationRequest

inquiry = property_inquiry.create(
    CreatePropertyInquiry(
        property_id="property_123",
        customer_id="cust_456",
        inquiry_type=PropertyInquiryType.GENERAL,
        message="Is this property still available?",
    )
)

by_property = property_inquiry.get_by_property(
    "property_123", PaginationRequest(page=1, page_size=20)
)

updated = property_inquiry.update(
    UpdatePropertyInquiry(id=inquiry.id, notes="Customer requested weekend viewing")
)

status_updated = property_inquiry.update_status(
    inquiry.id,
    UpdatePropertyInquiryStatus(
        id=inquiry.id,
        status=PropertyInquiryStatus.IN_PROGRESS,
    )
)
print(by_property.meta.total_count, updated.id, status_updated.status)
```

## Viewing Slots

Query available viewing slots for a property and schedule viewings using the slot's UTC timestamp.

```python
from datetime import datetime
from wiil.models.business_mgt import CreatePropertyInquiry, UpdatePropertyInquiryStatus
from wiil.models.type_definitions import PropertyInquiryType, PropertyInquiryStatus

# Get available viewing slots for a property on a specific date
slots_response = property_inquiry.get_viewing_slots(
    property_id="property_123",
    local_date="2026-06-25"
)

print(f"Timezone: {slots_response.timezone}")
print(f"Available slots for {slots_response.local_date}:")

for slot in slots_response.slots:
    print(f"  {slot.start_time_of_day} - Provider: {slot.provider_id}")
    print(f"    UTC start: {slot.start_time_utc_sec}")

# Schedule a viewing using the slot's start_time_utc_sec
if slots_response.slots:
    selected_slot = slots_response.slots[0]
    
    # Use start_time_utc_sec directly for scheduling (already in UTC seconds)
    inquiry = property_inquiry.create(
        CreatePropertyInquiry(
            property_id="property_123",
            customer_id="cust_456",
            inquiry_type=PropertyInquiryType.GENERAL,
            message="I'd like to schedule a viewing",
            scheduled_viewing_date=selected_slot.start_time_utc_sec,
            assigned_agent_id=selected_slot.provider_id,
        )
    )
    
    # Update status to viewing scheduled
    property_inquiry.update_status(
        inquiry.id,
        UpdatePropertyInquiryStatus(
            id=inquiry.id,
            status=PropertyInquiryStatus.VIEWING_SCHEDULED,
            scheduled_viewing_date=selected_slot.start_time_utc_sec,
        )
    )
    
    # For display purposes only, convert to datetime
    viewing_time = datetime.utcfromtimestamp(selected_slot.start_time_utc_sec)
    print(f"Viewing scheduled for: {viewing_time.isoformat()}")
```

**Timestamp Format:** All timestamps use UTC seconds. The `start_time_utc_sec` value from slots passes directly to API calls—no conversion needed. Only multiply by 1000 when converting to millisecond-based APIs for display.

## Batch Operations

Create multiple property categories, addresses, and properties efficiently.

### Create Categories in Batch

```python
from wiil.models.business_mgt import CreatePropertyCategory

categories = property_config.create_category_batch([
    CreatePropertyCategory(name="Apartments", property_type="residential", display_order=1),
    CreatePropertyCategory(name="Houses", property_type="residential", display_order=2),
    CreatePropertyCategory(name="Commercial", property_type="commercial", display_order=3),
])

print(f"Created {len(categories.data)} categories")
for category in categories.data:
    print(f"  - {category.name}")
```

**Limits:** Maximum 50 categories per batch

### Create Addresses in Batch

```python
from wiil.models.business_mgt import CreatePropertyAddress

addresses = property_config.create_address_batch([
    CreatePropertyAddress(
        street="123 Main St",
        city="New York",
        state="NY",
        postal_code="10001",
        country="US",
    ),
    CreatePropertyAddress(
        street="456 Oak Ave",
        city="Los Angeles",
        state="CA",
        postal_code="90001",
        country="US",
    ),
    CreatePropertyAddress(
        street="789 Beach Blvd",
        city="Miami",
        state="FL",
        postal_code="33139",
        country="US",
    ),
])

print(f"Created {len(addresses.data)} addresses")
for address in addresses.data:
    print(f"  - {address.street}, {address.city}")
```

**Limits:** Maximum 50 addresses per batch

### Create Properties in Batch

```python
from wiil.models.business_mgt import CreateProperty

properties = property_config.create_batch([
    CreateProperty(
        title="Downtown Loft",
        description="Modern 2BR loft in city center",
        category_id="cat_apartments",
        address_id="addr_nyc",
        property_type="residential",
        listing_type="rent",
        rental_price=2500,
        rental_period="monthly",
    ),
    CreateProperty(
        title="Beach House",
        description="3BR oceanfront property",
        category_id="cat_houses",
        address_id="addr_miami",
        property_type="residential",
        listing_type="sale",
        sale_price=750000,
        sale_price_currency="USD",
    ),
])

print(f"Created {len(properties.data)} properties")
for prop in properties.data:
    print(f"  - {prop.title}")
```

**Limits:** Maximum 50 properties per batch

### Handling Batch Errors

Batch operations validate each item and report errors with index information:

```python
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import CreateProperty

try:
    properties = property_config.create_batch([
        CreateProperty(title="Valid Property", property_type="residential"),
        CreateProperty(title="", property_type="residential"),  # Invalid: empty title
    ])
except WiilValidationError as e:
    print(f"Validation error: {e.message}")
    for detail in e.details:
        print(f"  - {detail}")
```
