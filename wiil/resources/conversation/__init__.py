"""Conversation resource classes for WIIL SDK."""

from .outbound_calls import OutboundCallsResource
from .outbound_emails import OutboundEmailsResource
from .outbound_sms import OutboundSmsResource
from .outbound_templates import OutboundTemplatesResource

__all__ = [
    "OutboundCallsResource",
    "OutboundEmailsResource",
    "OutboundSmsResource",
    "OutboundTemplatesResource",
]
