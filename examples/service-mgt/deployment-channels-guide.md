# Deployment Channels Guide

This guide covers creating and managing deployment channels using the WIIL Platform Python SDK. Deployment channels define the communication endpoints (phone numbers, web URLs, mobile apps) through which AI agents are accessible.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentChannel
from wiil.models.type_definitions import DeploymentType

client = WiilClient(api_key='your-api-key')

# Create a web deployment channel
channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='https://example.com',
        deployment_type=DeploymentType.WEB.value,
        channel_name='Main Website Chat',
        recording_enabled=True,
        configuration={
            'communicationType': 'unified',
            'widgetConfiguration': {
                'position': 'right',
                'customTheme': {
                    'primaryColor': '#007bff',
                },
            },
        },
    )
)

print(f'Channel created: {channel.id}')
```

## Architecture Overview

Deployment channels define the single communication endpoint through which a deployment is accessible:

- **1:1 Relationship**: Each Deployment Configuration has exactly one Deployment Channel
- **Multi-Channel Pattern**: To expose an agent through multiple channels (phone + web), create separate Deployment Configurations
- **Channel Types**: Phone (calls/SMS), Web (chat widget), Mobile (native apps)

## Enums

### DeploymentType

```python
from wiil.models.type_definitions import DeploymentType

# Available values:
DeploymentType.CALLS   # 'calls' - Voice phone calls
DeploymentType.SMS     # 'sms' - SMS text messaging
DeploymentType.WEB     # 'web' - Browser-based chat widget
DeploymentType.MOBILE  # 'mobile-app' - Native mobile applications
```

### DeploymentStatus

```python
from wiil.models.type_definitions import DeploymentStatus

# Available values:
DeploymentStatus.PENDING   # 'pending' - Created but not yet activated
DeploymentStatus.ACTIVE    # 'active' - Operational
DeploymentStatus.PAUSED    # 'paused' - Temporarily suspended
DeploymentStatus.ARCHIVED  # 'archived' - Decommissioned
```

## Deployment Channel Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| channel_identifier | str | Yes | Phone number (E.164), URL, or package name |
| deployment_type | str | Yes | Channel type (calls, sms, web, mobile-app) |
| channel_name | str | No | Human-readable name |
| recording_enabled | bool | No | Record interactions (default: True) |
| configuration | dict | Yes | Type-specific configuration |

### Channel Configuration by Type

**Phone Channels (calls/sms)**:
```python
{
    'phoneConfigurationId': 'phone_config_123'  # Reference to PhoneConfiguration
}
```

**Web Channels**:
```python
{
    'communicationType': 'text' | 'voice' | 'unified',
    'widgetConfiguration': {
        'position': 'left' | 'right',
        'customTheme': {'primaryColor': '#007bff'}
    }
}
```

**Mobile Channels**:
```python
{
    'packageName': 'com.example.app',
    'platform': 'ios' | 'android'
}
```

## CRUD Operations

### Create Deployment Channel

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentChannel
from wiil.models.type_definitions import DeploymentType

client = WiilClient(api_key='your-api-key')

# Web Channel
web_channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='https://example.com',
        deployment_type=DeploymentType.WEB.value,
        channel_name='Website Chat Widget',
        recording_enabled=True,
        configuration={
            'communicationType': 'unified',
            'widgetConfiguration': {
                'position': 'right',
                'customTheme': {'primaryColor': '#0066cc'},
            },
        },
    )
)

print(f'Web channel created: {web_channel.id}')
```

### Get Deployment Channel

```python
# Get by ID
channel = client.deployment_channels.get('channel_123')
print(f'Channel name: {channel.channel_name}')
print(f'Channel type: {channel.deployment_type}')

# Get by identifier and type
web_channel = client.deployment_channels.get_by_identifier(
    'https://example.com',
    DeploymentType.WEB.value
)
print(f'Found channel: {web_channel.id}')
```

### List Deployment Channels

```python
from wiil.types import PaginationRequest
from wiil.models.type_definitions import DeploymentType

# List all channels
result = client.deployment_channels.list(
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Total channels: {result.meta.total_count}')
for channel in result.data:
    print(f'- {channel.channel_name} ({channel.deployment_type})')

# List by type
web_channels = client.deployment_channels.list_by_type(
    DeploymentType.WEB.value,
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Web channels: {len(web_channels.data)}')
```

### Update Deployment Channel

```python
from wiil.models.service_mgt import UpdateDeploymentChannel

updated = client.deployment_channels.update(
    UpdateDeploymentChannel(
        id='channel_123',
        channel_name='Updated Channel Name',
        recording_enabled=False,
    )
)

print(f'Updated channel: {updated.channel_name}')
```

### Delete Deployment Channel

```python
# Delete channel only
deleted = client.deployment_channels.delete('channel_123')

# Delete channel and associated phone configuration
deleted_with_phone = client.deployment_channels.delete(
    'channel_123',
    delete_phone_config=True
)

if deleted:
    print('Channel deleted successfully')
```

## Channel Type Examples

### Web Chat Widget

```python
from wiil.models.service_mgt import CreateDeploymentChannel
from wiil.models.type_definitions import DeploymentType

web_channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='https://support.example.com',
        deployment_type=DeploymentType.WEB.value,
        channel_name='Support Portal Chat',
        recording_enabled=True,
        configuration={
            'communicationType': 'unified',
            'widgetConfiguration': {
                'position': 'right',
                'customTheme': {
                    'primaryColor': '#4CAF50',
                    'fontFamily': 'Arial, sans-serif',
                },
            },
        },
    )
)
```

