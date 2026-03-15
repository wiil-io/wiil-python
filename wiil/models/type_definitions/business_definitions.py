"""Business-related type definitions and enumerations.

This module mirrors src/core/type-definitions/business-definitions.ts
"""

from enum import Enum
from typing import List, TypedDict


class BusinessServiceType(str, Enum):
    """Business service type enumeration."""

    MENU = "menu"
    """Restaurant/food."""

    SERVICE = "service"
    """Professional services."""

    PRODUCT = "product"
    """Retail items."""

    APPOINTMENT = "appointment"
    """Bookable services."""


class CalendarProvider(str, Enum):
    """Calendar provider enumeration."""

    GOOGLE = "google"
    OUTLOOK = "outlook"
    CALENDLY = "calendly"


class ResourceType(str, Enum):
    """Resource type enumeration."""

    TABLE = "table"
    ROOM = "room"
    RENTALS = "rentals"
    RESOURCE = "resource"


class ResourceReservationDurationUnit(str, Enum):
    """Resource reservation duration unit enumeration."""

    MINUTES = "minutes"
    HOURS = "hours"
    NIGHTS = "nights"


class ReservationSettingType(str, Enum):
    """Reservation setting type enumeration."""

    CAPACITY = "capacity"
    RESOURCE_SPECIFIC = "resource_specific"


class AppointmentStatus(str, Enum):
    """Appointment status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    """For revenue tracking."""


class ReservationSlotStatus(str, Enum):
    """Reservation slot status enumeration."""

    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"
    MAINTENANCE = "maintenance"


class RecurrenceType(str, Enum):
    """Recurrence type enumeration."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""

    PENDING = "pending"
    PAID = "paid"
    PARTIAL = "partial"
    FAILED = "failed"
    REFUNDED = "refunded"


class MenuOrderType(str, Enum):
    """Menu order type enumeration."""

    DINE_IN = "dine_in"
    TAKEOUT = "takeout"
    DELIVERY = "delivery"


class ProductOrderType(str, Enum):
    """Product order type enumeration."""

    PICKUP = "pickup"
    DELIVERY = "delivery"
    SHIPPING = "shipping"


class InventoryUnit(str, Enum):
    """Inventory unit enumeration."""

    EACH = "each"
    """Single item."""

    PACK = "pack"
    """Small group/package (e.g., 6-pack)."""

    BOX = "box"
    """Boxed items."""

    CASE = "case"
    """Larger shipping case."""

    DOZEN = "dozen"
    """12 items."""

    PAIR = "pair"
    """Shoes, gloves, etc."""

    GRAM = "gram"
    """For small quantities (e.g., spices)."""

    POUNDS = "lbs"
    """Pounds."""

    KILOGRAM = "kg"
    """Kilogram."""

    MILLILITER = "ml"
    """Milliliter."""

    LITER = "l"
    """Liter."""

    METER = "m"
    """Meter."""

    CENTIMETER = "cm"
    """Centimeter."""

    ROLL = "rl"
    """Roll."""

    SET = "set"
    """Set."""

    OTHER = "other"
    """Catch-all for anything else."""


class StockAdjustmentType(str, Enum):
    """Stock adjustment type enumeration."""

    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    ADJUSTMENT = "adjustment"


class StockStatus(str, Enum):
    """Stock status enumeration."""

    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class RestockStatus(str, Enum):
    """Restock status enumeration."""

    NEEDED = "needed"
    """Needs to be ordered."""

    ORDERED = "ordered"
    """Order placed with supplier."""

    RECEIVED = "received"
    """Stock received and added."""

    CANCELLED = "cancelled"
    """Restock order cancelled."""


class BusinessServiceDocumentTypes(str, Enum):
    """Business service document types enumeration."""

    CUSTOMERS = "customers"
    MENU_CATALOG = "menu_catalog"
    PRODUCT_CATALOG = "product_catalog"
    SERVICE_CATALOG = "service_catalog"
    RESOURCE_CATALOG = "resource_catalog"
    INVENTORY_CATALOG = "inventory_catalog"
    SUPPLIER = "suppliers"


class BusinessDocumentTypes(str, Enum):
    """Business document types enumeration."""

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


class DayOfWeek(TypedDict):
    """Day of week type definition."""

    id: int
    name: str
    short: str


DAYS_OF_WEEK: List[DayOfWeek] = [
    {"id": 0, "name": "Sunday", "short": "Sun"},
    {"id": 1, "name": "Monday", "short": "Mon"},
    {"id": 2, "name": "Tuesday", "short": "Tue"},
    {"id": 3, "name": "Wednesday", "short": "Wed"},
    {"id": 4, "name": "Thursday", "short": "Thu"},
    {"id": 5, "name": "Friday", "short": "Fri"},
    {"id": 6, "name": "Saturday", "short": "Sat"},
]

TIMEZONES: List[str] = [
    "UTC",
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Paris",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Australia/Sydney",
]


class CallPriority(str, Enum):
    """Call priority enumeration."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PreferredContactMethod(str, Enum):
    """Preferred contact method enumeration."""

    EMAIL = "email"
    PHONE = "phone"
    SMS = "sms"


class BestTimeToCall(str, Enum):
    """Best time to call enumeration."""

    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    ANYTIME = "anytime"


class PropertyType(str, Enum):
    """Property type enumeration."""

    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    LAND = "land"


class PropertySubType(str, Enum):
    """Property sub-type enumeration."""

    # Residential
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    VILLA = "villa"
    # Commercial
    OFFICE = "office"
    RETAIL = "retail"
    WAREHOUSE = "warehouse"
    INDUSTRIAL = "industrial"
    # Land
    LOT = "lot"
    FARM = "farm"
    ACREAGE = "acreage"


class ListingType(str, Enum):
    """Listing type enumeration."""

    SALE = "sale"
    RENT = "rent"
    BOTH = "both"


class ListingStatus(str, Enum):
    """Listing status enumeration."""

    DRAFT = "draft"
    ACTIVE = "active"
    UNDER_OFFER = "under_offer"
    SOLD = "sold"
    LEASED = "leased"
    WITHDRAWN = "withdrawn"


class PropertyCondition(str, Enum):
    """Property condition enumeration."""

    NEW = "new"
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_WORK = "needs_work"


class RentalPeriod(str, Enum):
    """Rental period enumeration."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PropertyPurchaseStatus(str, Enum):
    """Property purchase status enumeration."""

    INQUIRY = "inquiry"
    OFFER_MADE = "offer_made"
    UNDER_CONTRACT = "under_contract"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PropertyLeaseStatus(str, Enum):
    """Property lease status enumeration."""

    PENDING = "pending"
    ACTIVE = "active"
    RENEWED = "renewed"
    TERMINATED = "terminated"
    EXPIRED = "expired"


class DepositStatus(str, Enum):
    """Deposit status enumeration."""

    PENDING = "pending"
    PAID = "paid"
    RETURNED = "returned"
    FORFEITED = "forfeited"


class PropertyInquiryType(str, Enum):
    """Property inquiry type enumeration."""

    OFFER = "offer"
    GENERAL = "general"


class PropertyInquiryStatus(str, Enum):
    """Property inquiry status enumeration."""

    NEW = "new"
    CONTACTED = "contacted"
    VIEWING_SCHEDULED = "viewing_scheduled"
    FOLLOW_UP = "follow_up"
    CONVERTED = "converted"
    CLOSED = "closed"
