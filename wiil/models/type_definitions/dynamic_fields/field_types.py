"""Dynamic Field Types.

Defines the supported field types for dynamic form field definitions.
Used across appointment and other configurable form schemas.

This module mirrors src/core/type-definitions/dynamic-fields/field-types.ts
"""

from enum import Enum
from typing import Dict, List, Literal, Optional, TypedDict


class DynamicFieldType(str, Enum):
    """Dynamic field type enumeration."""

    TEXT = "text"
    """Single-line text input."""

    TEXTAREA = "textarea"
    """Multi-line text input."""

    NUMBER = "number"
    """Numeric input."""

    BOOLEAN = "boolean"
    """Boolean checkbox/toggle."""

    DATE = "date"
    """Date picker (date only)."""

    TIME = "time"
    """Time picker (time only)."""

    DATETIME = "datetime"
    """DateTime picker (date and time)."""

    EMAIL = "email"
    """Email input with validation."""

    PHONE = "phone"
    """Phone number input."""

    SELECT = "select"
    """Single selection dropdown."""

    MULTISELECT = "multiselect"
    """Multiple selection input."""


# Array of all dynamic field types for validation
DYNAMIC_FIELD_TYPES: List[str] = [
    DynamicFieldType.TEXT.value,
    DynamicFieldType.TEXTAREA.value,
    DynamicFieldType.NUMBER.value,
    DynamicFieldType.BOOLEAN.value,
    DynamicFieldType.DATE.value,
    DynamicFieldType.TIME.value,
    DynamicFieldType.DATETIME.value,
    DynamicFieldType.EMAIL.value,
    DynamicFieldType.PHONE.value,
    DynamicFieldType.SELECT.value,
    DynamicFieldType.MULTISELECT.value,
]


class AgentToolParamType(TypedDict, total=False):
    """Agent tool call parameter type definition.

    Maps field types to JSON schema types for LLM tool calls.
    """

    type: Literal["string", "number", "boolean", "array"]
    format: Optional[str]
    items: Optional[Dict[str, str]]
    description: str


DYNAMIC_FIELD_TYPE_TO_AGENT_TOOL_PARAM: Dict[DynamicFieldType, AgentToolParamType] = {
    DynamicFieldType.TEXT: {
        "type": "string",
        "description": "Single-line text value",
    },
    DynamicFieldType.TEXTAREA: {
        "type": "string",
        "description": "Multi-line text value",
    },
    DynamicFieldType.NUMBER: {
        "type": "number",
        "description": "Numeric value",
    },
    DynamicFieldType.BOOLEAN: {
        "type": "boolean",
        "description": "True or false value",
    },
    DynamicFieldType.DATE: {
        "type": "string",
        "format": "date",
        "description": "Date in ISO 8601 format (YYYY-MM-DD)",
    },
    DynamicFieldType.TIME: {
        "type": "string",
        "format": "time",
        "description": "Time in 24-hour format (HH:MM)",
    },
    DynamicFieldType.DATETIME: {
        "type": "string",
        "format": "date-time",
        "description": "Date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)",
    },
    DynamicFieldType.EMAIL: {
        "type": "string",
        "format": "email",
        "description": "Valid email address",
    },
    DynamicFieldType.PHONE: {
        "type": "string",
        "format": "phone",
        "description": "Phone number with country code",
    },
    DynamicFieldType.SELECT: {
        "type": "string",
        "description": "Single selection from available options",
    },
    DynamicFieldType.MULTISELECT: {
        "type": "array",
        "items": {"type": "string"},
        "description": "Multiple selections from available options",
    },
}