### Phone Call Channel

```python
from wiil.models.service_mgt import CreateDeploymentChannel
from wiil.models.type_definitions import DeploymentType

# First, ensure you have a phone configuration
phone_channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='+12025551234',
        deployment_type=DeploymentType.CALLS.value,
        channel_name='Customer Support Line',
        recording_enabled=True,
        configuration={
            'phoneConfigurationId': 'phone_config_123',
        },
    )
)
```

### SMS Channel

```python
from wiil.models.service_mgt import CreateDeploymentChannel
from wiil.models.type_definitions import DeploymentType

sms_channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='+12025551234',
        deployment_type=DeploymentType.SMS.value,
        channel_name='SMS Support',
        recording_enabled=True,
        configuration={
            'phoneConfigurationId': 'phone_config_123',
        },
    )
)
```

## Complete Example

Full workflow demonstrating deployment channel lifecycle:

```python
import os
import time

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateDeploymentChannel,
    UpdateDeploymentChannel,
)
from wiil.models.type_definitions import DeploymentType
from wiil.types import PaginationRequest

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def manage_deployment_channels():
    timestamp = int(time.time())

    # 1. Create a web deployment channel
    web_channel = client.deployment_channels.create(
        CreateDeploymentChannel(
            channel_identifier=f'https://test-{timestamp}.example.com',
            deployment_type=DeploymentType.WEB.value,
            channel_name='Test Web Channel',
            recording_enabled=True,
            configuration={
                'communicationType': 'unified',
                'widgetConfiguration': {
                    'position': 'right',
                    'customTheme': {'primaryColor': '#007bff'},
                },
            },
        )
    )

    print(f'Channel created: {web_channel.id}')

    # 2. Retrieve channel by ID
    retrieved = client.deployment_channels.get(web_channel.id)
    print(f'Retrieved channel: {retrieved.channel_name}')

    # 3. List all web channels
    web_channels = client.deployment_channels.list_by_type(
        DeploymentType.WEB.value
    )
    print(f'Total web channels: {web_channels.meta.total_count}')

    # 4. Update channel configuration
    updated = client.deployment_channels.update(
        UpdateDeploymentChannel(
            id=web_channel.id,
            channel_name='Updated Test Channel',
            recording_enabled=False,
        )
    )

    print(f'Updated channel name: {updated.channel_name}')
    print(f'Recording enabled: {updated.recording_enabled}')

    # 5. Find channel by identifier
    found = client.deployment_channels.get_by_identifier(
        web_channel.channel_identifier,
        DeploymentType.WEB.value
    )
    print(f'Found by identifier: {found.id}')

    # 6. Clean up
    client.deployment_channels.delete(web_channel.id)
    print('Channel deleted')


if __name__ == '__main__':
    manage_deployment_channels()
```

## Best Practices

1. **Use descriptive channel names** - Channel names appear in administrative interfaces. Use clear names that indicate the channel's purpose.

2. **Enable recording for compliance** - Keep recording enabled unless there's a specific reason to disable it. Recordings help with quality assurance and compliance.

3. **Match channel identifier format to type** - Use E.164 format for phone numbers (+12025551234), valid URLs for web channels, and package names for mobile.

4. **One channel per deployment** - Each deployment configuration has exactly one channel. Create separate deployments for multi-channel agents.

5. **Use list_by_type for filtering** - When you need channels of a specific type, use `list_by_type()` for better performance.

## Troubleshooting

### Invalid Channel Identifier

**Error:**
```
WiilValidationError: Invalid website URL format
```

**Solution:**
Ensure the identifier matches the expected format for the deployment type:

```python
# Web channels: valid URL
channel_identifier = 'https://example.com'  # Correct
channel_identifier = 'example.com'          # May fail validation

# Phone channels: E.164 format
channel_identifier = '+12025551234'         # Correct
channel_identifier = '202-555-1234'         # May fail validation
```

### Missing Phone Configuration

**Error:**
```
WiilAPIError: Phone configuration not found
```

**Solution:**
Create or reference a valid phone configuration before creating phone/SMS channels:

```python
# Ensure phone config exists
phone_configs = client.phone_configurations.list()
phone_config_id = phone_configs.data[0].id if phone_configs.data else None

if not phone_config_id:
    raise ValueError('No phone configuration available')

channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='+12025551234',
        deployment_type=DeploymentType.CALLS.value,
        configuration={
            'phoneConfigurationId': phone_config_id,  # Must be valid
        },
    )
)
```

### Channel Already Exists

**Error:**
```
WiilAPIError: Channel identifier already in use
```

**Solution:**
Channel identifiers must be unique per deployment type. Check for existing channels first:

```python
try:
    existing = client.deployment_channels.get_by_identifier(
        'https://example.com',
        DeploymentType.WEB.value
    )
    print(f'Channel already exists: {existing.id}')
except Exception:
    # Channel doesn't exist, safe to create
    new_channel = client.deployment_channels.create(
        CreateDeploymentChannel(
            channel_identifier='https://example.com',
            deployment_type=DeploymentType.WEB.value,
            # ...
        )
    )
```
