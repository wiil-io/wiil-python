"""Assistant setup schema definitions.

This module mirrors src/core/assistant-setups/
"""

from wiil.models.assistant_setups.assistant_setup_result import AssistantSetupResult
from wiil.models.assistant_setups.base_assistant_setup import (
    AdvanceBaseAssistant,
    BaseAssistant,
)
from wiil.models.assistant_setups.phone_assistant_setup import (
    ChainedPhoneAssistantSetup,
    PhoneAssistantSetup,
)
from wiil.models.assistant_setups.web_assistant_setup import (
    ChainedWebAssistantSetup,
    WebAssistantSetup,
)

__all__ = [
    # Base
    "BaseAssistant",
    "AdvanceBaseAssistant",
    # Phone
    "PhoneAssistantSetup",
    "ChainedPhoneAssistantSetup",
    # Web
    "WebAssistantSetup",
    "ChainedWebAssistantSetup",
    # Result
    "AssistantSetupResult",
]
