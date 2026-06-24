# WIIL Python SDK Examples

This directory contains examples and guides for building AI-powered business workflows with the WIIL Python SDK.

## Getting Started

### Prerequisites

1. **WIIL Platform Account**
   - Sign up at [https://console.wiil.io](https://console.wiil.io)
   - Complete email verification

2. **API Key**
   - Navigate to **Settings** -> **API Keys** in the WIIL Console
   - Generate and securely store your API key

3. **Python Environment**
   - Python 3.8 or higher
   - A virtual environment is recommended

### Installation

```bash
pip install wiil-python
```

### Environment Setup

Create a `.env` file or export the variable in your shell:

```env
WIIL_API_KEY=your-api-key-here
```

Never commit API keys or `.env` files to version control.

---

## Quick Start Guides

### Dynamic Agent Setup

**File**: [dynamic-agent-setup-guide.md](./dynamic-agent-setup-guide.md)

The fastest path to deploy phone or web agents. Use this when you want the platform to provision the required agent, instruction, deployment, and channel pieces for you.

```python
import os

from wiil import WiilClient
from wiil.models.service_mgt.dynamic_setup import DynamicPhoneAgentSetup
from wiil.types import BusinessSupportServices

client = WiilClient(api_key=os.environ["WIIL_API_KEY"])

result = client.dynamic_phone_agent.create(
    DynamicPhoneAgentSetup(
        assistant_name="Sarah",
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

print("Phone number:", result.phone_number)
```

[Read the Dynamic Setup Guide](./dynamic-agent-setup-guide.md)

### Fundamental Configuration Setup

**File**: [fundamental-configuration-setup.md](./fundamental-configuration-setup.md)

Use the fundamental setup guide when you need fine-grained control over instructions, support models, agent configurations, deployment channels, and deployment configurations.

Setup steps:

1. Initialize the client and verify organization access
2. Create or select a project
3. Create an instruction configuration
4. Select a support model
5. Create an agent configuration
6. Create a deployment channel
7. Create a deployment configuration
8. Deploy and verify

[Read the Fundamental Configuration Guide](./fundamental-configuration-setup.md)

---

## Outbound Communications

### Full Guide

**File**: [outbound-communications-guide.md](./outbound-communications-guide.md)

Build notification workflows across SMS, email, and AI-powered outbound calls without managing provider integrations directly.

### Messaging Quick Start

**File**: [messaging-guide.md](./messaging-guide.md)

Send your first SMS, email, and outbound call:

```python
from wiil.models.conversation import CreateSmsRequest

sms = client.outbound_sms.create(
    CreateSmsRequest(
        to="+12125551234",
        from_number="+12125559999",
        body="Your appointment is confirmed for tomorrow at 3 PM.",
    )
)
```

[Read the Messaging Guide](./messaging-guide.md)

---

## Business Service Guides

**Directory**: [business-services/](./business-services/)

| Guide | What You Build |
| ----- | -------------- |
| [Services & Appointments](./business-services/services-and-appointments-guide.md) | Bookable services and appointment scheduling |
| [Menus & Orders](./business-services/menus-and-orders-guide.md) | Restaurant menus, item variants, modifiers, and orders |
| [Products & Orders](./business-services/products-and-orders-guide.md) | Product catalogs, variants, pricing, and product orders |
| [Reservations](./business-services/reservations-guide.md) | Reservable tables, rooms, rentals, and booking flows |
| [Property Management](./business-services/property-management-guide.md) | Property listings, inquiries, and lead tracking |

---

## Channels

**Directory**: [channels/](./channels/)

| Guide | What You Build |
| ----- | -------------- |
| [Channel Overview](./channels/README.md) | Channel concepts and setup flow |
| [Understanding Channels](./channels/understanding-channels.md) | Channel types and architecture |
| [Web Channels](./channels/web-channels.md) | Web chat widget deployment |
| [Voice Channels](./channels/voice-channels.md) | Phone call handling |
| [SMS Channels](./channels/sms-channels.md) | Text messaging channels |
| [Phone Purchase](./channels/phone-purchase.md) | Phone number provisioning |
| [Troubleshooting](./channels/troubleshooting.md) | Common channel issues |

---

## Service Management Guides

**Directory**: [service-mgt/](./service-mgt/)

| Guide | What You Configure |
| ----- | ------------------ |
| [Agent Configs](./service-mgt/agent-configs-guide.md) | Agent identity, services, and model selection |
| [Instruction Configs](./service-mgt/instruction-configs-guide.md) | Agent role, instructions, and guardrails |
| [Deployment Channels](./service-mgt/deployment-channels-guide.md) | Web, voice, SMS, and email channels |
| [Deployment Configs](./service-mgt/deployment-configs-guide.md) | Live deployment bindings |
| [Provisioning Configs](./service-mgt/provisioning-configs-guide.md) | STT/TTS voice chains |
| [Knowledge Sources](./service-mgt/knowledge-sources-guide.md) | Agent knowledge bases |
| [Support Models](./service-mgt/support-models-guide.md) | Available AI, STT, and TTS models |
| [Telephony Provider](./service-mgt/telephony-provider-guide.md) | Phone number/provider operations |
| [Translation Sessions](./service-mgt/translation-sessions-guide.md) | Real-time translation sessions |

---

## Configuration Flow

```text
Organization
  -> Project
    -> Instruction Configuration
    -> Support Model
    -> Agent Configuration
    -> Deployment Channel
    -> Deployment Configuration
      -> Live Agent
```

Dynamic setup creates much of this chain for you. Fundamental setup exposes each step directly.

---

## Error Handling

```python
from wiil.errors import WiilAPIError, WiilNetworkError, WiilValidationError

try:
    result = client.deployment_configs.create(payload)
except WiilValidationError as exc:
    print("Invalid input:", exc.details)
except WiilAPIError as exc:
    print(f"API error {exc.status_code}:", exc.message)
except WiilNetworkError:
    print("Network error. Check connectivity and retry.")
```

---

## Security

The WIIL Python SDK is intended for server-side use. Never expose your API key in browser or mobile client code.

```python
import os

from wiil import WiilClient

client = WiilClient(api_key=os.environ["WIIL_API_KEY"])
```

---

## Support

- **Documentation**: [https://docs.wiil.io](https://docs.wiil.io)
- **API Reference**: [https://docs.wiil.io/developer/api-reference](https://docs.wiil.io/developer/api-reference)
- **SDK Reference**: [https://github.com/wiil-io/wiil-python](https://github.com/wiil-io/wiil-python)
- **Email**: [dev-support@wiil.io](mailto:dev-support@wiil.io)

---

Start with [Dynamic Agent Setup](./dynamic-agent-setup-guide.md) for the quickest deployment path, or use [Fundamental Configuration](./fundamental-configuration-setup.md) when you need full control.
