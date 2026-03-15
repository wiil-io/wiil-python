"""Service layer for higher-level workflow APIs.

This package mirrors TypeScript service abstractions that are not directly tied
to CRUD-style resources.
"""

from wiil.services.ott import (
    GetOttConfigurationRequest,
    OttChatConnectionConfig,
    OttContactInfo,
    OttService,
    OttVoiceConnectionConfig,
)
from wiil.services.translation import (
    SupportLanguage,
    TranslationConnectionConfig,
    TranslationRequest,
    TranslationService,
)

__all__ = [
    "GetOttConfigurationRequest",
    "OttChatConnectionConfig",
    "OttContactInfo",
    "OttService",
    "OttVoiceConnectionConfig",
    "SupportLanguage",
    "TranslationConnectionConfig",
    "TranslationRequest",
    "TranslationService",
]
