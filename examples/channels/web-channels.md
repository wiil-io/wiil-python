# Web Chat Widget Guide

Create and manage web channels for browser-based chat/voice experiences.

## Step 1: Create a Web Channel

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentChannel
from wiil.types import DeploymentType, OttCommunicationType

client = WiilClient(api_key="YOUR_API_KEY")

channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        deployment_type=DeploymentType.WEB,
        channel_name="Website Chat",
        channel_identifier="https://example.com",
        recording_enabled=True,
        configuration={
            "communicationType": OttCommunicationType.UNIFIED,
            "widgetConfiguration": {
                "position": "right",
            },
        },
    )
)

print("channel_id:", channel.id)
```

## Step 2: Create Deployment

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentConfiguration
from wiil.types import DeploymentProvisioningType, DeploymentStatus

client = WiilClient(api_key="YOUR_API_KEY")

deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id="YOUR_PROJECT_ID",
        deployment_channel_id="YOUR_WEB_CHANNEL_ID",
        agent_configuration_id="YOUR_AGENT_CONFIG_ID",
        instruction_configuration_id="YOUR_INSTRUCTION_CONFIG_ID",
        deployment_name="Website Support",
        deployment_status=DeploymentStatus.PENDING,
        provisioning_type=DeploymentProvisioningType.DIRECT,
        is_active=True,
    )
)

print("deployment_id:", deployment.id)
```

## Step 3: Add Widget to Website

```html
<div id="wiil-widget" data-config-id="YOUR_DEPLOYMENT_ID" data-features="chat,voice"></div>
<script src="https://cdn.wiil.io/public/wiil-widget.js"></script>
<script>WiilWidget.init();</script>
```

## Update Web Channel Settings

```python
from wiil import WiilClient
from wiil.models.service_mgt import UpdateDeploymentChannel
from wiil.types import OttCommunicationType

client = WiilClient(api_key="YOUR_API_KEY")

updated = client.deployment_channels.update(
    UpdateDeploymentChannel(
        id="YOUR_WEB_CHANNEL_ID",
        configuration={
            "communicationType": OttCommunicationType.TEXT,
            "widgetConfiguration": {"position": "left"},
        },
    )
)

print(updated.configuration)
```

[Back to channels home](./README.md)
