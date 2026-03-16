# Knowledge Sources Guide

This guide covers accessing knowledge sources using the WIIL Platform Python SDK. Knowledge sources represent repositories of information that AI agents can access for context and factual grounding.

## Quick Start

```python
from wiil import WiilClient

client = WiilClient(api_key='your-api-key')

# List knowledge sources
result = client.knowledge_sources.list()

print(f'Total sources: {result.meta.total_count}')
for source in result.data:
    print(f'- {source.name} ({source.type})')
```

## Architecture Overview

Knowledge sources are a **read-only resource** that provides:

- **Information Repositories**: Documents, FAQs, product catalogs, and other data
- **Agent Context**: Factual grounding for AI agent responses
- **Referenced by Instructions**: Instruction configurations link to knowledge sources via `knowledge_source_ids`

**Relationship with Instruction Configurations:**
```python
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        # ... other fields
        knowledge_source_ids=['ks_123', 'ks_456'],  # Link to knowledge sources
    )
)
```

## Operations

### List Knowledge Sources

```python
from wiil import WiilClient

client = WiilClient(api_key='your-api-key')

# List with default pagination
result = client.knowledge_sources.list()

print(f'Total knowledge sources: {result.meta.total_count}')
print(f'Page: {result.meta.page} of {result.meta.total_pages}')

for source in result.data:
    print(f'{source.name}:')
    print(f'  ID: {source.id}')
    print(f'  Type: {source.type}')
```

### List with Custom Pagination

```python
from wiil.types import PaginationRequest

result = client.knowledge_sources.list(
    params=PaginationRequest(page=2, page_size=50)
)

print(f'Page {result.meta.page} of {result.meta.total_pages}')
print(f'Showing {len(result.data)} of {result.meta.total_count} sources')
```

### Get Knowledge Source by ID

```python
source = client.knowledge_sources.get('ks_123')

print('Knowledge Source:')
print(f'  ID: {source.id}')
print(f'  Name: {source.name}')
print(f'  Type: {source.type}')
print(f'  Created: {source.created_at}')
```

## Using Knowledge Sources with Instructions

Knowledge sources provide context for AI agents through instruction configurations:

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateInstructionConfiguration,
    CreateAgentConfiguration,
)
from wiil.models.type_definitions import BusinessSupportServices

client = WiilClient(api_key='your-api-key')

# 1. List available knowledge sources
sources = client.knowledge_sources.list()

print('Available knowledge sources:')
for source in sources.data:
    print(f'  {source.id}: {source.name}')

# 2. Select relevant sources for your agent
relevant_source_ids = [
    s.id for s in sources.data
    if s.type in ('faq', 'documentation')
]

# 3. Get a model
models = client.support_models.list()
model = next(
    (m for m in models if m.type == 'multi_mode' and not m.discontinued),
    None
)

# 4. Create instruction with knowledge sources
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Knowledge-Enhanced Agent',
        role='Support Agent',
        introduction_message='Hello! I have access to our knowledge base.',
        instructions='Use the linked knowledge sources to answer questions.',
        guardrails='Only provide information from verified knowledge sources.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
        knowledge_source_ids=relevant_source_ids,
    )
)

# 5. Create agent with the instruction
agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='KnowledgeBot',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,
    )
)

