# Support Models Guide

This guide covers accessing the WIIL Platform Support Model Registry using the Python SDK. The registry maintains a curated list of LLM models from various providers (OpenAI, Anthropic, Google, ElevenLabs, etc.) that are supported by the platform.

## Quick Start

```python
import os
from wiil import WiilClient

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

# Get the default multi-mode model for agent configurations
model = client.support_models.get_default_multi_mode()

print('Model ID:', model.model_id)
print('Name:', model.name)
print('Proprietor:', model.proprietor)
```

## Architecture Overview

The Support Model Registry is a **read-only resource** that provides:

- **Centralized Catalog**: All supported LLM models with their capabilities
- **Model Types**: TEXT, VOICE (TTS), STT, MULTI_MODE, etc.
- **Provider Info**: OpenAI, Anthropic, Google, ElevenLabs, Deepgram, Cartesia
- **Used By**: Agent Configurations reference models via `model_id`

**Key Distinction:**
- `model_id`: WIIL Platform unique identifier (use this in configurations)
- `provider_model_id`: Original ID from the provider's system (e.g., 'gpt-4-1106-preview')

## Enums

### SupportedProprietor

```python
from wiil.models.service_mgt import SupportedProprietor

# Available values:
SupportedProprietor.OPENAI      # 'OpenAI'
SupportedProprietor.GOOGLE      # 'Google'
SupportedProprietor.ANTHROPIC   # 'Anthropic'
SupportedProprietor.GROQ        # 'Groq'
SupportedProprietor.DEEPGRAM    # 'Deepgram'
SupportedProprietor.ELEVENLABS  # 'ElevenLabs'
SupportedProprietor.CARTESIA    # 'Cartesia'
```

### LLMType

```python
from wiil.models.service_mgt import LLMType

# Available values:
LLMType.STS              # 'sts' - Speech-to-speech
LLMType.TTS              # 'tts' - Text-to-speech
LLMType.STT              # 'stt' - Speech-to-text
LLMType.TRANSCRIBE       # 'transcribe' - Transcription
LLMType.TEXT_PROCESSING  # 'text' - Text processing
LLMType.MULTI_MODE       # 'multi_mode' - Multi-modal
```

## Support Model Schema

| Field | Type | Description |
|-------|------|-------------|
| model_id | str | WIIL Platform unique model identifier |
| name | str | Human-readable model name |
| proprietor | SupportedProprietor | Model provider (OpenAI, Anthropic, etc.) |
| provider_model_id | str | Original provider model ID |
| description | str | Model capabilities and use cases |
| type | LLMType | Model functionality type |
| discontinued | bool | Whether model is discontinued |
| supported_voices | list[Voice] | Available voices (for TTS models) |
| support_languages | list[Language] | Supported languages |

## Operations

### List All Models

```python
models = client.support_models.list()

print('Available models:', len(models.data))
for model in models.data:
    print(f'- {model.name} ({model.proprietor}) - {model.type}')
```

### Get Model by ID

```python
model = client.support_models.get('model_123')

print('Model:', model.name)
print('Proprietor:', model.proprietor)
print('Provider Model ID:', model.provider_model_id)
print('Type:', model.type)
print('Discontinued:', model.discontinued)
```

### Get Default Models

The registry provides default models for each capability type:

```python
# Default multi-mode model (for agent configurations)
multi_mode = client.support_models.get_default_multi_mode()
print('Default multi-mode:', multi_mode.name if multi_mode else None)

# Default Text-to-Speech model
tts = client.support_models.get_default_tts()
print('Default TTS:', tts.name if tts else None)
if tts and tts.supported_voices:
    print('Available voices:', len(tts.supported_voices))

# Default Speech-to-Text model
stt = client.support_models.get_default_stt()
print('Default STT:', stt.name if stt else None)
if stt and stt.support_languages:
    print('Supported languages:', len(stt.support_languages))

# Default Speech-to-Speech model
sts = client.support_models.get_default_sts()
print('Default STS:', sts.name if sts else None)

# Default Transcription model
transcribe = client.support_models.get_default_transcribe()
print('Default transcription:', transcribe.name if transcribe else None)

# Default Batch processing model
batch = client.support_models.get_default_batch()
print('Default batch:', batch.name if batch else None)

# Default Translation STT model
translation_stt = client.support_models.get_default_translation_stt()
print('Default translation STT:', translation_stt.name if translation_stt else None)

# Default Translation TTS model
translation_tts = client.support_models.get_default_translation_tts()
print('Default translation TTS:', translation_tts.name if translation_tts else None)
```

### Lookup Models

Find models by type and proprietor or by provider model ID:

