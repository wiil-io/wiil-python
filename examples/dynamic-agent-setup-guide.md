# Dynamic Agent Setup Guide

**Simplified, single-call AI agent deployment**

This guide covers the Dynamic Agent Setup API - a streamlined approach to deploying AI agents that abstracts the multi-step configuration process into single API calls.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Phone Agent Setup](#phone-agent-setup)
4. [Web Agent Setup](#web-agent-setup)
5. [Updating Configurations](#updating-configurations)
6. [Voice Configuration (STT/TTS)](#voice-configuration-stttts)
7. [Role Templates & Capabilities](#role-templates--capabilities)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)

---

## Introduction

### What is Dynamic Agent Setup?

The Dynamic Agent Setup API provides a **simplified alternative** to the traditional [Fundamental Configuration Setup](./fundamental-configuration-setup.md) workflow. Instead of making 7+ separate API calls to create instruction configs, agent configs, deployment channels, and deployment configurations, you can deploy a fully functional AI agent with a single API call.

### Comparison

| Traditional Setup | Dynamic Setup |
| ----------------- | ------------- |
| 7+ separate API calls | Single API call |
| Create instruction config | Auto-generated |
| Create agent config | Auto-generated |
| Create deployment channel | Auto-generated |
| Create deployment config | Auto-generated |
| Manual linking | Automatic |

### When to Use Dynamic Setup

**Choose Dynamic Setup when:**

- Rapid prototyping and testing
- Standard use cases without complex customization
- Quick deployments for demos or MVPs
- You want simplicity over granular control

**Choose Traditional Setup when:**

- You need fine-grained control over each configuration
- Custom instruction configurations with detailed guidelines
- Complex multi-agent deployments
- Advanced deployment channel configurations

### Prerequisites

1. **WIIL Platform Account** - Sign up at [https://console.wiil.io](https://console.wiil.io)
2. **API Key** - Generate in **Settings** → **API Keys**
3. **SDK Installation**:

   ```bash
   pip install wiil
   ```

---

## Quick Start

### Minimal Phone Agent

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import BusinessSupportServices

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

result = client.dynamic_phone_agent.create(
    assistant_name='Sarah',
    capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT]
)

print('Phone number:', result.phone_number)
print('Agent ID:', result.agent_configuration_id)
```

### Minimal Web Agent

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import BusinessSupportServices

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

result = client.dynamic_web_agent.create(
    assistant_name='Emma',
    website_url='https://example.com',
    capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT]
)

print('Integration snippets:', result.integration_snippets)
print('Agent ID:', result.agent_configuration_id)
```

---

## Phone Agent Setup

### Overview

The Dynamic Phone Agent API provisions a phone-based AI agent with automatic phone number assignment.

### Required Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `assistant_name` | `str` | Name of the AI assistant |
| `capabilities` | `list[BusinessSupportServices]` | Platform services enabled for this agent |

### Optional Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `role_template_identifier` | `AgentRoleTemplateIdentifier` | Role/persona for the agent |
| `language` | `str` | Language code (default: `"en"`) |
| `phone_configuration_id` | `str` | Existing phone configuration to use |
| `test_phone_number` | `str` | Phone number for testing |
| `instruction_configuration_id` | `str` | Existing instruction config to use |
| `knowledge_source_ids` | `list[str]` | Knowledge sources to associate |
| `voice` | `str` | Voice ID for the assistant |
| `provider_type` | `SupportedProprietor` | AI model provider |
| `provider_model_id` | `str` | Specific model ID |
| `stt_configuration` | `DynamicSTTModelConfiguration` | Speech-to-text config |
| `tts_configuration` | `DynamicTTSModelConfiguration` | Text-to-speech config |

### Full Example with Voice

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import (
    BusinessSupportServices,
    AgentRoleTemplateIdentifier,
    SupportedProprietor,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration
)

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

result = client.dynamic_phone_agent.create(
    # Required
    assistant_name='Marcus',
    capabilities=[
        BusinessSupportServices.APPOINTMENT_MANAGEMENT,
        BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT
    ],

    # Optional - Role & Language
    role_template_identifier=AgentRoleTemplateIdentifier.CUSTOMER_SUPPORT_GENERAL,
    language='en-US',

    # Optional - Phone Configuration
    phone_configuration_id='phone_config_123',

    # Optional - Voice Configuration
    stt_configuration=DynamicSTTModelConfiguration(
        provider_type=SupportedProprietor.DEEPGRAM.value,
        provider_model_id='nova-2',
        language_id='en-US'
    ),
    tts_configuration=DynamicTTSModelConfiguration(
        provider_type=SupportedProprietor.ELEVENLABS.value,
        provider_model_id='eleven_turbo_v2',
        language_id='en-US',
        voice_id='voice_rachel'
    )
)

print('Setup successful:', result.success)
print('Phone number:', result.phone_number)
print('Agent Config ID:', result.agent_configuration_id)
print('Instruction Config ID:', result.instruction_configuration_id)
```

### Result Type

The `DynamicPhoneAgentSetupResult` includes:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `success` | `bool` | Whether setup succeeded |
| `agent_configuration_id` | `str` | Created agent config ID |
| `instruction_configuration_id` | `str` | Created instruction config ID |
| `phone_number` | `str` | Provisioned phone number |
| `error_message` | `str` (optional) | Error message if failed |
| `metadata` | `dict` (optional) | Additional metadata |

### CRUD Operations

```python
# Create
created = client.dynamic_phone_agent.create(...)

# Update (partial)
updated = client.dynamic_phone_agent.update(
    id='agent_123',
    assistant_name='Nathan'
)

# Delete
deleted = client.dynamic_phone_agent.delete('agent_123')
```

---

## Web Agent Setup

### Overview

The Dynamic Web Agent API provisions a web-based AI agent with integration snippets for website embedding.

### Required Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `assistant_name` | `str` | Name of the AI assistant |
| `website_url` | `str` | URL of the website |
| `capabilities` | `list[BusinessSupportServices]` | Platform services enabled |

### Optional Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `communication_type` | `OttCommunicationType` | TEXT, VOICE, or UNIFIED (default: UNIFIED) |
| `role_template_identifier` | `AgentRoleTemplateIdentifier` | Role/persona for the agent |
| `language` | `str` | Language code (default: `"en"`) |
| `instruction_configuration_id` | `str` | Existing instruction config |
| `knowledge_source_ids` | `list[str]` | Knowledge sources |
| `voice` | `str` | Voice ID |
| `provider_type` | `SupportedProprietor` | AI model provider |
| `provider_model_id` | `str` | Specific model ID |
| `stt_configuration` | `DynamicSTTModelConfiguration` | Speech-to-text config |
| `tts_configuration` | `DynamicTTSModelConfiguration` | Text-to-speech config |

### Communication Types

```python
from wiil.models.service_mgt import OttCommunicationType

# Text-only chat
communication_type = OttCommunicationType.TEXT

# Voice-only interaction
communication_type = OttCommunicationType.VOICE

# Combined text and voice (default)
communication_type = OttCommunicationType.UNIFIED
```

### Full Example with Voice

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import (
    BusinessSupportServices,
    AgentRoleTemplateIdentifier,
    OttCommunicationType,
    SupportedProprietor,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration
)

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

result = client.dynamic_web_agent.create(
    # Required
    assistant_name='Olivia',
    website_url='https://example.com',
    capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],

    # Optional - Communication Type
    communication_type=OttCommunicationType.UNIFIED,

    # Optional - Role & Language
    role_template_identifier=AgentRoleTemplateIdentifier.CUSTOMER_SUPPORT_GENERAL,
    language='en-US',

    # Optional - Voice Configuration
    stt_configuration=DynamicSTTModelConfiguration(
        provider_type=SupportedProprietor.DEEPGRAM.value,
        provider_model_id='nova-2',
        language_id='en-US'
    ),
    tts_configuration=DynamicTTSModelConfiguration(
        provider_type=SupportedProprietor.ELEVENLABS.value,
        provider_model_id='eleven_turbo_v2',
        language_id='en-US',
        voice_id='voice_rachel'
    )
)

print('Setup successful:', result.success)
print('Agent Config ID:', result.agent_configuration_id)
print('Integration snippets:')
for i, snippet in enumerate(result.integration_snippets):
    print(f'  Snippet {i + 1}:', snippet)
```

### Result Type

The `DynamicWebAgentSetupResult` includes:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `success` | `bool` | Whether setup succeeded |
| `agent_configuration_id` | `str` | Created agent config ID |
| `instruction_configuration_id` | `str` | Created instruction config ID |
| `integration_snippets` | `list[str]` | Code snippets for embedding |
| `error_message` | `str` (optional) | Error message if failed |
| `metadata` | `dict` (optional) | Additional metadata |

### Website Integration

Use the returned integration snippets in your HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Website</title>
</head>
<body>
  <h1>Welcome to Our Website</h1>

  <!-- WIIL Widget - paste integration snippets here -->
  <script src="https://cdn.wiil.io/widget.js"></script>
  <div id="wiil-widget" data-agent="agent_123"></div>
  <script>WiilWidget.init({ agentId: "agent_123" });</script>
</body>
</html>
```

### CRUD Operations

```python
# Create
created = client.dynamic_web_agent.create(...)

# Update (partial)
updated = client.dynamic_web_agent.update(
    id='agent_123',
    assistant_name='Sophia',
    communication_type=OttCommunicationType.TEXT
)

# Delete
deleted = client.dynamic_web_agent.delete('agent_123')

# Get integration snippets separately
snippets = client.dynamic_web_agent.get_integration_snippets('agent_123')
```

---

## Updating Configurations

### Partial Updates

Both phone and web agents support partial updates. Only include the fields you want to change, plus the required `id` field.

```python
# Update phone agent
updated_phone = client.dynamic_phone_agent.update(
    id='agent_123',
    assistant_name='Carlos',
    language='es-MX'
)

# Update web agent
updated_web = client.dynamic_web_agent.update(
    id='agent_456',
    website_url='https://new-website.com',
    communication_type=OttCommunicationType.VOICE
)
```

### Update Voice Configuration

```python
from wiil.models.service_mgt import (
    SupportedProprietor,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration
)

updated = client.dynamic_phone_agent.update(
    id='agent_123',
    stt_configuration=DynamicSTTModelConfiguration(
        provider_type=SupportedProprietor.GOOGLE.value,
        provider_model_id='chirp',
        language_id='en-US'
    ),
    tts_configuration=DynamicTTSModelConfiguration(
        provider_type=SupportedProprietor.ELEVENLABS.value,
        provider_model_id='eleven_multilingual_v2',
        language_id='en-US',
        voice_id='voice_adam'
    )
)
```

---

## Voice Configuration (STT/TTS)

### Overview

Both phone and web agents support voice interactions through Speech-to-Text (STT) and Text-to-Speech (TTS) configurations.

**Important**: STT and TTS configurations must be provided together or neither. You cannot configure one without the other.

### STT Configuration

```python
from wiil.models.service_mgt import (
    SupportedProprietor,
    DynamicSTTModelConfiguration
)

stt_configuration = DynamicSTTModelConfiguration(
    provider_type=SupportedProprietor.DEEPGRAM.value,  # Required
    provider_model_id='nova-2',                         # Required
    language_id='en-US'                                 # Optional, default: 'en'
)
```

### TTS Configuration

```python
from wiil.models.service_mgt import (
    SupportedProprietor,
    DynamicTTSModelConfiguration
)

tts_configuration = DynamicTTSModelConfiguration(
    provider_type=SupportedProprietor.ELEVENLABS.value,  # Required
    provider_model_id='eleven_turbo_v2',                 # Required
    language_id='en-US',                                 # Optional, default: 'en'
    voice_id='voice_rachel'                              # Optional
)
```

### Supported Providers

```python
from wiil.models.service_mgt import SupportedProprietor

# Available providers
SupportedProprietor.OPENAI      # "OpenAI"
SupportedProprietor.GOOGLE      # "Google"
SupportedProprietor.ANTHROPIC   # "Anthropic"
SupportedProprietor.GROQ        # "Groq"
SupportedProprietor.DEEPGRAM    # "Deepgram" - Recommended for STT
SupportedProprietor.ELEVENLABS  # "ElevenLabs" - Recommended for TTS
SupportedProprietor.CARTESIA    # "Cartesia"
```

### Recommended Configurations

**For STT (Speech-to-Text):**

```python
stt_configuration = DynamicSTTModelConfiguration(
    provider_type=SupportedProprietor.DEEPGRAM.value,
    provider_model_id='nova-2',
    language_id='en-US'
)
```

**For TTS (Text-to-Speech):**

```python
tts_configuration = DynamicTTSModelConfiguration(
    provider_type=SupportedProprietor.ELEVENLABS.value,
    provider_model_id='eleven_turbo_v2',
    language_id='en-US',
    voice_id='voice_rachel'  # Choose appropriate voice
)
```

---

## Role Templates & Capabilities

### Agent Role Templates

Role templates define the agent's persona and behavior style:

```python
from wiil.models.service_mgt import AgentRoleTemplateIdentifier

# Available role templates
AgentRoleTemplateIdentifier.CUSTOMER_SUPPORT_GENERAL      # General customer support
AgentRoleTemplateIdentifier.TECHNICAL_SUPPORT_SPECIALIST  # Technical assistance
AgentRoleTemplateIdentifier.SALES_REPRESENTATIVE          # Sales and lead generation
AgentRoleTemplateIdentifier.ONBOARDING_SPECIALIST         # Customer onboarding
AgentRoleTemplateIdentifier.BILLING_SUPPORT_SPECIALIST    # Billing and payments
```

### Business Capabilities

Capabilities define which platform services (tools) the agent can use:

```python
from wiil.models.service_mgt import BusinessSupportServices

# Available capabilities
BusinessSupportServices.APPOINTMENT_MANAGEMENT    # Appointment scheduling
BusinessSupportServices.INVENTORY_MANAGEMENT      # Inventory tracking
BusinessSupportServices.MENU_ORDER_MANAGEMENT     # Restaurant menu orders
BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT  # Product/retail orders
BusinessSupportServices.RESERVATION_MANAGEMENT    # Table/room reservations
BusinessSupportServices.PROPERTY_MANAGEMENT       # Property listings
BusinessSupportServices.NONE                      # No business services
```

### Example: E-commerce Support Agent

```python
result = client.dynamic_web_agent.create(
    assistant_name='Ava',
    website_url='https://shop.example.com',
    capabilities=[
        BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT,
        BusinessSupportServices.INVENTORY_MANAGEMENT
    ],
    role_template_identifier=AgentRoleTemplateIdentifier.CUSTOMER_SUPPORT_GENERAL
)
```

### Example: Restaurant Agent

```python
result = client.dynamic_phone_agent.create(
    assistant_name='Mia',
    capabilities=[
        BusinessSupportServices.RESERVATION_MANAGEMENT,
        BusinessSupportServices.MENU_ORDER_MANAGEMENT
    ],
    role_template_identifier=AgentRoleTemplateIdentifier.CUSTOMER_SUPPORT_GENERAL
)
```

---

## Error Handling

### Error Types

```python
from wiil.errors import (
    WiilAPIError,
    WiilValidationError,
    WiilNetworkError
)

try:
    result = client.dynamic_phone_agent.create(
        assistant_name='Liam',
        capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT]
    )
except WiilValidationError as error:
    # Invalid input data
    print('Validation failed:', error.details)
except WiilAPIError as error:
    # API returned an error
    print(f'API Error {error.status_code}:', error.message)
except WiilNetworkError as error:
    # Network connectivity issue
    print('Network error:', error.message)
```

### Common Errors

| Error | Cause | Solution |
| ----- | ----- | -------- |
| 400 Bad Request | Invalid input data | Check required fields and enum values |
| 401 Unauthorized | Invalid API key | Verify API key is correct and active |
| 404 Not Found | Agent ID doesn't exist | Verify the agent ID is correct |
| 422 Validation Error | STT/TTS mismatch | Provide both STT and TTS configs together |

### STT/TTS Validation

Both configurations must be provided together or neither:

```python
# Valid: Both provided
create_args = {
    'stt_configuration': DynamicSTTModelConfiguration(...),
    'tts_configuration': DynamicTTSModelConfiguration(...)
}

# Valid: Neither provided
create_args = {
    # No STT/TTS config
}

# Invalid: Only one provided - will throw validation error
create_args = {
    'stt_configuration': DynamicSTTModelConfiguration(...)
    # Missing tts_configuration
}
```

---

## Best Practices

### 1. Naming Conventions

Use actual personal names for a natural, human-like experience:

```python
# Good
assistant_name = 'Sarah'
assistant_name = 'Alex'
assistant_name = 'Emma'

# Avoid
assistant_name = 'bot1'
assistant_name = 'test'
assistant_name = 'Customer Support - Premium Tier'
```

### 2. Choose Appropriate Capabilities

Only enable capabilities the agent will actually use:

```python
# Good - specific capabilities for use case
capabilities = [BusinessSupportServices.APPOINTMENT_MANAGEMENT]

# Avoid - enabling everything
capabilities = [
    BusinessSupportServices.APPOINTMENT_MANAGEMENT,
    BusinessSupportServices.INVENTORY_MANAGEMENT,
    BusinessSupportServices.MENU_ORDER_MANAGEMENT,
    BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT,
    BusinessSupportServices.RESERVATION_MANAGEMENT,
    BusinessSupportServices.PROPERTY_MANAGEMENT
]
```

### 3. Web vs Phone Channel Selection

**Use Phone Agent when:**

- Primary interaction is voice calls
- Customers prefer phone support
- Complex issues requiring real-time conversation
- Accessibility requirements

**Use Web Agent when:**

- Website-based customer support
- E-commerce and online services
- Need text and/or voice options
- Integration with web applications

### 4. Voice Configuration

- Use Deepgram Nova-2 for high-quality STT
- Use ElevenLabs for natural-sounding TTS
- Match language IDs across STT and TTS
- Test voice quality in development environment

### 5. Error Handling

Always implement comprehensive error handling in production:

```python
def create_agent():
    try:
        result = client.dynamic_phone_agent.create(...)

        if not result.success:
            print('Setup failed:', result.error_message)
            return None

        return result
    except Exception as error:
        # Handle specific error types
        raise error
```

---

## Support & Resources

### Documentation

- **Platform Docs**: [https://docs.wiil.io](https://docs.wiil.io)
- **API Reference**: [https://docs.wiil.io/developer/api-reference](https://docs.wiil.io/developer/api-reference)
- **SDK Reference**: [https://github.com/wiil-io/wiil-python](https://github.com/wiil-io/wiil-python)

### Support

- **Email**: [dev-support@wiil.io](mailto:dev-support@wiil.io)
- **Console**: [https://console.wiil.io](https://console.wiil.io)
- **GitHub Issues**: [https://github.com/wiil-io/wiil-python/issues](https://github.com/wiil-io/wiil-python/issues)

### Related Guides

- [Fundamental Configuration Setup](./fundamental-configuration-setup.md) - Traditional multi-step setup
- [Voice Channels](./channels/voice-channels.md) - Phone call integration
- [Web Channels](./channels/web-channels.md) - Web chat widget integration

---

*Built with the WIIL team*
