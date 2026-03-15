"""Knowledge-related type definitions and enumerations.

This module mirrors src/core/type-definitions/knowledge-definitions.ts
"""

from enum import Enum


class KnowledgeBaseProcessingStatus(str, Enum):
    """Knowledge base processing status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class KnowledgeTypes(str, Enum):
    """Knowledge types enumeration."""

    DOCUMENT = "document"
    URL = "url"
    BUSINESS_WEBSITE = "business_website"
    CORPUS = "corpus"
    BATCH_DOCUMENT = "batch_document"


class StorageTier(str, Enum):
    """Storage tier enumeration."""

    FIRESTORE = "firestore"
    CLOUD_STORAGE_STANDARD = "cloud_storage_standard"
    CLOUD_STORAGE_COLDLINE = "cloud_storage_coldline"


class SupportedDocumentTypes(str, Enum):
    """Supported document types enumeration."""

    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    TXT = "text/plain"
    MD = "text/markdown"
    RTF = "application/rtf"
    HTML = "text/html"
    WORD = "application/msword"
    CSV = "text/csv"
    XLS = "application/vnd.ms-excel"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
