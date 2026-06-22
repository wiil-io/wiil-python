"""Central export point for customer management schemas."""

from wiil.models.business_mgt.customer_management.customer import (
    CreateCustomer,
    Customer,
    CustomerFilters,
    CustomerQueryOptions,
    CustomerSorting,
    UpdateCustomer,
)
from wiil.models.business_mgt.customer_management.customer_group import (
    CreateCustomerGroup,
    CustomerGroup,
    CustomerGroupFilters,
    CustomerGroupQueryOptions,
    CustomerGroupSorting,
    UpdateCustomerGroup,
)
from wiil.models.business_mgt.customer_management.shipping_address import (
    CreateShippingAddress,
    ShippingAddress,
    ShippingAddressFilters,
    ShippingAddressQueryOptions,
    ShippingAddressSorting,
    UpdateShippingAddress,
)

__all__ = [
    "Customer",
    "CreateCustomer",
    "UpdateCustomer",
    "CustomerFilters",
    "CustomerSorting",
    "CustomerQueryOptions",
    "CustomerGroup",
    "CreateCustomerGroup",
    "UpdateCustomerGroup",
    "CustomerGroupFilters",
    "CustomerGroupSorting",
    "CustomerGroupQueryOptions",
    "ShippingAddress",
    "CreateShippingAddress",
    "UpdateShippingAddress",
    "ShippingAddressFilters",
    "ShippingAddressSorting",
    "ShippingAddressQueryOptions",
]
