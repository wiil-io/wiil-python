"""HTTP client for making requests to the WIIL Platform API.

This module provides the HTTP client used internally by the WIIL SDK
to communicate with the WIIL Platform API.

Example:
    >>> from wiil.client.types import WiilClientConfig
    >>> from wiil.client.http_client import HttpClient
    >>> config = WiilClientConfig(api_key='your-key')
    >>> http = HttpClient(config)
    >>> data = http.get('/organizations')
"""

import json
from typing import Any, Dict, Optional, Type, TypeVar

import requests
from pydantic import BaseModel, ValidationError
from requests.exceptions import RequestException, Timeout, ConnectionError

from wiil.client.types import WiilClientConfig, APIResponse, APIErrorResponse
from wiil.errors import (
    WiilAPIError,
    WiilNetworkError,
    WiilValidationError,
)

# Type variable for response types
T = TypeVar('T')


class HttpClient:
    """HTTP client for communicating with the WIIL Platform API.

    This class handles all HTTP communication with the WIIL Platform API,
    including authentication, request/response validation, and error handling.
    It is used internally by resource classes and should not be instantiated directly.

    Attributes:
        api_key: API key for authentication
        base_url: Base URL for the API
        timeout: Request timeout in seconds
        session: Requests session for connection pooling

    Example:
        >>> from wiil.client.types import WiilClientConfig
        >>> config = WiilClientConfig(api_key='your-key')
        >>> http = HttpClient(config)
    """

    def __init__(self, config: WiilClientConfig):
        """Create a new HttpClient instance.

        Args:
            config: Client configuration containing API key, base URL, and timeout

        Example:
            >>> from wiil.client.types import WiilClientConfig
            >>> config = WiilClientConfig(api_key='your-key')
            >>> http = HttpClient(config)
        """
        self.api_key = config.api_key
        self.base_url = config.base_url.rstrip('/')
        self.timeout = config.timeout

        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-WIIL-API-Key': self.api_key,
        })

    def get(self, path: str, **kwargs: Any) -> Any:
        """Make a GET request to the API.

        Args:
            path: API endpoint path (e.g., '/organizations')
            **kwargs: Additional keyword arguments to pass to requests.get()

        Returns:
            The response data extracted from the APIResponse wrapper

        Raises:
            WiilAPIError: When the API returns an error response (4xx or 5xx)
            WiilNetworkError: When network communication fails

        Example:
            >>> data = http.get('/organizations')
            >>> print(data['id'])
        """
        url = f"{self.base_url}{path}"

        try:
            response = self.session.get(
                url,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            response.raise_for_status()

            # Parse the response
            response_data = response.json()

            # Return the data field from the APIResponse wrapper
            if isinstance(response_data, dict) and 'data' in response_data:
                return response_data['data']

            return response_data

        except Timeout:
            raise WiilNetworkError(
                'Request timeout',
                details={'url': url, 'timeout': self.timeout}
            )
        except ConnectionError as e:
            raise WiilNetworkError(
                'Connection error occurred',
                details={'url': url, 'error': str(e)}
            )
        except requests.HTTPError as e:
            raise self._handle_http_error(e)
        except RequestException as e:
            raise WiilNetworkError(
                f'Network error occurred: {str(e)}',
                details={'url': url, 'error': str(e)}
            )
        except json.JSONDecodeError as e:
            raise WiilAPIError(
                'Invalid JSON response from API',
                details={'error': str(e)}
            )

    def post(
        self,
        path: str,
        data: Any,
        schema: Optional[Type[BaseModel]] = None,
        **kwargs: Any
    ) -> Any:
        """Make a POST request to the API with optional validation.

        Args:
            path: API endpoint path
            data: Request payload (will be JSON-encoded)
            schema: Optional Pydantic model for validating the request payload
            **kwargs: Additional keyword arguments to pass to requests.post()

        Returns:
            The response data extracted from the APIResponse wrapper

        Raises:
            WiilValidationError: When request validation fails
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> from pydantic import BaseModel
            >>> class CreateOrgRequest(BaseModel):
            ...     name: str
            >>> data = http.post(
            ...     '/organizations',
            ...     {'name': 'Acme Corp'},
            ...     schema=CreateOrgRequest
            ... )
        """
        # Validate request if schema provided
        if schema:
            try:
                if isinstance(data, dict):
                    validated_data = schema(**data)
                    data = validated_data.model_dump(exclude_none=True)
                elif isinstance(data, BaseModel):
                    data = data.model_dump(exclude_none=True)
            except ValidationError as e:
                raise WiilValidationError(
                    'Request validation failed',
                    details=e.errors()
                )

        url = f"{self.base_url}{path}"

        try:
            response = self.session.post(
                url,
                json=data,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            response.raise_for_status()

            # Parse the response
            response_data = response.json()

            # Return the data field from the APIResponse wrapper
            if isinstance(response_data, dict) and 'data' in response_data:
                return response_data['data']

            return response_data

        except Timeout:
            raise WiilNetworkError(
                'Request timeout',
                details={'url': url, 'timeout': self.timeout}
            )
        except ConnectionError as e:
            raise WiilNetworkError(
                'Connection error occurred',
                details={'url': url, 'error': str(e)}
            )
        except requests.HTTPError as e:
            raise self._handle_http_error(e)
        except RequestException as e:
            raise WiilNetworkError(
                f'Network error occurred: {str(e)}',
                details={'url': url, 'error': str(e)}
            )
        except json.JSONDecodeError as e:
            raise WiilAPIError(
                'Invalid JSON response from API',
                details={'error': str(e)}
            )

    def put(
        self,
        path: str,
        data: Any,
        schema: Optional[Type[BaseModel]] = None,
        **kwargs: Any
    ) -> Any:
        """Make a PUT request to the API with optional validation.

        Args:
            path: API endpoint path
            data: Request payload (will be JSON-encoded)
            schema: Optional Pydantic model for validating the request payload
            **kwargs: Additional keyword arguments to pass to requests.put()

        Returns:
            The response data extracted from the APIResponse wrapper

        Raises:
            WiilValidationError: When request validation fails
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> data = http.put(
            ...     '/organizations/org_123',
            ...     {'name': 'Acme Corporation'}
            ... )
        """
        # Validate request if schema provided
        if schema:
            try:
                if isinstance(data, dict):
                    validated_data = schema(**data)
                    data = validated_data.model_dump(exclude_none=True)
                elif isinstance(data, BaseModel):
                    data = data.model_dump(exclude_none=True)
            except ValidationError as e:
                raise WiilValidationError(
                    'Request validation failed',
                    details=e.errors()
                )

        url = f"{self.base_url}{path}"

        try:
            response = self.session.put(
                url,
                json=data,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            response.raise_for_status()

            # Parse the response
            response_data = response.json()

            # Return the data field from the APIResponse wrapper
            if isinstance(response_data, dict) and 'data' in response_data:
                return response_data['data']

            return response_data

        except Timeout:
            raise WiilNetworkError(
                'Request timeout',
                details={'url': url, 'timeout': self.timeout}
            )
        except ConnectionError as e:
            raise WiilNetworkError(
                'Connection error occurred',
                details={'url': url, 'error': str(e)}
            )
        except requests.HTTPError as e:
            raise self._handle_http_error(e)
        except RequestException as e:
            raise WiilNetworkError(
                f'Network error occurred: {str(e)}',
                details={'url': url, 'error': str(e)}
            )
        except json.JSONDecodeError as e:
            raise WiilAPIError(
                'Invalid JSON response from API',
                details={'error': str(e)}
            )

    def patch(
        self,
        path: str,
        data: Any,
        schema: Optional[Type[BaseModel]] = None,
        **kwargs: Any
    ) -> Any:
        """Make a PATCH request to the API with optional validation.

        Args:
            path: API endpoint path
            data: Request payload (will be JSON-encoded)
            schema: Optional Pydantic model for validating the request payload
            **kwargs: Additional keyword arguments to pass to requests.patch()

        Returns:
            The response data extracted from the APIResponse wrapper

        Raises:
            WiilValidationError: When request validation fails
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> data = http.patch(
            ...     '/organizations/org_123',
            ...     {'name': 'Acme Corp Updated'}
            ... )
        """
        # Validate request if schema provided
        if schema:
            try:
                if isinstance(data, dict):
                    validated_data = schema(**data)
                    data = validated_data.model_dump(exclude_none=True)
                elif isinstance(data, BaseModel):
                    data = data.model_dump(exclude_none=True)
            except ValidationError as e:
                raise WiilValidationError(
                    'Request validation failed',
                    details=e.errors()
                )

        url = f"{self.base_url}{path}"

        try:
            response = self.session.patch(
                url,
                json=data,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            response.raise_for_status()

            # Parse the response
            response_data = response.json()

            # Return the data field from the APIResponse wrapper
            if isinstance(response_data, dict) and 'data' in response_data:
                return response_data['data']

            return response_data

        except Timeout:
            raise WiilNetworkError(
                'Request timeout',
                details={'url': url, 'timeout': self.timeout}
            )
        except ConnectionError as e:
            raise WiilNetworkError(
                'Connection error occurred',
                details={'url': url, 'error': str(e)}
            )
        except requests.HTTPError as e:
            raise self._handle_http_error(e)
        except RequestException as e:
            raise WiilNetworkError(
                f'Network error occurred: {str(e)}',
                details={'url': url, 'error': str(e)}
            )
        except json.JSONDecodeError as e:
            raise WiilAPIError(
                'Invalid JSON response from API',
                details={'error': str(e)}
            )

    def delete(self, path: str, **kwargs: Any) -> Any:
        """Make a DELETE request to the API.

        Args:
            path: API endpoint path
            **kwargs: Additional keyword arguments to pass to requests.delete()

        Returns:
            The response data extracted from the APIResponse wrapper (may be None)

        Raises:
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> http.delete('/organizations/org_123')
        """
        url = f"{self.base_url}{path}"

        try:
            response = self.session.delete(
                url,
                timeout=kwargs.pop('timeout', self.timeout),
                **kwargs
            )
            response.raise_for_status()

            # Check if there's a response body
            if response.text:
                response_data = response.json()

                # Return the data field from the APIResponse wrapper
                if isinstance(response_data, dict) and 'data' in response_data:
                    return response_data['data']

                return response_data

            return None

        except Timeout:
            raise WiilNetworkError(
                'Request timeout',
                details={'url': url, 'timeout': self.timeout}
            )
        except ConnectionError as e:
            raise WiilNetworkError(
                'Connection error occurred',
                details={'url': url, 'error': str(e)}
            )
        except requests.HTTPError as e:
            raise self._handle_http_error(e)
        except RequestException as e:
            raise WiilNetworkError(
                f'Network error occurred: {str(e)}',
                details={'url': url, 'error': str(e)}
            )
        except json.JSONDecodeError as e:
            raise WiilAPIError(
                'Invalid JSON response from API',
                details={'error': str(e)}
            )

    def _handle_http_error(self, error: requests.HTTPError) -> WiilAPIError:
        """Transform requests HTTP errors to WiilAPIError.

        Args:
            error: HTTP error from requests library

        Returns:
            WiilAPIError with appropriate status code and message

        Example:
            >>> try:
            ...     response.raise_for_status()
            ... except requests.HTTPError as e:
            ...     raise self._handle_http_error(e)
        """
        response = error.response
        status_code = response.status_code

        # Try to parse error response
        try:
            error_data = response.json()

            # Check if it's a standard WIIL API error response
            if isinstance(error_data, dict) and not error_data.get('success', True):
                error_info = error_data.get('error', {})
                return WiilAPIError(
                    message=error_info.get('message', f'Request failed with status {status_code}'),
                    status_code=status_code,
                    code=error_info.get('code', 'UNKNOWN_ERROR'),
                    details=error_info.get('details')
                )

        except (json.JSONDecodeError, ValueError):
            # If we can't parse the error response, use the status text
            pass

        # Fallback for non-standard error responses
        return WiilAPIError(
            message=f'Request failed with status {status_code}',
            status_code=status_code,
            code='UNKNOWN_ERROR',
            details={'response_text': response.text}
        )

    def __del__(self):
        """Close the session when the client is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()


__all__ = ['HttpClient']
