"""Base models and common types for WIIL SDK.

This module contains base Pydantic models and common types
used across all WIIL SDK models.
"""

from typing import Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Canonical configuration base for all WIIL SDK models.

    This is the single source of truth for model configuration across the
    SDK. Every other model in the SDK should extend this class (directly or
    transitively) so that validation behavior remains consistent.

    The configuration enforces:
        - Population by both field name and alias (``validate_by_name`` and
          ``validate_by_alias``).
        - Enum values are used during validation (``use_enum_values``).
        - Strict type coercion rules (``strict``).
        - Rejection of unknown fields (``extra="forbid"``).

    This class intentionally declares no fields; it exists purely to provide
    shared configuration.
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
        strict=True,
        extra="forbid",
    )


class EntityModel(BaseModel):
    """Base model for persisted WIIL entities.

    Extends :class:`BaseModel` with the fields common to all entities that
    are stored and tracked over time. Inherits the strict configuration from
    :class:`BaseModel`.

    Attributes:
        id: Unique identifier for the entity.
        created_at: Date when the entity was created (Unix timestamp).
        updated_at: Date when the entity was last updated (Unix timestamp).
    """

    id: str = Field(..., description="Unique identifier for the entity")
    created_at: Optional[int] = Field(
        None,
        alias="createdAt",
        description="Date when the entity was created",
    )
    updated_at: Optional[int] = Field(
        None,
        alias="updatedAt",
        description="Date when the entity was last updated",
    )


class Address(BaseModel):
    """Physical address model.

    Represents a complete mailing/physical address with all required components.
    Inherits the strict configuration from :class:`BaseModel`.

    Attributes:
        street: Primary street address
        street2: Secondary street address (apartment, suite, etc.)
        city: City name
        state: State/province/region
        postal_code: Postal/ZIP code
        country: Country name or code

    Example:
        ```python
        address = Address(
            street="123 Main St",
            city="San Francisco",
            state="CA",
            postal_code="94102",
            country="USA"
        )
        ```
    """

    street: str = Field(..., min_length=2, description="Primary street address")
    street2: Optional[str] = Field(None, description="Secondary street address")
    city: str = Field(..., min_length=2, description="City name")
    state: str = Field(..., min_length=2, description="State/province/region")
    postal_code: str = Field(
        ...,
        min_length=2,
        description="Postal/ZIP code",
        alias="postalCode"
    )
    country: str = Field(..., min_length=2, description="Country name or code")


# Language code type - ISO 639-1 language codes
LanguageCode = Literal[
    "en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko",
    "ar", "hi", "bn", "pa", "te", "mr", "ta", "ur", "gu", "kn",
    "ml", "or", "as", "mai", "ne", "si", "my", "km", "lo", "th",
    "vi", "id", "ms", "fil", "nl", "pl", "uk", "ro", "cs", "hu",
    "sv", "no", "da", "fi", "el", "he", "tr", "fa", "sw", "am"
]
