"""Business Management resource classes for managing business operations."""

from wiil.resources.business_mgt.customers import CustomersResource
from wiil.resources.business_mgt.menus import MenusResource
from wiil.resources.business_mgt.menu_orders import MenuOrdersResource
from wiil.resources.business_mgt.products import ProductsResource
from wiil.resources.business_mgt.product_orders import ProductOrdersResource
from wiil.resources.business_mgt.reservations import ReservationsResource
from wiil.resources.business_mgt.reservation_resources import ReservationResourcesResource
from wiil.resources.business_mgt.service_appointments import ServiceAppointmentsResource
from wiil.resources.business_mgt.business_services import BusinessServicesResource

__all__ = [
    'CustomersResource',
    'MenusResource',
    'MenuOrdersResource',
    'ProductsResource',
    'ProductOrdersResource',
    'ReservationsResource',
    'ReservationResourcesResource',
    'ServiceAppointmentsResource',
    'BusinessServicesResource',
]
