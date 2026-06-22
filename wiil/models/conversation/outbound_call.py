"""Outbound call request schema definitions for AI-powered telephony campaigns.

Provides schemas for scheduling and managing outbound phone calls initiated by AI agents.
Supports immediate, scheduled, and recurring call patterns with configurable retry logic,
calling hours restrictions, and integration with agent configurations.
"""

from datetime import datetime
from typing import Any, Dict, Literal, List, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.types.conversation_types import CallRequestStatus, ScheduleType


class CallingHours(BaseModel):
    """Calling hours configuration for outbound calls.

    Defines permitted time windows for outbound calls to ensure compliance with
    TCPA regulations and respect customer preferences. Calls scheduled outside
    these hours are queued until the next available window.

    Day of Week Values:
        - 0 = Sunday
        - 1 = Monday
        - 2 = Tuesday
        - 3 = Wednesday
        - 4 = Thursday
        - 5 = Friday
        - 6 = Saturday

    Attributes:
        start_time: Start time for permitted calling window in HH:MM 24-hour format
            (e.g., '09:00' for 9 AM). Calls before this time are queued.
        end_time: End time for permitted calling window in HH:MM 24-hour format
            (e.g., '17:00' for 5 PM). Calls after this time are queued.
        days_of_week: Array of permitted days of week for calling (0=Sunday through
            6=Saturday). Defaults to weekdays [1,2,3,4,5].

    Example:
        ```python
        calling_hours = CallingHours(
            start_time="09:00",
            end_time="17:00",
            days_of_week=[1, 2, 3, 4, 5]  # Weekdays only
        )
        ```
    """

    start_time: str = Field(
        ...,
        alias="startTime",
        pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Start time for permitted calling window in HH:MM 24-hour format (e.g., '09:00' for 9 AM)"
    )
    end_time: str = Field(
        ...,
        alias="endTime",
        pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="End time for permitted calling window in HH:MM 24-hour format (e.g., '17:00' for 5 PM)"
    )
    days_of_week: List[int] = Field(
        default=[1, 2, 3, 4, 5],
        alias="daysOfWeek",
        description="Array of permitted days of week for calling (0=Sunday through 6=Saturday)"
    )


class BusinessCallRequest(EntityModel):
    """Business call request schema for outbound AI-powered phone calls.

    Represents a complete outbound call request with all configuration options for
    AI-powered telephony campaigns. Supports immediate execution, scheduled calls,
    and recurring patterns with configurable retry logic.

    Architecture Context:
        - Agent Powered: References AgentConfiguration for AI behavior
        - Telephony Integration: Uses PhoneConfiguration for caller ID and routing
        - Conversation Tracking: Links to ServiceConversationConfig for analytics

    Schedule Types:
        - IMMEDIATE: Executes as soon as possible within calling hours
        - SCHEDULED: Executes at specific scheduledAt timestamp
        - RECURRING: Executes on callingHours schedule pattern

    Call Request Lifecycle:
        - PENDING: Created, awaiting execution window
        - SCHEDULED: Queued for specific time
        - IN_PROGRESS: Call currently active
        - COMPLETED: Call finished successfully
        - FAILED: Call failed after all retries
        - CANCELLED: Manually cancelled before execution

    Attributes:
        phone_configuration_id: Phone configuration ID for caller ID display and
            telephony routing settings. When omitted, uses organization default.
        to: Destination phone number in E.164 international format (e.g., '+12125551234').
        from_number: Caller ID phone number in E.164 format displayed to the recipient.
        agent_configuration_id: Agent configuration ID defining AI behavior, persona,
            and capabilities for this call.
        instruction_configuration_id: Optional instruction configuration ID to override
            agent defaults with call-specific behavioral guidelines.
        max_duration: Maximum call duration in seconds to prevent runaway calls.
        schedule_type: Call timing strategy (IMMEDIATE, SCHEDULED, or RECURRING).
        service_conversation_config_id: Linked conversation record ID for tracking.
        time_zone: IANA timezone identifier (e.g., 'America/New_York').
        scheduled_at: Unix timestamp in milliseconds for scheduled call execution.
        calling_hours: Permitted calling window configuration for TCPA compliance.
        max_retries: Maximum number of retry attempts if call fails (0-5).
        retry_delay_minutes: Delay in minutes between retry attempts.
        status: Current status of the call request lifecycle.
        metadata: Additional custom metadata for campaign tracking.

    Example:
        ```python
        call_request = BusinessCallRequest(
            to="+12125551234",
            from_number="+12125559999",
            agent_configuration_id="agent_456",
            schedule_type=ScheduleType.IMMEDIATE,
            calling_hours=CallingHours(
                start_time="09:00",
                end_time="17:00"
            ),
            max_retries=3,
            retry_delay_minutes=30
        )
        ```
    """

    phone_configuration_id: Optional[str] = Field(
        None,
        alias="phoneConfigurationId",
        description="Phone configuration ID for caller ID display and telephony routing"
    )
    to: str = Field(
        ...,
        description="Destination phone number in E.164 international format"
    )
    from_number: str = Field(
        ...,
        alias="from",
        description="Caller ID phone number in E.164 format displayed to the recipient"
    )
    agent_configuration_id: str = Field(
        ...,
        alias="agentConfigurationId",
        description="Agent configuration ID defining AI behavior for this call"
    )
    instruction_configuration_id: Optional[str] = Field(
        None,
        alias="instructionConfigurationId",
        description="Optional instruction configuration ID to override agent defaults"
    )
    max_duration: Optional[int] = Field(
        None,
        alias="maxDuration",
        gt=0,
        description="Maximum call duration in seconds"
    )
    schedule_type: ScheduleType = Field(
        ...,
        alias="scheduleType",
        description="Call timing strategy (IMMEDIATE, SCHEDULED, or RECURRING)"
    )
    service_conversation_config_id: Optional[str] = Field(
        None,
        alias="serviceConversationConfigId",
        description="Linked conversation record ID for tracking call outcomes"
    )

    # Time constraints
    time_zone: Optional[str] = Field(
        None,
        alias="timeZone",
        description="IANA timezone identifier (e.g., 'America/New_York')"
    )
    scheduled_at: Optional[int] = Field(
        None,
        alias="scheduledAt",
        description="Unix timestamp in milliseconds for scheduled call execution"
    )
    calling_hours: Optional[CallingHours] = Field(
        None,
        alias="callingHours",
        description="Permitted calling window configuration for TCPA compliance"
    )

    # Retry configuration
    max_retries: Optional[int] = Field(
        None,
        alias="maxRetries",
        ge=0,
        le=5,
        description="Maximum number of retry attempts if call fails (0-5)"
    )
    retry_delay_minutes: Optional[int] = Field(
        None,
        alias="retryDelayMinutes",
        gt=0,
        description="Delay in minutes between retry attempts"
    )

    # Status tracking
    status: CallRequestStatus = Field(
        default=CallRequestStatus.PENDING,
        description="Current status of the call request lifecycle"
    )

    # Extensibility
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom metadata for campaign tracking"
    )


