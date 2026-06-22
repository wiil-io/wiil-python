# Messaging Guide

This guide covers sending outbound messages using the WIIL Platform Python SDK. The messaging service supports AI-powered phone calls, SMS text messages, and emails.

## Quick Start

```python
from wiil import WiilService

service = WiilService(api_key="your-api-key")

# Send an SMS
sms = service.messaging.send_sms({
    "to": "+12125551234",
    "body": "Your appointment is confirmed for tomorrow at 3 PM.",
})

print(f"SMS sent: {sms.id}")
```

## Request a Call

Initiate an AI-powered outbound phone call:

```python
call = service.messaging.request_call({
    "to": "+12125551234",
    "from": "+12125559999",
    "agentConfigurationId": "agent_456",
    "scheduleType": "IMMEDIATE",
})

print(f"Call requested: {call.id}")
print(f"Status: {call.status}")
```

### Scheduled Call with Calling Hours

```python
import time

scheduled_call = service.messaging.request_call({
    "to": "+12125551234",
    "from": "+12125559999",
    "agentConfigurationId": "agent_456",
    "scheduleType": "SCHEDULED",
    "scheduledAt": int(time.time() * 1000) + 3600000,  # 1 hour from now
    "callingHours": {
        "startTime": "09:00",
        "endTime": "17:00",
        "daysOfWeek": [1, 2, 3, 4, 5],  # Monday-Friday
    },
    "maxRetries": 3,
    "retryDelayMinutes": 30,
})
```

## Send SMS

Send a text message with optional template variables:

```python
sms = service.messaging.send_sms({
    "to": "+12125551234",
    "body": "Hi {{firstName}}, your code is {{code}}.",
    "variables": {
        "firstName": "John",
        "code": "123456",
    },
})

print(f"SMS sent: {sms.id}")
```

### Scheduled SMS

```python
import time

scheduled_sms = service.messaging.send_sms({
    "to": "+12125551234",
    "body": "Reminder: Your appointment is in 1 hour.",
    "scheduledAt": int(time.time() * 1000) + 3600000,
})
```

## Send Email

Send an email with HTML content:

```python
email = service.messaging.send_email({
    "to": [{"email": "customer@example.com", "name": "John Smith"}],
    "subject": "Order Confirmation - #{{orderId}}",
    "bodyHtml": "<h1>Thank you, {{name}}!</h1><p>Your order has been confirmed.</p>",
    "variables": {
        "orderId": "12345",
        "name": "John",
    },
})

print(f"Email sent: {email.id}")
```

### Email with CC and Attachments

```python
import base64
from pathlib import Path

pdf_content = base64.b64encode(Path("invoice.pdf").read_bytes()).decode()

email = service.messaging.send_email({
    "to": [{"email": "customer@example.com", "name": "Customer"}],
    "cc": [{"email": "sales@company.com"}],
    "replyTo": "support@company.com",
    "subject": "Your Invoice",
    "bodyHtml": "<p>Please find your invoice attached.</p>",
    "bodyText": "Please find your invoice attached.",
    "attachments": [
        {
            "filename": "invoice.pdf",
            "content": pdf_content,
            "contentType": "application/pdf",
        },
    ],
})
```

## Schedule Types

| Type | Description |
|------|-------------|
| `IMMEDIATE` | Execute as soon as possible within calling hours |
| `SCHEDULED` | Execute at specific `scheduledAt` timestamp |
| `RECURRING` | Execute on `callingHours` schedule pattern |

## Complete Example

```python
import os
import time
from datetime import datetime

from wiil import WiilService

service = WiilService(api_key=os.environ["WIIL_API_KEY"])


def send_notifications(customer_id: str, appointment_time: str) -> None:
    """Send confirmation notifications for an appointment."""
    # Send confirmation SMS
    sms = service.messaging.send_sms({
        "to": "+12125551234",
        "body": f"Your appointment is confirmed for {appointment_time}.",
    })
    print(f"SMS sent: {sms.id}")

    # Send confirmation email
    email = service.messaging.send_email({
        "to": [{"email": "customer@example.com"}],
        "subject": "Appointment Confirmed",
        "bodyHtml": f"<p>Your appointment is confirmed for <strong>{appointment_time}</strong>.</p>",
    })
    print(f"Email sent: {email.id}")

    # Schedule reminder call 1 hour before
    appointment_dt = datetime.fromisoformat(appointment_time.replace("Z", "+00:00"))
    reminder_time = int(appointment_dt.timestamp() * 1000) - 3600000

    call = service.messaging.request_call({
        "to": "+12125551234",
        "from": "+12125559999",
        "agentConfigurationId": "reminder_agent",
        "scheduleType": "SCHEDULED",
        "scheduledAt": reminder_time,
    })
    print(f"Reminder call scheduled: {call.id}")


if __name__ == "__main__":
    send_notifications("cust_123", "2024-12-20T15:00:00Z")
```
