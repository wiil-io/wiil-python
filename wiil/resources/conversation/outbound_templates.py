"""Outbound templates resource for managing message templates."""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.conversation import (
    CreateEmailTemplate,
    CreateSmsTemplate,
    CreateWhatsappTemplate,
    EmailTemplate,
    OutboundTemplate,
    SmsTemplate,
    UpdateEmailTemplate,
    UpdateSmsTemplate,
    UpdateWhatsappTemplate,
    WhatsappTemplate,
)
from wiil.types import OutboundTemplateChannel, PaginatedResult, PaginationRequest


class OutboundTemplatesResource:
    """Resource class for managing outbound message templates in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and listing outbound
    message templates for email, SMS, and WhatsApp channels. Templates support
    variable substitution for personalized messaging.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/outbound-templates"

    def create_email_template(self, data: CreateEmailTemplate) -> EmailTemplate:
        """Create a new email template."""
        return self._http.post(
            f"{self._base_path}/email",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateEmailTemplate,
            response_model=EmailTemplate,
        )

    def create_sms_template(self, data: CreateSmsTemplate) -> SmsTemplate:
        """Create a new SMS template."""
        return self._http.post(
            f"{self._base_path}/sms",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateSmsTemplate,
            response_model=SmsTemplate,
        )

    def create_whatsapp_template(
        self,
        data: CreateWhatsappTemplate,
    ) -> WhatsappTemplate:
        """Create a new WhatsApp template."""
        return self._http.post(
            f"{self._base_path}/whatsapp",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateWhatsappTemplate,
            response_model=WhatsappTemplate,
        )

    def get(self, template_id: str) -> OutboundTemplate:
        """Retrieve a template by ID."""
        return self._http.get(
            f"{self._base_path}/{template_id}",
            response_model=OutboundTemplate,
        )

    def get_by_code(self, code: str) -> OutboundTemplate:
        """Retrieve a template by code."""
        return self._http.get(
            f"{self._base_path}/by-code/{code}",
            response_model=OutboundTemplate,
        )

    def get_by_channel(
        self,
        channel: OutboundTemplateChannel,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[OutboundTemplate]:
        """Retrieve templates by channel."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-channel/{channel}{query_string}",
            response_model=PaginatedResult[OutboundTemplate],
        )

    def get_by_tags(
        self,
        tags: List[str],
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[OutboundTemplate]:
        """Retrieve templates by tags."""
        query_params: Dict[str, Any] = {}
        for tag in tags:
            if "tags" not in query_params:
                query_params["tags"] = []
            query_params["tags"].append(tag)

        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        # Build query string with multiple tags
        parts = []
        for tag in tags:
            parts.append(f"tags={tag}")
        if params:
            parts.append(f"page={params.page}")
            parts.append(f"pageSize={params.page_size}")

        query_string = "&".join(parts)
        return self._http.get(
            f"{self._base_path}/by-tags?{query_string}",
            response_model=PaginatedResult[OutboundTemplate],
        )

    def update_email_template(self, data: UpdateEmailTemplate) -> EmailTemplate:
        """Update an existing email template."""
        return self._http.patch(
            f"{self._base_path}/email/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateEmailTemplate,
            response_model=EmailTemplate,
        )

    def update_sms_template(self, data: UpdateSmsTemplate) -> SmsTemplate:
        """Update an existing SMS template."""
        return self._http.patch(
            f"{self._base_path}/sms/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateSmsTemplate,
            response_model=SmsTemplate,
        )

    def update_whatsapp_template(
        self,
        data: UpdateWhatsappTemplate,
    ) -> WhatsappTemplate:
        """Update an existing WhatsApp template."""
        return self._http.patch(
            f"{self._base_path}/whatsapp/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateWhatsappTemplate,
            response_model=WhatsappTemplate,
        )

    def activate(self, template_id: str) -> OutboundTemplate:
        """Activate a template."""
        return self._http.post(
            f"{self._base_path}/{template_id}/activate",
            {},
            response_model=OutboundTemplate,
        )

    def deactivate(self, template_id: str) -> OutboundTemplate:
        """Deactivate a template."""
        return self._http.post(
            f"{self._base_path}/{template_id}/deactivate",
            {},
            response_model=OutboundTemplate,
        )

    def render(
        self,
        template_id: str,
        variables: Dict[str, str],
    ) -> Dict[str, Optional[str]]:
        """Render a template with provided variables.

        Returns:
            Dict with optional keys: subject, bodyHtml, bodyText, body
        """
        return self._http.post(
            f"{self._base_path}/{template_id}/render",
            {"variables": variables},
            response_model=dict,
        )

    def delete(self, template_id: str) -> bool:
        """Delete a template."""
        return self._http.delete(f"{self._base_path}/{template_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[OutboundTemplate]:
        """List templates with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[OutboundTemplate],
        )


__all__ = ["OutboundTemplatesResource"]
