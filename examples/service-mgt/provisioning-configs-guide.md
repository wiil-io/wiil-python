# Translation Chain Configurations Guide

This guide covers creating and managing translation chain configurations using
the WIIL Platform Python SDK. Translation chains define voice processing
pipelines (STT -> Processing -> TTS) for real-time translation deployments.

## Quick Start

```python
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateTranslationChainConfig,
    SupportedProprietor,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

client = WiilClient(api_key='your-api-key')

chain = client.provisioning_configs.create(
    CreateTranslationChainConfig(
        chain_name='english-spanish-translation',
        description='Real-time English to Spanish translation',
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
            provider_model_id='eleven_multilingual_v2',
            language_id='es',
            voice_id='spanish-voice-id'
        )
    )
)

print(f'Translation chain created: {chain.id}')
```

## Architecture Overview

Translation chain configurations define **voice processing pipelines**:

- **STT Config**: Speech-to-Text for converting voice input to text
- **Processing Config**: AI model that processes/translates the text
- **TTS Config**: Text-to-Speech for converting responses to voice

**Use Cases:**

- Real-time translation services
- Multilingual phone assistants
- Voice-enabled translation applications

## Translation Chain Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chain_name | str | Yes | Unique name for the chain |
| description | str | No | Description of the chain's purpose |
| stt_config | DynamicSTTModelConfiguration | Yes | Speech-to-Text config |
| processing_config | DynamicModelConfiguration | Yes | Processing model config |
| tts_config | DynamicTTSModelConfiguration | Yes | Text-to-Speech config |

### STT Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider_type | str | Yes | Provider (e.g., 'deepgram', 'google') |
| provider_model_id | str | Yes | Provider's model ID |
| language_id | str | Yes | Input language (e.g., 'en-US') |

### Processing Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider_type | str | Yes | Provider (e.g., 'openai', 'anthropic') |
| provider_model_id | str | Yes | Provider's model ID |

### TTS Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider_type | str | Yes | Provider (e.g., 'elevenlabs', 'google') |
| provider_model_id | str | Yes | Provider's model ID |
| language_id | str | Yes | Output language (e.g., 'es') |
| voice_id | str | Yes | Voice ID from the TTS model |

## CRUD Operations

### Create Translation Chain

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

chain = client.provisioning_configs.create(
    CreateTranslationChainConfig(
        chain_name='french-english-translation',
        description='French to English real-time translation',
        stt_config=DynamicSTTModelConfiguration(
            provider_type=SupportedProprietor.DEEPGRAM.value,
            provider_model_id='nova-2',
            language_id='fr'
        ),
        processing_config=DynamicModelConfiguration(
            provider_type=SupportedProprietor.OPENAI.value,
            provider_model_id='gpt-4o-mini'
        ),
        tts_config=DynamicTTSModelConfiguration(
            provider_type=SupportedProprietor.ELEVENLABS.value,
            provider_model_id='eleven_multilingual_v2',
            language_id='en-US',
            voice_id='voice_rachel'
        )
    )
)

print(f'Chain created: {chain.id}')
print(f'Chain name: {chain.chain_name}')
```

### Get Translation Chain

```python
# Get by ID
chain = client.provisioning_configs.get('chain_123')
print(f'Chain name: {chain.chain_name}')

# Get by chain name
by_name = client.provisioning_configs.get_by_chain_name(
    'french-english-translation'
)
print(f'Found chain: {by_name.id}')
```

### List Translation Chains

```python
from wiil.types import PaginationRequest

# List all translation chains
chains = client.provisioning_configs.list(
    params=PaginationRequest(page=1, page_size=20)
)

print(f'Total chains: {chains.meta.total_count}')

for chain in chains.data:
    print(f'  {chain.id}: {chain.chain_name}')
```

### Update Translation Chain

```python
from wiil.models.service_mgt import UpdateTranslationChainConfig

updated = client.provisioning_configs.update(
    UpdateTranslationChainConfig(
        id='chain_123',
        description='Updated translation chain description',
        chain_name='updated-translation-chain',
    )
)

print(f'Updated chain: {updated.chain_name}')
```

### Delete Translation Chain

```python
deleted = client.provisioning_configs.delete('chain_123')

if deleted:
    print('Chain deleted successfully')
