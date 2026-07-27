"""Service layer for higher-level workflow APIs.

This package mirrors TypeScript service abstractions that are not directly tied
to CRUD-style resources.
"""

from wiil.services.messaging import MessagingService
from wiil.services.ott import (
    GetOttConfigurationRequest,
    OttChatConnectionConfig,
    OttContactInfo,
    OttService,
    OttVoiceConnectionConfig,
)

__all__ = [
    # Messaging service
    "MessagingService",
    # OTT service
    "GetOttConfigurationRequest",
    "OttChatConnectionConfig",
    "OttContactInfo",
    "OttService",
    "OttVoiceConnectionConfig",
]
