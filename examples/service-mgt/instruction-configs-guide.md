# Instruction Configuration Guide

This guide covers creating and managing instruction configurations using the WIIL Platform Python SDK. Instruction configurations define the prompts, behavioral guidelines, and conversation flow for AI agents.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateInstructionConfiguration
from wiil.models.type_definitions import BusinessSupportServices

client = WiilClient(api_key='your-api-key')

# Create an instruction configuration
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Customer Support Instructions',
        role='Customer Support Specialist',
        introduction_message='Hello! How can I help you today?',
        instructions='You are a helpful customer support agent. Focus on resolving customer issues efficiently.',
        guardrails='Always be polite and professional. Never share sensitive customer data.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
    )
)

print(f'Instruction created: {instruction.id}')
```

## Architecture Overview

Instruction configurations are the **heart of agent behavior** in the WIIL platform:

- **Central Role**: Defines how agents operate during conversations
- **1:N Relationship**: One instruction configuration can govern multiple Agent Configurations
- **Reusability**: Designed to be reused across multiple deployments

**Example**: A "Customer Service Guidelines" instruction set might govern both a "Sales Agent" and a "Support Agent", ensuring uniform tone and compliance.

## Enums

### BusinessSupportServices

```python
from wiil.models.type_definitions import BusinessSupportServices

# Available values:
BusinessSupportServices.APPOINTMENT_MANAGEMENT      # 'appointment-management'
BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT    # 'product-order-management'
BusinessSupportServices.MENU_ORDER_MANAGEMENT       # 'menu-order-management'
BusinessSupportServices.RESERVATION_MANAGEMENT      # 'reservation-management'
BusinessSupportServices.PROPERTY_LISTING_MANAGEMENT # 'property-listing-management'
```

## Instruction Configuration Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| instruction_name | str | Yes | System-readable name (e.g., 'customer-support-agent') |
| role | str | Yes | Role the agent adopts (e.g., 'Customer Support Specialist') |
| introduction_message | str | Yes | Initial greeting message |
| instructions | str | Yes | Detailed behavioral guidelines and conversation flow |
| guardrails | str | Yes | Safety constraints and ethical guidelines |
| supported_services | list | No | Platform business services (tools) enabled |
| knowledge_source_ids | list[str] | No | IDs of linked knowledge sources |
| required_skills | list[str] | No | Skills required (e.g., 'appointment_booking') |
| validation_rules | dict | No | Custom validation rules |
| is_template | bool | No | Whether this is a reusable template (default: False) |
| is_primary | bool | No | Whether this is the primary template (default: False) |
| metadata | dict | No | Custom metadata |

## CRUD Operations

### Create Instruction Configuration

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateInstructionConfiguration
from wiil.models.type_definitions import BusinessSupportServices

client = WiilClient(api_key='your-api-key')

instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Sales Agent Instructions',
        role='Sales Representative',
        introduction_message='Hello! I can help you find the perfect solution.',
        instructions='You are a knowledgeable and helpful sales agent. Focus on understanding customer needs and recommending appropriate solutions.',
        guardrails='Always be honest about product capabilities. Never make promises the product cannot deliver. Respect customer privacy.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
        metadata={'department': 'sales', 'version': '1.0'},
    )
)

print(f'Created instruction: {instruction.id}')
print(f'Instruction name: {instruction.instruction_name}')
```

### Get Instruction Configuration

```python
instruction = client.instruction_configs.get('instr_123')

print(f'Instruction name: {instruction.instruction_name}')
print(f'Role: {instruction.role}')
print(f'Introduction: {instruction.introduction_message}')
```

### List Instruction Configurations

```python
from wiil.types import PaginationRequest

result = client.instruction_configs.list(
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Total instructions: {result.meta.total_count}')
for instruction in result.data:
    print(f'- {instruction.instruction_name} ({instruction.id})')
```

### Update Instruction Configuration

```python
from wiil.models.service_mgt import UpdateInstructionConfiguration

updated = client.instruction_configs.update(
    UpdateInstructionConfiguration(
        id='instr_123',
        introduction_message='Hi! How may I assist you today?',
        guardrails='Updated: Always be honest and transparent. Respect privacy.',
    )
)

print(f'Updated introduction: {updated.introduction_message}')
```

### Delete Instruction Configuration

```python
deleted = client.instruction_configs.delete('instr_123')

if deleted:
    print('Instruction deleted successfully')
```

### Get Supported Templates

```python
templates = client.instruction_configs.get_supported_templates()

print(f'Available templates: {len(templates)}')
for template in templates:
    print(f'- {template.instruction_name}: {template.role}')
```

## Complete Example

