"""Base models and common types for WIIL SDK.

This module contains base Pydantic models and common types
used across all WIIL SDK models.
"""

from typing import Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    """Base model for all WIIL entities.

    Provides common fields for all models including unique identifier
    and timestamp tracking.

    Attributes:
        id: Unique identifier for the model
        created_at: Date when the model was created (Unix timestamp)
        updated_at: Date when the model was last updated (Unix timestamp)
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
        validate_assignment=True,
    )

    id: str = Field(..., description="Unique identifier for the model")
    created_at: Optional[int] = Field(
        None,
        description="Date when the model was created",
        alias="createdAt"
    )
    updated_at: Optional[int] = Field(
        None,
        description="Date when the model was last updated",
        alias="updatedAt"
    )


class Address(PydanticBaseModel):
    """Physical address model.

    Represents a complete mailing/physical address with all required components.

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

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

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