class CreateCallRequest(BaseModel):
    """Schema for creating a new outbound call request.

    Omits auto-generated fields (id, timestamps, audit fields) that are
    populated by the system upon creation.

    Example:
        ```python
        create_request = CreateCallRequest(
            to="+12125551234",
            from_number="+12125559999",
            agent_configuration_id="agent_456",
            schedule_type=ScheduleType.IMMEDIATE
        )
        ```
    """

    phone_configuration_id: Optional[str] = Field(None, alias="phoneConfigurationId")
    to: str = Field(...)
    from_number: str = Field(..., alias="from")
    agent_configuration_id: str = Field(..., alias="agentConfigurationId")
    instruction_configuration_id: Optional[str] = Field(None, alias="instructionConfigurationId")
    max_duration: Optional[int] = Field(None, alias="maxDuration", gt=0)
    schedule_type: ScheduleType = Field(..., alias="scheduleType")
    service_conversation_config_id: Optional[str] = Field(None, alias="serviceConversationConfigId")
    time_zone: Optional[str] = Field(None, alias="timeZone")
    scheduled_at: Optional[int] = Field(None, alias="scheduledAt")
    calling_hours: Optional[CallingHours] = Field(None, alias="callingHours")
    max_retries: Optional[int] = Field(None, alias="maxRetries", ge=0, le=5)
    retry_delay_minutes: Optional[int] = Field(None, alias="retryDelayMinutes", gt=0)
    status: CallRequestStatus = Field(default=CallRequestStatus.PENDING)
    metadata: Optional[Dict[str, Any]] = Field(None)


class UpdateCallRequest(CreateCallRequest):
    """Schema for updating an existing call request."""

    id: str = Field(..., description="Unique identifier of the CallRequest to update")


class CallRequestResult(BaseModel):
    """Result schema for telephony request operations.

    Attributes:
        success: Whether the telephony request was successful.
        request: Original call request details.
        error_message: Error message if the request failed.
    """

    success: Optional[bool] = Field(
        default=False,
        description="Whether the telephony request was successful"
    )
    request: Optional[BusinessCallRequest] = Field(
        None,
        description="Original call request details"
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if the request failed"
    )


class DateRange(TypedDict, total=False):
    """Date range filter for call request queries."""

    start: Optional[datetime]
    end: Optional[datetime]


class CallRequestFilters(TypedDict, total=False):
    """Call request filter options."""

    search: Optional[str]
    status: Optional[CallRequestStatus]
    schedule_type: Optional[ScheduleType]
    agent_configuration_id: Optional[str]
    date_range: Optional[DateRange]


class CallRequestSorting(TypedDict):
    """Call request sorting options."""

    field: Literal["scheduledAt", "status", "createdAt"]
    direction: Literal["asc", "desc"]


class CallRequestQueryOptions(TypedDict, total=False):
    """Call request query options."""

    page: int
    page_size: int
    filters: Optional[CallRequestFilters]
    sorting: Optional[CallRequestSorting]