Full workflow demonstrating instruction configuration lifecycle:

```python
import os

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateInstructionConfiguration,
    CreateAgentConfiguration,
    UpdateInstructionConfiguration,
)
from wiil.models.type_definitions import BusinessSupportServices
from wiil.types import PaginationRequest

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def manage_instruction_configurations():
    # 1. Create instruction configuration
    instruction = client.instruction_configs.create(
        CreateInstructionConfiguration(
            instruction_name='Technical Support Instructions',
            role='Technical Support Specialist',
            introduction_message='Hello! I am your technical support specialist.',
            instructions='''You are a knowledgeable technical support agent.
            - Listen carefully to understand the issue
            - Ask clarifying questions when needed
            - Provide step-by-step solutions
            - Escalate complex issues appropriately''',
            guardrails='''Safety guidelines:
            - Never ask for passwords or sensitive credentials
            - Do not make changes without customer confirmation
            - Escalate security-related issues immediately
            - Follow data protection regulations''',
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
            metadata={'department': 'technical-support', 'tier': 'L1'},
        )
    )

    print(f'Instruction created: {instruction.id}')

    # 2. Retrieve instruction by ID
    retrieved = client.instruction_configs.get(instruction.id)
    print(f'Retrieved instruction: {retrieved.instruction_name}')

    # 3. List all instructions
    all_instructions = client.instruction_configs.list(
        params=PaginationRequest(page=1, page_size=50)
    )
    print(f'Total instructions: {all_instructions.meta.total_count}')

    # 4. Update instruction configuration
    updated = client.instruction_configs.update(
        UpdateInstructionConfiguration(
            id=instruction.id,
            introduction_message='Welcome to technical support! How can I assist?',
            metadata={'department': 'technical-support', 'tier': 'L1', 'updated': True},
        )
    )

    print(f'Updated introduction: {updated.introduction_message}')

    # 5. Use instruction with an agent configuration
    models = client.support_models.list()
    model = next(
        (m for m in models if m.type == 'multi_mode' and not m.discontinued),
        None
    )

    agent = client.agent_configs.create(
        CreateAgentConfiguration(
            name='TechSupportBot',
            model_id=model.model_id,
            instruction_configuration_id=instruction.id,
        )
    )

    print(f'Agent created with instruction: {agent.id}')

    # 6. Clean up
    client.agent_configs.delete(agent.id)
    print('Agent deleted')

    client.instruction_configs.delete(instruction.id)
    print('Instruction deleted')


if __name__ == '__main__':
    manage_instruction_configurations()
```

## Best Practices

1. **Write clear, detailed instructions** - The instructions field is the core of agent behavior. Be specific about how the agent should respond, what tone to use, and how to handle different scenarios.

2. **Define comprehensive guardrails** - Guardrails protect your business and customers. Include compliance rules, forbidden topics, escalation criteria, and ethical guidelines.

3. **Use supported_services wisely** - Only enable the business services (tools) that the agent needs. This follows the principle of least privilege.

4. **Keep instruction names descriptive** - Use snake_case names that clearly describe the purpose (e.g., 'customer_support_sales', 'technical_support_l1').

5. **Version your configurations** - Use metadata to track versions. This helps with rollbacks and auditing.

6. **Reuse instruction configurations** - Design instruction sets to be reusable across multiple agents when they share common behavioral requirements.

## Troubleshooting

### Missing Required Fields

**Error:**
```
WiilValidationError: instruction_name is required
```

**Solution:**
Ensure all required fields are provided:

```python
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='My Instructions',      # Required
        role='Assistant',                        # Required
        introduction_message='Hello!',           # Required
        instructions='Be helpful.',              # Required
        guardrails='Be safe.',                   # Required
    )
)
```

### Instruction Not Found

**Error:**
```
WiilAPIError: Instruction configuration not found
```

**Solution:**
Verify the instruction ID exists before using it:

```python
try:
    instruction = client.instruction_configs.get('instr_123')
    # Use instruction
except Exception as e:
    if 'NOT_FOUND' in str(e):
        print('Instruction does not exist')
```

### Cannot Delete Instruction in Use

**Error:**
```
WiilAPIError: Cannot delete instruction configuration that is referenced by agent configurations
```

**Solution:**
Delete or update agent configurations that reference this instruction first:

```python
# First, list agents using this instruction
agents = client.agent_configs.list()
using_instruction = [
    a for a in agents.data
    if a.instruction_configuration_id == 'instr_123'
]

# Delete or update those agents
for agent in using_instruction:
    client.agent_configs.delete(agent.id)

# Now delete the instruction
client.instruction_configs.delete('instr_123')
```
