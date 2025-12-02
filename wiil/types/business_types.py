"""Business management type definitions and enumerations."""

from enum import Enum


class BusinessServiceType(str, Enum):
    """Business service type enumeration."""

    MENU = "menu"
    """Restaurant/food services"""

    SERVICE = "service"
    """Professional services"""

    PRODUCT = "product"
    """Retail items"""

    APPOINTMENT = "appointment"
    """Bookable services"""


class CallPriority(str, Enum):
    """Customer call priority levels."""

    HIGH = "high"
    """VIP or urgent priority"""

    MEDIUM = "medium"
    """Standard priority"""

    LOW = "low"
    """Non-urgent priority"""


class PreferredContactMethod(str, Enum):
    """Customer preferred contact method."""

    EMAIL = "email"
    """Email contact"""

    PHONE = "phone"
    """Phone contact"""

    SMS = "sms"
    """SMS/text message contact"""


class BestTimeToCall(str, Enum):
    """Best time window for phone contact."""

    MORNING = "morning"
    """Morning hours"""

    AFTERNOON = "afternoon"
    """Afternoon hours"""

    EVENING = "evening"
    """Evening hours"""

    ANYTIME = "anytime"
    """Any time is acceptable"""


class CalendarProvider(str, Enum):
    """Calendar provider enumeration."""

    GOOGLE = "google"
    """Google Calendar"""

    OUTLOOK = "outlook"
    """Microsoft Outlook"""

    CALENDLY = "calendly"
    """Calendly"""


class ResourceType(str, Enum):
    """Resource type enumeration for reservations."""

    TABLE = "table"
    """Restaurant table"""

    ROOM = "room"
    """Room (hotel, meeting, etc.)"""

    RENTALS = "rentals"
    """Rental items"""

    RESOURCE = "resource"
    """General resource"""


class ResourceReservationDurationUnit(str, Enum):
    """Duration unit for resource reservations."""

    MINUTES = "minutes"
    """Duration in minutes"""

    HOURS = "hours"
    """Duration in hours"""

    NIGHTS = "nights"
    """Duration in nights (for overnight stays)"""


class ReservationSettingType(str, Enum):
    """Reservation setting type."""

    CAPACITY = "capacity"
    """Capacity-based reservations"""

    RESOURCE_SPECIFIC = "resource_specific"
    """Resource-specific reservations"""


class AppointmentStatus(str, Enum):
    """Appointment status enumeration."""

    PENDING = "pending"
    """Appointment pending confirmation"""

    CONFIRMED = "confirmed"
    """Appointment confirmed"""

    CANCELLED = "cancelled"
    """Appointment cancelled"""

    COMPLETED = "completed"
    """Appointment completed"""

    NO_SHOW = "no_show"
    """Customer did not show up (for revenue tracking)"""


class ReservationSlotStatus(str, Enum):
    """Reservation slot status."""

    AVAILABLE = "available"
    """Slot available for booking"""

    BOOKED = "booked"
    """Slot already booked"""

    BLOCKED = "blocked"
    """Slot blocked/unavailable"""

    MAINTENANCE = "maintenance"
    """Slot under maintenance"""


class RecurrenceType(str, Enum):
    """Recurrence type for appointments and reservations."""

    NONE = "none"
    """No recurrence"""

    DAILY = "daily"
    """Daily recurrence"""

    WEEKLY = "weekly"
    """Weekly recurrence"""

    MONTHLY = "monthly"
    """Monthly recurrence"""


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    """Order pending confirmation"""

    CONFIRMED = "confirmed"
    """Order confirmed"""

    PREPARING = "preparing"
    """Order being prepared"""

    READY = "ready"
    """Order ready for pickup/delivery"""

    OUT_FOR_DELIVERY = "out_for_delivery"
    """Order out for delivery"""

    COMPLETED = "completed"
    """Order completed"""

    CANCELLED = "cancelled"
    """Order cancelled"""

    RETURNED = "returned"
    """Order returned"""


