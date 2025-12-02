"""Service Management resource classes for managing AI service configurations."""

from wiil.resources.service_mgt.agent_configs import AgentConfigurationsResource
from wiil.resources.service_mgt.deployment_configs import DeploymentConfigurationsResource
from wiil.resources.service_mgt.deployment_channels import DeploymentChannelsResource
from wiil.resources.service_mgt.instruction_configs import InstructionConfigurationsResource
from wiil.resources.service_mgt.phone_configs import PhoneConfigurationsResource
from wiil.resources.service_mgt.provisioning_configs import ProvisioningConfigurationsResource
from wiil.resources.service_mgt.conversation_configs import ConversationConfigurationsResource
from wiil.resources.service_mgt.translation_sessions import TranslationSessionsResource
from wiil.resources.service_mgt.knowledge_sources import KnowledgeSourcesResource

__all__ = [
    'AgentConfigurationsResource',
    'DeploymentConfigurationsResource',
    'DeploymentChannelsResource',
    'InstructionConfigurationsResource',
    'PhoneConfigurationsResource',
    'ProvisioningConfigurationsResource',
    'ConversationConfigurationsResource',
    'TranslationSessionsResource',
    'KnowledgeSourcesResource',
]
