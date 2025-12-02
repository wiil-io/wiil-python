"""Instruction configuration schema definitions.

The Instruction Configuration is the heart of agent behaviour in the Service Configuration
architecture. It contains the prompts, guidelines, and contextual instructions that
fundamentally define how agents operate during conversations.
"""

from typing import Any, Dict, List, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.account_types import BusinessSupportServices


class InstructionConfiguration(BaseModel):
    """Instruction Configuration model.

    The Instruction Configuration is the core element that shapes agent behavior.
    A single Instruction Configuration can be associated with multiple Agent
    Configurations (1:N relationship), allowing consistent behavioral guidelines
    across different agent types.

    Architecture Context:
        - Central Role: Core element that shapes agent behavior
        - Relationship: 1:N with Agent Configurations
        - Reusability: Designed to be reused across multiple deployments
        - Managed By: Service Configuration

    Example Use Case:
        A "Customer Service Guidelines" instruction set might govern both a
        "Sales Agent" and a "Support Agent", ensuring uniform tone and compliance.

    Attributes:
        id: Unique identifier
        instruction_name: System-readable name
        role: The role or persona the agent should adopt
        introduction_message: Initial greeting message
        instructions: Detailed behavioral guidelines
        guardrails: Safety and behavioral constraints
        required_skills: Specific skills or capabilities required
        validation_rules: Custom validation rules
        service_id: ID of associated service
        supported_services: Platform business services enabled
        tools: Tool identifiers the agent can use
        is_template: Whether this is a reusable template
        is_primary: Whether this is the primary system instruction
        metadata: Additional metadata
        knowledge_source_ids: IDs of knowledge sources
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        instruction = InstructionConfiguration(
            id="123",
            instruction_name="customer-support-agent",
            role="Customer Support Specialist",
            introduction_message="Hello! How can I help you today?",
            instructions="You are a helpful customer support agent...",
            guardrails="Never share sensitive customer data...",
            supported_services=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
            knowledge_source_ids=["789"],
            is_template=False,
            is_primary=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    instruction_name: str = Field(
        ...,
        description="System-readable name (e.g., 'customer-support-agent')",
        alias="instructionName"
    )
    role: str = Field(
        ...,
        description="The role or persona the agent should adopt"
    )
    introduction_message: str = Field(
        ...,
        description="Initial greeting message presented to users",
        alias="introductionMessage"
    )
    instructions: str = Field(
        ...,
        description="Detailed instructions that define agent behavior"
    )
    guardrails: str = Field(
        ...,
        description="Safety and behavioral constraints"
    )
    required_skills: Optional[List[str]] = Field(
        None,
        description="Specific skills or capabilities required",
        alias="requiredSkills"
    )
    validation_rules: Optional[Dict[str, Any]] = Field(
        None,
        description="Custom validation rules for input/output processing",
        alias="validationRules"
    )
    service_id: Optional[str] = Field(
        None,
        description="ID of the parent service",
        alias="serviceId"
    )
    supported_services: List[BusinessSupportServices] = Field(
        default_factory=list,
        description="Platform business services enabled for this agent",
        alias="supportedServices"
    )
    tools: Optional[List[str]] = Field(
        None,
        description="Tool identifiers the agent can use"
    )
    is_template: bool = Field(
        False,
        description="Whether this is a reusable template",
        alias="isTemplate"
    )
    is_primary: bool = Field(
        False,
        description="Whether this is the primary system instruction",
        alias="isPrimary"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata"
    )
    knowledge_source_ids: List[str] = Field(
        default_factory=list,
        description="IDs of knowledge sources providing context",
        alias="knowledgeSourceIds"
    )


class CreateInstructionConfiguration(BaseModel):
    """Schema for creating a new instruction configuration.

    Omits auto-generated fields (id, timestamps).

    Example:
        ```python
        create_data = CreateInstructionConfiguration(
            instruction_name="sales-agent",
            role="Sales Representative",
            introduction_message="Hi! I can help you find the perfect solution.",
            instructions="You are a knowledgeable sales agent...",
            guardrails="Always be honest about product capabilities...",
            supported_services=[BusinessSupportServices.PRODUCT_ORDER_MANAGEMENT],
            knowledge_source_ids=["123"],
            is_template=False,
            is_primary=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

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

    Example:
        ```python
        update_data = UpdateInstructionConfiguration(
            id="123",
            role="Senior Sales Representative",
            metadata={"version": "2.0"}
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    instruction_name: Optional[str] = Field(None, alias="instructionName")
    role: Optional[str] = None
    introduction_message: Optional[str] = Field(None, alias="introductionMessage")
    instructions: Optional[str] = None
    guardrails: Optional[str] = None
    required_skills: Optional[List[str]] = Field(None, alias="requiredSkills")
    validation_rules: Optional[Dict[str, Any]] = Field(None, alias="validationRules")
    service_id: Optional[str] = Field(None, alias="serviceId")
    supported_services: Optional[List[BusinessSupportServices]] = Field(None, alias="supportedServices")
    tools: Optional[List[str]] = None
    is_template: Optional[bool] = Field(None, alias="isTemplate")
    is_primary: Optional[bool] = Field(None, alias="isPrimary")
    metadata: Optional[Dict[str, Any]] = None
    knowledge_source_ids: Optional[List[str]] = Field(None, alias="knowledgeSourceIds")
