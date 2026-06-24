# Dynamic Agent Setup Guide

Deploy phone and web agents with one SDK call.

Dynamic setup is the recommended path when you want WIIL to provision the required service-management pieces for you: agent configuration, instructions, deployment, channel setup, and optional voice model configuration.

---

## Setup

```python
import os

from wiil import WiilClient

client = WiilClient(api_key=os.environ["WIIL_API_KEY"])
```

---

## Phone Agent

```python
from wiil.models.service_mgt.dynamic_setup import DynamicPhoneAgentSetup
from wiil.types import BusinessSupportServices

result = client.dynamic_phone_agent.create(
    DynamicPhoneAgentSetup(
        assistant_name="Sarah",
        language="en-US",
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

print("Setup ID:", result.id)
print("Agent ID:", result.agent_configuration_id)
print("Phone number:", result.phone_number)
```

Use phone agents for voice workflows such as appointment booking, order follow-up, reservation confirmation, or support triage.

---

## Web Agent

```python
from wiil.models.service_mgt.dynamic_setup import DynamicWebAgentSetup
from wiil.types import BusinessSupportServices, OttCommunicationType

result = client.dynamic_web_agent.create(
    DynamicWebAgentSetup(
        assistant_name="Emma",
        website_url="https://example.com",
        communication_type=OttCommunicationType.UNIFIED,
        language="en-US",
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

print("Setup ID:", result.id)
print("Agent ID:", result.agent_configuration_id)
print("Integration snippets:", result.integration_snippets)
```

Use web agents for chat widgets, voice-enabled widgets, or combined web support experiences.

---

## Add Voice Model Configuration

```python
from wiil.models.service_mgt.dynamic_setup import (
    DynamicPhoneAgentSetup,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
)
from wiil.types import BusinessSupportServices

result = client.dynamic_phone_agent.create(
    DynamicPhoneAgentSetup(
        assistant_name="Marcus",
        language="en-US",
        capabilities=[
            BusinessSupportServices.APPOINTMENT_MANAGEMENT,
            BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT,
        ],
        stt_configuration=DynamicSTTModelConfiguration(
            provider_type="Deepgram",
            provider_model_id="nova-2",
            language_id="en-US",
        ),
        tts_configuration=DynamicTTSModelConfiguration(
            provider_type="ElevenLabs",
            provider_model_id="eleven_turbo_v2",
            language_id="en-US",
            voice_id="voice_rachel",
        ),
    )
)
```

Use explicit STT/TTS configuration when you need a specific voice stack instead of the platform default.

---

## Create Without Waiting for Completion

By default, dynamic setup can poll until provisioning completes. Use create options when you want to enqueue setup and continue immediately.

```python
from wiil.resources.service_mgt.dynamic_phone_agent import PhoneAgentCreateOptions

result = client.dynamic_phone_agent.create(
    DynamicPhoneAgentSetup(
        assistant_name="Queue Only",
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    ),
    options=PhoneAgentCreateOptions(poll_until_complete=False),
)

print("Setup ID:", result.id)
```

For web agents, use `WebAgentCreateOptions` from `wiil.resources.service_mgt.dynamic_web_agent`.

---

## Update an Agent

```python
from wiil.models.service_mgt.dynamic_setup import UpdateDynamicPhoneAgent

updated = client.dynamic_phone_agent.update(
    UpdateDynamicPhoneAgent(
        id=result.id,
        assistant_name="Sarah Updated",
        language="en-US",
    )
)

print("Updated:", updated.id)
```

---

## Delete an Agent Setup

```python
deleted = client.dynamic_phone_agent.delete(result.id)
print("Deleted:", deleted)
```

---

## Capabilities

Capabilities define which business workflows the agent can use.

```python
from wiil.types import BusinessSupportServices

capabilities = [
    BusinessSupportServices.APPOINTMENT_MANAGEMENT,
    BusinessSupportServices.MENU_ORDER_MANAGEMENT,
    BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT,
    BusinessSupportServices.RESERVATION_MANAGEMENT,
]
```

Choose only the capabilities the agent needs. This keeps behavior focused and reduces unnecessary tool access.

---

## Recommended Flow

1. Choose phone or web agent.
2. Select business capabilities.
3. Use platform defaults for model configuration unless you need a specific STT/TTS provider.
4. Create the agent.
5. Store the returned setup ID, agent configuration ID, phone number, or integration snippets.
6. Monitor setup status and conversation behavior in the WIIL Console.

---

## Related Guides

- [Fundamental Configuration Setup](./fundamental-configuration-setup.md)
- [Deployment Channels](./service-mgt/deployment-channels-guide.md)
- [Outbound Communications](./outbound-communications-guide.md)