print(f'Agent created with knowledge sources: {agent.id}')
```

## Complete Example

```python
import os

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateInstructionConfiguration,
    CreateAgentConfiguration,
)
from wiil.models.type_definitions import BusinessSupportServices
from wiil.types import PaginationRequest

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def explore_knowledge_sources():
    # 1. List all knowledge sources
    all_sources = client.knowledge_sources.list(
        params=PaginationRequest(page=1, page_size=100)
    )

    print(f'Total knowledge sources: {all_sources.meta.total_count}')

    if not all_sources.data:
        print('No knowledge sources available')
        return

    # 2. Categorize by type
    by_type = {}

    for source in all_sources.data:
        source_type = source.type or 'unknown'
        by_type[source_type] = by_type.get(source_type, 0) + 1

    print('\nKnowledge sources by type:')
    for source_type, count in by_type.items():
        print(f'  {source_type}: {count}')

    # 3. Get details of a specific source
    source_id = all_sources.data[0].id
    source_details = client.knowledge_sources.get(source_id)

    print('\nSource details:')
    print(f'  ID: {source_details.id}')
    print(f'  Name: {source_details.name}')
    print(f'  Type: {source_details.type}')

    # 4. Example: Create an agent with knowledge sources
    print('\nExample: Creating agent with knowledge sources...')

    models = client.support_models.list()
    model = next(
        (m for m in models if m.type == 'multi_mode' and not m.discontinued),
        None
    )
    if not model:
        print('No model available')
        return

    # Select first 3 knowledge sources
    selected_source_ids = [s.id for s in all_sources.data[:3]]

    import time
    timestamp = int(time.time())

    instruction = client.instruction_configs.create(
        CreateInstructionConfiguration(
            instruction_name=f'KS_Test_Instructions_{timestamp}',
            role='Knowledge Base Agent',
            introduction_message='Hello! I can answer questions using our knowledge base.',
            instructions='Answer questions using the linked knowledge sources.',
            guardrails='Cite sources when providing information.',
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
            knowledge_source_ids=selected_source_ids,
        )
    )

    print(f'Instruction created with {len(selected_source_ids)} knowledge sources')

    agent = client.agent_configs.create(
        CreateAgentConfiguration(
            name='KnowledgeAgent',
            model_id=model.model_id,
            instruction_configuration_id=instruction.id,
        )
    )

    print(f'Agent created: {agent.id}')

    # Cleanup
    client.agent_configs.delete(agent.id)
    client.instruction_configs.delete(instruction.id)
    print('Cleanup complete')


if __name__ == '__main__':
    explore_knowledge_sources()
```

## Best Practices

1. **Select relevant sources** - Only link knowledge sources that are relevant to the agent's purpose. Too many sources can slow down responses.

2. **Check source availability** - Always list and verify knowledge sources exist before referencing them in instruction configurations.

3. **Use appropriate source types** - Match source types to your use case:
   - FAQs for common questions
   - Documentation for technical details
   - Product catalogs for sales agents

4. **Keep sources updated** - Knowledge sources should be kept current. Outdated information can lead to incorrect agent responses.

## Troubleshooting

### Knowledge Source Not Found

**Error:**
```
WiilAPIError: Knowledge source not found
```

**Solution:**
Verify the source ID exists by listing available sources:

```python
sources = client.knowledge_sources.list()

source_ids = [s.id for s in sources.data]
print(f'Available source IDs: {source_ids}')

# Check if your ID exists
target_id = 'ks_123'
if target_id in source_ids:
    source = client.knowledge_sources.get(target_id)
    print(f'Source found: {source.name}')
else:
    print('Source not found in available sources')
```

### No Knowledge Sources Available

If no knowledge sources exist, they need to be created through the WIIL Console or admin API. Knowledge sources are typically managed by administrators and include:

- Uploaded documents (PDFs, text files)
- FAQ databases
- Product catalogs
- Help center content
- Custom knowledge bases

### Invalid Knowledge Source Reference

**Error:**
```
WiilValidationError: Invalid knowledge_source_ids
```

**Solution:**
Ensure all referenced knowledge source IDs are valid:

```python
sources = client.knowledge_sources.list()
valid_ids = {s.id for s in sources.data}

requested_ids = ['ks_123', 'ks_456', 'ks_789']
invalid_ids = [id for id in requested_ids if id not in valid_ids]

if invalid_ids:
    print(f'Invalid knowledge source IDs: {invalid_ids}')

valid_requested_ids = [id for id in requested_ids if id in valid_ids]
# Use valid_requested_ids in your instruction configuration
```
