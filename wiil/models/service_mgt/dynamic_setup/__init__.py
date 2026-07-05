"""Central export point for dynamic agent setup schemas.

Provides schemas for dynamically configuring AI assistants across different
communication channels (phone, web). Includes base configuration schemas
and channel-specific extensions for voice and text interactions.
"""

# Base agent setup models
from wiil.models.service_mgt.dynamic_setup.base_agent_setup import (
    DynamicAgentProcessingState,
    DynamicAgentSetupResult,
    DynamicBaseAgentSetup,
    DynamicModelConfiguration,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
    ProcessingStatus,
    TextBasedKnowledgeSource,
)

# Phone agent setup models
from wiil.models.service_mgt.dynamic_setup.phone_agent_setup import (
    DynamicPhoneAgentSetup,
    DynamicPhoneAgentSetupResult,
    UpdateDynamicPhoneAgent,
)

# Web agent setup models
from wiil.models.service_mgt.dynamic_setup.web_agent_setup import (
    DynamicWebAgentSetup,
    DynamicWebAgentSetupResult,
    UpdateDynamicWebAgent,
)

__all__ = [
    # Base agent setup models
    "DynamicAgentProcessingState",
    "DynamicAgentSetupResult",
    "DynamicBaseAgentSetup",
    "DynamicModelConfiguration",
    "DynamicSTTModelConfiguration",
    "DynamicTTSModelConfiguration",
    "ProcessingStatus",
    "TextBasedKnowledgeSource",
    # Phone agent setup models
    "DynamicPhoneAgentSetup",
    "DynamicPhoneAgentSetupResult",
    "UpdateDynamicPhoneAgent",
    # Web agent setup models
    "DynamicWebAgentSetup",
    "DynamicWebAgentSetupResult",
    "UpdateDynamicWebAgent",
]
