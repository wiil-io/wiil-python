"""Type definitions and enumerations for WIIL Platform.

This module contains all type definitions organized by domain:
- account_types: Account-related enumerations
- business_types: Business management enumerations
- service_types: Service configuration enumerations
- conversation_types: Conversation and messaging enumerations
- knowledge_types: Knowledge base enumerations
- paginated_result: Pagination models for API responses
- paginated_quest: Timestamp-based query models
"""

from wiil.types.account_types import (
    BusinessSupportServices,
    ServiceStatus,
    ServiceSuspensionType,
)
from wiil.types.paginated_result import (
    PaginatedResult,
    PaginationMeta,
    PaginatedAccountRequest,
    PaginationRequest,
    SearchablePaginationRequest,
)
from wiil.types.paginated_quest import (
    TimestampQuery,
    AccountPaginatedTimestampQuery,
)
from wiil.types.business_types import (
    AppointmentStatus,
    BestTimeToCall,
    BusinessDocumentTypes,
    BusinessServiceDocumentTypes,
    BusinessServiceType,
    CalendarProvider,
    CallPriority,
    DAYS_OF_WEEK,
    DepositStatus,
    InventoryUnit,
    ListingStatus,
    ListingType,
    MenuOrderType,
    OrderStatus,
    PaymentStatus,
    PreferredContactMethod,
    PropertyCondition,
    PropertyInquiryStatus,
    PropertyInquiryType,
    PropertyLeaseStatus,
    PropertyPurchaseStatus,
    PropertySubType,
    PropertyType,
    ProductOrderType,
    RecurrenceType,
    RentalPeriod,
    ReservationSettingType,
    ReservationSlotStatus,
    ResourceReservationDurationUnit,
    ResourceType,
    RestockStatus,
    StockAdjustmentType,
    StockStatus,
    TIMEZONES,
)
from wiil.types.conversation_types import (
    ConversationDirection,
    ConversationEventType,
    ConversationStatus,
    ConversationSummarySentiment,
    MessageType,
    ServiceConversationType,
    TranslationDirection,
)
from wiil.types.knowledge_types import (
    KnowledgeBaseProcessingStatus,
    KnowledgeTypes,
    StorageTier,
    SupportedDocumentTypes,
)
from wiil.types.service_types import (
    AssistantType,
    DeploymentProvisioningType,
    DeploymentStatus,
    DeploymentType,
    LLMRequestType,
    LLMType,
    MobilePlatform,
    ModelProprietor,
    OttCommunicationType,
    PhoneNumberType,
    PhonePurchaseStatus,
    PhoneStatus,
    ProviderType,
    SupportedLLMKit,
    SupportedProprietor,
)

__all__ = [
    # Account types
    "BusinessSupportServices",
    "ServiceStatus",
    "ServiceSuspensionType",
    # Business types
    "AppointmentStatus",
    "BestTimeToCall",
    "BusinessDocumentTypes",
    "BusinessServiceDocumentTypes",
    "BusinessServiceType",
    "CalendarProvider",
    "CallPriority",
    "DAYS_OF_WEEK",
    "DepositStatus",
    "InventoryUnit",
    "ListingStatus",
    "ListingType",
    "MenuOrderType",
    "OrderStatus",
    "PaymentStatus",
    "PreferredContactMethod",
    "PropertyCondition",
    "PropertyInquiryStatus",
    "PropertyInquiryType",
    "PropertyLeaseStatus",
    "PropertyPurchaseStatus",
    "PropertySubType",
    "PropertyType",
    "ProductOrderType",
    "RecurrenceType",
    "RentalPeriod",
    "ReservationSettingType",
    "ReservationSlotStatus",
    "ResourceReservationDurationUnit",
    "ResourceType",
    "RestockStatus",
    "StockAdjustmentType",
    "StockStatus",
    "TIMEZONES",
    # Service types
    "AssistantType",
    "DeploymentProvisioningType",
    "DeploymentStatus",
    "DeploymentType",
    "LLMRequestType",
    "LLMType",
    "MobilePlatform",
    "ModelProprietor",
    "OttCommunicationType",
    "PhoneNumberType",
    "PhonePurchaseStatus",
    "PhoneStatus",
    "ProviderType",
    "SupportedLLMKit",
    "SupportedProprietor",
    # Conversation types
    "ConversationDirection",
    "ConversationEventType",
    "ConversationStatus",
    "ConversationSummarySentiment",
    "MessageType",
    "ServiceConversationType",
    "TranslationDirection",
    # Knowledge types
    "KnowledgeBaseProcessingStatus",
    "KnowledgeTypes",
    "StorageTier",
    "SupportedDocumentTypes",
    # Pagination types
    "PaginatedResult",
    "PaginationMeta",
    "PaginatedAccountRequest",
    "PaginationRequest",
    "SearchablePaginationRequest",
    # Timestamp query types
    "TimestampQuery",
    "AccountPaginatedTimestampQuery",
]
