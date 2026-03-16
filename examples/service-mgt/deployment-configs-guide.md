# Deployment Configuration Guide

This guide covers creating and managing deployment configurations using the WIIL Platform Python SDK. Deployment configurations are the central composition entity that brings together agents, instructions, channels, and projects to create complete AI deployments.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateDeploymentConfiguration

client = WiilClient(api_key='your-api-key')

# Assuming you have already created:
# - A project
# - An instruction configuration
# - An agent configuration
# - A deployment channel

deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id='proj_123',
        deployment_channel_id='channel_456',
        agent_configuration_id='agent_789',
        instruction_configuration_id='instr_abc',
        deployment_name='Customer Support Deployment',
    )
)

print(f'Deployment created: {deployment.id}')
```

## Architecture Overview

Deployment configurations are the **central composition entity** in the WIIL platform:

- **Brings Together**: Agent Configuration + Instruction Configuration + Deployment Channel + Project
- **1:1 with Channel**: Each deployment has exactly one channel
- **N:1 Relationships**: Multiple deployments can share agents, instructions, and projects
- **Multi-Channel Pattern**: Create separate deployments for each channel to expose an agent through multiple channels

**Provisioning Types:**
- **DIRECT**: Agent processes interactions directly
- **CHAINED**: Uses provisioning chain (STT -> Processing -> TTS) for voice processing

## Enums

### DeploymentStatus

```python
from wiil.models.type_definitions import DeploymentStatus

# Available values:
DeploymentStatus.PENDING   # 'pending' - Created but not yet activated
DeploymentStatus.ACTIVE    # 'active' - Operational and accepting interactions
DeploymentStatus.PAUSED    # 'paused' - Temporarily suspended
DeploymentStatus.ARCHIVED  # 'archived' - Decommissioned
```

### DeploymentProvisioningType

```python
from wiil.models.type_definitions import DeploymentProvisioningType

# Available values:
DeploymentProvisioningType.DIRECT   # 'direct' - Direct agent processing
DeploymentProvisioningType.CHAINED  # 'chained' - Provisioning chain (STT -> Processing -> TTS)
```

## Deployment Configuration Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| project_id | str | Yes | Project this deployment belongs to |
| deployment_channel_id | str | Yes | Deployment channel ID (1:1 relationship) |
| agent_configuration_id | str | Yes | Agent configuration ID (N:1 relationship) |
| instruction_configuration_id | str | Yes | Instruction configuration ID (N:1 relationship) |
| deployment_name | str | No | Human-readable name |
| deployment_status | DeploymentStatus | Auto | Current status (defaults to PENDING) |
| provisioning_type | DeploymentProvisioningType | No | Processing type (default: DIRECT) |
| provisioning_config_chain_id | str | No | Chain ID (required for CHAINED type) |
| is_active | bool | No | Whether accepting interactions (default: False) |

## CRUD Operations

### Create Deployment Configuration

```python
import time

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateDeploymentConfiguration,
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
    CreateDeploymentChannel,
)
from wiil.models.type_definitions import DeploymentType, BusinessSupportServices

client = WiilClient(api_key='your-api-key')

# Get or create prerequisites
models = client.support_models.list()
model = next(
    (m for m in models if m.type == 'multi_mode' and not m.discontinued),
    None
)

instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Support Instructions',
        role='Support Agent',
        introduction_message='Hello!',
        instructions='You are a helpful support agent.',
        guardrails='Be professional.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='SupportBot',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,
    )
)

timestamp = int(time.time())
channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier=f'https://support-{timestamp}.example.com',
        deployment_type=DeploymentType.WEB.value,
        channel_name='Support Chat',
        recording_enabled=True,
        configuration={'communicationType': 'unified'},
    )
)

# Get project
projects = client.projects.list()
project_id = projects.data[0].id

# Create deployment
deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id=project_id,
        deployment_channel_id=channel.id,
        agent_configuration_id=agent.id,
        instruction_configuration_id=instruction.id,
        deployment_name='Customer Support',
    )
)

print(f'Deployment created: {deployment.id}')
print(f'Status: {deployment.deployment_status}')
```

### Create Chained Deployment

For voice deployments with STT/TTS processing:

```python
from wiil.models.service_mgt import CreateDeploymentConfiguration

