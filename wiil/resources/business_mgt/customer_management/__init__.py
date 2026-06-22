"""Customer management business resource classes."""

from .customer_groups import CustomerGroupsResource
from .customers import CustomersResource
from .shipping_addresses import ShippingAddressesResource

__all__ = [
    "CustomersResource",
    "CustomerGroupsResource",
    "ShippingAddressesResource",
]
