"""Business Management Pydantic models.

This module contains all business management models including customers, orders,
reservations, appointments, and service configurations.
"""

# Customer models
from wiil.models.business_mgt.customer import (
    CreateCustomer,
    Customer,
    UpdateCustomer,
)

# Menu configuration models
from wiil.models.business_mgt.menu_config import (
    BusinessMenuItem,
    CreateBusinessMenuItem,
    CreateMenuCategory,
    MenuCategory,
    MenuQRCode,
    NutritionalInfo,
    UpdateBusinessMenuItem,
    UpdateMenuCategory,
)

# Menu order models
from wiil.models.business_mgt.menu_order import (
    CreateMenuOrder,
    DeliveryAddress,
    MenuItemCustomization,
    MenuOrder,
    MenuOrderItem,
    MenuOrderItemBase,
    UpdateMenuOrder,
    UpdateMenuOrderStatus,
)

# Order shared models
from wiil.models.business_mgt.order import (
    OrderAddress,
    OrderCustomer,
    OrderPricing,
)

# Product configuration models
from wiil.models.business_mgt.product_config import (
    BusinessProduct,
    CreateBusinessProduct,
    CreateProductCategory,
    ProductCategory,
    ProductDimensions,
    UpdateBusinessProduct,
    UpdateProductCategory,
)

# Product order models
from wiil.models.business_mgt.product_order import (
    CreateProductOrder,
    InventoryAdjustment,
    OrderInventoryUpdate,
    ProductOrder,
    ProductOrderItem,
    ProductOrderItemBase,
    UpdateProductOrder,
    UpdateProductOrderStatus,
)

# Reservation models
from wiil.models.business_mgt.reservation import (
    CreateReservation,
    CreateReservationSettings,
    Reservation,
    ReservationSettings,
    UpdateReservation,
    UpdateReservationSettings,
)

# Reservation resource models
from wiil.models.business_mgt.reservation_resource import (
    CreateResource,
    RentalResource,
    Resource,
    RoomResource,
    UpdateResource,
)

# Service appointment models
from wiil.models.business_mgt.service_appointment import (
    CreateServiceAppointment,
    ServiceAppointment,
    UpdateServiceAppointment,
)

# Service configuration models
from wiil.models.business_mgt.service_config import (
    BusinessServiceConfig,
    CreateBusinessService,
    ServiceQRCode,
    UpdateBusinessService,
)

# Service person models
from wiil.models.business_mgt.service_person import (
    CreateServicePerson,
    ServicePerson,
    UpdateServicePerson,
)

__all__ = [
    # Customer models
    "Customer",
    "CreateCustomer",
    "UpdateCustomer",
    # Menu configuration models
    "MenuCategory",
    "CreateMenuCategory",
    "UpdateMenuCategory",
    "BusinessMenuItem",
    "CreateBusinessMenuItem",
    "UpdateBusinessMenuItem",
    "MenuQRCode",
    "NutritionalInfo",
    # Menu order models
    "MenuOrder",
    "MenuOrderItem",
    "MenuOrderItemBase",
    "MenuItemCustomization",
    "DeliveryAddress",
    "CreateMenuOrder",
    "UpdateMenuOrder",
    "UpdateMenuOrderStatus",
    # Order shared models
    "OrderAddress",
    "OrderCustomer",
    "OrderPricing",
    # Product configuration models
    "ProductCategory",
    "CreateProductCategory",
    "UpdateProductCategory",
    "BusinessProduct",
    "CreateBusinessProduct",
    "UpdateBusinessProduct",
    "ProductDimensions",
    # Product order models
    "ProductOrder",
    "ProductOrderItem",
    "ProductOrderItemBase",
    "CreateProductOrder",
    "UpdateProductOrder",
    "UpdateProductOrderStatus",
    "InventoryAdjustment",
    "OrderInventoryUpdate",
    # Reservation models
    "ReservationSettings",
    "CreateReservationSettings",
    "UpdateReservationSettings",
    "Reservation",
    "CreateReservation",
    "UpdateReservation",
    # Reservation resource models
    "Resource",
    "CreateResource",
    "UpdateResource",
    "RoomResource",
    "RentalResource",
    # Service appointment models
    "ServiceAppointment",
    "CreateServiceAppointment",
    "UpdateServiceAppointment",
    # Service configuration models
    "BusinessServiceConfig",
    "CreateBusinessService",
    "UpdateBusinessService",
    "ServiceQRCode",
    # Service person models
    "ServicePerson",
    "CreateServicePerson",
    "UpdateServicePerson",
]
