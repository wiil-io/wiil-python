# Provisioning Configurations Guide

This guide covers creating and managing provisioning configurations using the WIIL Platform JS SDK. Provisioning configurations define voice processing chains (STT -> Agent -> TTS) and translation configurations for AI deployments.

## Quick Start

```typescript
import { WiilClient } from 'wiil-js';

const client = new WiilClient({
  apiKey: 'your-api-key',
});

// Get STT and TTS models
const sttModel = await client.supportModels.getDefaultSTT();
const ttsModel = await client.supportModels.getDefaultTTS();

// Create a provisioning chain
const chain = await client.provisioningConfigs.create({
  chainName: 'customer-support-voice-chain',
  description: 'Voice processing chain for customer support',
  sttConfig: {
    modelId: sttModel!.modelId,
    defaultLanguage: 'en-US',
  },
  agentConfigurationId: 'agent_123',
  ttsConfig: {
    modelId: ttsModel!.modelId,
    voiceId: ttsModel!.supportedVoices![0].voiceId,
    defaultLanguage: 'en-US',
  },
});

console.log('Chain created:', chain.id);
```

## Architecture Overview

Provisioning configurations define **voice processing chains**:

- **STT Config**: Speech-to-Text configuration for converting voice input to text
- **Agent Configuration**: The AI agent that processes the text
- **TTS Config**: Text-to-Speech configuration for converting responses to voice

**Use Cases:**
- Phone-based AI assistants
- Voice-enabled web applications
- Real-time translation services

## Provisioning Chain Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| chainName | string | Yes | Unique name for the chain |
| description | string | No | Description of the chain's purpose |
| sttConfig | STTConfig | Yes | Speech-to-Text configuration |
| agentConfigurationId | string | Yes | Agent configuration ID |
| ttsConfig | TTSConfig | Yes | Text-to-Speech configuration |

### STT Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| modelId | string | Yes | STT model ID from support models |
| defaultLanguage | string | Yes | Default input language (e.g., 'en-US') |

### TTS Config Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| modelId | string | Yes | TTS model ID from support models |
| voiceId | string | Yes | Voice ID from the TTS model's supported voices |
| defaultLanguage | string | Yes | Default output language (e.g., 'en-US') |

## CRUD Operations

### Create Provisioning Configuration

```typescript
// Get available models
const models = await client.supportModels.list();
const sttModel = models.find(m => m.type === 'stt' && !m.discontinued);
const ttsModel = models.find(m => m.type === 'tts' && !m.discontinued && m.supportedVoices?.length > 0);

if (!sttModel || !ttsModel) {
  throw new Error('Required models not available');
}

// Create the provisioning chain
const chain = await client.provisioningConfigs.create({
  chainName: 'voice-support-chain',
  description: 'Voice processing for customer support',
  sttConfig: {
    modelId: sttModel.modelId,
    defaultLanguage: 'en-US',
  },
  agentConfigurationId: 'agent_123',
  ttsConfig: {
    modelId: ttsModel.modelId,
    voiceId: ttsModel.supportedVoices![0].voiceId,
    defaultLanguage: 'en-US',
  },
});

console.log('Chain created:', chain.id);
console.log('Chain name:', chain.chainName);
```

### Create Translation Configuration

```typescript
const translationChain = await client.provisioningConfigs.createTranslation({
  chainName: 'english-spanish-translation',
  description: 'Real-time English to Spanish translation',
  sourceLanguage: 'en-US',
  targetLanguage: 'es-ES',
  sttModelId: sttModel.modelId,
  ttsModelId: ttsModel.modelId,
  voiceId: ttsModel.supportedVoices![0].voiceId,
});

console.log('Translation chain created:', translationChain.id);
```

### Get Provisioning Configuration

```typescript
// Get by ID
const chain = await client.provisioningConfigs.get('chain_123');
console.log('Chain name:', chain.chainName);

// Get by chain name
const byName = await client.provisioningConfigs.getByChainName('voice-support-chain');
console.log('Found chain:', byName.id);
```

### List Provisioning Configurations

```typescript
// List all configurations
const all = await client.provisioningConfigs.list({
  page: 1,
  pageSize: 20,
});

console.log('Total configs:', all.meta.totalCount);

// List only provisioning chains (STT -> Agent -> TTS)
const provisioningChains = await client.provisioningConfigs.listProvisioningChains();
console.log('Provisioning chains:', provisioningChains.data.length);

// List only translation chains
const translationChains = await client.provisioningConfigs.listTranslationChains();
console.log('Translation chains:', translationChains.data.length);
```

### Update Provisioning Configuration

```typescript
const updated = await client.provisioningConfigs.update({
  id: 'chain_123',
  description: 'Updated voice processing chain',
  chainName: 'updated-voice-chain',
});

console.log('Updated chain:', updated.chainName);
```

### Delete Provisioning Configuration

```typescript
const deleted = await client.provisioningConfigs.delete('chain_123');

if (deleted) {
  console.log('Chain deleted successfully');
}
```

## Complete Example

Full workflow demonstrating provisioning configuration lifecycle:

