"""Main WIIL SDK client class.

This module provides the primary entry point for the WIIL SDK, the WiilClient class.

Example:
    >>> from wiil import WiilClient
    >>> client = WiilClient(api_key='your-api-key')
    >>> org = client.organizations.get()
    >>> print(org.company_name)
"""

from urllib.parse import urlparse

from wiil.client.types import WiilClientConfig
from wiil.client.http_client import HttpClient
from wiil.errors import WiilConfigurationError

# Import all resource classes
from wiil.resources.account import OrganizationsResource, ProjectsResource
from wiil.resources.business_mgt import (
    CustomersResource,
    MenusResource,
    MenuOrdersResource,
    ProductsResource,
    ProductOrdersResource,
    ReservationsResource,
    ReservationResourcesResource,
    ServiceAppointmentsResource,
    BusinessServicesResource,
)
from wiil.resources.service_mgt import (
    AgentConfigurationsResource,
    DeploymentConfigurationsResource,
    DeploymentChannelsResource,
    InstructionConfigurationsResource,
    PhoneConfigurationsResource,
    ProvisioningConfigurationsResource,
    ConversationConfigurationsResource,
    TranslationSessionsResource,
    KnowledgeSourcesResource,
)

# Default configuration values
DEFAULT_CONFIG = {
    'base_url': 'https://api.wiil.io/v1',
    'timeout': 30,  # seconds (note: TS uses 30000 milliseconds)
}


class WiilClient:
    """Main client for interacting with the WIIL Platform API.

    This is the primary entry point for the WIIL SDK. It provides access to all
    API resources through resource-specific properties. The client handles
    authentication, request/response validation, and error handling automatically.

    Attributes:
        _http: Internal HTTP client for making requests

    Example:
        >>> from wiil import WiilClient
        >>> client = WiilClient(api_key='your-api-key')
        >>>
        >>> # Get the organization that owns the API key
        >>> org = client.organizations.get()
        >>> print('Organization:', org.company_name)
        >>>
        >>> # Create a project
        >>> project = client.projects.create(
        ...     name='Production Environment',
        ...     is_default=True
        ... )

    Example:
        >>> # Custom configuration
        >>> client = WiilClient(
        ...     api_key='your-api-key',
        ...     base_url='https://api.wiil.io/v1',
        ...     timeout=60  # 60 seconds
        ... )
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_CONFIG['base_url'],
        timeout: int = DEFAULT_CONFIG['timeout']
    ):
        """Initialize WIIL client.

        Args:
            api_key: API key for authentication. Required for all API requests.
                You can obtain an API key from your WIIL Platform dashboard.
            base_url: API base URL (default: https://api.wiil.io/v1).
                Override this if you're using a custom deployment or different environment.
            timeout: Request timeout in seconds (default: 30).
                Requests that exceed this timeout will raise a WiilNetworkError.

        Raises:
            WiilConfigurationError: If configuration is invalid

        Example:
            >>> client = WiilClient(api_key='your-api-key')

        Example:
            >>> # With custom configuration
            >>> client = WiilClient(
            ...     api_key='your-api-key',
            ...     base_url='https://api.wiil.io/v1',
            ...     timeout=60
            ... )
        """
        # Validate configuration before creating client
        self._validate_config(api_key, base_url, timeout)

        # Create configuration
        config = WiilClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout
        )

        # Initialize HTTP client
        self._http = HttpClient(config)

        # Account resources
        self.organizations = OrganizationsResource(self._http)
        self.projects = ProjectsResource(self._http)

        # Business Management resources
        self.customers = CustomersResource(self._http)
        self.menus = MenusResource(self._http)
        self.menu_orders = MenuOrdersResource(self._http)
        self.products = ProductsResource(self._http)
        self.product_orders = ProductOrdersResource(self._http)
        self.reservations = ReservationsResource(self._http)
        self.reservation_resources = ReservationResourcesResource(self._http)
        self.service_appointments = ServiceAppointmentsResource(self._http)
        self.business_services = BusinessServicesResource(self._http)

        # Service Management resources
        self.agent_configs = AgentConfigurationsResource(self._http)
        self.deployment_configs = DeploymentConfigurationsResource(self._http)
        self.deployment_channels = DeploymentChannelsResource(self._http)
        self.instruction_configs = InstructionConfigurationsResource(self._http)
        self.phone_configs = PhoneConfigurationsResource(self._http)
        self.provisioning_configs = ProvisioningConfigurationsResource(self._http)
        self.conversation_configs = ConversationConfigurationsResource(self._http)
        self.translation_sessions = TranslationSessionsResource(self._http)
        self.knowledge_sources = KnowledgeSourcesResource(self._http)

    def _validate_config(
        self,
        api_key: str,
        base_url: str,
        timeout: int
    ) -> None:
        """Validate client configuration.

        Args:
            api_key: API key to validate
            base_url: Base URL to validate
            timeout: Timeout value to validate

        Raises:
            WiilConfigurationError: If any configuration parameter is invalid

        Example:
            >>> self._validate_config('key', 'https://api.wiil.io/v1', 30)
        """
        # Validate API key
        if not api_key:
            raise WiilConfigurationError(
                'API key is required. Please provide a valid API key in the configuration.'
            )

        if not api_key.strip():
            raise WiilConfigurationError(
                'API key cannot be empty. Please provide a valid API key.'
            )

        # Validate base URL
        try:
            result = urlparse(base_url)
            if not all([result.scheme, result.netloc]):
                raise ValueError('Invalid URL structure')
        except Exception:
            raise WiilConfigurationError(
                f'Invalid base URL: {base_url}. Please provide a valid URL.'
            )

        # Validate timeout
        if timeout <= 0:
            raise WiilConfigurationError(
                'Timeout must be a positive number in seconds.'
            )


__all__ = ['WiilClient']
