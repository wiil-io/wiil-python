# Provisioning Configurations Guide

This guide covers creating and managing provisioning configurations using the WIIL Platform Python SDK. Provisioning configurations define voice processing chains (STT -> Processing -> TTS) and translation configurations for AI deployments.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    SupportedProprietor,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

client = WiilClient(api_key='your-api-key')

chain = client.provisioning_configs.create(
    CreateProvisioningConfig(
        chain_name='customer-support-voice-chain',
        description='Voice processing chain for customer support',
        stt_config=DynamicSTTModelConfiguration(
            provider_type=SupportedProprietor.DEEPGRAM.value,
            provider_model_id='nova-2',
            language_id='en-US'
        ),
        processing_config=DynamicModelConfiguration(
            provider_type=SupportedProprietor.OPENAI.value,
            provider_model_id='gpt-4o-mini'
        ),
        tts_config=DynamicTTSModelConfiguration(
            provider_type=SupportedProprietor.ELEVENLABS.value,
            provider_model_id='eleven_turbo_v2',
            language_id='en-US',
            voice_id='voice_rachel'
        )
    )
)

print(f'Chain created: {chain.id}')
```

## Architecture Overview

Provisioning configurations define **voice processing chains**:

- **STT Config**: Speech-to-Text configuration for converting voice input to text
- **Processing Config**: The AI model that processes the text
- **TTS Config**: Text-to-Speech configuration for converting responses to voice

**Use Cases:**
- Phone-based AI assistants
- Voice-enabled web applications
- Real-time translation services

## Provisioning Chain Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chain_name | str | Yes | Unique name for the chain |
| description | str | No | Description of the chain's purpose |
| stt_config | DynamicSTTModelConfiguration | Yes | Speech-to-Text configuration |
| processing_config | DynamicModelConfiguration | Yes | Processing model configuration |
| tts_config | DynamicTTSModelConfiguration | Yes | Text-to-Speech configuration |

### STT Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider_type | str | Yes | Provider type (e.g., 'deepgram', 'google') |
| provider_model_id | str | Yes | Provider's model ID |
| language_id | str | Yes | Input language (e.g., 'en-US') |

### Processing Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider_type | str | Yes | Provider type (e.g., 'openai', 'anthropic') |
| provider_model_id | str | Yes | Provider's model ID |

### TTS Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider_type | str | Yes | Provider type (e.g., 'elevenlabs', 'google') |
| provider_model_id | str | Yes | Provider's model ID |
| language_id | str | Yes | Output language (e.g., 'en-US') |
| voice_id | str | Yes | Voice ID from the TTS model's supported voices |

## CRUD Operations

### Create Provisioning Configuration

```python
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    SupportedProprietor,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

chain = client.provisioning_configs.create(
    CreateProvisioningConfig(
        chain_name='voice-support-chain',
        description='Voice processing for customer support',
        stt_config=DynamicSTTModelConfiguration(
            provider_type=SupportedProprietor.DEEPGRAM.value,
            provider_model_id='nova-2',
            language_id='en-US'
        ),
        processing_config=DynamicModelConfiguration(
            provider_type=SupportedProprietor.OPENAI.value,
            provider_model_id='gpt-4o-mini'
        ),
        tts_config=DynamicTTSModelConfiguration(
            provider_type=SupportedProprietor.ELEVENLABS.value,
            provider_model_id='eleven_turbo_v2',
            language_id='en-US',
            voice_id='voice_rachel'
        )
    )
)

