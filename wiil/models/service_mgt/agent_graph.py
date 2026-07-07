"""Read-only agent graph composite view.

Fully hydrated graph of an agent and all its related entities, intended for
API responses, management UIs, and graph-aware operations. Read-only by design
— no Create/Update variants.
"""

from typing import List, Optional

from pydantic import Field

from wiil.models.base import BaseModel
from wiil.models.service_mgt.agent_config import AgentConfiguration
from wiil.models.service_mgt.instruction_config import InstructionConfiguration
from wiil.models.service_mgt.knowledge import KnowledgeSource
from wiil.models.service_mgt.deployment_config import DeploymentConfiguration
from wiil.models.service_mgt.interaction_channels import DeploymentChannel


class AgentDeploymentNode(BaseModel):
    """Deployment node in the agent graph.

    Pairs a deployment configuration with its resolved channel.

    Attributes:
        deployment: Deployment configuration using this agent
        channel: Resolved deployment channel for this deployment
    """

    deployment: DeploymentConfiguration = Field(
        ...,
        description="Deployment configuration using this agent"
    )
    channel: Optional[DeploymentChannel] = Field(
        None,
        description="Resolved deployment channel for this deployment"
    )


class AgentGraph(BaseModel):
    """Read-only agent graph — fully hydrated view of an agent.

    Full graph structure:
        Root: AgentConfiguration
          ├── instruction: InstructionConfiguration
          │     └── knowledgeSources: KnowledgeSource[]
          └── deployments: AgentDeploymentNode[]
                └── channel: DeploymentChannel

    Attributes:
        agent: Core agent configuration — root node of the graph
        instruction: Instruction configuration (role/persona) linked to this agent
        knowledge_sources: Knowledge sources attached to the instruction configuration
        deployments: All deployment configurations that use this agent
    """

    agent: AgentConfiguration = Field(
        ...,
        description="Core agent configuration — root node of the graph"
    )
    instruction: Optional[InstructionConfiguration] = Field(
        None,
        description="Instruction configuration (role/persona) linked to this agent"
    )
    knowledge_sources: List[KnowledgeSource] = Field(
        default_factory=list,
        description="Knowledge sources attached to the instruction configuration",
        alias="knowledgeSources"
    )
    deployments: List[AgentDeploymentNode] = Field(
        default_factory=list,
        description="All deployment configurations that use this agent, each paired with its channel"
    )
