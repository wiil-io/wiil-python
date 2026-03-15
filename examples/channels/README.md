# Deployment Channels Guides

This directory explains how to work with channel-related APIs in the WIIL Python SDK.

## Quick Navigation

- [Understanding Deployment Channels](./understanding-channels.md)
- [Phone Number Purchase Guide](./phone-purchase.md)
- [Voice Call Channels](./voice-channels.md)
- [SMS Channels](./sms-channels.md)
- [Web Chat Widget Guide](./web-channels.md)
- [Troubleshooting](./troubleshooting.md)

## Quick Start (Python)

### Create a web deployment

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentChannel, CreateDeploymentConfiguration
from wiil.types import (
    DeploymentProvisioningType,
    DeploymentStatus,
    DeploymentType,
    OttCommunicationType,
)

client = WiilClient(api_key="YOUR_API_KEY")

web_channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        deployment_type=DeploymentType.WEB,
        channel_name="Website Chat",
        channel_identifier="https://example.com",
        recording_enabled=True,
        configuration={
            "communicationType": OttCommunicationType.UNIFIED,
            "widgetConfiguration": {"position": "right"},
        },
    )
)

deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id="YOUR_PROJECT_ID",
        deployment_channel_id=web_channel.id,
        agent_configuration_id="YOUR_AGENT_CONFIG_ID",
        instruction_configuration_id="YOUR_INSTRUCTION_CONFIG_ID",
        deployment_name="Website Chat",
        deployment_status=DeploymentStatus.PENDING,
        provisioning_type=DeploymentProvisioningType.DIRECT,
        is_active=True,
    )
)

print("Deployment ID:", deployment.id)
```

### Discover phone numbers

```python
from wiil import WiilClient
from wiil.types import ProviderType

client = WiilClient(api_key="YOUR_API_KEY")

numbers = client.telephony_provider.get_phone_numbers(
    ProviderType.SIGNALWIRE,
    "US",
    area_code="212",
)

for number in numbers[:5]:
    print(number.phone_number)
```

Note: the current Python SDK exposes telephony discovery methods (`get_regions`, `get_phone_numbers`, `get_pricing`). If your workflow requires purchasing numbers through a custom/internal endpoint, complete that step outside this SDK and then use `client.phone_configs` plus `client.deployment_configs` for deployment setup.

## Channel Types Overview

| Type | Description | Typical setup path |
|------|-------------|--------------------|
| `calls` | Voice telephony | Existing `PhoneConfiguration.voice_channel_id` |
| `sms` | Text messaging | Existing `PhoneConfiguration.sms_channel_id` |
| `web` | Chat widget | `deployment_channels.create(...)` |
| `mobile-app` | Mobile app channel | `deployment_channels.create(...)` |
