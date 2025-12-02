"""Knowledge source schema definitions for managing AI knowledge bases.

Knowledge Sources provide contextual information, documentation, and domain knowledge
that Instruction Configurations can reference to enhance agent capabilities.
"""

from typing import Any, Dict, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.knowledge_types import (
    KnowledgeBaseProcessingStatus,
    KnowledgeTypes,
    StorageTier,
)


class KnowledgeSource(BaseModel):
    """Knowledge Source model.

    Knowledge Sources provide contextual information and domain knowledge for AI agents.
    They are referenced by Instruction Configurations (1:N relationship) to give agents
    access to specific information, documentation, or business knowledge.

    Architecture Context:
        - Relationship: Referenced by Instruction Configurations (1:N)
        - Purpose: Provides domain knowledge and context for agent responses
        - Storage Strategy: Multi-tier storage with automatic optimization
        - Processing Pipeline: Raw content → Processing → Prepared content

    Storage Tiers:
        - FIRESTORE: Fast access for frequently used knowledge
        - CLOUD_STORAGE: Cost-effective for less frequently accessed content
        - Automatic Optimization: Access patterns drive tier migration

    Attributes:
        id: Unique identifier
        name: Human-readable name
        source_type: Type of knowledge source
        request_success: Whether creation request was successful
        processing_status: Current processing status
        content: Raw extracted content
        prepped_content: Processed content optimized for AI
        content_path: Storage path for raw content
        prepped_content_path: Storage path for processed content
        original_content_url: Original source URL
        stored_content_url: Cloud storage URL for raw content
        prepped_content_url: Cloud storage URL for processed content
        content_size: Size of raw content in bytes
        prepped_content_size: Size of processed content in bytes
        storage_tier: Current storage tier
        last_accessed: Last access timestamp
        access_count: Number of times accessed
        is_compressed: Whether content is compressed
        compression_ratio: Compression ratio if compressed
        metadata: Additional metadata
        original_content_type: Original MIME type
        content_hash: Content hash for deduplication
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        knowledge = KnowledgeSource(
            id="123",
            name="Product Documentation",
            source_type=KnowledgeTypes.DOCUMENT,
            request_success=True,
            processing_status=KnowledgeBaseProcessingStatus.COMPLETED,
            content="Raw document content...",
            prepped_content="Processed content...",
            storage_tier=StorageTier.FIRESTORE,
            access_count=42,
            is_compressed=False
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(
        ...,
        description="Human-readable name (e.g., 'Product Documentation')"
    )
    source_type: KnowledgeTypes = Field(
        ...,
        description="Type of knowledge source"
    )
    request_success: bool = Field(
        ...,
        description="Whether creation request was successful"
    )
    processing_status: KnowledgeBaseProcessingStatus = Field(
        KnowledgeBaseProcessingStatus.PENDING,
        description="Current processing status"
    )

    # Content storage
    content: Optional[str] = Field(
        None,
        description="Raw extracted content (null if in cloud storage)"
    )
    prepped_content: Optional[str] = Field(
        None,
        description="Processed content optimized for AI"
    )
    content_path: Optional[str] = Field(
        None,
        description="Storage path for raw content"
    )
    prepped_content_path: Optional[str] = Field(
        None,
        description="Storage path for processed content"
    )

    # Public URLs
    original_content_url: Optional[str] = Field(
        None,
        description="Original source URL"
    )
    stored_content_url: Optional[str] = Field(
        None,
        description="Cloud storage URL for raw content"
    )
    prepped_content_url: Optional[str] = Field(
        None,
        description="Cloud storage URL for processed content"
    )

    # Storage metadata
    content_size: Optional[int] = Field(
        None,
        description="Size of raw content in bytes"
    )
    prepped_content_size: Optional[int] = Field(
        None,
        description="Size of processed content in bytes"
    )
    storage_tier: StorageTier = Field(
        StorageTier.FIRESTORE,
        description="Current storage tier"
    )

    # Access tracking
    last_accessed: Optional[int] = Field(
        None,
        description="Last access timestamp"
    )
    access_count: int = Field(
        0,
        description="Number of times accessed"
    )

    # Compression
    is_compressed: bool = Field(
        False,
        description="Whether content is compressed"
    )
    compression_ratio: Optional[float] = Field(
        None,
        description="Compression ratio if compressed"
    )

    # Additional metadata
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata"
    )
    original_content_type: Optional[str] = Field(
        None,
        description="Original MIME type"
    )
    content_hash: Optional[str] = Field(
        None,
        description="Content hash for deduplication"
    )


class CreateKnowledgeSource(BaseModel):
    """Schema for creating a new knowledge source."""

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    name: str
    source_type: KnowledgeTypes = Field(...)
    request_success: bool = Field(...)
    processing_status: KnowledgeBaseProcessingStatus = Field(
        KnowledgeBaseProcessingStatus.PENDING
    )
    content: Optional[str] = None
    prepped_content: Optional[str] = Field(None)
    content_path: Optional[str] = Field(None)
    prepped_content_path: Optional[str] = Field(None)
    original_content_url: Optional[str] = Field(None)
    stored_content_url: Optional[str] = Field(None)
    prepped_content_url: Optional[str] = Field(None)
    content_size: Optional[int] = Field(None)
    prepped_content_size: Optional[int] = Field(None)
    storage_tier: StorageTier = Field(StorageTier.FIRESTORE)
    is_compressed: bool = Field(False)
    compression_ratio: Optional[float] = Field(None)
    metadata: Optional[Dict[str, Any]] = None
    original_content_type: Optional[str] = Field(None)
    content_hash: Optional[str] = Field(None)


class UpdateKnowledgeSource(BaseModel):
    """Schema for updating an existing knowledge source."""

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    name: Optional[str] = None
    processing_status: Optional[KnowledgeBaseProcessingStatus] = Field(None)
    content: Optional[str] = None
    prepped_content: Optional[str] = Field(None)
    storage_tier: Optional[StorageTier] = Field(None)
    access_count: Optional[int] = Field(None)
    is_compressed: Optional[bool] = Field(None)
    metadata: Optional[Dict[str, Any]] = None
