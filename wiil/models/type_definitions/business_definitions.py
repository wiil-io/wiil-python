"""Business-related type definitions and enumerations.

This module mirrors src/core/type-definitions/business-definitions.ts
"""

import re
from enum import Enum
from typing import Dict, List, Optional, TypedDict

from pydantic import Field

from wiil.models.base import BaseModel


class ExternalRef(BaseModel):
    """External system reference for imported/synced records."""

    external_id: str = Field(..., alias="externalId")
    source: str
    url: Optional[str] = None
    synced_at: Optional[int] = Field(None, alias="syncedAt")


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
    RENTAL = "rental"
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


class ReservationStatus(str, Enum):
    """Reservation lifecycle status."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    SEATED = "seated"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentStatus(str, Enum):
    """Appointment status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    """For revenue tracking."""


class ServiceProviderTimeOffType(str, Enum):
    """Service provider time-off block type."""

    SPECIFIC = "specific"
    RECURRING = "recurring"


class ServiceProviderTimeOffStatus(str, Enum):
    """Service provider time-off approval status."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


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


class PricingChannel(str, Enum):
    """Pricing channel enumeration for pricing rules."""

    ALL = "ALL"
    DIRECT = "DIRECT"
    ONLINE = "ONLINE"
    PHONE = "PHONE"
    WALK_IN = "WALK_IN"


class MenuPricingChannel(str, Enum):
    """Menu-pricing channel enumeration for menu pricing rules."""

    ALL = "all"
    DINE_IN = "dine_in"
    TAKEOUT = "takeout"
    DELIVERY = "delivery"
    ONLINE = "online"


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
    DOCX = (
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    )
    PPTX = (
        "application/vnd.openxmlformats-officedocument."
        "presentationml.presentation"
    )
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


class TimeSlot(TypedDict):
    """Shared time slot schema with HH:MM 24-hour strings."""

    start: str
    end: str


BreakTime = TimeSlot


class SimpleDaySchedule(TypedDict):
    """Simple day schedule without breaks."""

    isOpen: bool
    startTime: str
    endTime: str


class DaySchedule(SimpleDaySchedule, total=False):
    """Day schedule with optional break periods."""

    breakTimes: List[BreakTime]


SimpleWeeklySchedule = Dict[str, SimpleDaySchedule]
WeeklySchedule = Dict[str, DaySchedule]


def _validate_time_hhmm(value: str) -> bool:
    """Validate HH:MM time string."""
    return re.fullmatch(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", value) is not None


def validate_time_slot(slot: TimeSlot) -> None:
    """Validate a time slot shape and time format."""
    if not _validate_time_hhmm(slot["start"]):
        raise ValueError("Invalid time format (HH:MM)")
    if not _validate_time_hhmm(slot["end"]):
        raise ValueError("Invalid time format (HH:MM)")


def validate_simple_day_schedule(schedule: SimpleDaySchedule) -> None:
    """Validate simple day schedule time fields."""
    if not _validate_time_hhmm(schedule["startTime"]):
        raise ValueError("Invalid time format (HH:MM)")
    if not _validate_time_hhmm(schedule["endTime"]):
        raise ValueError("Invalid time format (HH:MM)")


def validate_simple_weekly_schedule(schedule: SimpleWeeklySchedule) -> None:
    """Validate weekly schedule keys are day indexes and values are valid."""
    for day, day_schedule in schedule.items():
        if re.fullmatch(r"^[0-6]$", day) is None:
            raise ValueError("Day must be 0-6")
        validate_simple_day_schedule(day_schedule)


def validate_weekly_schedule(schedule: WeeklySchedule) -> None:
    """Validate weekly schedule including break periods."""
    for day, day_schedule in schedule.items():
        if re.fullmatch(r"^[0-6]$", day) is None:
            raise ValueError("Day must be 0-6")
        validate_simple_day_schedule(day_schedule)
        for break_time in day_schedule.get("breakTimes", []):
            validate_time_slot(break_time)


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


class TaxScope(str, Enum):
    """Tax rule scope."""

    ORDER = "ORDER"
    ITEM = "ITEM"
    SERVICE = "SERVICE"
    DELIVERY = "DELIVERY"


class TaxRateType(str, Enum):
    """Tax rate type."""

    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"


class TaxCatalogScope(str, Enum):
    """Tax catalog scope."""

    ALL = "ALL"
    MENU = "MENU"
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    SET = "SET"


class DiscountScope(str, Enum):
    """Discount rule scope."""

    ORDER = "ORDER"
    ITEM = "ITEM"
    SHIPPING = "SHIPPING"
    SET = "SET"


class DiscountType(str, Enum):
    """Discount type."""

    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"


class DiscountCatalogScope(str, Enum):
    """Discount catalog scope."""

    ALL = "ALL"
    MENU = "MENU"
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    SET = "SET"


class PricingRuleApplyLevel(str, Enum):
    """Pricing rule application level."""

    ITEM = "ITEM"
    ORDER = "ORDER"


class PricingRuleAdjustmentType(str, Enum):
    """Pricing rule adjustment type."""

    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"
    OVERRIDE = "OVERRIDE"


class VariantAxisType(str, Enum):
    """Variant axis display/input type."""

    SWATCH = "swatch"
    TEXT = "text"
    IMAGE = "image"
    NUMERIC = "numeric"
