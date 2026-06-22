"""Messaging service operations.

This module provides the MessagingService class for outbound messaging workflows.
"""

from typing import Dict, List, Type, TypeVar, Union

from pydantic import ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.conversation import (
    BusinessCallRequest,
    CreateCallRequest,
    CreateEmailRequest,
    CreateSmsRequest,
    EmailRequest,
    SmsRequest,
)
from wiil.types import PaginatedResult

RequestModelT = TypeVar(
    "RequestModelT",
    CreateCallRequest,
    CreateSmsRequest,
    CreateEmailRequest,
)


CALL_REQUEST_RESOURCE_PATH = "/business-requests/calls"
SMS_REQUEST_RESOURCE_PATH = "/business-requests/sms"
EMAIL_REQUEST_RESOURCE_PATH = "/business-requests/emails"
BATCH_LIMIT = 100


class MessagingService:
    """Service class for outbound messaging workflows."""

    def __init__(self, http: HttpClient):
        """Creates a new MessagingService instance.

        Args:
            http: HTTP client for API communication.
        """
        self._http = http

    def request_call(
        self,
        request: Union[CreateCallRequest, Dict[str, object]],
    ) -> BusinessCallRequest:
        """Requests an outbound AI-powered phone call.

        Schedules or immediately initiates an outbound call using the configured AI agent.
        Supports immediate execution, scheduled calls, and recurring patterns with
        configurable retry logic and TCPA-compliant calling hours restrictions.

        Args:
            request: Call request configuration containing:
                - ``to`` - Destination phone number in E.164 format (e.g., '+12125551234')
                - ``from_`` - Caller ID phone number in E.164 format
                - ``agent_configuration_id`` - AI agent configuration defining behavior and persona
                - ``schedule_type`` - Timing strategy: 'IMMEDIATE', 'SCHEDULED', or 'RECURRING'
                - ``calling_hours`` - Optional permitted calling window for TCPA compliance
                - ``max_retries`` - Optional retry attempts if call fails (0-5)
                - ``scheduled_at`` - Optional Unix timestamp (ms) for scheduled execution

        Returns:
            The created business call request record with assigned ID and status.

        Raises:
            WiilValidationError: When request or response validation fails.

        Example:
            >>> call_request = messaging.request_call({
            ...     "to": "+12125551234",
            ...     "from": "+12125559999",
            ...     "agentConfigurationId": "agent_456",
            ...     "scheduleType": "IMMEDIATE",
            ...     "callingHours": {
            ...         "startTime": "09:00",
            ...         "endTime": "17:00",
            ...         "daysOfWeek": [1, 2, 3, 4, 5]
            ...     }
            ... })
        """
        validated_request = self._validate_request(
            request,
            CreateCallRequest,
            "Invalid call request payload.",
        )

        return self._http.post(
            CALL_REQUEST_RESOURCE_PATH,
            validated_request.model_dump(by_alias=True, exclude_none=True),
            schema=CreateCallRequest,
            response_model=BusinessCallRequest,
        )

    def send_sms(
        self,
        request: Union[CreateSmsRequest, Dict[str, object]],
    ) -> SmsRequest:
        """Sends an outbound SMS text message.

        Delivers a text message to the specified recipient with support for
        template-based composition, variable substitution, and scheduled delivery.
        Standard SMS supports 160 characters (GSM-7) or 70 characters per segment (Unicode).

        Args:
            request: SMS request configuration containing:
                - ``to`` - Recipient phone number in E.164 format (e.g., '+12125551234')
                - ``body`` - Text content of the message
                - ``from_`` - Optional sender phone number in E.164 format
                - ``template_id`` - Optional pre-defined SMS template ID
                - ``variables`` - Optional template variable substitutions (e.g., ``{"firstName": "John"}``)
                - ``scheduled_at`` - Optional Unix timestamp (ms) for scheduled delivery

        Returns:
            The created SMS request record with assigned ID and delivery status.

        Raises:
            WiilValidationError: When request or response validation fails.

        Example:
            >>> sms = messaging.send_sms({
            ...     "to": "+12125551234",
            ...     "body": "Hi {{firstName}}, your appointment is confirmed for {{time}}.",
            ...     "variables": {"firstName": "John", "time": "3:00 PM"}
            ... })
        """
        validated_request = self._validate_request(
            request,
            CreateSmsRequest,
            "Invalid SMS request payload.",
        )

        return self._http.post(
            SMS_REQUEST_RESOURCE_PATH,
            validated_request.model_dump(by_alias=True, exclude_none=True),
            schema=CreateSmsRequest,
            response_model=SmsRequest,
        )

    def send_email(
        self,
        request: Union[CreateEmailRequest, Dict[str, object]],
    ) -> EmailRequest:
        """Sends an outbound email message.

        Delivers an email to specified recipients with support for HTML/text content,
        file attachments, template-based composition with variable substitution,
        and scheduled delivery. Integrates with SendGrid, SES, and other providers.

        Args:
            request: Email request configuration containing:
                - ``to`` - Array of primary recipients with email and optional name
                - ``subject`` - Email subject line (supports ``{{variable}}`` substitution)
                - ``body_html`` - HTML content of the email body
                - ``body_text`` - Optional plain text alternative for accessibility
                - ``cc`` - Optional array of carbon copy recipients
                - ``bcc`` - Optional array of blind carbon copy recipients
                - ``reply_to`` - Optional reply-to email address
                - ``template_id`` - Optional pre-defined email template ID
                - ``variables`` - Optional template variable substitutions
                - ``attachments`` - Optional file attachments (base64-encoded, max 25MB total)
                - ``scheduled_at`` - Optional Unix timestamp (ms) for scheduled delivery

        Returns:
            The created email request record with assigned ID and delivery status.

        Raises:
            WiilValidationError: When request or response validation fails.

        Example:
            >>> email = messaging.send_email({
            ...     "to": [{"email": "customer@example.com", "name": "Customer"}],
            ...     "subject": "Your Order Confirmation - #{{orderId}}",
            ...     "bodyHtml": "<h1>Thank you, {{name}}!</h1><p>Your order is confirmed.</p>",
            ...     "variables": {"orderId": "12345", "name": "John"}
            ... })
        """
        validated_request = self._validate_request(
            request,
            CreateEmailRequest,
            "Invalid email request payload.",
        )

        return self._http.post(
            EMAIL_REQUEST_RESOURCE_PATH,
            validated_request.model_dump(by_alias=True, exclude_none=True),
            schema=CreateEmailRequest,
            response_model=EmailRequest,
        )

    def request_call_batch(
        self,
        requests: List[Union[CreateCallRequest, Dict[str, object]]],
    ) -> PaginatedResult[BusinessCallRequest]:
        """Requests multiple outbound AI-powered phone calls in a single batch operation.

        Schedules or immediately initiates multiple outbound calls using the configured AI agent.
        Useful for campaign launches, bulk notifications, or scheduled outreach programs.

        Args:
            requests: Array of call request configurations (max 100 items).

        Returns:
            Paginated result containing created call request records.

        Raises:
            WiilValidationError: When batch size exceeds limit or item validation fails.

        Example:
            >>> calls = messaging.request_call_batch([
            ...     {"to": "+12125551234", "from": "+12125559999", "agentConfigurationId": "agent_1", "scheduleType": "IMMEDIATE"},
            ...     {"to": "+12125551235", "from": "+12125559999", "agentConfigurationId": "agent_1", "scheduleType": "IMMEDIATE"}
            ... ])
            >>> print(f"Scheduled {len(calls.data)} calls")
        """
        if len(requests) > BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {BATCH_LIMIT}",
                details=[
                    {
                        "path": ["requests"],
                        "message": (
                            f"Array length {len(requests)} exceeds "
                            f"maximum of {BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        validated_requests = []
        for i, request in enumerate(requests):
            try:
                validated = self._validate_request(
                    request,
                    CreateCallRequest,
                    f"Validation failed for call request at index {i}",
                )
                validated_requests.append(
                    validated.model_dump(by_alias=True, exclude_none=True)
                )
            except WiilValidationError:
                raise

        return self._http.post(
            f"{CALL_REQUEST_RESOURCE_PATH}/batch",
            validated_requests,
            response_model=PaginatedResult[BusinessCallRequest],
        )

    def send_sms_batch(
        self,
        requests: List[Union[CreateSmsRequest, Dict[str, object]]],
    ) -> PaginatedResult[SmsRequest]:
        """Sends multiple outbound SMS text messages in a single batch operation.

        Delivers text messages to multiple recipients efficiently. Useful for
        bulk notifications, marketing campaigns, or scheduled reminders.

        Args:
            requests: Array of SMS request configurations (max 100 items).

        Returns:
            Paginated result containing created SMS request records.

        Raises:
            WiilValidationError: When batch size exceeds limit or item validation fails.

        Example:
            >>> sms_messages = messaging.send_sms_batch([
            ...     {"to": "+12125551234", "body": "Your appointment is confirmed."},
            ...     {"to": "+12125551235", "body": "Your appointment is confirmed."}
            ... ])
            >>> print(f"Sent {len(sms_messages.data)} SMS messages")
        """
        if len(requests) > BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {BATCH_LIMIT}",
                details=[
                    {
                        "path": ["requests"],
                        "message": (
                            f"Array length {len(requests)} exceeds "
                            f"maximum of {BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        validated_requests = []
        for i, request in enumerate(requests):
            try:
                validated = self._validate_request(
                    request,
                    CreateSmsRequest,
                    f"Validation failed for SMS request at index {i}",
                )
                validated_requests.append(
                    validated.model_dump(by_alias=True, exclude_none=True)
                )
            except WiilValidationError:
                raise

        return self._http.post(
            f"{SMS_REQUEST_RESOURCE_PATH}/batch",
            validated_requests,
            response_model=PaginatedResult[SmsRequest],
        )

    def send_email_batch(
        self,
        requests: List[Union[CreateEmailRequest, Dict[str, object]]],
    ) -> PaginatedResult[EmailRequest]:
        """Sends multiple outbound email messages in a single batch operation.

        Delivers emails to multiple recipients efficiently. Useful for
        bulk communications, newsletters, or transactional email campaigns.

        Args:
            requests: Array of email request configurations (max 100 items).

        Returns:
            Paginated result containing created email request records.

        Raises:
            WiilValidationError: When batch size exceeds limit or item validation fails.

        Example:
            >>> emails = messaging.send_email_batch([
            ...     {"to": [{"email": "user1@example.com"}], "subject": "Welcome!", "bodyHtml": "<h1>Hello</h1>"},
            ...     {"to": [{"email": "user2@example.com"}], "subject": "Welcome!", "bodyHtml": "<h1>Hello</h1>"}
            ... ])
            >>> print(f"Sent {len(emails.data)} emails")
        """
        if len(requests) > BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {BATCH_LIMIT}",
                details=[
                    {
                        "path": ["requests"],
                        "message": (
                            f"Array length {len(requests)} exceeds "
                            f"maximum of {BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        validated_requests = []
        for i, request in enumerate(requests):
            try:
                validated = self._validate_request(
                    request,
                    CreateEmailRequest,
                    f"Validation failed for email request at index {i}",
                )
                validated_requests.append(
                    validated.model_dump(by_alias=True, exclude_none=True)
                )
            except WiilValidationError:
                raise

        return self._http.post(
            f"{EMAIL_REQUEST_RESOURCE_PATH}/batch",
            validated_requests,
            response_model=PaginatedResult[EmailRequest],
        )

    @staticmethod
    def _validate_request(
        request: Union[RequestModelT, Dict[str, object]],
        model: Type[RequestModelT],
        error_message: str,
    ) -> RequestModelT:
        try:
            if isinstance(request, model):
                return request
            return model.model_validate(request)
        except ValidationError as exc:
            raise WiilValidationError(error_message, exc.errors())

