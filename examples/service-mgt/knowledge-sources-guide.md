# Knowledge Sources Guide

This guide covers managing knowledge sources using the WIIL Platform Python SDK. Knowledge sources represent repositories of information that AI agents can access for context and factual grounding.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import CreateTextKnowledgeSource

client = WiilClient(api_key='your-api-key')

# Create a text knowledge source
source = client.knowledge_sources.create_text(
    CreateTextKnowledgeSource(
        name='Product FAQ',
        content='Your text content here (minimum 1000 characters)...',
        metadata={'category': 'support', 'version': '1.0'},
    )
)

print('Created:', source.id)
print('Processing status:', source.processing_status)

# List knowledge sources
result = client.knowledge_sources.list()

print('Total sources:', result.meta.total_count)
for source in result.data:
    print(f'- {source.name} ({source.source_type})')
```

## Architecture Overview

Knowledge sources provide:

- **Information Repositories**: Documents, FAQs, product catalogs, and other data
- **Agent Context**: Factual grounding for AI agent responses
- **Referenced by Instructions**: Instruction configurations link to knowledge sources via `knowledge_source_ids`
- **Multi-tier Storage**: Automatic optimization between Firestore (fast) and Cloud Storage (cost-effective)

### Knowledge Source Types

- `document` - Uploaded files (PDF, DOCX, TXT, etc.)
- `url` - Web page content
- `business_website` - Crawled website content
- `corpus` - Text collections (created via `create_text`)
- `batch_document` - Multiple files processed together

### Processing Status

- `pending` - Awaiting processing
- `processing` - Being prepared for AI consumption
- `completed` - Ready for use
- `failed` - Processing error

## Operations

### Create Text Knowledge Source

Create a knowledge source from raw text content (minimum 1000 characters):

```python
from wiil.models.service_mgt import CreateTextKnowledgeSource

source = client.knowledge_sources.create_text(
    CreateTextKnowledgeSource(
        name='Company Policies',
        content='''
            Your comprehensive text content here...
            This must be at least 1000 characters long.
            Include all the information you want the AI agent to access.
            The content will be processed and optimized for AI consumption.
            ...
        ''',
        metadata={
            'category': 'policies',
            'department': 'HR',
            'version': '2.0',
            'last_updated': '2024-01-15',
        },
    )
)

print('Created:', source.id)
print('Name:', source.name)
print('Type:', source.source_type)  # 'corpus'
print('Status:', source.processing_status)
```

### List Knowledge Sources

```python
# List with default pagination
result = client.knowledge_sources.list()

print('Total knowledge sources:', result.meta.total_count)
print('Page:', result.meta.page, 'of', result.meta.total_pages)

for source in result.data:
    print(f'{source.name}:')
    print(f'  ID: {source.id}')
    print(f'  Type: {source.source_type}')
    print(f'  Status: {source.processing_status}')
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
from datetime import datetime

source = client.knowledge_sources.get('ks_123')

print('Knowledge Source:')
print('  ID:', source.id)
print('  Name:', source.name)
print('  Type:', source.source_type)
print('  Status:', source.processing_status)
print('  Storage Tier:', source.storage_tier)
print('  Access Count:', source.access_count)

if source.content_size:
    print(f'  Content Size: {source.content_size / 1024:.2f} KB')

if source.created_at:
    print('  Created:', datetime.fromtimestamp(source.created_at / 1000).isoformat())
```

## API Reference

### `create_text(data)` - Create text knowledge source

```python
source = client.knowledge_sources.create_text(
    CreateTextKnowledgeSource(
        name='FAQ Document',           # Optional - server may auto-name
        content='Text content...',     # Required - min 1000 chars
        metadata={'key': 'value'},     # Optional
    )
)
# Returns: KnowledgeSource
```

### `get(source_id)` - Get by ID

```python
source = client.knowledge_sources.get('ks_123')
# Returns: KnowledgeSource
```

### `list(params?)` - List with pagination

```python
result = client.knowledge_sources.list(
    params=PaginationRequest(page=1, page_size=50)
)
# Returns: PaginatedResult[KnowledgeSource]
```

## Using Knowledge Sources with Instructions

Knowledge sources provide context for AI agents through instruction configurations:

```python
from wiil.models.service_mgt import (
    CreateTextKnowledgeSource,
    CreateInstructionConfiguration,
    CreateAgentConfiguration,
)
from wiil.models.type_definitions import BusinessSupportServices

# 1. Create a knowledge source
faq_source = client.knowledge_sources.create_text(
    CreateTextKnowledgeSource(
        name='Product FAQ',
        content='''
            Q: What are your business hours?
            A: We are open Monday through Friday, 9 AM to 5 PM EST.
            
            Q: How do I return a product?
            A: You can return any product within 30 days for a full refund...
            
            ... (continue with at least 1000 characters of FAQ content)
        ''',
    )
)

# 2. Wait for processing to complete (poll or check later)
print('Processing status:', faq_source.processing_status)

# 3. List all available knowledge sources
sources = client.knowledge_sources.list()
completed_sources = [
    s for s in sources.data
    if s.processing_status == 'completed'
]

