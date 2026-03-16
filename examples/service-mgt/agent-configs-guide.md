# Agent Configuration Guide

This guide covers creating and managing AI agent configurations using the WIIL Platform Python SDK. Agent configurations define the model, behavior, and capabilities of AI assistants deployed across various channels.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
)
from wiil.models.type_definitions import (
    LLMType,
    AssistantType,
    BusinessSupportServices,
)

client = WiilClient(api_key='your-api-key')

# Get a valid model_id from the support models registry
models = client.support_models.list()
model = next((m for m in models if m.type == 'multi_mode' and not m.discontinued), None)

# First, create an instruction configuration
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Customer Support Instructions',
        role='Customer Support Agent',
        introduction_message='Hello! How can I help you today?',
        instructions='You are a helpful customer support agent.',
        guardrails='Always be polite and professional.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

# Create an agent configuration
agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='Harper',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,
        default_function_state=LLMType.MULTI_MODE,
        assistant_type=AssistantType.GENERAL,
    )
)

print(f'Agent created: {agent.id}')
```

## Prerequisites

Agent configurations require an **Instruction Configuration** to be created first. The instruction configuration defines the agent's role, behavior guidelines, and conversation flow.

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
)
from wiil.models.type_definitions import BusinessSupportServices

client = WiilClient(api_key='your-api-key')

# Get a valid model_id from the support models registry
models = client.support_models.list()
model = next((m for m in models if m.type == 'multi_mode' and not m.discontinued), None)

# First, create an instruction configuration
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Customer Support Instructions',
        role='Customer Support Agent',
        introduction_message='Hello! How can I help you today?',
        instructions='You are a helpful customer support agent.',
        guardrails='Always be polite and professional.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

# Then create the agent configuration
agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='Harper',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,
    )
)
```

## Enums

### LLMType

```python
from wiil.models.type_definitions import LLMType

# Available values:
LLMType.STS          # 'sts' - Speech-to-speech
LLMType.TTS          # 'tts' - Text-to-speech
LLMType.STT          # 'stt' - Speech-to-text
LLMType.TRANSCRIBE   # 'transcribe' - Transcription
LLMType.TEXT         # 'text' - Text processing only
LLMType.MULTI_MODE   # 'multi_mode' - Multi-modal (default)
```

### AssistantType

```python
from wiil.models.type_definitions import AssistantType

# Available values:
AssistantType.PHONE    # 'phone' - Phone-based assistant
AssistantType.WEB      # 'web' - Web chat assistant
AssistantType.EMAIL    # 'email' - Email assistant
AssistantType.GENERAL  # 'general' - General purpose (default)
```

## Agent Configuration Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | str | Yes | Agent name (max 30 characters) |
| model_id | str | Yes | LLM model ID from Wiil model registry |
| instruction_configuration_id | str | Yes | ID of linked instruction configuration |
| default_function_state | LLMType | No | Operational mode (default: MULTI_MODE) |
| assistant_type | AssistantType | No | Channel specialization (default: GENERAL) |
| uses_wiil_support_model | bool | No | Use Wiil's model registry (default: True) |
| required_model_config | dict | No | Additional model parameters |
| call_transfer_config | list | No | Phone transfer configurations |
| metadata | dict | No | Custom metadata |

### CallTransferConfig Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| transfer_number | str | Yes | Phone number to transfer to |
| transfer_type | str | No | 'blind' or 'warm' (default: 'warm') |
| transfer_conditions | list[str] | Yes | Conditions that trigger transfer |

## CRUD Operations

### Create Agent Configuration

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
)
from wiil.models.type_definitions import (
    LLMType,
    AssistantType,
    BusinessSupportServices,
)

client = WiilClient(api_key='your-api-key')

# Get a valid model_id from the support models registry
models = client.support_models.list()
model = next((m for m in models if m.type == 'multi_mode' and not m.discontinued), None)

# Create instruction configuration first (see Prerequisites section)
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Support Agent Instructions',
        role='Support Agent',
        introduction_message='Hello!',
        instructions='You are a helpful support agent.',
        guardrails='Be professional.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='Harper',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,
        default_function_state=LLMType.MULTI_MODE,
        assistant_type=AssistantType.GENERAL,
        metadata={'department': 'support', 'tier': 'premium'},
    )
)

print(f'Created agent: {agent.id}')
print(f'Agent name: {agent.name}')
```

### Get Agent Configuration

```python
agent = client.agent_configs.get('agent_123')

print(f'Agent name: {agent.name}')
print(f'Model ID: {agent.model_id}')
print(f'Assistant type: {agent.assistant_type}')
```

### List Agent Configurations

```python
from wiil.types import PaginationRequest