chained_deployment = client.deployment_configs.create_chain(
    CreateDeploymentConfiguration(
        project_id='proj_123',
        deployment_channel_id='channel_456',
        agent_configuration_id='agent_789',
        instruction_configuration_id='instr_abc',
        provisioning_config_chain_id='chain_xyz',
        deployment_name='Voice Support Line',
    )
)
```

### Get Deployment Configuration

```python
# Get by ID
deployment = client.deployment_configs.get('deploy_123')
print(f'Deployment name: {deployment.deployment_name}')
print(f'Status: {deployment.deployment_status}')
print(f'Active: {deployment.is_active}')

# Get by channel ID
by_channel = client.deployment_configs.get_by_channel('channel_456')
print(f'Deployment for channel: {by_channel.id}')
```

### List Deployment Configurations

```python
from wiil.types import PaginationRequest

# List all deployments
result = client.deployment_configs.list(
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Total deployments: {result.meta.total_count}')
for d in result.data:
    print(f'- {d.deployment_name} ({d.deployment_status})')

# List by project
project_deployments = client.deployment_configs.list_by_project('proj_123')
print(f'Project deployments: {len(project_deployments.data)}')

# List by agent
agent_deployments = client.deployment_configs.list_by_agent('agent_789')
print(f'Agent deployments: {len(agent_deployments.data)}')

# List by instruction
instr_deployments = client.deployment_configs.list_by_instruction('instr_abc')
print(f'Instruction deployments: {len(instr_deployments.data)}')
```

### Update Deployment Configuration

```python
from wiil.models.service_mgt import UpdateDeploymentConfiguration

updated = client.deployment_configs.update(
    UpdateDeploymentConfiguration(
        id='deploy_123',
        deployment_name='Updated Support Deployment',
        is_active=True,
    )
)

print(f'Updated name: {updated.deployment_name}')
print(f'Now active: {updated.is_active}')
```

### Delete Deployment Configuration

```python
deleted = client.deployment_configs.delete('deploy_123')

if deleted:
    print('Deployment deleted successfully')
```

## Complete Example

Full workflow demonstrating deployment configuration lifecycle:

```python
import os
import time

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateDeploymentConfiguration,
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
    CreateDeploymentChannel,
    UpdateDeploymentConfiguration,
)
from wiil.models.type_definitions import DeploymentType, BusinessSupportServices

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def create_full_deployment():
    # 1. Get model
    models = client.support_models.list()
    model = next(
        (m for m in models if m.type == 'multi_mode' and not m.discontinued),
        None
    )
    if not model:
        raise ValueError('No model available')
    print(f'Using model: {model.model_id}')

    # 2. Get or create project
    projects = client.projects.list()
    if projects.data:
        project_id = projects.data[0].id
    else:
        project = client.projects.create(
            name='Test Project',
            description='Integration test project',
        )
        project_id = project.id
    print(f'Using project: {project_id}')

    timestamp = int(time.time())

    # 3. Create instruction configuration
    instruction = client.instruction_configs.create(
        CreateInstructionConfiguration(
            instruction_name=f'Deployment_Test_Instructions_{timestamp}',
            role='Deployment Test Agent',
            introduction_message='Hello! I am a test deployment agent.',
            instructions='You are a helpful assistant for deployment testing.',
            guardrails='Follow all safety guidelines.',
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
        )
    )
    print(f'Instruction created: {instruction.id}')

    # 4. Create agent configuration
    agent = client.agent_configs.create(
        CreateAgentConfiguration(
            name='DeployTestAgent',
            model_id=model.model_id,
            instruction_configuration_id=instruction.id,
            metadata={'test': True},
        )
    )
    print(f'Agent created: {agent.id}')

    # 5. Create deployment channel
    channel = client.deployment_channels.create(
        CreateDeploymentChannel(
            channel_identifier=f'https://test-deploy-{timestamp}.example.com',
            deployment_type=DeploymentType.WEB.value,
            channel_name='Test Deployment Channel',
            recording_enabled=True,
            configuration={'communicationType': 'unified'},
        )
    )
    print(f'Channel created: {channel.id}')

    # 6. Create deployment configuration
    deployment = client.deployment_configs.create(
        CreateDeploymentConfiguration(
            project_id=project_id,
            deployment_channel_id=channel.id,
            agent_configuration_id=agent.id,
            instruction_configuration_id=instruction.id,
            deployment_name=f'Test_Deployment_{timestamp}',
        )
    )
    print(f'Deployment created: {deployment.id}')
    print(f'Status: {deployment.deployment_status}')

    # 7. Retrieve deployment
    retrieved = client.deployment_configs.get(deployment.id)
    print(f'Retrieved deployment: {retrieved.deployment_name}')

    # 8. List deployments by project
    project_deployments = client.deployment_configs.list_by_project(project_id)
    print(f'Project has {len(project_deployments.data)} deployments')

    # 9. Update deployment
    updated = client.deployment_configs.update(
        UpdateDeploymentConfiguration(
            id=deployment.id,
            deployment_name='Updated_Test_Deployment',
        )
    )
    print(f'Updated name: {updated.deployment_name}')

    # 10. Clean up (in reverse order of dependencies)
    client.deployment_configs.delete(deployment.id)
    print('Deployment deleted')

    client.deployment_channels.delete(channel.id)
    print('Channel deleted')

    client.agent_configs.delete(agent.id)
    print('Agent deleted')

    client.instruction_configs.delete(instruction.id)
    print('Instruction deleted')

    print('Cleanup complete!')


