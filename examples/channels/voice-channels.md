# Voice Call Channels Guide

Voice channels are used when a deployment is linked to a `calls` deployment channel.

## Prerequisites

- A provisioned phone configuration with `voice_channel_id`
- `project_id`, `agent_configuration_id`, `instruction_configuration_id`

## Step 1: Get Voice Channel ID

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

phone_config = client.phone_configs.get_by_phone_number("+12125551234")
voice_channel_id = phone_config.voice_channel_id

print("phone status:", phone_config.status)
print("voice_channel_id:", voice_channel_id)
```

## Step 2: Create Deployment for Voice Channel

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentConfiguration
from wiil.types import DeploymentProvisioningType, DeploymentStatus

client = WiilClient(api_key="YOUR_API_KEY")

deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id="YOUR_PROJECT_ID",
        deployment_channel_id="YOUR_VOICE_CHANNEL_ID",
        agent_configuration_id="YOUR_AGENT_CONFIG_ID",
        instruction_configuration_id="YOUR_INSTRUCTION_CONFIG_ID",
        deployment_name="Voice Support",
        deployment_status=DeploymentStatus.PENDING,
        provisioning_type=DeploymentProvisioningType.DIRECT,
        is_active=True,
    )
)

print("deployment_id:", deployment.id)
```

## Step 3: Inspect Channel Metadata

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

channel = client.deployment_channels.get("YOUR_VOICE_CHANNEL_ID")
print(channel.deployment_type, channel.channel_identifier)

# Find by identifier and type
same_channel = client.deployment_channels.get_by_identifier(
    "+12125551234",
    "calls",
)
print(same_channel.id)
```

## Step 4: Toggle Recording

```python
from wiil import WiilClient
from wiil.models.service_mgt import UpdateDeploymentChannel

client = WiilClient(api_key="YOUR_API_KEY")

updated = client.deployment_channels.update(
    UpdateDeploymentChannel(
        id="YOUR_VOICE_CHANNEL_ID",
        recording_enabled=True,
    )
)

print(updated.recording_enabled)
```

[Back to channels home](./README.md)
