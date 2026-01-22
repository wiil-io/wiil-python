"""Service Management Pydantic models."""

from wiil.models.service_mgt.agent_config import (
    AgentConfiguration,
    CreateAgentConfiguration,
    UpdateAgentConfiguration,
)
from wiil.models.service_mgt.call_transfer_config import (
    CallTransferConfig,
    TransferType,
)
from wiil.models.service_mgt.deployment_channels import (
    CallChannel,
    CreateDeploymentChannel,
    DeploymentChannel,
    MobileAppChannel,
    MobileAppChannelConfig,
    PhoneChannelConfig,
    SmsChannel,
    UpdateDeploymentChannel,
    WebChannel,
    WebChannelConfig,
    WidgetConfiguration,
)
from wiil.models.service_mgt.deployment_config import (
    CreateDeploymentConfiguration,
    DeploymentConfiguration,
    UpdateDeploymentConfiguration,
)
from wiil.models.service_mgt.instruction_config import (
    CreateInstructionConfiguration,
    InstructionConfiguration,
    UpdateInstructionConfiguration,
)
from wiil.models.service_mgt.knowledge import (
    CreateKnowledgeSource,
    KnowledgeSource,
    UpdateKnowledgeSource,
)
from wiil.models.service_mgt.phone_config import (
    PhoneConfiguration,
    UpdatePhoneConfiguration,
)
from wiil.models.service_mgt.phone_number import (
    BasePhoneNumberInfo,
    PhoneCapabilities,
    PhoneProviderRegion,
    SWPhoneNumberInfo,
    TwilioPhoneNumberInfo,
)
from wiil.models.service_mgt.provisioning_config import (
    CreateProvisioningConfigChain,
    ProvisioningConfigChain,
    SttModelConfig,
    TtsModelConfig,
    UpdateProvisioningConfigChain,
)
from wiil.models.service_mgt.support_llm import WiilSupportModel
from wiil.models.service_mgt.voice_language import Language, Voice, VoiceGender

__all__ = [
    # Agent Configuration
    "AgentConfiguration",
    "CreateAgentConfiguration",
    "UpdateAgentConfiguration",
    # Call Transfer
    "CallTransferConfig",
    "TransferType",
    # Deployment Channels
    "DeploymentChannel",
    "CreateDeploymentChannel",
    "UpdateDeploymentChannel",
    "CallChannel",
    "SmsChannel",
    "WebChannel",
    "MobileAppChannel",
    "PhoneChannelConfig",
    "WebChannelConfig",
    "WidgetConfiguration",
    "MobileAppChannelConfig",
    # Deployment Configuration
    "DeploymentConfiguration",
    "CreateDeploymentConfiguration",
    "UpdateDeploymentConfiguration",
    # Instruction Configuration
    "InstructionConfiguration",
    "CreateInstructionConfiguration",
    "UpdateInstructionConfiguration",
    # Knowledge Source
    "KnowledgeSource",
    "CreateKnowledgeSource",
    "UpdateKnowledgeSource",
    # Phone Configuration
    "PhoneConfiguration",
    "UpdatePhoneConfiguration",
    # Phone Number
    "PhoneProviderRegion",
    "PhoneCapabilities",
    "BasePhoneNumberInfo",
    "SWPhoneNumberInfo",
    "TwilioPhoneNumberInfo",
    # Provisioning Configuration
    "ProvisioningConfigChain",
    "CreateProvisioningConfigChain",
    "UpdateProvisioningConfigChain",
    "SttModelConfig",
    "TtsModelConfig",
    # Support Models
    "WiilSupportModel",
    # Voice & Language
    "Voice",
    "Language",
    "VoiceGender",
]