if __name__ == '__main__':
    create_full_deployment()
```

## Best Practices

1. **Create resources in order** - Follow the dependency chain: Project -> Instruction -> Agent -> Channel -> Deployment

2. **Delete in reverse order** - When cleaning up, delete deployments first, then channels, agents, and instructions

3. **Use meaningful deployment names** - Names help identify deployments in administrative interfaces

4. **Keep is_active false initially** - Start with deployments inactive, then activate after verification

5. **Use list_by_x methods for filtering** - Use `list_by_project()`, `list_by_agent()`, or `list_by_instruction()` for efficient filtering

6. **One channel per deployment** - Remember the 1:1 relationship. Multi-channel requires multiple deployments.

## Troubleshooting

### Missing Required References

**Error:**
```
WiilValidationError: agent_configuration_id is required
```

**Solution:**
Ensure all required IDs are provided and valid:

```python
# Verify all IDs exist before creating deployment
agent = client.agent_configs.get(agent_id)
instruction = client.instruction_configs.get(instruction_id)
channel = client.deployment_channels.get(channel_id)

deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        project_id=project_id,
        deployment_channel_id=channel.id,
        agent_configuration_id=agent.id,
        instruction_configuration_id=instruction.id,
    )
)
```

### Channel Already in Use

**Error:**
```
WiilAPIError: Deployment channel is already associated with another deployment
```

**Solution:**
Each channel can only be used by one deployment. Create a new channel or remove the existing deployment:

```python
# Check if channel is in use
try:
    existing = client.deployment_configs.get_by_channel(channel_id)
    print(f'Channel already used by deployment: {existing.id}')
    # Either use a different channel or delete the existing deployment
except Exception:
    # Channel is available
    deployment = client.deployment_configs.create(
        CreateDeploymentConfiguration(
            deployment_channel_id=channel_id,
            # ...
        )
    )
```

### Cannot Delete Deployment

**Error:**
```
WiilAPIError: Cannot delete active deployment
```

**Solution:**
Deactivate the deployment before deleting:

```python
# First deactivate
client.deployment_configs.update(
    UpdateDeploymentConfiguration(
        id=deployment_id,
        is_active=False,
    )
)

# Then delete
client.deployment_configs.delete(deployment_id)
```

### Invalid Provisioning Type

**Error:**
```
WiilValidationError: provisioning_config_chain_id is required for CHAINED provisioning type
```

**Solution:**
Use `create_chain()` for chained deployments or provide the chain ID:

```python
# Option 1: Use create_chain method
deployment = client.deployment_configs.create_chain(
    CreateDeploymentConfiguration(
        # ... other fields
        provisioning_config_chain_id='chain_123',
    )
)

# Option 2: Stick with DIRECT provisioning (default)
deployment = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        # provisioning_type defaults to DIRECT, no chain needed
        # ...
    )
)
```
