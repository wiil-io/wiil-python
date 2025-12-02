"""Organization schema definitions for account management."""

from typing import Any, Dict, List, Literal, Optional

from pydantic import ConfigDict, Field

from wiil.models.base import BaseModel
from wiil.types.account_types import ServiceStatus, ServiceSuspensionType

# Supported business vertical IDs
SupportedBusinessVerticalId = Literal[
    "healthcare",
    "health-wellness",
    "retail",
    "finance",
    "real-estate",
    "technology",
    "education",
    "legal",
    "automotive",
    "hospitality",
    "professional",
    "others"
]


class OrganizationServiceStatusRecord(BaseModel):
    """Organization service status history record.

    Tracks all status changes for an organization over time, providing
    an audit trail of service state transitions.

    Attributes:
        id: Unique identifier for the status record
        status: Current status at the time of this record
        previous_status: Previous status before this change
        suspension_type: Type of suspension if status is SUSPENDED
        timestamp: Unix timestamp when the status change occurred
        reason: Explanation for the status change
        changed_by: User ID who initiated the status change
        is_current: Whether this is the current active status record
        created_at: Timestamp when the record was created
        updated_at: Timestamp when the record was last updated

    Example:
        ```python
        status_record = OrganizationServiceStatusRecord(
            id='123',
            status=ServiceStatus.SUSPENDED,
            previous_status=ServiceStatus.ACTIVE,
            suspension_type=ServiceSuspensionType.QUOTA_EXCEEDED,
            timestamp=1234567890,
            reason='Monthly usage quota exceeded',
            changed_by='system',
            is_current=True,
            created_at=1234567890,
            updated_at=1234567890
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    status: ServiceStatus = Field(
        ...,
        description="Current status at the time of this record"
    )
    previous_status: Optional[ServiceStatus] = Field(
        None,
        description="Previous status before this change",
        alias="previousStatus"
    )
    suspension_type: Optional[ServiceSuspensionType] = Field(
        None,
        description="Type of suspension if status is SUSPENDED",
        alias="suspensionType"
    )
    timestamp: int = Field(
        ...,
        description="Unix timestamp when the status change occurred"
    )
    reason: str = Field(..., description="Explanation for the status change")
    changed_by: str = Field(
        ...,
        description="User ID who initiated the status change",
        alias="changedBy"
    )
    is_current: bool = Field(
        True,
        description="Whether this is the current active status record",
        alias="isCurrent"
    )


class Organization(BaseModel):
    """Organization entity.

    Represents a complete organization (company/business account) within the platform,
    including service status tracking and configuration.

    Attributes:
        id: Unique identifier for the organization
        company_name: Organization's company name
        business_vertical_id: Business industry vertical classification ID
        metadata: Additional custom metadata for the organization
        service_status: Current service status
        last_service_status_changed: Timestamp of last service status change
        service_status_history: Complete history of service status changes
        platform_email: Organization's platform contact email
        created_at: Timestamp when the organization was created
        updated_at: Timestamp when the organization was last updated

    Example:
        ```python
        organization = Organization(
            id='123',
            company_name='Acme Corporation',
            business_vertical_id='technology',
            service_status=ServiceStatus.ACTIVE,
            platform_email='admin@acme.com',
            metadata={'industry': 'technology'},
            created_at=1234567890,
            updated_at=1234567890
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    company_name: str = Field(
        ...,
        min_length=2,
        description="Organization's company name (minimum 2 characters)",
        alias="companyName"
    )
    business_vertical_id: Optional[SupportedBusinessVerticalId] = Field(
        None,
        description="Business industry vertical classification ID (healthcare, retail, technology, etc.)",
        alias="businessVerticalId"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional custom metadata for the organization"
    )
    service_status: ServiceStatus = Field(
        ServiceStatus.ACTIVE,
        description="Current service status of the organization",
        alias="serviceStatus"
    )
    last_service_status_changed: Optional[int] = Field(
        None,
        description="Timestamp of last service status change",
        alias="lastServiceStatusChanged"
    )
    service_status_history: Optional[List[OrganizationServiceStatusRecord]] = Field(
        None,
        description="Complete history of service status changes",
        alias="serviceStatusHistory"
    )
    platform_email: Optional[str] = Field(
        None,
        description="Organization's platform contact email",
        alias="platformEmail"
    )
