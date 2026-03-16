# Fundamental Configuration Setup

**Complete guide from signup to deploying your first AI agent**

This guide walks you through the complete, chronological steps to set up and configure an AI agent in a service channel on the WIIL Platform - from account creation to deployment.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Step 1: Initialize Client & Verify Organization](#step-1-initialize-client--verify-organization)
4. [Step 2: Create or Select Project](#step-2-create-or-select-project)
5. [Step 3: Create Instruction Configuration](#step-3-create-instruction-configuration)
6. [Step 4: Get Wiil Support Models](#step-4-get-wiil-support-models)
7. [Step 5: Create Agent Configuration](#step-5-create-agent-configuration)
8. [Step 5.1: Find Available Phone Numbers](#step-51-find-available-phone-numbers)
9. [Step 6: Create Deployment Channel](#step-6-create-deployment-channel)
10. [Step 7: Create Deployment Configuration](#step-7-create-deployment-configuration)
11. [Step 8: Deploy Agent](#step-8-deploy-agent)
12. [Step 9: Verify Deployment](#step-9-verify-deployment)
13. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have:

1. **WIIL Platform Account**
   - Sign up at [https://console.wiil.io](https://console.wiil.io)
   - Complete email verification

2. **API Key**
   - Navigate to **Settings** → **API Keys** in the WIIL Console
   - Click **Generate New API Key**
   - Copy and securely store your API key

3. **Development Environment**
   - Python 3.9 or higher
   - pip package manager
   - Text editor or IDE

4. **SDK Installation**

   ```bash
   pip install wiil
   ```

---

## Environment Setup

### 1. Create Project Directory

```bash
mkdir my-wiil-agent
cd my-wiil-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install wiil
```

### 2. Configure Environment Variables

Create a `.env` file in your project root:

```env
WIIL_API_KEY=your-api-key-here
```

**Security Note**: Never commit your `.env` file to version control. Add it to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### 3. Create Your Setup Script

Create a new file `setup.py`:

```python
import os
from wiil import WiilClient

# Initialize client
client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

def main():
    # Your setup code will go here
    pass

if __name__ == '__main__':
    main()
```

---

## Step 1: Initialize Client & Verify Organization

**Objective**: Connect to the WIIL Platform and verify your organization details.

### Code

```python
import os
from wiil import WiilClient

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

# Verify your organization
organization = client.organizations.get()

print('Organization Details:')
print(f'  Company Name: {organization.company_name}')
print(f'  Organization ID: {organization.id}')
print(f'  Service Status: {organization.service_status}')
print(f'  Business Vertical: {organization.business_vertical_id}')
```

### Expected Output

```text
Organization Details:
  Company Name: ACME Corporation
  Organization ID: 1a2b3c4d5e
  Service Status: ACTIVE
  Business Vertical: RETAIL
```

### What This Does

- Validates your API key
- Confirms your organization is active
- Retrieves your organization ID (needed for subsequent steps)

---

## Step 2: Create or Select Project

**Objective**: Set up a project for organizing your configurations.

### Understanding Projects

Projects help you organize deployments by business unit (Sales, Support, Operations) or use case.

### Code

```python
from wiil.models.service_mgt import CreateProject

# Option A: Use the existing default project (created by the system)
try:
    project = client.projects.get_default()
    print(f'Using default project: {project.name}')
except Exception:
    # Option B: Create a new project (if no default exists)
    project = client.projects.create(
        CreateProject(
            name='Customer Support',
            description='Customer support AI agent deployments'
        )
    )
    print(f'Created new project: {project.name}')

print(f'Project ID: {project.id}')
```

### Expected Output

```text
Created new project: Customer Support
Project ID: 9x8y7z6w5v
```

---

## Step 3: Create Instruction Configuration

**Objective**: Define how your agent behaves, communicates, and handles conversations.

### Understanding Instruction Configuration

This is the **heart of your agent's behavior**. It includes:

- **Role**: The agent's persona and responsibilities
- **Introduction Message**: Initial greeting presented to customers
- **Instructions**: Detailed behavioral guidelines and conversation flow
- **Guardrails**: Safety constraints, compliance rules, and ethical boundaries

**Note**: The instruction configuration must be created first because the agent configuration requires an `instruction_configuration_id`.

### Code

```python
from wiil.models.service_mgt import (
    BusinessSupportServices,
    CreateInstructionConfiguration
)

instruction_config = client.instruction_configs.create(
    CreateInstructionConfiguration(
        # ====================================================================
        # INSTRUCTION NAME - System-readable identifier
        # ====================================================================
        instruction_name='customer-support-agent',

        # ====================================================================
        # ROLE - The agent's persona
        # ====================================================================
        role='Customer Support Specialist',

        # ====================================================================
        # INTRODUCTION MESSAGE - Initial greeting
        # ====================================================================
        introduction_message="Hello! I'm an AI assistant from ACME Corporation. How can I help you today?",

        # ====================================================================
        # INSTRUCTIONS - Detailed behavioral guidelines
        # ====================================================================
        instructions="""You are a professional customer support agent for ACME Corporation, a leading provider of business solutions.

Your role and responsibilities:
- Greet customers warmly and professionally
- Answer questions about products, services, and orders
- Help customers book appointments and make reservations
- Provide accurate, clear, and concise information
- Resolve issues efficiently and empathetically
- Escalate complex issues to human agents when appropriate

Your communication style:
- Professional yet friendly and approachable
- Clear and concise - avoid jargon
- Patient and empathetic
- Proactive in offering solutions
- Respectful of customer time

Conversation guidelines:
1. Opening: Start with a warm greeting, identify yourself, address customer by name if available
2. Engagement: Ask clarifying questions, listen actively, acknowledge concerns
3. Problem Solving: Offer specific solutions, confirm understanding, set clear expectations
4. Bookings & Transactions: Confirm all details (date, time, service, customer info), provide confirmation numbers
5. Closing: Summarize resolution, ask if anything else is needed, thank the customer

Your knowledge:
- Product catalog and pricing
- Service offerings and availability
- Company policies and procedures
- Booking and reservation systems
- Order tracking and status

Remember: You represent ACME Corporation. Always maintain professionalism while being genuinely helpful.""",

        # ====================================================================
        # GUARDRAILS - Safety and compliance constraints
        # ====================================================================
        guardrails="""Data Privacy:
- NEVER share or request sensitive personal information (SSN, passwords, full credit card numbers)
- Follow GDPR and data privacy regulations
- Do not access or reference customer data unless necessary for the current request

Professional Boundaries:
- Do not make medical diagnoses or provide medical advice
- Do not provide legal advice or interpretations
- Do not make financial recommendations or guarantees
- Do not make commitments beyond standard company policies

Ethical Guidelines:
- Be honest if you don't know something - don't make up information
- Admit limitations and escalate when appropriate
- Treat all customers with equal respect and priority
- Do not engage in discriminatory language or behavior

Brand Protection:
- Do not speak negatively about competitors
- Do not share confidential company information
- Follow brand voice and messaging guidelines

Escalation Triggers:
- Customer requests to speak with a human more than once
- Keywords: complaint, refund, manager, supervisor, legal, lawyer, lawsuit, discrimination, harassment
- Issue requires access to systems the agent cannot use
- Customer is experiencing an emergency or urgent situation
- Conversation exceeds 10 minutes without resolution
- Customer is dissatisfied with the agent's responses""",

        # ====================================================================
        # SUPPORTED SERVICES - Platform business services (tools) enabled
        # ====================================================================
        supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT]
    )
)

print(f'Instructions Created: {instruction_config.instruction_name}')
print(f'Instructions ID: {instruction_config.id}')
```

### Expected Output

```text
Instructions Created: customer-support-agent
Instructions ID: f6g7h8i9j0
```

### Tips for Writing Effective Instructions

1. **Be Specific**: Vague instructions lead to inconsistent behavior
2. **Use Examples**: Show the agent what good responses look like
3. **Set Boundaries**: Clearly define what the agent should NOT do
4. **Plan for Edge Cases**: Account for unusual customer requests
5. **Iterate**: Start simple, then refine based on real conversations

---

## Step 4: Get Wiil Support Models

**Objective**: Retrieve available AI models from the Wiil Support Model Registry.

### Understanding Support Models

The WIIL Platform maintains a curated registry of AI models from various providers (OpenAI, Anthropic, Google, etc.). Each model has a unique **Wiil Model ID** that you'll use when configuring agents.

The Support Model Registry includes:

- **Text Models**: GPT-4, Claude, Gemini for conversational AI
- **Voice Models**: Speech-to-Text (STT) and Text-to-Speech (TTS)
- **Multi-Mode Models**: Models supporting text, voice, and vision
- **Translation Models**: Specialized for multilingual translation

### Code

```python
# List all available models
all_models = client.support_models.list()
print(f'Available models: {len(all_models.data)}')

# Get default multi-mode model (recommended for conversational agents)
default_model = client.support_models.get_default_multi_mode()
if default_model:
    print('Default Multi-Mode Model:')
    print(f'  Name: {default_model.name}')
    print(f'  Wiil Model ID: {default_model.model_id}')
    print(f'  Proprietor: {default_model.proprietor}')
    print(f'  Provider Model ID: {default_model.provider_model_id}')
    print(f'  Type: {default_model.type}')
    print(f'  Discontinued: {default_model.discontinued}')

# Lookup a specific model by provider details
gemini_model = client.support_models.get_by_proprietor_and_provider_model_id(
    'Google',
    'gemini-2.0-flash-exp'
)
if gemini_model:
    print(f'Gemini Wiil Model ID: {gemini_model.model_id}')
```

### Expected Output

```text
Available models: 47
Default Multi-Mode Model:
  Name: Gemini 2.0 Flash (Experimental)
  Wiil Model ID: abc123xyz
  Proprietor: Google
  Provider Model ID: gemini-2.0-flash-exp
  Type: MULTI_MODE
  Discontinued: False
Gemini Wiil Model ID: abc123xyz
```

### Available Default Models

| Method | Purpose | Returns |
|--------|---------|---------|
| `get_default_multi_mode()` | General conversational AI | Best multi-mode model (text, voice, vision) |
| `get_default_tts()` | Text-to-Speech | Best TTS model for voice synthesis |
| `get_default_stt()` | Speech-to-Text | Best STT model for transcription |
| `get_default_sts()` | Speech-to-Speech | Best model for direct voice-to-voice |
| `get_default_transcribe()` | Transcription | Best model for audio transcription |
| `get_default_batch()` | Batch processing | Best model for bulk operations |
| `get_default_translation_stt()` | Translation STT | Best STT for translation workflows |
| `get_default_translation_tts()` | Translation TTS | Best TTS for translation workflows |

---

## Step 5: Create Agent Configuration

**Objective**: Define your AI agent by linking the instruction configuration with an AI model.

### Understanding Agent Configuration

The Agent Configuration links together:

- **Instruction Configuration**: Behavioral guidelines (from Step 3)
- **AI Model**: Language model from Support Model Registry (from Step 4)
- **Assistant Type**: Channel specialization (GENERAL, WEB, PHONE, EMAIL)

### Code

```python
from wiil.models.service_mgt import CreateAgentConfiguration

# Verify we have the required dependencies from previous steps
if not default_model:
    raise Exception('No default multi-mode model available')

# Create agent configuration
agent_config = client.agent_configs.create(
    CreateAgentConfiguration(
        name='SupportAgent',
        model_id=default_model.model_id,  # Wiil Model ID from Step 4
        instruction_configuration_id=instruction_config.id  # From Step 3
    )
)

print(f'Agent Created: {agent_config.name}')
print(f'Agent ID: {agent_config.id}')
print(f'Using Model: {default_model.name} ({default_model.model_id})')
print(f'Using Instructions: {instruction_config.instruction_name}')
```

### Expected Output

```text
Agent Created: SupportAgent
Agent ID: a1b2c3d4e5
Using Model: Gemini 2.0 Flash (Experimental) (abc123xyz)
Using Instructions: customer-support-agent
```

---

## Step 5.1: Find Available Phone Numbers

**Objective**: Search for available phone numbers for voice or SMS channels.

### When to Use This

Before purchasing a phone number for CALLS or SMS channels, use the Telephony Provider API to:

- Search available phone numbers by area code, pattern, or postal code
- Check pricing for different number types
- Purchase phone numbers for deployment

### Code

```python
from wiil.models.service_mgt import PurchasePhoneNumber

# Step 1: Get pricing information
pricing = client.telephony_provider.get_pricing()

print('Pricing Information:')
for price in pricing:
    print(f'  {price.number_type}: ${price.price}/month')

# Step 2: Search for available phone numbers
numbers = client.telephony_provider.get_phone_numbers()

print(f'\nFound {len(numbers)} available phone numbers')

# Display first 5 numbers
for number in numbers[:5]:
    print(f'  {number.phone_number} - {number.friendly_name}')

# Step 3: Search with area code filter
seattle_numbers = client.telephony_provider.get_phone_numbers(
    area_code='206'  # Seattle area code
)

print(f'\nFound {len(seattle_numbers)} Seattle area numbers')
```

### Expected Output

```text
Pricing Information:
  local: $1.00/month
  toll-free: $2.00/month

Found 150 available phone numbers
  +12065551234 - (206) 555-1234
  +12065551235 - (206) 555-1235
  +12125551000 - (212) 555-1000
  ...

Found 25 Seattle area numbers
```

### Search Options

| Option | Type | Description |
|--------|------|-------------|
| area_code | str | Filter by area code (e.g., '206', '415') |
| contains | str | Filter by number pattern (e.g., '555') |
| postal_code | str | Filter by postal code (e.g., '98101') |

### Purchase Phone Number

Once you've found a suitable number, purchase it:

```python
purchase = client.telephony_provider.purchase(
    PurchasePhoneNumber(
        phone_number=numbers[0].phone_number  # Use number from search results
    )
)

print(f'Purchase ID: {purchase.id}')
print(f'Status: {purchase.status}')
print(f'Phone Number: {purchase.phone_number}')

# The purchase() method automatically polls until completion
# Check status if needed:
status = client.telephony_provider.get_purchase_status(purchase.id)
print(f'Final Status: {status.status}')
```

See the [Telephony Provider Guide](./service-mgt/telephony-provider-guide.md) for complete documentation.

---

## Step 6: Create Deployment Channel

**Objective**: Set up a communication channel where customers can interact with your agent.

### Understanding Deployment Channels

Channels define how customers reach your agent:

- **WEB**: Web chat widget
- **CALLS**: Phone calls (telephony)
- **SMS**: Text messaging
- **WHATSAPP**: WhatsApp messaging (Coming Soon)
- **EMAIL**: Email conversations
- **MOBILE**: Mobile app integration (Coming Soon)

**Note**: The deployment channel must be created first because the deployment configuration requires a `deployment_channel_id`.

### Code - Web Chat Channel

```python
from wiil.models.service_mgt import DeploymentType, CreateDeploymentChannel

web_chat_channel = client.deployment_channels.create(
    CreateDeploymentChannel(
        channel_identifier='https://example.com',  # URL for web channels
        deployment_type=DeploymentType.WEB.value,
        channel_name='Website Live Chat',
        recording_enabled=True,
        configuration={
            'communicationType': 'unified',  # 'text', 'voice', or 'unified'
            'widgetConfiguration': {
                'position': 'right'  # 'left' or 'right'
            }
        }
    )
)

print(f'Channel Created: {web_chat_channel.channel_name}')
print(f'Channel ID: {web_chat_channel.id}')
print(f'Channel Type: {web_chat_channel.deployment_type}')
```

### Expected Output

```text
Channel Created: Website Live Chat
Channel ID: p6q7r8s9t0
Channel Type: WEB
```

---

## Step 7: Create Deployment Configuration

**Objective**: Link your agent, instructions, and channel into a deployable unit.

### Understanding Deployment Configuration

The Deployment Configuration:

- Links Agent Configuration, Instruction Configuration, and Deployment Channel
- Sets deployment status and activation state
- Uses provisioning type (DIRECT or CHAINED for voice processing)
- Requires a project context for organizational grouping

### Code

```python
from wiil.models.service_mgt import (
    DeploymentStatus,
    DeploymentProvisioningType,
    CreateDeploymentConfiguration
)

deployment_config = client.deployment_configs.create(
    CreateDeploymentConfiguration(
        # Required fields
        project_id=project.id,                           # From Step 2
        deployment_channel_id=web_chat_channel.id,       # From Step 6
        agent_configuration_id=agent_config.id,          # From Step 5
        instruction_configuration_id=instruction_config.id,  # From Step 3

        # Optional fields
        deployment_name='Customer Support Deployment',
        is_active=True,
        deployment_status=DeploymentStatus.PENDING.value,  # PENDING, ACTIVE, PAUSED, ARCHIVED
        provisioning_type=DeploymentProvisioningType.DIRECT.value  # DIRECT or CHAINED
    )
)

print(f'Deployment Created: {deployment_config.deployment_name}')
print(f'Deployment ID: {deployment_config.id}')
print(f'Status: {deployment_config.deployment_status}')
print(f'Active: {deployment_config.is_active}')
```

### Expected Output

```text
Deployment Created: Customer Support Deployment
Deployment ID: k1l2m3n4o5
Status: pending
Active: True
```

---

## Step 8: Deploy Agent

**Objective**: Integrate the agent into your application or website.

### For Web Chat

After creating the deployment configuration, integrate the WIIL widget into your website using the `deployment_config_id`:

#### HTML Integration

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Website</title>
</head>
<body>
  <!-- Your website content -->
  <h1>Welcome to ACME Corporation</h1>

  <!-- WIIL Widget - Add before closing </body> tag -->
  <div
    id="wiil-widget"
    data-config-id="k1l2m3n4o5"
    data-features="chat,voice"
  ></div>
  <script src="https://cdn.wiil.io/public/wiil-widget.js"></script>
  <script>WiilWidget.init();</script>
</body>
</html>
```

**Configuration Options:**

- `data-config-id`: Your deployment configuration ID from Step 7 (required)
- `data-features`: Comma-separated list of features to enable (e.g., "chat", "voice", "chat,voice")

#### React Integration

```tsx
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    // Create widget container
    const widgetDiv = document.createElement('div');
    widgetDiv.id = 'wiil-widget';
    widgetDiv.setAttribute('data-config-id', 'k1l2m3n4o5');  // Your deployment config ID
    widgetDiv.setAttribute('data-features', 'chat,voice');
    document.body.appendChild(widgetDiv);

    // Load WIIL Widget script
    const script = document.createElement('script');
    script.src = 'https://cdn.wiil.io/public/wiil-widget.js';
    script.async = true;
    script.onload = () => {
      window.WiilWidget.init();
    };
    document.body.appendChild(script);

    return () => {
      // Cleanup on unmount
      document.body.removeChild(widgetDiv);
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="App">
      <h1>Welcome to ACME Corporation</h1>
      {/* Your app content */}
    </div>
  );
}
```

### For Telephony

No integration needed - customers can immediately call your configured phone number.

### For SMS

No integration needed - customers can text your configured SMS number.

---

## Step 9: Verify Deployment

**Objective**: Confirm your agent is live and functioning correctly.

### Code

```python
# Retrieve and verify deployment
verified_deployment = client.deployment_configs.get(deployment_config.id)
verified_channel = client.deployment_channels.get(web_chat_channel.id)

print('=' * 60)
print('DEPLOYMENT VERIFICATION')
print('=' * 60)

print('\nDeployment Status:')
active_status = '✓ YES' if verified_deployment.is_active else '✗ NO'
print(f'  Active: {active_status}')
print(f'  Agent: {verified_deployment.agent_configuration_id}')
print(f'  Instructions: {verified_deployment.instruction_configuration_id}')

print('\nChannel Status:')
print(f'  Name: {verified_channel.channel_name}')
print(f'  Type: {verified_channel.deployment_type}')
print(f'  Channel ID: {verified_channel.id}')

print('\n' + '=' * 60)
print('✓ DEPLOYMENT COMPLETE - Agent is LIVE!')
print('=' * 60)
```

### Expected Output

```text
============================================================
DEPLOYMENT VERIFICATION
============================================================

Deployment Status:
  Active: ✓ YES
  Agent: a1b2c3d4e5
  Instructions: f6g7h8i9j0

Channel Status:
  Name: Website Live Chat
  Type: web
  Channel ID: p6q7r8s9t0

============================================================
✓ DEPLOYMENT COMPLETE - Agent is LIVE!
============================================================
```

### Testing Your Agent

1. **Visit your website** where you integrated the chat widget
2. **Start a conversation** with test queries:
   - "What are your business hours?"
   - "I need to book an appointment"
   - "Tell me about your products"
3. **Test escalation** by saying "I want to speak with a manager"
4. **Monitor in WIIL Console**:
   - Navigate to **Conversations** to see live interactions
   - View **Analytics** for performance metrics

---

## Next Steps

Congratulations! Your AI agent is now deployed and ready to handle customer conversations.

### 1. Monitor Performance

**WIIL Console → Analytics Dashboard**

Track key metrics:

- Conversation volume and trends
- Average conversation duration
- Customer satisfaction scores
- Escalation rate
- Response accuracy

### 2. Refine Instructions

Based on real conversations, update your instruction configuration:

```python
from wiil.models.service_mgt import UpdateInstructionConfiguration

updated_instructions = client.instruction_configs.update(
    instruction_config.id,
    UpdateInstructionConfiguration(
        instructions='... improved instructions based on learnings ...',
        guardrails='... updated safety constraints ...'
    )
)
```

### 3. Enable Multi-Channel

Deploy the same agent across multiple channels. See the [Channels Guide](./channels/README.md) for detailed setup:

- **[Voice Channels](./channels/voice-channels.md)**: Phone call support
- **[SMS Channels](./channels/sms-channels.md)**: Text messaging support

### 4. Explore Advanced Features

- **Analytics**: Monitor conversation performance in WIIL Console
- **A/B Testing**: Test different instruction configurations
- **Custom Integrations**: Connect to your business systems

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

### Community

- **Discord**: Join our developer community
- **Blog**: Technical articles and best practices
- **Changelog**: Stay updated with new features

---

**Congratulations!** You've successfully deployed your first AI agent on the WIIL Platform.

Your agent is now handling customer conversations 24/7, helping your business scale customer support while maintaining quality interactions.

---

*Built by the WIIL team*
