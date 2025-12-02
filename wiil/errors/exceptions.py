"""Custom exception classes for WIIL SDK.

This module provides a hierarchy of exception classes for handling different
types of errors that can occur when using the WIIL SDK.

Example:
    >>> from wiil.errors import WiilError, WiilAPIError
    >>> try:
    ...     # SDK operation
    ...     pass
    ... except WiilAPIError as e:
    ...     print(f"API Error {e.status_code}: {e.message}")
    ... except WiilError as e:
    ...     print(f"SDK Error: {e.message}")
"""

from typing import Any, Optional


class WiilError(Exception):
    """Base exception for all WIIL SDK errors.

    All custom errors in the SDK extend from this base class, providing
    a consistent error handling interface across the SDK.

    Attributes:
        message: Human-readable error message
        details: Additional error context or details

    Example:
        >>> try:
        ...     raise WiilError("Something went wrong", {"code": "ERROR_001"})
        ... except WiilError as e:
        ...     print(e.message)
        ...     print(e.details)
    """

    def __init__(self, message: str, details: Any = None):
        """Create a new WiilError instance.

        Args:
            message: Human-readable error message
            details: Additional error context or details
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} (details: {self.details})"
        return self.message

    def __repr__(self) -> str:
        """Return detailed string representation of the error."""
        return f"{self.__class__.__name__}(message={self.message!r}, details={self.details!r})"


class WiilAPIError(WiilError):
    """Error thrown when an API request fails.

    This error is thrown for HTTP 4xx and 5xx responses from the WIIL Platform API.
    It includes the HTTP status code and error code from the API response.

    Attributes:
        message: Human-readable error message
        status_code: HTTP status code from the API response
        code: Error code from the API response
        details: Additional error context

    Example:
        >>> try:
        ...     # API call that fails
        ...     pass
        ... except WiilAPIError as e:
        ...     print(f"API Error {e.status_code}: {e.message}")
        ...     print(f"Error Code: {e.code}")
        ...     if e.details:
        ...         print(f"Details: {e.details}")
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        details: Any = None
    ):
        """Create a new WiilAPIError instance.

        Args:
            message: Human-readable error message
            status_code: HTTP status code
            code: Error code from API
            details: Additional error context
        """
        super().__init__(message, details)
        self.status_code = status_code
        self.code = code

    def __str__(self) -> str:
        """Return string representation of the error."""
        parts = [self.message]
        if self.status_code:
            parts.append(f"status_code={self.status_code}")
        if self.code:
            parts.append(f"code={self.code}")
        if self.details:
            parts.append(f"details={self.details}")

        if len(parts) > 1:
            return f"{parts[0]} ({', '.join(parts[1:])})"
        return parts[0]

    def __repr__(self) -> str:
        """Return detailed string representation of the error."""
        return (
            f"{self.__class__.__name__}(message={self.message!r}, "
            f"status_code={self.status_code!r}, code={self.code!r}, "
            f"details={self.details!r})"
        )


class WiilValidationError(WiilError):
    """Error thrown when request or response validation fails.

    This error is thrown when Pydantic schema validation fails for request payloads
    or API responses. It includes validation error details from Pydantic.

    Attributes:
        message: Human-readable error message
        details: Validation error details from Pydantic

    Example:
        >>> try:
        ...     # Validation that fails
        ...     pass
        ... except WiilValidationError as e:
        ...     print(f"Validation failed: {e.message}")
        ...     print(f"Details: {e.details}")
    """

    def __init__(self, message: str, details: Any = None):
        """Create a new WiilValidationError instance.

        Args:
            message: Human-readable error message
            details: Validation error details from Pydantic
        """
        super().__init__(message, details)


class WiilNetworkError(WiilError):
    """Error thrown when network communication fails.

    This error is thrown for network-level failures such as connection timeouts,
    DNS resolution failures, or network unavailability.

    Attributes:
        message: Human-readable error message
        details: Additional error context

    Example:
        >>> try:
        ...     # Network operation that fails
        ...     pass
        ... except WiilNetworkError as e:
        ...     print(f"Network error: {e.message}")
        ...     print("Consider retrying the request")
    """

    def __init__(self, message: str, details: Any = None):
        """Create a new WiilNetworkError instance.

        Args:
            message: Human-readable error message
            details: Additional error context
        """
        super().__init__(message, details)


class WiilConfigurationError(WiilError):
    """Error thrown when SDK configuration is invalid.

    This error is thrown when the SDK is initialized with invalid configuration,
    such as missing API key or invalid base URL.

    Attributes:
        message: Human-readable error message

    Example:
        >>> try:
        ...     from wiil import WiilClient
        ...     client = WiilClient(api_key='')  # Invalid: empty API key
        ... except WiilConfigurationError as e:
        ...     print(f"Configuration error: {e.message}")
    """

    def __init__(self, message: str):
        """Create a new WiilConfigurationError instance.

        Args:
            message: Human-readable error message
        """
        super().__init__(message)


__all__ = [
    'WiilError',
    'WiilAPIError',
    'WiilValidationError',
    'WiilNetworkError',
    'WiilConfigurationError',
]
