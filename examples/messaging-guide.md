# Messaging Guide

Quick-start guide for outbound messaging with the WIIL Python SDK: SMS, email, and AI-powered calls.

---

## Why This Exists

You need to notify customers without building provider infrastructure:

- SMTP or email-provider integration
- SMS gateway contracts
- Telephony stacks
- Retry logic and delivery tracking
- Bounce, failure, and status handling

The WIIL outbound APIs expose those workflows through one client.

---

## Quick Start

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

# Send an SMS
sms = client.outbound_sms.create(
    CreateSmsRequest(
        to="+12125551234",
        from_number="+12125559999",
        body="Your appointment is confirmed for tomorrow at 3 PM.",
    )
)

# Send an email
email = client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com", name="John Smith")],
        subject="Order Confirmed",
        body_html="<h1>Thank you!</h1><p>Your order is confirmed.</p>",
        body_text="Thank you! Your order is confirmed.",
    )
)

# Request an AI-powered call
call = client.outbound_calls.create(
    CreateCallRequest(
        to="+12125551234",
        from_number="+12125559999",
        agent_configuration_id="confirmation_agent",
        schedule_type=ScheduleType.IMMEDIATE,
    )
)

print(sms.id, email.id, call.id)
```

---

## Send SMS

Direct message:

```python
from wiil.models.conversation import CreateSmsRequest

sms = client.outbound_sms.create(
    CreateSmsRequest(
        to="+12125551234",
        from_number="+12125559999",
        body="Your verification code is 847291. Valid for 10 minutes.",
        max_retries=2,
    )
)
```

Template-based message:

```python
sms = client.outbound_sms.create(
    CreateSmsRequest(
        to="+12125551234",
        from_number="+12125559999",
        template_id="verification_code",
        body="Your verification code is {{code}}.",
        variables={"code": "847291"},
    )
)
```

Scheduled SMS:

```python
import time

sms = client.outbound_sms.create(
    CreateSmsRequest(
        to="+12125551234",
        from_number="+12125559999",
        body="Reminder: your appointment starts in one hour.",
        scheduled_at=int(time.time() * 1000) + 60 * 60 * 1000,
    )
)
```

---

## Send Email

Direct content:

```python
from wiil.models.conversation import CreateEmailRequest, EmailRecipient

email = client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com", name="John Smith")],
        subject="Your Order Has Shipped",
        body_html="<h1>Good news!</h1><p>Your order is on its way.</p>",
        body_text="Good news! Your order is on its way.",
        reply_to="support@example.com",
    )
)
```

Template-based email:

```python
email = client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com", name="John Smith")],
        template_id="order_shipped",
        subject="Your order {{orderNumber}} has shipped",
        body_html="<p>Track your order here: {{trackingUrl}}</p>",
        body_text="Track your order: {{trackingUrl}}",
        variables={
            "orderNumber": "ORD-12345",
            "trackingUrl": "https://track.example.com/12345",
        },
    )
)
```

With CC/BCC:

```python
email = client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com")],
        cc=[EmailRecipient(email="manager@example.com")],
        bcc=[EmailRecipient(email="archive@example.com")],
        subject="Team Update",
        body_html="<p>Weekly update attached.</p>",
        body_text="Weekly update attached.",
    )
)
```

With an attachment:

```python
import base64
from pathlib import Path

from wiil.models.conversation import EmailAttachment

pdf_content = base64.b64encode(Path("invoice.pdf").read_bytes()).decode()

email = client.outbound_emails.create(
    CreateEmailRequest(
        to=[EmailRecipient(email="customer@example.com")],
        subject="Your Invoice",
        body_html="<p>Please find your invoice attached.</p>",
        body_text="Please find your invoice attached.",
        attachments=[
            EmailAttachment(
                filename="invoice.pdf",
                content=pdf_content,
                content_type="application/pdf",
            )
        ],
    )
)
```

---

## Request Calls

Immediate call:

```python
from wiil.models.conversation import CreateCallRequest
from wiil.types import ScheduleType

call = client.outbound_calls.create(
    CreateCallRequest(
        to="+12125551234",
        from_number="+12125559999",
        agent_configuration_id="agent_456",
        schedule_type=ScheduleType.IMMEDIATE,
    )
)
```

Scheduled call with calling hours:

```python
import time

from wiil.models.conversation import CallingHours

call = client.outbound_calls.create(
    CreateCallRequest(
        to="+12125551234",
        from_number="+12125559999",
        agent_configuration_id="agent_456",
        schedule_type=ScheduleType.SCHEDULED,
        scheduled_at=int(time.time() * 1000) + 60 * 60 * 1000,
        calling_hours=CallingHours(
            start_time="09:00",
            end_time="17:00",
            days_of_week=[1, 2, 3, 4, 5],
        ),
        max_retries=3,
        retry_delay_minutes=30,
    )
)
```

---

## Status Queries

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

## Error Handling

```python
from wiil.errors import WiilAPIError, WiilNetworkError, WiilValidationError

try:
    sms = client.outbound_sms.create(
        CreateSmsRequest(to="+12125551234", body="Hello")
    )
except WiilValidationError as exc:
    print("Invalid request:", exc.details)
except WiilAPIError as exc:
    print(f"API error {exc.status_code}:", exc.message)
except WiilNetworkError:
    print("Network error. Retry with backoff.")
```

---

## Production Checklist

- Store phone numbers in E.164 format.
- Use templates for messages edited by non-developers.
- Set retry limits intentionally.
- Respect local calling-hour and consent rules.
- Track message IDs and statuses in your own system.
