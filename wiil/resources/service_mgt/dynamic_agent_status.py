"""Dynamic Agent Status resource for polling agent setup progress.

This module provides functionality for checking and polling the status of
dynamic agent setup operations. Supports both phone and web agent configurations.
"""

import time
from dataclasses import dataclass
from typing import Callable, Optional, Union

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.dynamic_setup import (
    DynamicAgentProcessingState,
    DynamicAgentSetupResult,
)
from wiil.models.service_mgt.dynamic_setup.phone_agent_setup import (
    DynamicPhoneAgentSetupResult,
)
from wiil.models.service_mgt.dynamic_setup.web_agent_setup import (
    DynamicWebAgentSetupResult,
)


@dataclass
class PollOptions:
    """Options for configuring long-polling behavior.

    Attributes:
        interval: Polling interval in milliseconds. Defaults to 5000.
        timeout: Maximum wait time in milliseconds before timing out. Defaults to 120000.
        on_progress: Callback invoked on each poll with current state.
    """

    interval: int = 5000
    timeout: int = 120000
    on_progress: Optional[Callable[[DynamicAgentProcessingState], None]] = None


class PollTimeoutError(Exception):
    """Error thrown when polling times out before completion.

    Attributes:
        last_state: The last known processing state before timeout.
    """

    def __init__(self, message: str, last_state: DynamicAgentProcessingState):
        super().__init__(message)
        self.last_state = last_state


class DynamicAgentStatusResource:
    """Resource class for polling dynamic agent setup status.

    Provides methods for checking and polling the status of dynamic agent setup
    operations. Supports both phone and web agent configurations. Use this resource
    to track long-running setup operations and wait for completion.

    Example:
        ```python
        from wiil import WiilClient
        from wiil.models.service_mgt import BusinessSupportServices

        client = WiilClient(api_key='your-api-key')

        # Create a dynamic agent (returns immediately)
        result = client.dynamic_phone_agent.create(
            DynamicPhoneAgentSetup(
                assistant_name='Support Agent',
                capabilities=[BusinessSupportServices.APPOINTMENT_MANAGEMENT],
            )
        )

        # Poll until setup completes
        def on_progress(state):
            print(f'{state.progress_percentage}% - {state.message}')

        final = client.dynamic_agent_status.poll(
            result.id,
            PollOptions(
                interval=2000,
                timeout=60000,
                on_progress=on_progress,
            )
        )

        if final.success:
            print('Agent ready:', final.agent_configuration_id)
        ```
    """

    def __init__(self, http: HttpClient):
        """Creates a new DynamicAgentStatusResource instance.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._base_path = '/dynamic-setup'

    def get(
        self, id: str
    ) -> Union[DynamicAgentSetupResult, DynamicWebAgentSetupResult, DynamicPhoneAgentSetupResult]:
        """Retrieves the current status of a dynamic agent setup operation.

        Args:
            id: Dynamic agent setup ID

        Returns:
            The setup result (base, web, or phone agent type)

        Raises:
            WiilAPIError: When the setup ID is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            ```python
            status = client.dynamic_agent_status.get('setup_123')
            print('Status:', status.processing_state.status)
            print('Progress:', status.processing_state.progress_percentage)

            # Access web agent specific properties
            if hasattr(status, 'integration_snippets') and status.integration_snippets:
                print('Snippets:', status.integration_snippets)

            # Access phone agent specific properties
            if hasattr(status, 'phone_number') and status.phone_number:
                print('Phone:', status.phone_number)
            ```
        """
        return self._http.get(
            f'{self._base_path}/{id}',
            response_model=DynamicAgentSetupResult
        )

    def poll(
        self,
        id: str,
        options: Optional[PollOptions] = None
    ) -> Union[DynamicAgentSetupResult, DynamicWebAgentSetupResult, DynamicPhoneAgentSetupResult]:
        """Polls the status of a dynamic agent setup until completion or failure.

        Args:
            id: Dynamic agent setup ID
            options: Polling configuration options

        Returns:
            The final setup result (base, web, or phone agent type)

        Raises:
            PollTimeoutError: When polling times out before completion
            WiilAPIError: When the setup ID is not found or API returns an error
            WiilNetworkError: When network communication fails

        Remarks:
            This method will continuously poll the API until the processing state
            reaches 'completed' or 'failed'. If the timeout is reached before
            completion, a PollTimeoutError is thrown containing the last known state.

        Example:
            ```python
            from wiil.resources.service_mgt import PollOptions, PollTimeoutError

            try:
                def on_progress(state):
                    print(f'Progress: {state.progress_percentage}%')

                result = client.dynamic_agent_status.poll(
                    'setup_123',
                    PollOptions(
                        interval=5000,
                        timeout=120000,
                        on_progress=on_progress,
                    )
                )

                if result.success:
                    print('Agent ID:', result.agent_configuration_id)

                    # Web agent: access integration snippets
                    if hasattr(result, 'integration_snippets') and result.integration_snippets:
                        print('Snippets:', result.integration_snippets)

                    # Phone agent: access phone number
                    if hasattr(result, 'phone_number') and result.phone_number:
                        print('Phone:', result.phone_number)

            except PollTimeoutError as e:
                print(f'Polling timed out at: {e.last_state.progress_percentage}%')
            ```
        """
        opts = options or PollOptions()
        interval = opts.interval
        timeout = opts.timeout
        on_progress = opts.on_progress

        start_time = time.time() * 1000  # Convert to milliseconds
        last_state: Optional[DynamicAgentProcessingState] = None

        while True:
            result = self.get(id)
            last_state = result.processing_state

            # Invoke progress callback if provided
            if on_progress:
                on_progress(result.processing_state)

            # Check for terminal states
            if result.processing_state.status in ('completed', 'failed'):
                return result

            # Check for timeout
            elapsed = (time.time() * 1000) - start_time
            if elapsed >= timeout:
                raise PollTimeoutError(
                    f'Polling timed out after {timeout}ms. '
                    f'Last status: {last_state.status} at {last_state.progress_percentage}%',
                    last_state
                )

            # Wait before next poll
            time.sleep(interval / 1000)  # Convert to seconds


__all__ = ['DynamicAgentStatusResource', 'PollOptions', 'PollTimeoutError']
