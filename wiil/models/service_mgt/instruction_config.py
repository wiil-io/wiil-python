"""Instruction configuration schema definitions.

The Instruction Configuration is the heart of agent behaviour in the Service Configuration architecture.
It contains the prompts, guidelines, and contextual instructions that fundamentally define how agents
operate during conversations.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions import BusinessSupportServices


class InstructionConfiguration(EntityModel):
    """Instruction configuration for agent behavior.

    The Instruction Configuration is the heart of agent behaviour in the Service Configuration architecture.
    It contains the prompts, guidelines, and contextual instructions that fundamentally define how an agent
    operates during conversations. A single Instruction Configuration can be associated with multiple Agent
    Configurations (1:N relationship), allowing consistent behavioral guidelines across different agent types.

    Architecture Context:
        - Central Role: The Instruction Configuration is the core element that shapes agent behavior
        - Relationship: 1:N with Agent Configurations - one instruction set can govern multiple agents
        - Reusability: Designed to be reused across multiple deployments
        - Managed By: Service Configuration (lifecycle management)
        - Used By: Deployment Configurations reference instruction sets for agent behavior

    Example Use Case:
        A "Customer Service Guidelines" instruction set might govern both a "Sales Agent" and a "Support Agent",
        ensuring uniform tone and compliance while each agent maintains its specialized capabilities.

    Attributes:
        instruction_name: System-readable name, typically auto-generated based on role
        role: The role or persona the agent should adopt
        introduction_message: Initial greeting message presented to users
        instructions: Detailed instructions that guide agent behavior
        guardrails: Safety and behavioral constraints the agent must follow
        required_skills: Specific skills required for this instruction set
        validation_rules: Custom validation rules for input/output processing
        service_id: ID of the service this instruction configuration is associated with
        supported_services: Platform business services (tools) enabled for this agent
        tools: Tool identifiers the agent can use
        is_template: Whether this is a reusable template
        is_primary: Whether this is the primary system instruction configuration template
        metadata: Additional metadata for the instruction configuration
        knowledge_source_ids: Array of IDs referencing knowledge sources
    """

    instruction_name: str = Field(
        ...,
        description="System-readable name for the instruction configuration (e.g., 'customer-support-agent')",
        alias="instructionName"
    )
    role: str = Field(
        ...,
        description="The role or persona the agent should adopt (e.g., 'Customer Support Specialist', 'Sales Representative')"
    )
    introduction_message: str = Field(
        ...,
        description="Initial greeting message presented to users when starting a conversation",
        alias="introductionMessage"
    )
    instructions: str = Field(
        ...,
        description="Detailed instructions that fundamentally define how the agent operates"
    )
    guardrails: str = Field(
        ...,
        description="Safety and behavioral constraints the agent must strictly follow"
    )
    required_skills: Optional[List[str]] = Field(
        None,
        description="Specific skills or capabilities required for this instruction set (e.g., 'appointment_booking')",
        alias="requiredSkills"
    )
    validation_rules: Optional[Dict[str, Any]] = Field(
        None,
        description="Custom validation rules for input/output processing",
        alias="validationRules"
    )
    service_id: Optional[str] = Field(
        None,
        description="ID of the parent service this instruction configuration is associated with",
        alias="serviceId"
    )
    supported_services: List[BusinessSupportServices] = Field(
        default_factory=list,
        description="Array of platform business services (tools) enabled for this agent",
        alias="supportedServices"
    )
    tools: Optional[List[str]] = Field(
        None,
        description="Array of tool identifiers the agent can use"
    )
    is_template: bool = Field(
        False,
        description="Whether this instruction configuration is a reusable template",
        alias="isTemplate"
    )
    is_primary: bool = Field(
        False,
        description="Whether this is the primary system instruction configuration template",
        alias="isPrimary"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata for the instruction configuration"
    )
    knowledge_source_ids: List[str] = Field(
        default_factory=list,
        description="Array of IDs referencing knowledge sources that provide context for this instruction set",
        alias="knowledgeSourceIds"
    )


class CreateInstructionConfiguration(BaseModel):
    """Schema for creating a new instruction configuration.

    Omits auto-generated fields (id, timestamps) that are populated by the system.
    """

    instruction_name: str = Field(..., alias="instructionName")
    role: str
    introduction_message: str = Field(..., alias="introductionMessage")
    instructions: str
    guardrails: str
    required_skills: Optional[List[str]] = Field(None, alias="requiredSkills")
    validation_rules: Optional[Dict[str, Any]] = Field(None, alias="validationRules")
    service_id: Optional[str] = Field(None, alias="serviceId")
    supported_services: List[BusinessSupportServices] = Field(
        default_factory=list,
        alias="supportedServices"
    )
    tools: Optional[List[str]] = None
    is_template: bool = Field(False, alias="isTemplate")
    is_primary: bool = Field(False, alias="isPrimary")
    metadata: Optional[Dict[str, Any]] = None
    knowledge_source_ids: List[str] = Field(
        default_factory=list,
        alias="knowledgeSourceIds"
    )


class UpdateInstructionConfiguration(BaseModel):
    """Schema for updating an existing instruction configuration.

    All fields are optional except id.
    """

    id: str
    instruction_name: Optional[str] = Field(None, alias="instructionName")
    role: Optional[str] = None
    introduction_message: Optional[str] = Field(None, alias="introductionMessage")
    instructions: Optional[str] = None
    guardrails: Optional[str] = None
    required_skills: Optional[List[str]] = Field(None, alias="requiredSkills")
    validation_rules: Optional[Dict[str, Any]] = Field(None, alias="validationRules")
    service_id: Optional[str] = Field(None, alias="serviceId")
    supported_services: Optional[List[BusinessSupportServices]] = Field(
        None,
        alias="supportedServices"
    )
    tools: Optional[List[str]] = None
    is_template: Optional[bool] = Field(None, alias="isTemplate")
    is_primary: Optional[bool] = Field(None, alias="isPrimary")
    metadata: Optional[Dict[str, Any]] = None
    knowledge_source_ids: Optional[List[str]] = Field(
        None,
        alias="knowledgeSourceIds"
    )
