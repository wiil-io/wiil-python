"""WIIL Platform Python SDK.

Official Python SDK for the WIIL Platform - AI-powered conversational services
for intelligent customer interactions, voice processing, real-time translation,
and business management.
"""

from wiil.client import WiilClient
from wiil.errors import (
    WiilAPIError,
    WiilConfigurationError,
    WiilError,
    WiilNetworkError,
    WiilValidationError,
)

__version__ = "0.0.0"
__all__ = [
    "WiilClient",
    "WiilError",
    "WiilAPIError",
    "WiilValidationError",
    "WiilNetworkError",
    "WiilConfigurationError",
]