class PaymentStatus(str, Enum):
    """Payment status enumeration."""

    PENDING = "pending"
    """Payment pending"""

    PAID = "paid"
    """Payment completed"""

    PARTIAL = "partial"
    """Partial payment"""

    FAILED = "failed"
    """Payment failed"""

    REFUNDED = "refunded"
    """Payment refunded"""


class MenuOrderType(str, Enum):
    """Menu order type enumeration."""

    DINE_IN = "dine_in"
    """Dine-in order"""

    TAKEOUT = "takeout"
    """Takeout order"""

    DELIVERY = "delivery"
    """Delivery order"""


class ProductOrderType(str, Enum):
    """Product order type enumeration."""

    PICKUP = "pickup"
    """Pickup order"""

    DELIVERY = "delivery"
    """Delivery order"""

    SHIPPING = "shipping"
    """Shipping order"""


class InventoryUnit(str, Enum):
    """Inventory unit enumeration."""

    EACH = "each"
    """Single item"""

    PACK = "pack"
    """Small group/package (e.g., 6-pack)"""

    BOX = "box"
    """Boxed items"""

    CASE = "case"
    """Larger shipping case"""

    DOZEN = "dozen"
    """12 items"""

    PAIR = "pair"
    """Shoes, gloves, etc."""

    GRAM = "gram"
    """For small quantities (e.g., spices)"""

    POUNDS = "lbs"
    """Pounds"""

    KILOGRAM = "kg"
    """Kilogram"""

    MILLILITER = "ml"
    """Milliliter"""

    LITER = "l"
    """Liter"""

    METER = "m"
    """Meter"""

    CENTIMETER = "cm"
    """Centimeter"""

    ROLL = "rl"
    """Roll"""

    SET = "set"
    """Set"""

    OTHER = "other"
    """Catch-all for anything else"""


class StockAdjustmentType(str, Enum):
    """Stock adjustment type."""

    ADDITION = "addition"
    """Add to stock"""

    SUBTRACTION = "subtraction"
    """Remove from stock"""

    ADJUSTMENT = "adjustment"
    """Stock adjustment/correction"""


class StockStatus(str, Enum):
    """Stock status enumeration."""

    IN_STOCK = "in_stock"
    """In stock and available"""

    LOW_STOCK = "low_stock"
    """Low stock warning"""

    OUT_OF_STOCK = "out_of_stock"
    """Out of stock"""

    DISCONTINUED = "discontinued"
    """Product discontinued"""


class RestockStatus(str, Enum):
    """Restock status enumeration."""

    NEEDED = "needed"
    """Needs to be ordered"""

    ORDERED = "ordered"
    """Order placed with supplier"""

    RECEIVED = "received"
    """Stock received and added"""

    CANCELLED = "cancelled"
    """Restock order cancelled"""


class BusinessServiceDocumentTypes(str, Enum):
    """Business service document types."""

    CUSTOMERS = "customers"
    """Customer documents"""

    MENU_CATALOG = "menu_catalog"
    """Menu catalog documents"""

    PRODUCT_CATALOG = "product_catalog"
    """Product catalog documents"""

    SERVICE_CATALOG = "service_catalog"
    """Service catalog documents"""

    RESOURCE_CATALOG = "resource_catalog"
    """Resource catalog documents"""

    INVENTORY_CATALOG = "inventory_catalog"
    """Inventory catalog documents"""

    SUPPLIER = "suppliers"
    """Supplier documents"""


class BusinessDocumentTypes(str, Enum):
    """Business document MIME types."""

    CSV = "text/csv"
    XLS = "application/vnd.ms-excel"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    TXT = "text/plain"
    JSON = "application/json"
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    PPT = "application/vnd.ms-powerpoint"
    HTML = "text/html"
    MD = "text/markdown"
    RTF = "application/rtf"
    JPEG = "image/jpeg"
    PNG = "image/png"
