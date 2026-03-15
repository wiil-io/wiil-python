# Channels Troubleshooting Guide

Use these Python checks to quickly validate channel and deployment wiring.

## Quick Diagnostic Script

```python
from wiil import WiilClient
from wiil.types import PaginationRequest


def diagnose_channel(client: WiilClient, channel_id: str) -> None:
    print("diagnosing channel:", channel_id)

    channel = client.deployment_channels.get(channel_id)
    print("type:", channel.deployment_type)
    print("identifier:", channel.channel_identifier)
    print("recording_enabled:", channel.recording_enabled)

    deployments = client.deployment_configs.list(PaginationRequest(page=1, page_size=200))
    matches = [d for d in deployments.data if d.deployment_channel_id == channel_id]

    if not matches:
        print("warning: no deployments linked to this channel")
        return

    active_count = len([d for d in matches if d.is_active])
    print("linked deployments:", len(matches))
    print("active deployments:", active_count)


client = WiilClient(api_key="YOUR_API_KEY")
diagnose_channel(client, "YOUR_CHANNEL_ID")
```

## Voice and SMS checks

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")
phone_config = client.phone_configs.get_by_phone_number("+12125551234")

print("status:", phone_config.status)
print("voice_channel_id:", phone_config.voice_channel_id)
print("sms_channel_id:", phone_config.sms_channel_id)
```

If either channel ID is missing, complete phone provisioning first and retry.

## Deployment checks

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")
deployment = client.deployment_configs.get("YOUR_DEPLOYMENT_ID")

print("is_active:", deployment.is_active)
print("status:", deployment.deployment_status)
print("channel_id:", deployment.deployment_channel_id)
```

If needed, update activation state:

```python
from wiil import WiilClient
from wiil.models.service_mgt import UpdateDeploymentConfiguration

client = WiilClient(api_key="YOUR_API_KEY")

updated = client.deployment_configs.update(
    UpdateDeploymentConfiguration(
        id="YOUR_DEPLOYMENT_ID",
        is_active=True,
    )
)

print(updated.is_active)
```

## Web widget checks

1. Confirm deployment is active.
2. Confirm widget uses deployment ID in `data-config-id`.
3. Confirm script URL is `https://cdn.wiil.io/public/wiil-widget.js`.
4. Use HTTPS if you need microphone access.

Minimal widget embed:

```html
<div id="wiil-widget" data-config-id="YOUR_DEPLOYMENT_ID" data-features="chat,voice"></div>
<script src="https://cdn.wiil.io/public/wiil-widget.js"></script>
<script>WiilWidget.init();</script>
```

## API connectivity check

```python
from wiil import WiilClient
from wiil.types import PaginationRequest

client = WiilClient(api_key="YOUR_API_KEY")
client.deployment_channels.list(PaginationRequest(page=1, page_size=1))
print("API connectivity OK")
```

## When to contact support

Collect:

1. Channel ID or deployment ID
2. Full error message
3. Timestamp of failure
4. Steps to reproduce

Then contact: `dev-support@wiil.io`

[Back to channels home](./README.md)
