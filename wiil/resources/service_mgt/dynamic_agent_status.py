"""Dynamic Agent Status resource for checking agent setup status."""

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.dynamic_setup import (
    DynamicAgentSetupResult,
)


class DynamicAgentStatusResource:
    """Resource class for checking dynamic agent setup status.

    Provides methods for retrieving the processing status of dynamic agent
    setup operations. Used to poll for completion of async setup processes.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/dynamic-agent-status'

    def get(self, setup_id: str) -> DynamicAgentSetupResult:
        """Retrieve the status of a dynamic agent setup operation.

        Args:
            setup_id: The setup operation ID

        Returns:
            The current status of the agent setup operation
        """
        return self._http.get(f'{self._base_path}/{setup_id}')


__all__ = ['DynamicAgentStatusResource']