# 4. Get a model
models = client.support_models.list()
model = next(
    (m for m in models if m.type == 'multi_mode' and not m.discontinued),
    None
)

# 5. Create instruction with knowledge sources
instruction = client.instruction_configs.create(
    CreateInstructionConfiguration(
        instruction_name='Knowledge-Enhanced Agent',
        role='Support Agent',
        introduction_message='Hello! I have access to our knowledge base.',
        instructions='Use the linked knowledge sources to answer questions accurately.',
        guardrails='Only provide information from verified knowledge sources.',
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
        knowledge_source_ids=[s.id for s in completed_sources],
    )
)

# 6. Create agent with the instruction
agent = client.agent_configs.create(
    CreateAgentConfiguration(
        name='KnowledgeBot',
        model_id=model.model_id,
        instruction_configuration_id=instruction.id,
    )
)

print('Agent created with knowledge sources:', agent.id)
```

## Complete Example

```python
import os
import time
from datetime import datetime

from wiil import WiilClient
from wiil.models.service_mgt import CreateTextKnowledgeSource
from wiil.types import PaginationRequest

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def knowledge_source_workflow():
    # 1. Create a text knowledge source
    print('Creating knowledge source...')
    
    content = '''
        Product Support Knowledge Base
        ==============================
        
        Getting Started
        ---------------
        Welcome to our product! This guide will help you get started quickly.
        
        Installation
        ------------
        1. Download the installer from our website
        2. Run the installer with administrator privileges
        3. Follow the on-screen instructions
        4. Restart your computer when prompted
        
        Common Issues
        -------------
        Q: The application won't start
        A: Try running as administrator or reinstalling the application.
        
        Q: I forgot my password
        A: Click "Forgot Password" on the login screen to reset it.
        
        Q: How do I contact support?
        A: Email support@example.com or call 1-800-EXAMPLE.
        
        ... (additional content to meet 1000 character minimum)
    '''

    source = client.knowledge_sources.create_text(
        CreateTextKnowledgeSource(
            name='Product Support KB',
            content=content,
            metadata={
                'category': 'support',
                'product': 'main-app',
                'version': '1.0',
            },
        )
    )

    print('Created knowledge source:', source.id)
    print('Processing status:', source.processing_status)

    # 2. List all knowledge sources
    all_sources = client.knowledge_sources.list(
        params=PaginationRequest(page_size=100)
    )
    print('\nTotal knowledge sources:', all_sources.meta.total_count)

    # 3. Categorize by type
    by_type = {}
    for s in all_sources.data:
        source_type = s.source_type or 'unknown'
        by_type[source_type] = by_type.get(source_type, 0) + 1

    print('\nKnowledge sources by type:')
    for source_type, count in by_type.items():
        print(f'  {source_type}: {count}')

    # 4. Categorize by processing status
    by_status = {}
    for s in all_sources.data:
        status = s.processing_status or 'unknown'
        by_status[status] = by_status.get(status, 0) + 1

    print('\nKnowledge sources by status:')
    for status, count in by_status.items():
        print(f'  {status}: {count}')

    # 5. Get details of the created source
    source_details = client.knowledge_sources.get(source.id)

    print('\nSource details:')
    print('  ID:', source_details.id)
    print('  Name:', source_details.name)
    print('  Type:', source_details.source_type)
    print('  Status:', source_details.processing_status)
    print('  Storage Tier:', source_details.storage_tier)


if __name__ == '__main__':
    knowledge_source_workflow()
```

## Best Practices

1. **Provide meaningful names** - Use descriptive names that indicate the content purpose.

2. **Structure content well** - Organize text content with clear headings and sections for better AI comprehension.

3. **Include metadata** - Add relevant metadata (categories, versions, dates) for organization and filtering.

4. **Check processing status** - Wait for `completed` status before using knowledge sources in instruction configurations.

5. **Select relevant sources** - Only link knowledge sources that are relevant to the agent's purpose. Too many sources can slow down responses.

6. **Keep sources updated** - Create new versions of knowledge sources when content changes significantly.

## Troubleshooting

### Content Too Short

**Error:**

```text
WiilValidationError: Content must be at least 1000 characters
```

**Solution:**
Ensure your content is at least 1000 characters:

```python
content = '...your text...'
print('Content length:', len(content))

if len(content) < 1000:
    print('Need', 1000 - len(content), 'more characters')
```

### Knowledge Source Not Found

**Error:**

```text
WiilAPIError: Knowledge source not found
```

**Solution:**
Verify the source ID exists by listing available sources:

```python
sources = client.knowledge_sources.list()
source_ids = [s.id for s in sources.data]

target_id = 'ks_123'
if target_id in source_ids:
    source = client.knowledge_sources.get(target_id)
    print('Source found:', source.name)
else:
    print('Source not found')
```

### Processing Failed

If a knowledge source has `processing_status == 'failed'`, the content could not be processed. Check:

- Content is valid text (not binary data)
- Content is at least 1000 characters
- No encoding issues

```python
source = client.knowledge_sources.get('ks_123')

if source.processing_status == 'failed':
    print('Processing failed for:', source.name)
    # Create a new knowledge source with corrected content
```
