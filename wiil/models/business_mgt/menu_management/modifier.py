"""Modifier schema definitions for menu management."""

from typing import List, Literal, Optional, TypedDict

from pydantic import Field, model_validator

from wiil.models.base import BaseModel, EntityModel


class ModifierGroupChannelMapping(BaseModel):
    """Per-channel external modifier group ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_modifier_group_id: str = Field(
        ...,
        alias="externalModifierGroupId",
    )


class ModifierOptionChannelMapping(BaseModel):
    """Per-channel external modifier option ID mapping."""

    channel_id: str = Field(..., alias="channelId")
    external_modifier_option_id: str = Field(
        ...,
        alias="externalModifierOptionId",
    )
    external_modifier_group_id: Optional[str] = Field(
        None,
        alias="externalModifierGroupId",
    )


class ModifierOption(EntityModel):
    """Modifier option within a modifier group."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    modifier_group_id: str = Field(..., alias="modifierGroupId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price_delta: float = Field(0.0, alias="priceDelta")
    is_default: bool = Field(False, alias="isDefault")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierOptionChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")


class ModifierGroup(EntityModel):
    """Group of related modifier options."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    options: List[ModifierOption] = Field(..., min_length=1)
    min_selection: int = Field(0, ge=0, alias="minSelection")
    max_selection: Optional[int] = Field(None, gt=0, alias="maxSelection")
    is_required: bool = Field(False, alias="isRequired")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierGroupChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_selection_bounds(self) -> "ModifierGroup":
        """Ensure max_selection >= min_selection when both are set."""
        if (
            self.max_selection is not None
            and self.max_selection < self.min_selection
        ):
            raise ValueError(
                "maxSelection must be greater than or equal to minSelection"
            )
        return self


class ModifierOptionOverride(BaseModel):
    """Per-option override within a binding."""

    modifier_option_id: str = Field(..., alias="modifierOptionId")
    price_delta_override: Optional[float] = Field(
        None,
        alias="priceDeltaOverride",
    )
    is_default_override: Optional[bool] = Field(
        None,
        alias="isDefaultOverride",
    )
    display_order_override: Optional[int] = Field(
        None,
        alias="displayOrderOverride",
    )


class ItemModifierBinding(EntityModel):
    """Links modifier groups to menu items or menu sets."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    menu_item_id: Optional[str] = Field(None, alias="menuItemId")
    menu_item_variant_id: Optional[str] = Field(
        None,
        alias="menuItemVariantId",
    )
    menu_set_id: Optional[str] = Field(None, alias="menuSetId")
    modifier_group_id: str = Field(..., alias="modifierGroupId")
    is_required_override: Optional[bool] = Field(
        None,
        alias="isRequiredOverride",
    )
    min_selection_override: Optional[int] = Field(
        None,
        ge=0,
        alias="minSelectionOverride",
    )
    max_selection_override: Optional[int] = Field(
        None,
        gt=0,
        alias="maxSelectionOverride",
    )
    excluded_option_ids: Optional[List[str]] = Field(
        None,
        alias="excludedOptionIds",
    )
    option_overrides: Optional[List[ModifierOptionOverride]] = Field(
        None,
        alias="optionOverrides",
    )
    display_order: int = Field(0, ge=0, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_binding_targets(self) -> "ItemModifierBinding":
        """Validate exclusive binding targets and selection overrides."""
        has_menu_item_target = bool(self.menu_item_id)
        has_menu_set_target = bool(self.menu_set_id)

        if has_menu_item_target == has_menu_set_target:
            raise ValueError(
                "Exactly one of menuItemId or menuSetId is required"
            )

        if self.menu_item_variant_id and not has_menu_item_target:
            raise ValueError(
                "menuItemVariantId can only be provided when menuItemId is set"
            )

        if (
            self.min_selection_override is not None
            and self.max_selection_override is not None
            and self.max_selection_override < self.min_selection_override
        ):
            raise ValueError(
                "maxSelectionOverride must be greater than or equal to "
                "minSelectionOverride"
            )

        return self


class AppliedModifier(BaseModel):
    """Modifier selected on an order item."""

    modifier_group_id: Optional[str] = Field(None, alias="modifierGroupId")
    modifier_option_id: Optional[str] = Field(None, alias="modifierOptionId")
    external_modifier_group_id: Optional[str] = Field(
        None,
        alias="externalModifierGroupId",
    )
    external_modifier_option_id: Optional[str] = Field(
        None,
        alias="externalModifierOptionId",
    )
    group_name: str = Field(..., min_length=1, alias="groupName")
    option_name: str = Field(..., min_length=1, alias="optionName")
    quantity: int = Field(1, gt=0)
    price_delta: float = Field(0.0, alias="priceDelta")


class ModifierOptionView(BaseModel):
    """Simplified modifier option view for display."""

    id: str
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price_delta: float = Field(0.0, alias="priceDelta")
    is_default: bool = Field(False, alias="isDefault")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierOptionChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")


class ModifierGroupView(BaseModel):
    """Simplified modifier group view for display."""

    id: str
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierGroupChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")
    is_required: bool = Field(False, alias="isRequired")
    min_selection: int = Field(0, ge=0, alias="minSelection")
    max_selection: Optional[int] = Field(None, gt=0, alias="maxSelection")
    options: List[ModifierOptionView] = Field(default_factory=list)


class CreateModifierOption(BaseModel):
    """Schema for creating a new modifier option."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    modifier_group_id: str = Field(..., alias="modifierGroupId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price_delta: float = Field(0.0, alias="priceDelta")
    is_default: bool = Field(False, alias="isDefault")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierOptionChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")


class CreateModifierGroupOption(BaseModel):
    """Create-time modifier option embedded in modifier group create."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price_delta: float = Field(0.0, alias="priceDelta")
    is_default: bool = Field(False, alias="isDefault")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierOptionChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")


class CreateModifierGroup(BaseModel):
    """Schema for creating a new modifier group."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    options: List[CreateModifierGroupOption] = Field(..., min_length=1)
    min_selection: int = Field(0, ge=0, alias="minSelection")
    max_selection: Optional[int] = Field(None, gt=0, alias="maxSelection")
    is_required: bool = Field(False, alias="isRequired")
    display_order: int = Field(0, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierGroupChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_group_create(self) -> "CreateModifierGroup":
        """Validate group selection bounds and options count."""
        if (
            self.max_selection is not None
            and self.max_selection < self.min_selection
        ):
            raise ValueError(
                "maxSelection must be greater than or equal to minSelection"
            )

        if (
            self.max_selection is not None
            and self.max_selection > len(self.options)
        ):
            raise ValueError(
                "maxSelection cannot exceed the number of provided options"
            )

        return self


class CreateItemModifierBinding(BaseModel):
    """Schema for creating a new item-modifier binding."""

    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    menu_item_id: Optional[str] = Field(None, alias="menuItemId")
    menu_item_variant_id: Optional[str] = Field(
        None,
        alias="menuItemVariantId",
    )
    menu_set_id: Optional[str] = Field(None, alias="menuSetId")
    modifier_group_id: str = Field(..., alias="modifierGroupId")
    is_required_override: Optional[bool] = Field(
        None,
        alias="isRequiredOverride",
    )
    min_selection_override: Optional[int] = Field(
        None,
        ge=0,
        alias="minSelectionOverride",
    )
    max_selection_override: Optional[int] = Field(
        None,
        gt=0,
        alias="maxSelectionOverride",
    )
    excluded_option_ids: Optional[List[str]] = Field(
        None,
        alias="excludedOptionIds",
    )
    option_overrides: Optional[List[ModifierOptionOverride]] = Field(
        None,
        alias="optionOverrides",
    )
    display_order: int = Field(0, ge=0, alias="displayOrder")
    is_active: bool = Field(True, alias="isActive")

    @model_validator(mode="after")
    def validate_binding_targets(self) -> "CreateItemModifierBinding":
        """Validate exclusive binding targets and selection overrides."""
        has_menu_item_target = bool(self.menu_item_id)
        has_menu_set_target = bool(self.menu_set_id)

        if has_menu_item_target == has_menu_set_target:
            raise ValueError(
                "Exactly one of menuItemId or menuSetId is required"
            )

        if self.menu_item_variant_id and not has_menu_item_target:
            raise ValueError(
                "menuItemVariantId can only be provided when menuItemId is set"
            )

        if (
            self.min_selection_override is not None
            and self.max_selection_override is not None
            and self.max_selection_override < self.min_selection_override
        ):
            raise ValueError(
                "maxSelectionOverride must be greater than or equal to "
                "minSelectionOverride"
            )

        return self


class UpdateModifierOption(BaseModel):
    """Schema for updating a modifier option."""

    id: str
    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    modifier_group_id: Optional[str] = Field(None, alias="modifierGroupId")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price_delta: Optional[float] = Field(None, alias="priceDelta")
    is_default: Optional[bool] = Field(None, alias="isDefault")
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierOptionChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: Optional[bool] = Field(None, alias="isActive")


class UpdateModifierGroup(BaseModel):
    """Schema for updating a modifier group."""

    id: str
    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    options: Optional[List[CreateModifierGroupOption]] = None
    min_selection: Optional[int] = Field(None, ge=0, alias="minSelection")
    max_selection: Optional[int] = Field(None, gt=0, alias="maxSelection")
    is_required: Optional[bool] = Field(None, alias="isRequired")
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    channel_mappings: Optional[List[ModifierGroupChannelMapping]] = Field(
        None,
        alias="channelMappings",
    )
    is_active: Optional[bool] = Field(None, alias="isActive")


class UpdateItemModifierBinding(BaseModel):
    """Schema for updating an item-modifier binding."""

    id: str
    modifier_revision_id: Optional[str] = Field(
        None,
        alias="modifierRevisionId",
    )
    location_id: Optional[str] = Field(None, alias="locationId")
    menu_item_id: Optional[str] = Field(None, alias="menuItemId")
    menu_item_variant_id: Optional[str] = Field(
        None,
        alias="menuItemVariantId",
    )
    menu_set_id: Optional[str] = Field(None, alias="menuSetId")
    modifier_group_id: Optional[str] = Field(None, alias="modifierGroupId")
    is_required_override: Optional[bool] = Field(
        None,
        alias="isRequiredOverride",
    )
    min_selection_override: Optional[int] = Field(
        None,
        ge=0,
        alias="minSelectionOverride",
    )
    max_selection_override: Optional[int] = Field(
        None,
        gt=0,
        alias="maxSelectionOverride",
    )
    excluded_option_ids: Optional[List[str]] = Field(
        None,
        alias="excludedOptionIds",
    )
    option_overrides: Optional[List[ModifierOptionOverride]] = Field(
        None,
        alias="optionOverrides",
    )
    display_order: Optional[int] = Field(None, ge=0, alias="displayOrder")
    is_active: Optional[bool] = Field(None, alias="isActive")


class ModifierGroupFilters(TypedDict, total=False):
    """Filters for querying modifier groups."""

    search: Optional[str]
    location_id: Optional[str]
    is_required: Optional[bool]
    is_active: Optional[bool]


class ModifierGroupSorting(TypedDict):
    """Sorting options for modifier group queries."""

    field: Literal["name", "display_order", "created_at"]
    direction: Literal["asc", "desc"]


class ModifierGroupQueryOptions(TypedDict, total=False):
    """Query options for modifier group retrieval."""

    page: int
    page_size: int
    filters: Optional[ModifierGroupFilters]
    sorting: Optional[ModifierGroupSorting]


class ModifierOptionFilters(TypedDict, total=False):
    """Filters for querying modifier options."""

    search: Optional[str]
    location_id: Optional[str]
    modifier_group_id: Optional[str]
    is_default: Optional[bool]
    is_active: Optional[bool]


class ModifierOptionSorting(TypedDict):
    """Sorting options for modifier option queries."""

    field: Literal["name", "display_order", "created_at"]
    direction: Literal["asc", "desc"]


class ModifierOptionQueryOptions(TypedDict, total=False):
    """Query options for modifier option retrieval."""

    page: int
    page_size: int
    filters: Optional[ModifierOptionFilters]
    sorting: Optional[ModifierOptionSorting]


class ItemModifierBindingFilters(TypedDict, total=False):
    """Filters for querying item-modifier bindings."""

    location_id: Optional[str]
    menu_item_id: Optional[str]
    menu_set_id: Optional[str]
    modifier_group_id: Optional[str]
    is_active: Optional[bool]


class ItemModifierBindingSorting(TypedDict):
    """Sorting options for item-modifier binding queries."""

    field: Literal["display_order", "created_at"]
    direction: Literal["asc", "desc"]


class ItemModifierBindingQueryOptions(TypedDict, total=False):
    """Query options for item-modifier binding retrieval."""

    page: int
    page_size: int
    filters: Optional[ItemModifierBindingFilters]
    sorting: Optional[ItemModifierBindingSorting]