print(f'Chain created: {chain.id}')
print(f'Chain name: {chain.chain_name}')
```

### Create Translation Configuration

```python
from wiil.models.service_mgt import (
    CreateTranslationChainConfig,
    SupportedProprietor,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

translation_chain = client.provisioning_configs.create_translation(
    CreateTranslationChainConfig(
        chain_name='english-spanish-translation',
        description='Real-time English to Spanish translation',
        stt_config=DynamicSTTModelConfiguration(
            provider_type=SupportedProprietor.DEEPGRAM.value,
            provider_model_id='nova-2',
            language_id='en'
        ),
        processing_config=DynamicModelConfiguration(
            provider_type=SupportedProprietor.OPENAI.value,
            provider_model_id='gpt-4o-mini'
        ),
        tts_config=DynamicTTSModelConfiguration(
            provider_type=SupportedProprietor.ELEVENLABS.value,
            provider_model_id='eleven_multilingual_v2',
            language_id='es',
            voice_id='spanish-voice-id'
        ),
        is_translation=True
    )
)

print(f'Translation chain created: {translation_chain.id}')
```

### Get Provisioning Configuration

```python
# Get by ID
chain = client.provisioning_configs.get('chain_123')
print(f'Chain name: {chain.chain_name}')

# Get by chain name
by_name = client.provisioning_configs.get_by_chain_name('voice-support-chain')
print(f'Found chain: {by_name.id}')
```

### List Provisioning Configurations

```python
from wiil.types import PaginationRequest

# List all configurations
all_configs = client.provisioning_configs.list(
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Total configs: {all_configs.meta.total_count}')

# List only provisioning chains (STT -> Processing -> TTS)
provisioning_chains = client.provisioning_configs.list_provisioning_chains()
print(f'Provisioning chains: {len(provisioning_chains.data)}')

# List only translation chains
translation_chains = client.provisioning_configs.list_translation_chains()
print(f'Translation chains: {len(translation_chains.data)}')
```

### Update Provisioning Configuration

```python
from wiil.models.service_mgt import UpdateProvisioningConfig

updated = client.provisioning_configs.update(
    UpdateProvisioningConfig(
        id='chain_123',
        description='Updated voice processing chain',
        chain_name='updated-voice-chain',
    )
)

print(f'Updated chain: {updated.chain_name}')
```

### Delete Provisioning Configuration

```python
deleted = client.provisioning_configs.delete('chain_123')

if deleted:
    print('Chain deleted successfully')
```

## Full Example with Voice

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    SupportedProprietor,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])

chain = client.provisioning_configs.create(
    CreateProvisioningConfig(
        # Required
        chain_name='customer-support-voice-chain',

        # Optional - Description
        description='Voice processing chain for customer support calls',

        # Required - STT Configuration
        stt_config=DynamicSTTModelConfiguration(
            provider_type=SupportedProprietor.DEEPGRAM.value,
            provider_model_id='nova-2',
            language_id='en-US'
        ),

        # Required - Processing Configuration
        processing_config=DynamicModelConfiguration(
            provider_type=SupportedProprietor.OPENAI.value,
            provider_model_id='gpt-4o-mini'
        ),

        # Required - TTS Configuration
        tts_config=DynamicTTSModelConfiguration(
            provider_type=SupportedProprietor.ELEVENLABS.value,
            provider_model_id='eleven_turbo_v2',
            language_id='en-US',
            voice_id='voice_rachel'
        )
    )
)

print(f'Chain created: {chain.id}')
print(f'Chain name: {chain.chain_name}')
```

---

## Voice Configuration

### Overview

Provisioning chains require Speech-to-Text (STT), Processing, and Text-to-Speech (TTS) configurations to define the complete voice processing pipeline.

### STT Configuration

```python
from wiil.models.service_mgt import SupportedProprietor
from wiil.models.service_mgt.dynamic_setup import DynamicSTTModelConfiguration

stt_config = DynamicSTTModelConfiguration(
    provider_type=SupportedProprietor.DEEPGRAM.value,  # Required
    provider_model_id='nova-2',                         # Required
    language_id='en-US'                                 # Optional, default: 'en'
)
```

### Processing Configuration

```python
from wiil.models.service_mgt import SupportedProprietor
from wiil.models.service_mgt.dynamic_setup import DynamicModelConfiguration

processing_config = DynamicModelConfiguration(
    provider_type=SupportedProprietor.OPENAI.value,  # Required
    provider_model_id='gpt-4o-mini'                  # Required
)
```

### TTS Configuration

```python
from wiil.models.service_mgt import SupportedProprietor
from wiil.models.service_mgt.dynamic_setup import DynamicTTSModelConfiguration

tts_config = DynamicTTSModelConfiguration(
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
stt_config = DynamicSTTModelConfiguration(
    provider_type=SupportedProprietor.DEEPGRAM.value,
    provider_model_id='nova-2',
    language_id='en-US'
)
```

**For Processing (LLM):**

```python
processing_config = DynamicModelConfiguration(
    provider_type=SupportedProprietor.OPENAI.value,
    provider_model_id='gpt-4o-mini'
)
```

**For TTS (Text-to-Speech):**

```python
tts_config = DynamicTTSModelConfiguration(
    provider_type=SupportedProprietor.ELEVENLABS.value,
    provider_model_id='eleven_turbo_v2',
    language_id='en-US',
    voice_id='voice_rachel'
)
```

---

## Complete Lifecycle Example

Full workflow demonstrating provisioning configuration lifecycle with dynamic model discovery:

```python
import os

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    CreateInstructionConfiguration,
    CreateAgentConfiguration,
    UpdateProvisioningConfig,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)
from wiil.models.type_definitions import BusinessSupportServices

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def create_voice_processing_chain():
    # 1. Get available models
    print('Fetching available models...')
    models = client.support_models.list()

    stt_model = next(
        (m for m in models if m.type == 'stt' and not m.discontinued),
        None
    )
    processing_model = next(
        (m for m in models if m.type in ('text', 'multi_mode') and not m.discontinued),
        None
    )
    tts_model = next(
        (m for m in models
         if m.type == 'tts' and not m.discontinued and m.supported_voices),
        None
    )

    if not all([stt_model, processing_model, tts_model]):
        raise ValueError('Required models not available')

    print(f'Using STT model: {stt_model.name}')
    print(f'Using Processing model: {processing_model.name}')
    print(f'Using TTS model: {tts_model.name}')

    # 2. Create instruction configuration
    instruction = client.instruction_configs.create(
        CreateInstructionConfiguration(
            instruction_name='Voice Agent Instructions',
            role='Voice Support Agent',
            introduction_message='Hello, how can I help you today?',
            instructions='You are a helpful voice support agent. Be concise.',
            guardrails='Keep responses brief for voice interactions.',
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
        )
    )
    print(f'Instruction created: {instruction.id}')

    # 3. Create agent configuration
    agent = client.agent_configs.create(
        CreateAgentConfiguration(
            name='VoiceAgent',
            model_id='model_gpt4_turbo',
            instruction_configuration_id=instruction.id,
        )
    )
    print(f'Agent created: {agent.id}')

    # 4. Create provisioning chain
    import time
    timestamp = int(time.time())

    chain = client.provisioning_configs.create(
        CreateProvisioningConfig(
            chain_name=f'voice-chain-{timestamp}',
            description='Voice processing chain for phone support',
            stt_config=DynamicSTTModelConfiguration(
                provider_type=stt_model.proprietor,
                provider_model_id=stt_model.provider_model_id,
                language_id='en-US',
            ),
            processing_config=DynamicModelConfiguration(
                provider_type=processing_model.proprietor,
                provider_model_id=processing_model.provider_model_id,
            ),
            tts_config=DynamicTTSModelConfiguration(
                provider_type=tts_model.proprietor,
                provider_model_id=tts_model.provider_model_id,
                language_id='en-US',
                voice_id=tts_model.supported_voices[0].voice_id,
            ),
        )
    )
    print(f'Provisioning chain created: {chain.id}')

    # 5. Retrieve and verify
    retrieved = client.provisioning_configs.get(chain.id)
    print(f'Retrieved chain: {retrieved.chain_name}')

    # 6. List all provisioning chains
    all_chains = client.provisioning_configs.list_provisioning_chains()
    print(f'Total provisioning chains: {all_chains.meta.total_count}')

    # 7. Update the chain
    updated = client.provisioning_configs.update(
        UpdateProvisioningConfig(
            id=chain.id,
            description='Updated voice processing chain',
        )
    )
    print('Updated chain description')

    # 8. Clean up
    client.provisioning_configs.delete(chain.id)
    print('Chain deleted')

    client.agent_configs.delete(agent.id)
    print('Agent deleted')

    client.instruction_configs.delete(instruction.id)
    print('Instruction deleted')

    print('Cleanup complete!')


if __name__ == '__main__':
    create_voice_processing_chain()
```

## Best Practices

1. **Verify model availability** - Always check that STT, Processing, and TTS models are available and not discontinued before creating chains.

2. **Use compatible voice IDs** - The `voice_id` must come from the TTS model's `supported_voices` array.

3. **Match languages** - Ensure the STT and TTS configurations use compatible languages.

4. **Use descriptive chain names** - Chain names should clearly indicate the purpose (e.g., 'customer-support-voice-en-us').

5. **Clean up in order** - Delete provisioning chains before deleting related configurations.

## Troubleshooting

### Model Not Found

**Error:**
```
WiilAPIError: STT model not found
```

**Solution:**
Verify the model exists and is not discontinued:

```python
models = client.support_models.list()
active_stt = [m for m in models if m.type == 'stt' and not m.discontinued]

print('Available STT models:')
for m in active_stt:
    print(f'  {m.proprietor}/{m.provider_model_id}: {m.name}')
```

### Invalid Voice ID

**Error:**
```
WiilValidationError: Voice ID not found for TTS model
```

**Solution:**
Use a voice ID from the TTS model's supported voices:

```python
tts_model = next(
    (m for m in models if m.type == 'tts' and m.supported_voices),
    None
)

if tts_model and tts_model.supported_voices:
    print('Available voices:')
    for v in tts_model.supported_voices:
        print(f'  {v.voice_id}: {v.name}')
```

### Unsupported Model

**Error:**
```
WiilValidationError: Unsupported STT model: provider/model-id
```

**Solution:**
The SDK validates models against the support registry. Verify the model is supported:

```python
# Check if a specific model is supported
is_supported = client.support_models.supports('deepgram', 'nova-2')
print(f'Model supported: {is_supported}')
```

### Chain Name Already Exists

**Error:**
```
WiilAPIError: Chain name already exists
```

**Solution:**
Use unique chain names or check existing chains first:

```python
try:
    existing = client.provisioning_configs.get_by_chain_name('my-chain')
    print(f'Chain already exists: {existing.id}')
except Exception:
    # Chain doesn't exist, safe to create
    chain = client.provisioning_configs.create(
        CreateProvisioningConfig(
            chain_name='my-chain',
            # ...
        )
    )
```
