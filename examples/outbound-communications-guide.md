# Outbound Communications Guide

Enterprise-grade notifications without provider infrastructure.

---

## What You Get

The WIIL outbound APIs let your Python application send:

- Email through `client.outbound_emails`
- SMS through `client.outbound_sms`
- AI-powered calls through `client.outbound_calls`
- Reusable templates through `client.outbound_templates`

The platform handles provider routing, queueing, retries, scheduling, and delivery tracking.

---

## Unified Pattern

```python
import os

from wiil import WiilClient
from wiil.models.conversation import (
    CreateCallRequest,
    CreateEmailRequest,
    CreateSmsRequest,
    EmailRecipient,
)
from wiil.types import ScheduleType

client = WiilClient(api_key=os.environ["WIIL_API_KEY"])

email = client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com")],
        template_id="order_confirmation",
        subject="Order confirmed",
        body_html="<p>Your order {{orderNumber}} is confirmed.</p>",
        body_text="Your order {{orderNumber}} is confirmed.",
        variables={"orderNumber": "ORD-5521"},
    )
)

sms = client.outbound_sms.create(
    CreateSmsRequest(
        to="+12125551234",
        from_number="+12125559999",
        template_id="appointment_reminder",
        body="Reminder: {{serviceName}} at {{time}}.",
        variables={"serviceName": "Hair Styling", "time": "3:00 PM"},
    )
)

call = client.outbound_calls.create(
    CreateCallRequest(
        to="+12125551234",
        from_number="+12125559999",
        agent_configuration_id="appointment_confirmation_agent",
        schedule_type=ScheduleType.IMMEDIATE,
    )
)
```

---

## Use Cases

### Transactional Notifications

```python
client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email=order.customer_email, name=order.customer_name)],
        template_id="order_confirmation",
        subject="Order {{orderNumber}} confirmed",
        body_html="<p>Total: {{total}}</p>",
        body_text="Total: {{total}}",
        variables={
            "orderNumber": order.id,
            "total": order.total,
        },
    )
)
```

### Appointment Reminders

```python
client.outbound_sms.create(
    CreateSmsRequest(
        to=appointment.customer_phone,
        from_number=business_phone,
        template_id="appointment_reminder_24h",
        body="{{serviceName}} is scheduled for {{dateTime}}.",
        variables={
            "serviceName": appointment.service_name,
            "dateTime": appointment.display_time,
        },
    )
)
```

### Scheduled Calls

```python
import time

client.outbound_calls.create(
    CreateCallRequest(
        to=customer.phone,
        from_number=business_phone,
        agent_configuration_id="satisfaction_survey_agent",
        schedule_type=ScheduleType.SCHEDULED,
        scheduled_at=int(time.time() * 1000) + 24 * 60 * 60 * 1000,
        max_duration=300,
        max_retries=2,
    )
)
```

---

## Templates

Use templates for copy that changes without code deploys. Template resources support email, SMS, and WhatsApp template management.

```python
from wiil.models.conversation import CreateEmailTemplate, TemplateVariable

template = client.outbound_templates.create_email_template(
    CreateEmailTemplate(
        name="Order Shipped",
        code="order_shipped",
        subject_template="Your order {{orderNumber}} is on the way",
        body_html_template="<p>{{customerName}}, your order shipped.</p>",
        variables=[
            TemplateVariable(key="customerName", required=True),
            TemplateVariable(key="orderNumber", required=True),
        ],
    )
)

rendered = client.outbound_templates.render(
    template.id,
    {"customerName": "Jane", "orderNumber": "ORD-5521"},
)
```

---

## Status Tracking

```python
from wiil.types import CallRequestStatus, EmailStatus, PaginationRequest, SmsStatus

pending_calls = client.outbound_calls.get_by_status(
    CallRequestStatus.PENDING,
    PaginationRequest(page=1, page_size=20),
)

queued_emails = client.outbound_emails.get_by_status(
    EmailStatus.QUEUED,
    PaginationRequest(page=1, page_size=20),
)

queued_sms = client.outbound_sms.get_by_status(
    SmsStatus.QUEUED,
    PaginationRequest(page=1, page_size=20),
)
```

---

## Production Checklist

- Store all phone numbers in E.164 format.
- Keep message templates in the platform when copy changes frequently.
- Persist outbound request IDs so you can reconcile delivery status.
- Configure retry counts deliberately per channel.
- Respect local consent, opt-out, and calling-hour rules.
- Use metadata to attach your own order, appointment, or campaign IDs.

---

## Related Guides

- [Messaging Quick Start](./messaging-guide.md)
- [Dynamic Agent Setup](./dynamic-agent-setup-guide.md)
- [Deployment Channels](./service-mgt/deployment-channels-guide.md)
