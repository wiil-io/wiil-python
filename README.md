# WIIL Python SDK

Ship AI-powered business features without building telecom, catalog infrastructure, or integration plumbing.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## What You Can Ship

This SDK gives you APIs to build:

- **Catalog-aware AI agents** - Agents grounded in real business data such as menus, products, services, reservations, and properties
- **Multi-channel conversations** - Web, phone, SMS, and email workflows through unified APIs
- **Transaction workflows** - Appointments, reservations, orders, inquiries, and outbound follow-ups
- **Outbound communications** - Automated calls, emails, and SMS without provider setup

What you skip building:

- Telephony integration, SMS gateways, SMTP servers
- Voice pipeline infrastructure for STT, LLM, and TTS workflows
- Catalog schema design and multi-location logic
- Retry logic, queue management, and delivery tracking
- Channel-specific protocols and failure handling

**You write the business logic. The SDK handles the infrastructure.**

---

## Installation

```bash
pip install wiil-python
```

For isolated projects:

```bash
python -m venv .venv
source .venv/bin/activate
pip install wiil-python
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install wiil-python
```

---

## Quick Start

```python
import os

from wiil import WiilClient

client = WiilClient(api_key=os.environ["WIIL_API_KEY"])
```

### Deploy an AI Agent

```python
from wiil.models.service_mgt.dynamic_setup import (
    DynamicPhoneAgentSetup,
    DynamicWebAgentSetup,
)
from wiil.types import BusinessSupportServices

# Phone agent with live number
phone = client.dynamic_phone_agent.create(
    DynamicPhoneAgentSetup(
        assistant_name="Sarah",
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)
print("Phone number:", phone.phone_number)

# Web agent with widget snippets
web = client.dynamic_web_agent.create(
    DynamicWebAgentSetup(
        assistant_name="Emma",
        website_url="https://example.com",
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)
print("Widget snippets:", web.integration_snippets)
```

### Send Notifications

```python
import time

from wiil.models.conversation import (
    CreateCallRequest,
    CreateEmailRequest,
    CreateSmsRequest,
    EmailRecipient,
)
from wiil.types import ScheduleType

# Email
client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com")],
        template_id="order_confirmation",
        subject="Order confirmed",
        body_html="<p>Your order {{orderNumber}} is confirmed.</p>",
        body_text="Your order {{orderNumber}} is confirmed.",
        variables={"orderNumber": "ORD-123"},
    )
)

# SMS
client.outbound_sms.create(
    CreateSmsRequest(
        to="+14155551234",
        from_number="+14155555678",
        body="Your appointment is confirmed for tomorrow at 2 PM.",
    )
)

# Voice call
client.outbound_calls.create(
    CreateCallRequest(
        to="+14155551234",
        from_number="+14155555678",
        agent_configuration_id="reminder_agent",
        schedule_type=ScheduleType.SCHEDULED,
        scheduled_at=int(time.time() * 1000) + 2 * 60 * 60 * 1000,
    )
)
```

### Manage Business Catalogs

```python
from wiil.models.business_mgt import (
    CreateBusinessMenuItem,
    CreateBusinessMenuItemVariant,
    CreateBusinessProduct,
    CreateBusinessProductVariant,
    CreateBusinessService,
)

# Services
service = client.business_services.create(
    CreateBusinessService(
        name="Hair Styling",
        duration=60,
        base_price=75.00,
    )
)

# Menu items with variants
menu_item = client.menus.create_item(
    CreateBusinessMenuItem(
        name="Cheeseburger",
        category_id="cat_main",
        price=12.99,
        variants=[
            CreateBusinessMenuItemVariant(
                name="Regular",
                price=12.99,
                is_default=True,
                is_active=True,
                is_available=True,
            )
        ],
    )
)

# Products with variants
product = client.products.create(
    CreateBusinessProduct(
        name="Wireless Mouse",
        category_id="cat_electronics",
        price=29.99,
        is_alcoholic=False,
        variants=[
            CreateBusinessProductVariant(
                axis_values={},
                price=29.99,
                is_default=True,
                is_active=True,
            )
        ],
    )
)
```

### Book Transactions Through AI Workflows

```python
from wiil.models.business_mgt import CreateServiceAppointment, CreateTableReservation

appointment = client.service_appointments.create(
    CreateServiceAppointment(
        business_service_id=service.id,
        customer_id="cust_123",
        start_time=int(time.time() * 1000) + 24 * 60 * 60 * 1000,
        duration=60,
    )
)

reservation = client.table_reservations.create(
    CreateTableReservation(
        resource_id="table_5",
        customer_id="cust_123",
        floor_plan_id="floor_main",
        persons_number=4,
        time=int(time.time() * 1000) + 2 * 60 * 60 * 1000,
        duration=90,
    )
)
```

---

## Examples & Guides

Comprehensive guides are in the [`examples/`](./examples/) directory.

