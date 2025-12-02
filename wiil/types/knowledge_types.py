"""Knowledge base type definitions and enumerations."""

from enum import Enum


class KnowledgeBaseProcessingStatus(str, Enum):
    """Knowledge base processing status enumeration."""

    PENDING = "pending"
    """Processing pending"""

    PROCESSING = "processing"
    """Currently processing"""

    COMPLETED = "completed"
    """Processing completed"""

    FAILED = "failed"
    """Processing failed"""


class KnowledgeTypes(str, Enum):
    """Knowledge source type enumeration."""

    DOCUMENT = "document"
    """Single document"""

    URL = "url"
    """URL source"""

    BUSINESS_WEBSITE = "business_website"
    """Business website"""

    CORPUS = "corpus"
    """Document corpus"""

    BATCH_DOCUMENT = "batch_document"
    """Batch of documents"""


class StorageTier(str, Enum):
    """Storage tier enumeration."""

    FIRESTORE = "firestore"
    """Firestore storage"""

    CLOUD_STORAGE_STANDARD = "cloud_storage_standard"
    """Cloud storage standard tier"""

    CLOUD_STORAGE_COLDLINE = "cloud_storage_coldline"
    """Cloud storage coldline tier"""


class SupportedDocumentTypes(str, Enum):
    """Supported document MIME types for knowledge base."""

    PDF = "application/pdf"
    """PDF document"""

    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    """Microsoft Word (DOCX)"""

    TXT = "text/plain"
    """Plain text"""

    MD = "text/markdown"
    """Markdown"""

    RTF = "application/rtf"
    """Rich Text Format"""

    HTML = "text/html"
    """HTML"""

    WORD = "application/msword"
    """Microsoft Word (DOC)"""

    CSV = "text/csv"
    """CSV"""

    XLS = "application/vnd.ms-excel"
    """Microsoft Excel (XLS)"""

    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    """Microsoft Excel (XLSX)"""
