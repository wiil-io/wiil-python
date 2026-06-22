"""Service management business resource classes."""

from .appointment_additional_info import AppointmentAdditionalInfoResource
from .appointment_field_configs import AppointmentFieldConfigsResource
from .business_services import BusinessServicesResource
from .service_appointments import ServiceAppointmentsResource
from .service_categories import ServiceCategoriesResource
from .service_persons import ServicePersonsResource
from .service_pricing_rules import ServicePricingRulesResource
from .service_providers import ServiceProvidersResource
from .service_time_offs import ServiceTimeOffsResource

__all__ = [
    "AppointmentAdditionalInfoResource",
    "AppointmentFieldConfigsResource",
    "BusinessServicesResource",
    "ServiceAppointmentsResource",
    "ServiceCategoriesResource",
    "ServicePersonsResource",
    "ServicePricingRulesResource",
    "ServiceProvidersResource",
    "ServiceTimeOffsResource",
]