```python
# Get model by type and proprietor
text_model = client.support_models.get_by_type_and_proprietor('TEXT', 'OpenAI')
if text_model:
    print('Found:', text_model.name)

# Get model by proprietor and provider model ID
specific_model = client.support_models.get_by_proprietor_and_provider_model_id(
    'Google',
    'gemini-2.0-flash-exp'
)
if specific_model:
    print('Wiil Model ID:', specific_model.model_id)
```

### Check Model Support

Verify if a specific model is supported:

```python
# Check if a model is supported
is_supported = client.support_models.is_supported('OpenAI', 'gpt-4-turbo')
if is_supported:
    print('Model is supported')
else:
    print('Model is not supported')

# Validate models before configuration
stt_supported = client.support_models.is_supported('Deepgram', 'nova-2')
tts_supported = client.support_models.is_supported('ElevenLabs', 'eleven_turbo_v2')

print('STT supported:', stt_supported)
print('TTS supported:', tts_supported)
```

## Complete Example

Full workflow demonstrating support models usage:

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import (
    LLMType,
    SupportedProprietor,
    BusinessSupportServices,
    CreateInstructionConfiguration,
    CreateAgentConfiguration
)

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

def explore_support_models():
    # 1. List all available models
    all_models = client.support_models.list()
    print('Total models in registry:', all_models.meta.total_count)

    # 2. Group models by type
    models_by_type = {}
    for model in all_models.data:
        model_type = model.type
        models_by_type[model_type] = models_by_type.get(model_type, 0) + 1

    print('Models by type:', models_by_type)

    # 3. Get default model for agent configuration
    default_model = client.support_models.get_default_multi_mode()
    if not default_model:
        raise Exception('No default multi-mode model available')

    print('Using model:', default_model.name)
    print('Model ID:', default_model.model_id)

    # 4. Create instruction configuration
    instruction = client.instruction_configs.create(
        CreateInstructionConfiguration(
            instruction_name='Demo Agent Instructions',
            role='Demo Agent',
            introduction_message='Hello!',
            instructions='You are a helpful assistant.',
            guardrails='Be professional.',
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT]
        )
    )

    # 5. Create agent configuration with the model
    agent = client.agent_configs.create(
        CreateAgentConfiguration(
            name='DemoAgent',
            model_id=default_model.model_id,
            instruction_configuration_id=instruction.id
        )
    )

    print('Agent created with model:', agent.model_id)

    # 6. Explore voice models for phone agents
    tts_model = client.support_models.get_default_tts()
    if tts_model and tts_model.supported_voices:
        print('Available voices for TTS:')
        for voice in tts_model.supported_voices[:5]:
            print(f'  - {voice.name} ({voice.voice_id})')

    # 7. Explore STT models for transcription
    stt_model = client.support_models.get_default_stt()
    if stt_model and stt_model.support_languages:
        print('Supported languages for STT:')
        for lang in stt_model.support_languages[:5]:
            print(f'  - {lang.name} ({lang.code})')

    # 8. Clean up
    client.agent_configs.delete(agent.id)
    client.instruction_configs.delete(instruction.id)
    print('Cleanup complete')

if __name__ == '__main__':
    explore_support_models()
```

## Best Practices

1. **Always use `get_default_multi_mode()` for agent configs** - This returns the recommended model for general agent configurations. Avoid hardcoding model IDs.

2. **Check for None results** - Default model methods return `None` if no model is configured. Always handle this case.

3. **Use `is_supported()` for validation** - Before using a specific provider model ID, verify it's supported by the platform.

4. **Avoid discontinued models** - Check the `discontinued` flag before using a model. Discontinued models are only for legacy support.

5. **Match model type to use case** - Use the appropriate model type for your needs:
   - `MULTI_MODE` for general agents
   - `TTS` for voice synthesis
   - `STT` for speech recognition
   - `TRANSCRIBE` for transcription

## Troubleshooting

### Model Not Found

**Error:**
```
WiilAPIError: Model not found
```

**Solution:**
Verify the model ID is correct by listing all available models:

```python
models = client.support_models.list()
model = next((m for m in models.data if m.model_id == 'your-model-id'), None)
if not model:
    print('Available models:')
    for m in models.data:
        print(f'  {m.model_id}: {m.name}')
```

### No Default Model Available

**Error:**
```
AttributeError: 'NoneType' object has no attribute 'model_id'
```

**Solution:**
Always check if the default model exists:

```python
model = client.support_models.get_default_multi_mode()
if not model:
    # Fall back to listing and selecting first available
    models = client.support_models.list()
    if models.data:
        model = models.data[0]
    else:
        raise Exception('No models available in registry')
```

### Model is Discontinued

**Warning:** Using a discontinued model may result in degraded service.

**Solution:**
Check the discontinued flag and use an active model:

```python
models = client.support_models.list()
active_models = [m for m in models.data if not m.discontinued]

print('Active models:', len(active_models))
for m in active_models:
    print(f'- {m.name} ({m.proprietor})')
```