```typescript
import { WiilClient, LLMType, AssistantType, BusinessSupportServices } from 'wiil-js';

const client = new WiilClient({
  apiKey: process.env.WIIL_API_KEY!,
});

async function createVoiceProcessingChain() {
  // 1. Get available models
  console.log('Fetching available models...');
  const models = await client.supportModels.list();

  const sttModel = models.find(m => m.type === 'stt' && !m.discontinued);
  const ttsModel = models.find(m => m.type === 'tts' && !m.discontinued && m.supportedVoices?.length > 0);
  const agentModel = await client.supportModels.getDefaultMultiMode();

  if (!sttModel || !ttsModel || !agentModel) {
    throw new Error('Required models not available');
  }

  console.log('Using STT model:', sttModel.name);
  console.log('Using TTS model:', ttsModel.name);
  console.log('Using Agent model:', agentModel.name);

  // 2. Create instruction configuration
  const instruction = await client.instructionConfigs.create({
    instructionName: 'Voice Agent Instructions',
    role: 'Voice Support Agent',
    introductionMessage: 'Hello, how can I help you today?',
    instructions: 'You are a helpful voice support agent. Be concise in your responses.',
    guardrails: 'Keep responses brief for voice interactions.',
    supportedServices: [BusinessSupportServices.APPOINTMENT_MANAGEMENT],
  });
  console.log('Instruction created:', instruction.id);

  // 3. Create agent configuration
  const agent = await client.agentConfigs.create({
    name: 'VoiceAgent',
    modelId: agentModel.modelId,
    instructionConfigurationId: instruction.id,
    assistantType: AssistantType.PHONE,
  });
  console.log('Agent created:', agent.id);

  // 4. Create provisioning chain
  const chain = await client.provisioningConfigs.create({
    chainName: `voice-chain-${Date.now()}`,
    description: 'Voice processing chain for phone support',
    sttConfig: {
      modelId: sttModel.modelId,
      defaultLanguage: 'en-US',
    },
    agentConfigurationId: agent.id,
    ttsConfig: {
      modelId: ttsModel.modelId,
      voiceId: ttsModel.supportedVoices![0].voiceId,
      defaultLanguage: 'en-US',
    },
  });
  console.log('Provisioning chain created:', chain.id);

  // 5. Retrieve and verify
  const retrieved = await client.provisioningConfigs.get(chain.id);
  console.log('Retrieved chain:', retrieved.chainName);

  // 6. List all provisioning chains
  const allChains = await client.provisioningConfigs.listProvisioningChains();
  console.log('Total provisioning chains:', allChains.meta.totalCount);

  // 7. Update the chain
  const updated = await client.provisioningConfigs.update({
    id: chain.id,
    description: 'Updated voice processing chain',
  });
  console.log('Updated chain description');

  // 8. Clean up
  await client.provisioningConfigs.delete(chain.id);
  console.log('Chain deleted');

  await client.agentConfigs.delete(agent.id);
  console.log('Agent deleted');

  await client.instructionConfigs.delete(instruction.id);
  console.log('Instruction deleted');

  console.log('Cleanup complete!');
}

createVoiceProcessingChain().catch(console.error);
```

## Best Practices

1. **Verify model availability** - Always check that STT and TTS models are available and not discontinued before creating chains.

2. **Use compatible voice IDs** - The voiceId must come from the TTS model's `supportedVoices` array.

3. **Match languages** - Ensure the STT, agent, and TTS configurations use compatible languages.

4. **Use descriptive chain names** - Chain names should clearly indicate the purpose (e.g., 'customer-support-voice-en-us').

5. **Clean up in order** - Delete provisioning chains before deleting the agent configurations they reference.

## Troubleshooting

### Model Not Found

**Error:**
```
WiilAPIError: STT model not found
```

**Solution:**
Verify the model exists and is not discontinued:

```typescript
const models = await client.supportModels.list();
const activeSTT = models.filter(m => m.type === 'stt' && !m.discontinued);

console.log('Available STT models:');
activeSTT.forEach(m => console.log(`  ${m.modelId}: ${m.name}`));
```

### Invalid Voice ID

**Error:**
```
WiilValidationError: Voice ID not found for TTS model
```

**Solution:**
Use a voice ID from the TTS model's supported voices:

```typescript
const ttsModel = models.find(m => m.type === 'tts' && m.supportedVoices?.length > 0);

if (ttsModel?.supportedVoices) {
  console.log('Available voices:');
  ttsModel.supportedVoices.forEach(v => {
    console.log(`  ${v.voiceId}: ${v.name}`);
  });
}
```

### Chain Name Already Exists

**Error:**
```
WiilAPIError: Chain name already exists
```

**Solution:**
Use unique chain names or check existing chains first:

```typescript
try {
  const existing = await client.provisioningConfigs.getByChainName('my-chain');
  console.log('Chain already exists:', existing.id);
} catch (error) {
  // Chain doesn't exist, safe to create
  const chain = await client.provisioningConfigs.create({
    chainName: 'my-chain',
    // ...
  });
}
```
