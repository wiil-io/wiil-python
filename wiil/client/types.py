"""Type definitions for WIIL SDK client configuration.

This module provides type definitions and data classes used throughout
the WIIL SDK client implementation.

Example:
    >>> from wiil.client.types import WiilClientConfig
    >>> config = WiilClientConfig(
    ...     api_key='your-api-key',
    ...     base_url='https://api.wiil.io/v1',
    ...     timeout=30
    ... )
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, TypeVar

# Type variable for generic response types
T = TypeVar('T')


@dataclass
class WiilClientConfig:
    """Configuration options for the WIIL SDK client.

    These options are used to initialize the WiilClient instance.

    Attributes:
        api_key: API key for authentication with the WIIL Platform.
            This is required for all API requests. You can obtain an API key
            from your WIIL Platform dashboard.
        base_url: Base URL for the WIIL Platform API.
            Defaults to 'https://api.wiil.io/v1'.
            Override this if you're using a custom deployment or different environment.
        timeout: Request timeout in seconds.
            Defaults to 30 seconds.
            Requests that exceed this timeout will raise a WiilNetworkError.

    Example:
        >>> config = WiilClientConfig(
        ...     api_key='your-api-key',
        ...     base_url='https://api.wiil.io/v1',
        ...     timeout=30
        ... )
    """

    api_key: str
    base_url: str = "https://api.wiil.io/v1"
    timeout: int = 30  # seconds


@dataclass
class APIResponseMetadata:
    """Response metadata from the WIIL Platform API.

    Attributes:
        timestamp: Unix timestamp (in milliseconds) when the response was generated
        version: API version used for this response

    Example:
        >>> metadata = APIResponseMetadata(
        ...     timestamp=1704067200000,
        ...     version='v1'
        ... )
    """

    timestamp: int
    version: str


@dataclass
class APIResponse(Generic[T]):
    """Standard API response wrapper.

    All WIIL Platform API responses follow this structure, wrapping the actual
    data with metadata about the request.

    Attributes:
        success: Indicates whether the request was successful
        data: The response data. This field contains the actual data returned by the API.
            The type varies based on the endpoint called.
        metadata: Response metadata containing additional information about the response
            such as timestamp and API version.

    Example:
        >>> from wiil.models.account import Organization
        >>> response = APIResponse(
        ...     success=True,
        ...     data=Organization(
        ...         id='org_123',
        ...         company_name='Acme Corp',
        ...         industry='Technology',
        ...         country='US'
        ...     ),
        ...     metadata={'timestamp': 1704067200000, 'version': 'v1'}
        ... )
    """

    success: bool
    data: T
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIErrorDetails:
    """Error details from an API error response.

    Attributes:
        code: Error code for programmatic handling
        message: Human-readable error message
        details: Additional error details (optional)

    Example:
        >>> error_details = APIErrorDetails(
        ...     code='VALIDATION_ERROR',
        ...     message='Invalid organization name',
        ...     details={'field': 'companyName', 'issue': 'Must be at least 2 characters'}
        ... )
    """

    code: str
    message: str
    details: Any = None


@dataclass
class APIErrorResponse:
    """Error response from the API.

    This structure is returned when an API request fails (4xx or 5xx responses).

    Attributes:
        success: Always False for error responses
        error: Error details containing code, message, and optional details
        metadata: Response metadata

    Example:
        >>> error_response = APIErrorResponse(
        ...     success=False,
        ...     error={
        ...         'code': 'VALIDATION_ERROR',
        ...         'message': 'Invalid organization name',
        ...         'details': {
        ...             'field': 'companyName',
        ...             'issue': 'Must be at least 2 characters'
        ...         }
        ...     },
        ...     metadata={'timestamp': 1704067200000, 'version': 'v1'}
        ... )
    """

    success: bool  # Always False for error responses
    error: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


__all__ = [
    'WiilClientConfig',
    'APIResponse',
    'APIResponseMetadata',
    'APIErrorResponse',
    'APIErrorDetails',
]
