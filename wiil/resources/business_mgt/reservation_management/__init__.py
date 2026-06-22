"""Reservation management business resource classes."""

from .floor_plan_sections import FloorPlanSectionsResource
from .floor_plans import FloorPlansResource
from .maintenance_blocks import MaintenanceBlocksResource
from .rental_assignments import RentalAssignmentsResource
from .rental_reservations import RentalReservationsResource
from .reservation_resources import ReservationResourcesResource
from .reservation_settings import ReservationSettingsResource
from .resource_categories import ResourceCategoriesResource
from .resource_instances import ResourceInstancesResource
from .room_assignments import RoomAssignmentsResource
from .room_reservations import RoomReservationsResource
from .table_assignments import TableAssignmentsResource
from .table_reservations import TableReservationsResource

__all__ = [
    # Reservations
    "TableReservationsResource",
    "RoomReservationsResource",
    "RentalReservationsResource",
    # Settings
    "ReservationSettingsResource",
    # Floor Plans & Sections
    "FloorPlansResource",
    "FloorPlanSectionsResource",
    # Resources
    "ReservationResourcesResource",
    "ResourceCategoriesResource",
    "ResourceInstancesResource",
    # Maintenance
    "MaintenanceBlocksResource",
    # Assignments
    "TableAssignmentsResource",
    "RoomAssignmentsResource",
    "RentalAssignmentsResource",
]
