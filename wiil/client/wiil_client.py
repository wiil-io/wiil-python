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
    AppointmentAdditionalInfoResource,
    AppointmentFieldConfigsResource,
    BusinessLocationsResource,
    CustomerGroupsResource,
    CustomersResource,
    DiscountRulesResource,
    FloorPlansResource,
    FloorPlanSectionsResource,
    MaintenanceBlocksResource,
    MenuItemVariantsResource,
    MenusResource,
    MenuOrdersResource,
    MenuPricingRulesResource,
    MenuSetsResource,
    ModifiersResource,
    ProductAxisBindingsResource,
    ProductsResource,
    ProductOrdersResource,
    ProductPricingRulesResource,
    ProductSetsResource,
    ProductVariantAxesResource,
    ProductVariantsResource,
    PropertyConfigResource,
    PropertyInquiryResource,
    RentalAssignmentsResource,
    RentalReservationsResource,
    ReservationResourcesResource,
    ReservationSettingsResource,
    ResourceCategoriesResource,
    ResourceInstancesResource,
    RoomAssignmentsResource,
    RoomReservationsResource,
    BusinessServicesResource,
    ServiceAppointmentsResource,
    ServiceCategoriesResource,
    ServicePersonsResource,
    ServicePricingRulesResource,
    ServiceProvidersResource,
    ServiceTimeOffsResource,
    ShippingAddressesResource,
    TableAssignmentsResource,
    TableReservationsResource,
    TaxRulesResource,
)
from wiil.resources.conversation import (
    OutboundCallsResource,
    OutboundEmailsResource,
    OutboundSmsResource,
    OutboundTemplatesResource,
)
from wiil.resources.service_mgt import (
    AgentConfigurationsResource,
    DynamicAgentStatusResource,
    DynamicPhoneAgentResource,
    DynamicWebAgentResource,
    DeploymentConfigurationsResource,
    DeploymentChannelsResource,
    InstructionConfigurationsResource,
    PhoneConfigurationsResource,
    ProvisioningConfigurationsResource,
    ConversationConfigurationsResource,
    KnowledgeSourcesResource,
    SupportModelsResource,
    TelephonyProviderResource,
)
from wiil.services import OttService

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
        self.customer_groups = CustomerGroupsResource(self._http)
        self.shipping_addresses = ShippingAddressesResource(self._http)
        self.menus = MenusResource(self._http)
        self.menu_orders = MenuOrdersResource(self._http)
        self.menu_item_variants = MenuItemVariantsResource(self._http)
        self.menu_pricing_rules = MenuPricingRulesResource(self._http)
        self.menu_sets = MenuSetsResource(self._http)
        self.modifiers = ModifiersResource(self._http)
        self.products = ProductsResource(self._http)
        self.product_orders = ProductOrdersResource(self._http)
        self.product_variants = ProductVariantsResource(self._http)
        self.product_variant_axes = ProductVariantAxesResource(self._http)
        self.product_axis_bindings = ProductAxisBindingsResource(self._http)
        self.product_sets = ProductSetsResource(self._http)
        self.product_pricing_rules = ProductPricingRulesResource(self._http)
        self.discount_rules = DiscountRulesResource(self._http)
        self.tax_rules = TaxRulesResource(self._http)
        self.property_config = PropertyConfigResource(self._http)
        self.property_inquiry = PropertyInquiryResource(self._http)
        self.business_locations = BusinessLocationsResource(self._http)
        self.reservation_resources = ReservationResourcesResource(self._http)
        self.reservation_settings = ReservationSettingsResource(self._http)
        self.resource_categories = ResourceCategoriesResource(self._http)
        self.resource_instances = ResourceInstancesResource(self._http)
        self.floor_plans = FloorPlansResource(self._http)
        self.floor_plan_sections = FloorPlanSectionsResource(self._http)
        self.maintenance_blocks = MaintenanceBlocksResource(self._http)
        self.table_assignments = TableAssignmentsResource(self._http)
        self.room_assignments = RoomAssignmentsResource(self._http)
        self.rental_assignments = RentalAssignmentsResource(self._http)
        self.table_reservations = TableReservationsResource(self._http)
        self.room_reservations = RoomReservationsResource(self._http)
        self.rental_reservations = RentalReservationsResource(self._http)
        self.service_appointments = ServiceAppointmentsResource(self._http)
        self.appointment_additional_info = AppointmentAdditionalInfoResource(self._http)
        self.appointment_field_configs = AppointmentFieldConfigsResource(self._http)
        self.business_services = BusinessServicesResource(self._http)
        self.service_categories = ServiceCategoriesResource(self._http)
        self.service_persons = ServicePersonsResource(self._http)
        self.service_pricing_rules = ServicePricingRulesResource(self._http)
        self.service_providers = ServiceProvidersResource(self._http)
        self.service_time_offs = ServiceTimeOffsResource(self._http)

        # Service Management resources
        self.agent_configs = AgentConfigurationsResource(self._http)
        self.deployment_configs = DeploymentConfigurationsResource(self._http)
        self.deployment_channels = DeploymentChannelsResource(self._http)
        self.instruction_configs = InstructionConfigurationsResource(self._http)
        self.phone_configs = PhoneConfigurationsResource(self._http)
        self.provisioning_configs = ProvisioningConfigurationsResource(self._http)
        self.conversation_configs = ConversationConfigurationsResource(self._http)
        self.knowledge_sources = KnowledgeSourcesResource(self._http)
        self.support_models = SupportModelsResource(self._http)
        self.telephony_provider = TelephonyProviderResource(self._http)
        self.dynamic_phone_agent = DynamicPhoneAgentResource(self._http)
        self.dynamic_web_agent = DynamicWebAgentResource(self._http)
        self.dynamic_agent_status = DynamicAgentStatusResource(self._http)

        # Conversation resources
        self.outbound_calls = OutboundCallsResource(self._http)
        self.outbound_emails = OutboundEmailsResource(self._http)
        self.outbound_sms = OutboundSmsResource(self._http)
        self.outbound_templates = OutboundTemplatesResource(self._http)

        # Service layer helpers
        self.ott = OttService(self._http)

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