result = client.agent_configs.list(
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Total agents: {result.meta.total_count}')
for agent in result.data:
    print(f'- {agent.name} ({agent.id})')
```

### Update Agent Configuration

```python
from wiil.models.service_mgt import UpdateAgentConfiguration

updated = client.agent_configs.update(
    UpdateAgentConfiguration(
        id='agent_123',
        name='Riley',
        metadata={'department': 'sales', 'updated': True},
    )
)

print(f'Updated name: {updated.name}')
```

### Delete Agent Configuration

```python
deleted = client.agent_configs.delete('agent_123')

if deleted:
    print('Agent deleted successfully')
```

## Phone Agent with Call Transfer

Configure call transfer for phone-based agents:

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
)
from wiil.models.type_definitions import (
    AssistantType,
    BusinessSupportServices,
)

client = WiilClient(api_key='your-api-key')

# Get a valid model_id from the support models registry
models = client.support_models.list()
model = next((m for m in models if m.type == 'multi_mode' and not m.discontinued), None)

# Create phone support instruction configuration first
phone_instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Phone Support Instructions',
        role='Phone Support Agent',
        introduction_message='Thank you for calling. How can I assist you?',
        instructions='You are a phone support agent. Be concise and helpful.',
        guardrails='Transfer to human when requested or for complex issues.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

phone_agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='PhoneSupport',
        model_id=model.model_id,
        instruction_configuration_id=phone_instruction.id,
        assistant_type=AssistantType.PHONE,
        call_transfer_config=[
            {
                'transfer_number': '+15551234567',
                'transfer_type': 'warm',
                'transfer_conditions': [
                    'Customer requests human agent',
                    'Issue requires supervisor approval',
                    'Technical problem beyond AI capability',
                ],
            },
            {
                'transfer_number': '+15559876543',
                'transfer_type': 'blind',
                'transfer_conditions': [
                    'Billing dispute over $500',
                    'Legal inquiry',
                ],
            },
        ],
    )
)
```

## Complete Example

Full workflow demonstrating agent configuration lifecycle:

```python
import os

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateAgentConfiguration,
    CreateInstructionConfiguration,
    UpdateAgentConfiguration,
)
from wiil.models.type_definitions import (
    LLMType,
    AssistantType,
    BusinessSupportServices,
)
from wiil.types import PaginationRequest

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def manage_agent_configurations():
    # 1. Get a valid model_id from the support models registry
    models = client.support_models.list()
    model = next(
        (m for m in models if m.type == 'multi_mode' and not m.discontinued),
        None
    )
    print(f'Using model: {model.model_id}')

    # 2. Create instruction configuration first
    instruction = client.instruction_configs.create(
        CreateInstructionConfiguration(
            instruction_name='Sales Agent Instructions',
            role='Sales Representative',
            introduction_message='Hi! I can help you find the perfect product.',
            instructions='You are a knowledgeable sales assistant.',
            guardrails='Never pressure customers. Be honest about limitations.',
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
        )
    )

    print(f'Instruction created: {instruction.id}')

    # 3. Create agent configuration
    agent = client.agent_configs.create(
        CreateAgentConfiguration(
            name='SalesBot',
            model_id=model.model_id,
            instruction_configuration_id=instruction.id,
            default_function_state=LLMType.MULTI_MODE,
            assistant_type=AssistantType.WEB,
            metadata={'department': 'sales', 'version': '1.0'},
        )
    )

    print(f'Agent created: {agent.id}')

    # 4. Retrieve agent by ID
    retrieved = client.agent_configs.get(agent.id)
    print(f'Retrieved agent: {retrieved.name}')

    # 5. List all agents
    all_agents = client.agent_configs.list(
        params=PaginationRequest(page=1, page_size=50)
    )
    print(f'Total agents: {all_agents.meta.total_count}')

    # 6. Update agent configuration
    updated = client.agent_configs.update(
        UpdateAgentConfiguration(
            id=agent.id,
            name='SalesAssistant',
            metadata={'department': 'sales', 'version': '1.1', 'updated': True},
        )
    )

    print(f'Updated agent name: {updated.name}')

    # 7. Clean up - delete agent and instruction
    client.agent_configs.delete(agent.id)
    print('Agent deleted')

    client.instruction_configs.delete(instruction.id)
    print('Instruction deleted')


if __name__ == '__main__':
    manage_agent_configurations()
```

## Best Practices

1. **Create instruction configurations first** - Agent configurations require an instruction configuration ID. Always create the instruction before the agent.

2. **Use meaningful agent names** - Names are limited to 30 characters. Choose descriptive names that indicate the agent's purpose.

3. **Match assistant_type to deployment** - Set the appropriate assistant type for your deployment channel:
   - `PHONE` for voice-based interactions
   - `WEB` for chat widgets
   - `EMAIL` for email automation
   - `GENERAL` for multi-channel or API-only use

4. **Configure call transfers for phone agents** - When deploying phone agents, set up appropriate transfer conditions to route complex issues to human agents.

5. **Use metadata for organization** - Store department, version, and other organizational data in the metadata field.

## Troubleshooting

### Missing instruction_configuration_id

**Error:**
```
WiilValidationError: instruction_configuration_id is required
```

**Solution:**
Create an instruction configuration first and pass its ID:

```python
# Get a valid model_id from the support models registry
models = client.support_models.list()
model = next(
    (m for m in models if m.type == 'multi_mode' and not m.discontinued),
    None
)

instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='My Instructions',
        role='Assistant',
        introduction_message='Hello!',
        instructions='Be helpful.',
        guardrails='Be safe.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='MyAgent',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,  # Required
    )
)
```

### Invalid model_id

**Error:**
```
WiilAPIError: Model not found in registry
```

**Solution:**
Use a valid model ID from the Wiil support models registry:

```python
# Option 1: Find a multi-mode model
models = client.support_models.list()
model = next(
    (m for m in models if m.type == 'multi_mode' and not m.discontinued),
    None
)
print(f'Model ID: {model.model_id}')

# Option 2: List all available models
for m in models:
    print(f'{m.model_id}: {m.name}')
```

### Name Too Long

**Error:**
```
WiilValidationError: name must be at most 30 characters
```

**Solution:**
Keep agent names concise (30 characters or less):

```python
# Bad
agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='Super Advanced Customer Support AI Assistant v2',  # Too long!
        # ...
    )
)

# Good
agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='CustomerSupportAI',  # 17 characters
        # ...
    )
)
```
