"""Dynamic Phone Agent resource for phone-based AI agents."""

import time
from dataclasses import dataclass
from typing import Callable, Optional

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.service_mgt.dynamic_setup import (
    DynamicAgentProcessingState,
    DynamicPhoneAgentSetup,
    DynamicPhoneAgentSetupResult,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
    UpdateDynamicPhoneAgent,
)
from wiil.resources.service_mgt.dynamic_agent_status import PollTimeoutError


@dataclass
class PhoneAgentCreateOptions:
    """Options for configuring agent creation behavior."""

    poll_until_complete: bool = True
    """Whether to poll until setup completes."""

    poll_interval: float = 5.0
    """Polling interval in seconds."""

    poll_timeout: float = 120.0
    """Maximum wait time in seconds before timing out."""

    on_progress: Optional[Callable[[DynamicAgentProcessingState], None]] = None
    """Callback invoked on each poll with the current processing state."""

    silent: bool = False
    """Whether to suppress console logging."""


class DynamicPhoneAgentResource:
    """Resource class for managing dynamic phone agent provisioning.

    Provides methods for creating and updating dynamic phone agent
    configurations. Dynamic phone agents enable AI-powered phone
    interactions with configurable STT and TTS capabilities.

    Example:
        >>> from wiil.models.type_definitions import (
        ...     AgentCapabilities,
        ...     AgentRoleTemplateIdentifier,
        ... )
        >>>
        >>> client = WiilClient(api_key='your-api-key')
        >>>
        >>> # Create with polling (waits for completion)
        >>> result = client.dynamic_phone_agent.create(
        ...     DynamicPhoneAgentSetup(
        ...         assistant_name='Alex',
        ...         capabilities=[AgentCapabilities.APPOINTMENT_MANAGEMENT],
        ...         role_template_identifier=(
        ...             AgentRoleTemplateIdentifier.CUSTOMER_SUPPORT_GENERAL
        ...         ),
        ...     )
        ... )
        >>>
        >>> # Create without waiting
        >>> result = client.dynamic_phone_agent.create(
        ...     data,
        ...     options=PhoneAgentCreateOptions(poll_until_complete=False)
        ... )
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/dynamic-setup/phone-agent'
        self._status_path = '/dynamic-setup'

    def create(
        self,
        data: DynamicPhoneAgentSetup,
        options: Optional[PhoneAgentCreateOptions] = None
    ) -> DynamicPhoneAgentSetupResult:
        """Create and provision a new dynamic phone agent.

        Args:
            data: Phone agent configuration data
            options: Creation options for polling and logging behavior

        Returns:
            The setup result including provisioned phone number

        Raises:
            WiilValidationError: When validation fails or model not supported
            WiilAPIError: When the API returns an error
            PollTimeoutError: When polling times out before completion
        """
        opts = options or PhoneAgentCreateOptions()
        start_time = time.time()
        agent_name = data.assistant_name

        # Validate model configurations before proceeding
        self._validate_model_configurations(
            data.stt_configuration,
            data.tts_configuration
        )

        # Log initial creation
        if not opts.silent:
            self._log(f'Creating agent "{agent_name}"...')

        # Create the agent
        initial_result = self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=DynamicPhoneAgentSetup,
            response_model=DynamicPhoneAgentSetupResult
        )

        # If not polling, return immediately
        if not opts.poll_until_complete:
            if not opts.silent:
                self._log(f'Setup initiated (ID: {initial_result.id})')
            return initial_result

        # Check if already complete
        if initial_result.processing_state.status in ('completed', 'failed'):
            self._log_final_result(initial_result, start_time, opts.silent)
            return initial_result

        # Poll until complete
        while True:
            result = self._http.get(
                f'{self._status_path}/{initial_result.id}',
                response_model=DynamicPhoneAgentSetupResult
            )
            last_state = result.processing_state

            # Log progress
            if not opts.silent:
                self._log_progress(last_state)

            # Invoke callback
            if opts.on_progress:
                opts.on_progress(last_state)

            # Check for terminal states
            if last_state.status in ('completed', 'failed'):
                self._log_final_result(result, start_time, opts.silent)
                return result

            # Check for timeout
            elapsed = time.time() - start_time
            if elapsed >= opts.poll_timeout:
                if not opts.silent:
                    self._log(f'Timeout after {self._format_duration(elapsed)}')
                msg = (
                    f'Polling timed out after {opts.poll_timeout}s. '
                    f'Last status: {last_state.status} '
                    f'at {last_state.progress_percentage}%'
                )
                raise PollTimeoutError(msg, last_state)

            # Wait before next poll
            time.sleep(opts.poll_interval)

    def update(
        self,
        data: UpdateDynamicPhoneAgent
    ) -> DynamicPhoneAgentSetupResult:
        """Update an existing dynamic phone agent configuration.

        Args:
            data: Phone agent update data (must include id)

        Returns:
            The updated phone agent setup result

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When phone agent is not found or API error
        """
        # Validate model configurations before proceeding
        self._validate_model_configurations(
            data.stt_configuration,
            data.tts_configuration
        )

        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateDynamicPhoneAgent,
            response_model=DynamicPhoneAgentSetupResult
        )

    def _validate_model_configurations(
        self,
        stt_config: Optional[DynamicSTTModelConfiguration],
        tts_config: Optional[DynamicTTSModelConfiguration]
    ) -> None:
        """Validate STT and TTS model configs against support registry."""
        has_stt = (
            stt_config
            and stt_config.provider_type
            and stt_config.provider_model_id
        )
        if has_stt:
            self._validate_model(
                stt_config.provider_type,
                stt_config.provider_model_id,
                'STT'
            )

        has_tts = (
            tts_config
            and tts_config.provider_type
            and tts_config.provider_model_id
        )
        if has_tts:
            self._validate_model(
                tts_config.provider_type,
                tts_config.provider_model_id,
                'TTS'
            )

    def _validate_model(
        self,
        provider_type: str,
        provider_model_id: str,
        model_type: str
    ) -> None:
        """Validate a single model against the support registry."""
        is_supported = self._http.get(
            f'/support-models/supports/{provider_type}/{provider_model_id}',
            response_model=bool
        )

        if not is_supported:
            msg = (
                f'Unsupported {model_type} model: '
                f'{provider_type}/{provider_model_id}. '
                f'Verify the model is available in the support registry.'
            )
            raise WiilValidationError(msg)

    def _log(self, message: str) -> None:
        """Log a message with agent context."""
        print(f'[Phone Agent] {message}')

    def _log_progress(self, state: DynamicAgentProcessingState) -> None:
        """Log progress with a visual progress bar."""
        bar = self._create_progress_bar(state.progress_percentage)
        status_msg = state.message or self._get_status_message(state.status)
        pct = state.progress_percentage
        print(f'[Phone Agent] {bar} {pct}% | {status_msg}')

    def _log_final_result(
        self,
        result: DynamicPhoneAgentSetupResult,
        start_time: float,
        silent: bool
    ) -> None:
        """Log the final result with summary."""
        if silent:
            return

        elapsed = time.time() - start_time
        duration = self._format_duration(elapsed)

        is_success = (
            result.processing_state.status == 'completed' and result.success
        )
        if is_success:
            bar = self._create_progress_bar(100)
            print(f'[Phone Agent] {bar} 100% | Setup complete')
            print(f'[Phone Agent] Ready in {duration}')
            if result.phone_number:
                print(f'  -> Phone: {result.phone_number}')
            if result.agent_configuration_id:
                print(f'  -> Agent ID: {result.agent_configuration_id}')
            if result.instruction_configuration_id:
                inst_id = result.instruction_configuration_id
                print(f'  -> Instruction ID: {inst_id}')
        else:
            print(f'[Phone Agent] Setup failed after {duration}')
            if result.error_message:
                print(f'  -> Error: {result.error_message}')

    def _create_progress_bar(self, percentage: int) -> str:
        """Create a visual progress bar."""
        total = 20
        filled = round((percentage / 100) * total)
        empty = total - filled
        return '█' * filled + '░' * empty

    def _get_status_message(self, status: str) -> str:
        """Get a human-readable status message."""
        messages = {
            'pending': 'Initializing...',
            'in_progress': 'Processing...',
            'completed': 'Setup complete',
            'failed': 'Setup failed',
        }
        return messages.get(status, status)

    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable form."""
        if seconds < 1:
            return f'{int(seconds * 1000)}ms'
        return f'{seconds:.1f}s'


__all__ = ['DynamicPhoneAgentResource', 'PhoneAgentCreateOptions']
