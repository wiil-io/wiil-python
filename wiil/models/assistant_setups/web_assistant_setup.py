"""Web assistant setup schema definitions.

This module mirrors src/core/assistant-setups/web-assitant-setup.schema.ts
"""

from pydantic import Field, HttpUrl

from wiil.models.assistant_setups.base_assistant_setup import BaseAssistant
from wiil.models.type_definitions.service_config_definitions import OttCommunicationType


class WebAssistantSetup(BaseAssistant):
    """Schema for setting up a web AI assistant.

    Extends BaseAssistant with web-specific configuration.

    Attributes:
        website_url: URL of the website where this assistant will be deployed
        communication_type: Type of OTT communication (text, voice, unified)

    Example:
        ```python
        setup = WebAssistantSetup(
            assistant_name="Web Support",
            support_model_id="model-123",
            instruction_configuration_id="inst-456",
            website_url="https://example.com",
            communication_type=OttCommunicationType.UNIFIED
        )
        ```
    """

    website_url: HttpUrl = Field(
        ...,
        description="URL of the website where this assistant will be deployed",
        alias="websiteUrl"
    )
    communication_type: OttCommunicationType = Field(
        ...,
        description="Type of over-the-top communication method for the web channel (text, voice, unified)",
        alias="communicationType"
    )


class ChainedWebAssistantSetup(WebAssistantSetup):
    """Schema for setting up a web AI assistant with advanced configurations.

    Note: Currently identical to WebAssistantSetup as the TypeScript schema
    extends WebAssistantSetupSchema without adding new fields.

    Example:
        ```python
        setup = ChainedWebAssistantSetup(
            assistant_name="Advanced Web Support",
            support_model_id="model-123",
            instruction_configuration_id="inst-456",
            website_url="https://example.com",
            communication_type=OttCommunicationType.UNIFIED
        )
        ```
    """

    pass
