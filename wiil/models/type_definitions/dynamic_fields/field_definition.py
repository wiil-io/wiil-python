"""Field definition schemas for dynamic form fields.

This module mirrors src/core/type-definitions/dynamic-fields/field-definition.schema.ts
"""

from typing import Any, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from wiil.models.type_definitions.dynamic_fields.field_types import DynamicFieldType


class FieldOption(BaseModel):
    """Schema for select/multiselect field options."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    value: str = Field(..., description="Option value")
    label: str = Field(..., description="Option display label")
    display_order: Optional[int] = Field(
        None,
        description="Display order for the option",
        alias="displayOrder"
    )


class FieldValidationRules(BaseModel):
    """Validation rules schema for dynamic fields."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    required: Optional[bool] = Field(None, description="Whether the field is required")
    min_length: Optional[int] = Field(
        None,
        gt=0,
        description="Minimum length for text fields",
        alias="minLength"
    )
    max_length: Optional[int] = Field(
        None,
        gt=0,
        description="Maximum length for text fields",
        alias="maxLength"
    )
    min: Optional[float] = Field(None, description="Minimum value for number fields")
    max: Optional[float] = Field(None, description="Maximum value for number fields")
    pattern: Optional[str] = Field(None, description="Regex pattern for validation")
    pattern_message: Optional[str] = Field(
        None,
        description="Error message for pattern validation failure",
        alias="patternMessage"
    )


FieldWidth = Literal["full", "half", "third"]


class FieldUIHints(BaseModel):
    """UI hints schema for field rendering."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    placeholder: Optional[str] = Field(None, description="Placeholder text")
    help_text: Optional[str] = Field(
        None,
        description="Help text for the field",
        alias="helpText"
    )
    display_order: Optional[int] = Field(
        None,
        description="Display order for the field",
        alias="displayOrder"
    )
    width: Optional[FieldWidth] = Field(
        None,
        description="Field width hint (full, half, third)"
    )


FieldConditionOperator = Literal[
    "equals",
    "notEquals",
    "contains",
    "isEmpty",
    "isNotEmpty",
    "greaterThan",
    "lessThan",
]


class FieldCondition(BaseModel):
    """Schema for conditional field visibility.

    Show field X only if field Y meets a condition.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    depends_on: str = Field(
        ...,
        description="Field key that this condition depends on",
        alias="dependsOn"
    )
    operator: FieldConditionOperator = Field(
        ...,
        description="Comparison operator"
    )
    value: Optional[Any] = Field(
        None,
        description="Value to compare against"
    )


class FieldGroup(BaseModel):
    """Schema for field grouping/sections.

    Organize fields into logical groups (e.g., "Contact Info", "Preferences").
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    group_key: str = Field(..., description="Unique key for the group", alias="groupKey")
    label: str = Field(..., description="Display label for the group")
    description: Optional[str] = Field(None, description="Group description")
    display_order: Optional[int] = Field(
        None,
        description="Display order for the group",
        alias="displayOrder"
    )
    collapsible: Optional[bool] = Field(
        None,
        description="Whether the group can be collapsed"
    )
    default_collapsed: Optional[bool] = Field(
        None,
        description="Whether the group is collapsed by default",
        alias="defaultCollapsed"
    )


class FieldDefinition(BaseModel):
    """Core field definition schema.

    Defines a single dynamic field with its type, validation, and UI configuration.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    field_key: str = Field(
        ...,
        pattern=r"^[a-z][a-z0-9_]*$",
        description="Field key (lowercase alphanumeric with underscores, starting with a letter)",
        alias="fieldKey"
    )
    field_type: DynamicFieldType = Field(
        ...,
        description="Type of the field",
        alias="fieldType"
    )
    label: str = Field(..., min_length=1, description="Display label for the field")
    description: Optional[str] = Field(None, description="Field description")
    validation: Optional[FieldValidationRules] = Field(
        None,
        description="Validation rules for the field"
    )
    ui_hints: Optional[FieldUIHints] = Field(
        None,
        description="UI rendering hints",
        alias="uiHints"
    )
    options: Optional[List[FieldOption]] = Field(
        None,
        description="Options for select/multiselect fields"
    )
    default_value: Optional[Any] = Field(
        None,
        description="Default value for the field",
        alias="defaultValue"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the field is active",
        alias="isActive"
    )
    condition: Optional[FieldCondition] = Field(
        None,
        description="Conditional visibility rules"
    )
    group_key: Optional[str] = Field(
        None,
        description="Group key for field organization",
        alias="groupKey"
    )


class FieldOverride(BaseModel):
    """Field override schema for service-level customization.

    Allows overriding specific properties of inherited fields.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    field_key: str = Field(..., description="Field key to override", alias="fieldKey")
    label: Optional[str] = Field(None, description="Override label")
    validation: Optional[FieldValidationRules] = Field(
        None,
        description="Override validation rules"
    )
    ui_hints: Optional[FieldUIHints] = Field(
        None,
        description="Override UI hints",
        alias="uiHints"
    )
    default_value: Optional[Any] = Field(
        None,
        description="Override default value",
        alias="defaultValue"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Override active status",
        alias="isActive"
    )