```

## Full Example

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateTranslationChainConfig,
    SupportedProprietor,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])

chain = client.provisioning_configs.create(
    CreateTranslationChainConfig(
        # Required - Unique chain name
        chain_name='spanish-english-translation',

        # Optional - Description
        description='Spanish to English real-time translation',

        # Required - STT Configuration (source language)
        stt_config=DynamicSTTModelConfiguration(
            provider_type=SupportedProprietor.DEEPGRAM.value,
            provider_model_id='nova-2',
            language_id='es'
        ),

        # Required - Processing Configuration (translation)
        processing_config=DynamicModelConfiguration(
            provider_type=SupportedProprietor.OPENAI.value,
            provider_model_id='gpt-4o-mini'
        ),

        # Required - TTS Configuration (target language)
        tts_config=DynamicTTSModelConfiguration(
            provider_type=SupportedProprietor.ELEVENLABS.value,
            provider_model_id='eleven_multilingual_v2',
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

Translation chains require Speech-to-Text (STT), Processing, and
Text-to-Speech (TTS) configurations to define the complete pipeline.

### STT Configuration

```python
from wiil.models.service_mgt import SupportedProprietor
from wiil.models.service_mgt.dynamic_setup import DynamicSTTModelConfiguration

stt_config = DynamicSTTModelConfiguration(
    provider_type=SupportedProprietor.DEEPGRAM.value,  # Required
    provider_model_id='nova-2',                         # Required
    language_id='es'                                    # Source language
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
    provider_model_id='eleven_multilingual_v2',          # Required
    language_id='en-US',                                 # Target language
    voice_id='voice_rachel'                              # Voice selection
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
    language_id='es'  # Source language
)
```

**For Processing (Translation LLM):**

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
    provider_model_id='eleven_multilingual_v2',
    language_id='en-US',  # Target language
    voice_id='voice_rachel'
)
```

---

## Complete Lifecycle Example

Full workflow demonstrating translation chain lifecycle with dynamic model
discovery:

```python
import os
import time

from wiil import WiilClient
from wiil.models.service_mgt import (
    CreateTranslationChainConfig,
    UpdateTranslationChainConfig,
)
from wiil.models.service_mgt.dynamic_setup import (
    DynamicSTTModelConfiguration,
    DynamicModelConfiguration,
    DynamicTTSModelConfiguration,
)

client = WiilClient(api_key=os.environ['WIIL_API_KEY'])


def create_translation_chain():
    # 1. Get available models
    print('Fetching available models...')
    models = client.support_models.list()

    stt_model = next(
        (m for m in models if m.type == 'stt' and not m.discontinued),
        None
    )
    processing_model = next(
        (m for m in models
         if m.type in ('text', 'multi_mode') and not m.discontinued),
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

    # 2. Create translation chain
    timestamp = int(time.time())

    chain = client.provisioning_configs.create(
        CreateTranslationChainConfig(
            chain_name=f'translation-chain-{timestamp}',
            description='Spanish to English translation',
            stt_config=DynamicSTTModelConfiguration(
                provider_type=stt_model.proprietor,
                provider_model_id=stt_model.provider_model_id,
                language_id='es',
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
    print(f'Translation chain created: {chain.id}')

    # 3. Retrieve and verify
    retrieved = client.provisioning_configs.get(chain.id)
    print(f'Retrieved chain: {retrieved.chain_name}')

    # 4. List all translation chains
    all_chains = client.provisioning_configs.list()
    print(f'Total translation chains: {all_chains.meta.total_count}')

    # 5. Update the chain
    updated = client.provisioning_configs.update(
        UpdateTranslationChainConfig(
            id=chain.id,
            description='Updated translation chain',
        )
    )
    print('Updated chain description')

    # 6. Clean up
    client.provisioning_configs.delete(chain.id)
    print('Chain deleted')

    print('Complete!')


if __name__ == '__main__':
    create_translation_chain()
```

## Best Practices

1. **Verify model availability** - Always check that STT, Processing, and TTS
   models are available and not discontinued before creating chains.

2. **Use compatible voice IDs** - The `voice_id` must come from the TTS
   model's `supported_voices` array.

3. **Match language pairs** - Ensure the STT `language_id` matches the source
   language and TTS `language_id` matches the target language.

4. **Use descriptive chain names** - Chain names should indicate the
   translation direction (e.g., 'spanish-to-english-translation').

5. **Use multilingual models** - For TTS, prefer `eleven_multilingual_v2`
   or similar multilingual models for translation use cases.

## Troubleshooting

### Model Not Found

**Error:**

```text
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

```text
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

```text
WiilValidationError: Unsupported STT model: provider/model-id
```

**Solution:**
The SDK validates models against the support registry. Verify support:

```python
# Check if a specific model is supported
is_supported = client.support_models.supports('deepgram', 'nova-2')
print(f'Model supported: {is_supported}')
```

### Chain Name Already Exists

**Error:**

```text
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
        CreateTranslationChainConfig(
            chain_name='my-chain',
            # ...
        )
    )
```
