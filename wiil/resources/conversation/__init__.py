"""Conversation resource classes for WIIL SDK."""

from .outbound_calls import OutboundCallsResource
from .outbound_emails import OutboundEmailsResource
from .outbound_sms import OutboundSmsResource
from .outbound_templates import OutboundTemplatesResource
from .translation_services import TranslationServicesResource

__all__ = [
    "OutboundCallsResource",
    "OutboundEmailsResource",
    "OutboundSmsResource",
    "OutboundTemplatesResource",
    "TranslationServicesResource",
]
