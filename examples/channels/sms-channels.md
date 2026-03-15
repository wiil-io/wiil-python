# SMS Channels Guide

SMS channels are used when a deployment is linked to an `sms` deployment channel.

## Prerequisites

- A provisioned phone configuration with `sms_channel_id`
- `project_id`, `agent_configuration_id`, `instruction_configuration_id`

## Step 1: Get SMS Channel ID

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

phone_config = client.phone_configs.get_by_phone_number("+12125551234")
sms_channel_id = phone_config.sms_channel_id

print("phone status:", phone_config.status)
print("sms_channel_id:", sms_channel_id)
```

## Step 2: Create Deployment for SMS Channel

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentConfiguration
from wiil.types import DeploymentProvisioningType, DeploymentStatus

client = WiilClient(api_key="YOUR_API_KEY")

deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id="YOUR_PROJECT_ID",
        deployment_channel_id="YOUR_SMS_CHANNEL_ID",
        agent_configuration_id="YOUR_AGENT_CONFIG_ID",
        instruction_configuration_id="YOUR_INSTRUCTION_CONFIG_ID",
        deployment_name="SMS Support",
        deployment_status=DeploymentStatus.PENDING,
        provisioning_type=DeploymentProvisioningType.DIRECT,
        is_active=True,
    )
)

print("deployment_id:", deployment.id)
```

## Step 3: Inspect Channel

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

channel = client.deployment_channels.get("YOUR_SMS_CHANNEL_ID")
print(channel.deployment_type, channel.channel_identifier)

same_channel = client.deployment_channels.get_by_identifier(
    "+12125551234",
    "sms",
)
print(same_channel.id)
```

## Optional: List SMS Channels

```python
from wiil import WiilClient
from wiil.types import PaginationRequest

client = WiilClient(api_key="YOUR_API_KEY")

result = client.deployment_channels.list_by_type(
    "sms",
    PaginationRequest(page=1, page_size=20),
)

for item in result.data:
    print(item.id, item.channel_identifier)
```

[Back to channels home](./README.md)
4. ✅ Test with simple message first

### Messages marked as spam
1. ✅ Complete 10DLC registration
2. ✅ Improve A2P trust score
3. ✅ Avoid spam trigger words
4. ✅ Include opt-out instructions
5. ✅ Monitor user engagement

---

## Next Steps

- **Voice**: [Voice Channels Guide](./voice-channels.md)
- **Management**: [Channel Management](./channel-management.md)
- **Troubleshooting**: [Troubleshooting Guide](./troubleshooting.md)
- **Phone Purchase**: [Phone Purchase Guide](./phone-purchase.md)

---

[← Back to Channels Home](./README.md)