### Getting Started

| Guide | What You Build |
| ----- | -------------- |
| [Dynamic Agent Setup](./examples/dynamic-agent-setup-guide.md) | Deploy phone/web agents in one API call |
| [Fundamental Configuration](./examples/fundamental-configuration-setup.md) | Fine-grained multi-step agent setup |

### Outbound Communications

| Guide | What You Build |
| ----- | -------------- |
| [Outbound Communications](./examples/outbound-communications-guide.md) | Full notification system across calls, email, and SMS |
| [Messaging Quick Start](./examples/messaging-guide.md) | Send your first notification in minutes |

### Business Services

| Guide | What You Build |
| ----- | -------------- |
| [Services & Appointments](./examples/business-services/services-and-appointments-guide.md) | Bookable services and appointment scheduling |
| [Menus & Orders](./examples/business-services/menus-and-orders-guide.md) | Restaurant menus and food ordering |
| [Products & Orders](./examples/business-services/products-and-orders-guide.md) | Product catalogs and retail orders |
| [Reservations](./examples/business-services/reservations-guide.md) | Tables, rooms, rentals, and bookings |
| [Property Management](./examples/business-services/property-management-guide.md) | Listings, inquiries, and lead tracking |

### Channels

| Guide | What You Build |
| ----- | -------------- |
| [Web Channels](./examples/channels/web-channels.md) | Chat widget integration |
| [Voice Channels](./examples/channels/voice-channels.md) | Phone call handling |
| [SMS Channels](./examples/channels/sms-channels.md) | Text messaging |

[See all examples](./examples/README.md)

---

## SDK Features

- **Type-Safe** - Python type hints with Pydantic models
- **Validated** - Runtime validation using Pydantic
- **Production-Grade** - Robust error handling and configurable timeouts
- **Modern** - Synchronous and asynchronous clients
- **Comprehensive** - Account, service management, business management, conversation, and outbound resources

---

## Available Resources

### Dynamic Agent Setup

```python
client.dynamic_phone_agent
client.dynamic_web_agent
client.dynamic_agent_status
```

### Outbound APIs

```python
client.outbound_templates
client.outbound_calls
client.outbound_emails
client.outbound_sms
```

### Service Configuration

```python
client.agent_configs
client.instruction_configs
client.deployment_configs
client.deployment_channels
client.provisioning_configs
client.support_models
client.telephony_provider
client.conversation_configs
client.knowledge_sources
```

### Business Management

```python
client.business_services
client.customers
client.menus
client.menu_item_variants
client.modifiers
client.products
client.product_variants
client.product_sets
client.service_appointments
client.table_reservations
client.room_reservations
client.rental_reservations
client.menu_orders
client.product_orders
client.reservation_resources
client.floor_plans
client.property_config
client.property_inquiry
```

---

## Error Handling

```python
from wiil.errors import WiilAPIError, WiilNetworkError, WiilValidationError

try:
    result = client.business_services.create(
        CreateBusinessService(name="Consultation", duration=30, base_price=50)
    )
except WiilValidationError as exc:
    print("Invalid input:", exc.details)
except WiilAPIError as exc:
    print(f"API error {exc.status_code}:", exc.message)
    print("Code:", exc.code)
except WiilNetworkError:
    print("Network error. Retry with backoff.")
```

---

## Async Support

```python
import asyncio
import os

from wiil import AsyncWiilClient


async def main() -> None:
    async with AsyncWiilClient(api_key=os.environ["WIIL_API_KEY"]) as client:
        organization = await client.organizations.get()
        print("Organization:", organization.company_name)


asyncio.run(main())
```

---

## Configuration

```python
from wiil import WiilClient

client = WiilClient(
    api_key="your-api-key",
    base_url="https://api.wiil.io/v1",
    timeout=60,
)
```

---

## Security

Server-side only. Never expose your API key in client-side code.

```python
import os

from wiil import WiilClient

# Good: environment variable
client = WiilClient(api_key=os.environ["WIIL_API_KEY"])

# Bad: hardcoded key
client = WiilClient(api_key="sk_live_...")
```

---

## Requirements

- Python 3.8 or higher
- Pydantic
- requests/httpx, depending on sync or async usage

---

## Development

```bash
pip install -e ".[dev]"
pytest
pytest --cov=wiil --cov-report=html
black wiil tests
ruff check wiil tests
mypy wiil
```

---

## Support

- **Documentation**: [https://docs.wiil.io](https://docs.wiil.io)
- **API Reference**: [https://docs.wiil.io/developer/api-reference](https://docs.wiil.io/developer/api-reference)
- **Issues**: [GitHub Issues](https://github.com/wiil-io/wiil-python/issues)
- **Email**: [dev-support@wiil.io](mailto:dev-support@wiil.io)

---

## License

MIT (c) [WIIL](https://wiil.io)

---

Built with care by the WIIL team
