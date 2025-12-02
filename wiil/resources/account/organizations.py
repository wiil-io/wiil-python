"""Organizations resource for reading organization information.

This module provides the OrganizationsResource class for accessing
organization information in the WIIL Platform API.

Example:
    >>> from wiil import WiilClient
    >>> client = WiilClient(api_key='your-api-key')
    >>> org = client.organizations.get()
    >>> print(org.company_name)
"""

from typing import Any

from wiil.client.http_client import HttpClient
from wiil.models.account import Organization


class OrganizationsResource:
    """Resource class for reading organization information in the WIIL Platform.

    This resource provides read-only access to retrieve the organization that
    owns the API key. No create, update, delete, or list operations are available.

    Example:
        >>> client = WiilClient(api_key='your-api-key')
        >>> org = client.organizations.get()
        >>> print('Organization:', org.company_name)
        >>> print('Business Vertical:', org.business_vertical_id)
    """

    def __init__(self, http: HttpClient):
        """Initialize the organizations resource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http

    def get(self) -> Organization:
        """Retrieve the organization that owns the API key.

        Returns:
            The organization associated with the authenticated API key

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> org = client.organizations.get()
            >>> print('Organization ID:', org.id)
            >>> print('Company Name:', org.company_name)
            >>> print('Business Vertical:', org.business_vertical_id)
            >>> print('Platform Email:', org.platform_email)
            >>> print('Service Status:', org.service_status)
        """
        return self._http.get('/organizations')


__all__ = ['OrganizationsResource']
