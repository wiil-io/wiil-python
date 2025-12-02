"""WIIL error classes."""

from wiil.errors.exceptions import (
    WiilAPIError,
    WiilConfigurationError,
    WiilError,
    WiilNetworkError,
    WiilValidationError,
)

__all__ = [
    "WiilError",
    "WiilAPIError",
    "WiilValidationError",
    "WiilNetworkError",
    "WiilConfigurationError",
]
