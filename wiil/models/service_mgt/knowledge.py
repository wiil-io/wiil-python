"""Knowledge source schema definitions for managing AI knowledge bases.

Knowledge Sources provide contextual information, documentation, and domain knowledge that
Instruction Configurations can reference to enhance agent capabilities. They support multiple
content types and intelligent storage tier management for cost optimization.
"""

from typing import Any, Dict, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.models.type_definitions import (
    KnowledgeBaseProcessingStatus,
    KnowledgeTypes,
    StorageTier,
)


class KnowledgeSource(BaseModel):
    """Knowledge source for AI agent context.

    Knowledge Sources provide contextual information and domain knowledge for AI agents. They are
    referenced by Instruction Configurations (1:N relationship) to give agents access to specific
    information, documentation, or business knowledge needed for their tasks.

    Architecture Context:
        - Relationship: Referenced by Instruction Configurations via knowledgeSourceIds (1:N)
        - Purpose: Provides domain knowledge, documentation, and context for agent responses
        - Storage Strategy: Multi-tier storage (Firestore, Cloud Storage) with automatic optimization
        - Processing Pipeline: Raw content -> Processing -> Prepared content optimized for AI consumption

    Storage Tiers:
        - FIRESTORE: Fast access for frequently used knowledge (stored in database)
        - CLOUD_STORAGE: Cost-effective for less frequently accessed content
        - Automatic Optimization: Access patterns drive tier migration for cost efficiency

    Attributes:
        name: Human-readable name for the knowledge source
        source_type: Type of knowledge source (DOCUMENT, URL, BUSINESS_WEBSITE, etc.)
        request_success: Flag indicating if the creation request was successful
        processing_status: Current processing status (PENDING, PROCESSING, COMPLETED, FAILED)
        content: Raw extracted content from the knowledge source
        prepped_content: Processed content optimized for AI consumption
        content_path: Storage path for the raw content file
        prepped_content_path: Storage path for the processed content file
        original_content_url: Original source URL where content was obtained
        stored_content_url: Cloud storage URL for accessing raw content
        prepped_content_url: Cloud storage URL for accessing processed content
        content_size: Size of raw content in bytes
        prepped_content_size: Size of processed content in bytes
        storage_tier: Current storage tier for this knowledge source
        last_accessed: Unix timestamp when last accessed by an agent
        access_count: Number of times accessed, used for tier optimization
        is_compressed: Whether content is stored in compressed format
        compression_ratio: Compression ratio achieved if compressed
        metadata: Additional metadata about the knowledge source
        original_content_type: Original MIME type of the source content
        content_hash: Hash of content for deduplication and integrity
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        description="Human-readable name for the knowledge source (e.g., 'Product Documentation', 'Company Policies')"
    )
    source_type: KnowledgeTypes = Field(
        ...,
        description="Type of knowledge source determining how content is ingested (DOCUMENT, URL, BUSINESS_WEBSITE, CORPUS, BATCH_DOCUMENT)",
        alias="sourceType"
    )
    request_success: bool = Field(
        ...,
        description="Flag indicating whether the knowledge source creation and initial processing request completed successfully"
    )
    processing_status: KnowledgeBaseProcessingStatus = Field(
        KnowledgeBaseProcessingStatus.PENDING,
        description="Current processing status (PENDING, PROCESSING, COMPLETED, FAILED)",
        alias="processingStatus"
    )

    # Content storage
    content: Optional[str] = Field(
        None,
        description="Raw extracted content from the knowledge source stored inline (null if stored in cloud storage)"
    )
    prepped_content: Optional[str] = Field(
        None,
        description="Processed and prepared content optimized for AI consumption (null if stored in cloud storage)"
    )
    content_path: Optional[str] = Field(
        None,
        description="Storage path for the raw content file in cloud storage"
    )
    prepped_content_path: Optional[str] = Field(
        None,
        description="Storage path for the processed content file in cloud storage"
    )

    # Public URLs for client access
    original_content_url: Optional[str] = Field(
        None,
        description="Original source URL or upload URL where the content was obtained"
    )
    stored_content_url: Optional[str] = Field(
        None,
        description="Cloud storage URL for accessing the stored raw content"
    )
    prepped_content_url: Optional[str] = Field(
        None,
        description="Cloud storage URL for accessing the processed content"
    )

    # Storage metadata
    content_size: Optional[int] = Field(
        None,
        description="Size of the raw content in bytes"
    )
    prepped_content_size: Optional[int] = Field(
        None,
        description="Size of the processed content in bytes"
    )
    storage_tier: StorageTier = Field(
        StorageTier.FIRESTORE,
        description="Current storage tier: FIRESTORE (fast, expensive) or CLOUD_STORAGE (slower, cost-effective)"
    )

    # Access tracking for tier optimization
    last_accessed: Optional[int] = Field(
        None,
        description="Unix timestamp (milliseconds) when last accessed by an agent"
    )
    access_count: int = Field(
        0,
        description="Number of times accessed by agents, used for optimal storage tier placement"
    )

    # Compression info
    is_compressed: bool = Field(
        False,
        description="Flag indicating whether content is stored in compressed format"
    )
    compression_ratio: Optional[float] = Field(
        None,
        description="Compression ratio achieved if compressed (e.g., 0.5 means compressed to 50%)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata including tags, categories, custom attributes"
    )

    original_content_type: Optional[str] = Field(
        None,
        description="Original MIME type of the source content (e.g., 'application/pdf', 'text/html')"
    )
    content_hash: Optional[str] = Field(
        None,
        description="Hash of content (e.g., SHA-256) for deduplication and integrity verification"
    )
