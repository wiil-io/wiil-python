# Understanding Deployment Channels

Deployment channels define where your users talk to your agent (phone, SMS, web, mobile).

## Core Relationship

- One `DeploymentConfiguration` maps to exactly one `DeploymentChannel`.
- For multi-channel support, create multiple deployments that can share the same agent and instructions.

## Typical Architecture

```text
Project
   |- Deployment A (calls) -> channel: +12125551234
   |- Deployment B (sms)   -> channel: +12125551234
   |- Deployment C (web)   -> channel: https://example.com
```

## Channel Types

| Type | Identifier example | How it is created |
|------|---------------------|-------------------|
| `calls` | `+12125551234` | Usually created from phone configuration workflow |
| `sms` | `+12125551234` | Usually created from phone configuration workflow |
| `web` | `https://example.com` | Created directly via `deployment_channels.create` |
| `mobile-app` | `com.example.app` | Created directly via `deployment_channels.create` |

## Create and Link a Web Channel (Python)

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

channel = client.deployment_channels.create(
      CreateDeploymentChannel(
            deployment_type=DeploymentType.WEB,
            channel_name="Support Widget",
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
            deployment_channel_id=channel.id,
            agent_configuration_id="YOUR_AGENT_CONFIG_ID",
            instruction_configuration_id="YOUR_INSTRUCTION_CONFIG_ID",
            deployment_name="Support Widget Deployment",
            deployment_status=DeploymentStatus.PENDING,
            provisioning_type=DeploymentProvisioningType.DIRECT,
            is_active=True,
      )
)

print(channel.id, deployment.id)
```

## Fetch Existing Phone-Based Channel IDs

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

phone_config = client.phone_configs.get_by_phone_number("+12125551234")
print("voice_channel_id:", phone_config.voice_channel_id)
print("sms_channel_id:", phone_config.sms_channel_id)
```

[Back to channels home](./README.md)
