"""Account-related type definitions and enumerations.

This module contains enumerations for account management including
service status tracking and business support services.
"""

from enum import Enum


class ServiceStatus(str, Enum):
    """Service status enumeration for organizations and projects.

    Defines the operational state of a service within the platform.

    Example:
        ```python
        org_status = ServiceStatus.ACTIVE
        ```
    """

    ACTIVE = "active"
    """Service is operational and available"""

    INACTIVE = "inactive"
    """Service is not currently in use but can be reactivated"""

    SUSPENDED = "suspended"
    """Service is temporarily suspended and requires intervention to resume"""


class ServiceSuspensionType(str, Enum):
    """Service suspension type enumeration.

    Indicates the reason or trigger for a service suspension.

    Example:
        ```python
        suspension_reason = ServiceSuspensionType.QUOTA_EXCEEDED
        ```
    """

    MANUAL = "manual"
    """Service was manually suspended by an administrator or user"""

    AUTOMATIC = "automatic"
    """Service was automatically suspended by the system"""

    SUBSCRIPTION_QUOTA_EXCEEDED = "subscription_quota_exceeded"
    """Service was suspended due to subscription quota limits being exceeded"""

    QUOTA_EXCEEDED = "quota_exceeded"
    """Service was suspended due to usage quota limits being exceeded"""

    PAYMENT_FAILED = "payment_failed"
    """Service was suspended due to failed payment transaction"""


class BusinessSupportServices(str, Enum):
    """Business support services enumeration.

    Defines the types of business support services available in the platform
    for organizations to enable specific industry-focused features.

    Example:
        ```python
        enabled_services = [
            BusinessSupportServices.APPOINTMENT_MANAGEMENT,
            BusinessSupportServices.INVENTORY_MANAGEMENT
        ]
        ```
    """

    APPOINTMENT_MANAGEMENT = "appointment_management"
    """Appointment scheduling and management functionality"""

    INVENTORY_MANAGEMENT = "inventory_management"
    """Inventory tracking and stock management functionality"""

    MENU_ORDER_MANAGEMENT = "menu_order_management"
    """Restaurant menu and food order management functionality"""

    PRODUCT_ORDER_MANAGEMENT = "product_order_management"
    """E-commerce product order management functionality"""

    RESERVATION_MANAGEMENT = "reservation_management"
    """Table and venue reservation management functionality"""

    NONE = "none"
    """No business support services enabled"""
