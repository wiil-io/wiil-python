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
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, get_origin, get_args

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
            'X-Wiil-Api-Key': self.api_key,
        })

    def get(
        self,
        path: str,
        response_model: Optional[Type[T]] = None,
        **kwargs: Any
    ) -> T:
        """Make a GET request to the API.

        Args:
            path: API endpoint path (e.g., '/organizations')
            response_model: Optional Pydantic model to parse response into
            **kwargs: Additional keyword arguments to pass to requests.get()

        Returns:
            The response data parsed into response_model if provided,
            otherwise AttrDict

        Raises:
            WiilAPIError: When the API returns an error response (4xx or 5xx)
            WiilNetworkError: When network communication fails
            WiilValidationError: When response validation fails

        Example:
            >>> from wiil.models import Organization
            >>> org = http.get('/organizations/123', response_model=Organization)
            >>> print(org.id)
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

            # Check for API-level failure (success: false)
            self._check_api_success(response_data, response.status_code)

            # Extract data from APIResponse wrapper
            if isinstance(response_data, dict) and 'data' in response_data:
                return self._parse_response(response_data['data'], response_model)

            return self._parse_response(response_data, response_model)

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
        response_model: Optional[Type[T]] = None,
        **kwargs: Any
    ) -> T:
        """Make a POST request to the API with optional validation.

        Args:
            path: API endpoint path
            data: Request payload (will be JSON-encoded)
            schema: Optional Pydantic model for validating the request payload
            response_model: Optional Pydantic model to parse response into
            **kwargs: Additional keyword arguments to pass to requests.post()

        Returns:
            The response data parsed into response_model if provided,
            otherwise AttrDict

        Raises:
            WiilValidationError: When request or response validation fails
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> from wiil.models import Organization, CreateOrganization
            >>> org = http.post(
            ...     '/organizations',
            ...     {'name': 'Acme Corp'},
            ...     schema=CreateOrganization,
            ...     response_model=Organization
            ... )
        """
        # Validate request if schema provided
        if schema:
            try:
                if isinstance(data, dict):
                    # Validate in JSON mode so wire-format values (e.g. string
                    # enum members produced by model_dump under
                    # use_enum_values=True) are accepted while strict type and
                    # extra-key checks remain enforced — mirrors the response
                    # validation path.
                    validated_data = schema.model_validate_json(json.dumps(data))
                    data = validated_data.model_dump(by_alias=True, exclude_none=True)
                elif isinstance(data, BaseModel):
                    data = data.model_dump(by_alias=True, exclude_none=True)
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

            # Check for API-level failure (success: false)
            self._check_api_success(response_data, response.status_code)

            # Extract data from APIResponse wrapper and parse
            if isinstance(response_data, dict) and 'data' in response_data:
                return self._parse_response(response_data['data'], response_model)

            return self._parse_response(response_data, response_model)

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
        response_model: Optional[Type[T]] = None,
        **kwargs: Any
    ) -> T:
        """Make a PUT request to the API with optional validation.

        Args:
            path: API endpoint path
            data: Request payload (will be JSON-encoded)
            schema: Optional Pydantic model for validating the request payload
            response_model: Optional Pydantic model to parse response into
            **kwargs: Additional keyword arguments to pass to requests.put()

        Returns:
            The response data parsed into response_model if provided,
            otherwise AttrDict

        Raises:
            WiilValidationError: When request or response validation fails
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> from wiil.models import Organization
            >>> org = http.put(
            ...     '/organizations/org_123',
            ...     {'name': 'Acme Corporation'},
            ...     response_model=Organization
            ... )
        """
        # Validate request if schema provided
        if schema:
            try:
                if isinstance(data, dict):
                    # Validate in JSON mode so wire-format values (e.g. string
                    # enum members produced by model_dump under
                    # use_enum_values=True) are accepted while strict type and
                    # extra-key checks remain enforced — mirrors the response
                    # validation path.
                    validated_data = schema.model_validate_json(json.dumps(data))
                    data = validated_data.model_dump(by_alias=True, exclude_none=True)
                elif isinstance(data, BaseModel):
                    data = data.model_dump(by_alias=True, exclude_none=True)
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

            # Check for API-level failure (success: false)
            self._check_api_success(response_data, response.status_code)

            # Extract data from APIResponse wrapper and parse
            if isinstance(response_data, dict) and 'data' in response_data:
                return self._parse_response(response_data['data'], response_model)

            return self._parse_response(response_data, response_model)

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
        response_model: Optional[Type[T]] = None,
        **kwargs: Any
    ) -> T:
        """Make a PATCH request to the API with optional validation.

        Args:
            path: API endpoint path
            data: Request payload (will be JSON-encoded)
            schema: Optional Pydantic model for validating the request payload
            response_model: Optional Pydantic model to parse response into
            **kwargs: Additional keyword arguments to pass to requests.patch()

        Returns:
            The response data parsed into response_model if provided,
            otherwise AttrDict

        Raises:
            WiilValidationError: When request or response validation fails
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails

        Example:
            >>> from wiil.models import Organization
            >>> org = http.patch(
            ...     '/organizations/org_123',
            ...     {'name': 'Acme Corp Updated'},
            ...     response_model=Organization
            ... )
        """
        # Validate request if schema provided
        if schema:
            try:
                if isinstance(data, dict):
                    # Validate in JSON mode so wire-format values (e.g. string
                    # enum members produced by model_dump under
                    # use_enum_values=True) are accepted while strict type and
                    # extra-key checks remain enforced — mirrors the response
                    # validation path.
                    validated_data = schema.model_validate_json(json.dumps(data))
                    data = validated_data.model_dump(by_alias=True, exclude_none=True)
                elif isinstance(data, BaseModel):
                    data = data.model_dump(by_alias=True, exclude_none=True)
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

            # Check for API-level failure (success: false)
            self._check_api_success(response_data, response.status_code)

            # Extract data from APIResponse wrapper and parse
            if isinstance(response_data, dict) and 'data' in response_data:
                return self._parse_response(response_data['data'], response_model)

            return self._parse_response(response_data, response_model)

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

    def delete(
        self,
        path: str,
        response_model: Optional[Type[T]] = None,
        **kwargs: Any
    ) -> Optional[T]:
        """Make a DELETE request to the API.

        Args:
            path: API endpoint path
            response_model: Optional Pydantic model to parse response into
            **kwargs: Additional keyword arguments to pass to requests.delete()

        Returns:
            The response data parsed into response_model if provided,
            otherwise AttrDict or None

        Raises:
            WiilAPIError: When the API returns an error response
            WiilNetworkError: When network communication fails
            WiilValidationError: When response validation fails

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

                # Check for API-level failure (success: false)
                self._check_api_success(response_data, response.status_code)

                # Extract data from APIResponse wrapper and parse
                if isinstance(response_data, dict) and 'data' in response_data:
                    return self._parse_response(response_data['data'], response_model)

                return self._parse_response(response_data, response_model)

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

            # Check if it's a standard WIIL API error response (flat structure)
            if isinstance(error_data, dict) and not error_data.get('success', True):
                return WiilAPIError(
                    message=error_data.get('message', f'Request failed with status {status_code}'),
                    status_code=error_data.get('status', status_code),
                    code=error_data.get('code', 'UNKNOWN_ERROR'),
                    details=error_data.get('meta')
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

    def _check_api_success(self, response_data: Any, status_code: int = 200) -> None:
        """Check if API response indicates failure even with 2xx status.

        The WIIL API may return HTTP 200 with success=false for logical errors.
        This method checks for that condition and raises WiilAPIError.

        Args:
            response_data: Parsed JSON response data
            status_code: HTTP status code for error reporting

        Raises:
            WiilAPIError: When response has success=false
        """
        if isinstance(response_data, dict) and response_data.get('success') is False:
            # Extract error fields from flat structure (matches TypeScript SDK)
            raise WiilAPIError(
                message=response_data.get('message', 'Request failed'),
                status_code=response_data.get('status', status_code),
                code=response_data.get('code', 'API_ERROR'),
                details=response_data.get('meta')
            )

    def _to_attr_obj(self, value: Any) -> Any:
        """Recursively convert dict payloads into attribute-accessible mappings."""
        if isinstance(value, dict):
            return AttrDict({k: self._to_attr_obj(v) for k, v in value.items()})
        if isinstance(value, list):
            return [self._to_attr_obj(item) for item in value]
        return value

    def _validate_response_json(self, model: Type[T], data: Any) -> T:
        """Validate response JSON while tolerating additive API fields.

        The reference TypeScript schemas use Zod objects, which strip unknown
        keys by default. Request validation remains strict in the HTTP verb
        methods; this response-only path mirrors the reference behavior for
        forward-compatible reads.
        """
        payload = json.dumps(data)
        try:
            return model.model_validate_json(payload, extra="ignore")
        except TypeError as exc:
            if "extra" not in str(exc):
                raise
            return model.model_validate_json(payload)

    def _parse_response(
        self,
        data: Any,
        response_model: Optional[Type[T]] = None
    ) -> Union[T, Any]:
        """Parse response data into a Pydantic model if specified.

        Args:
            data: Raw response data (dict or list)
            response_model: Optional Pydantic model type to parse into

        Returns:
            Parsed model instance(s) or raw AttrDict if no model specified

        Raises:
            WiilValidationError: When response validation fails
        """
        if response_model is None:
            return self._to_attr_obj(data)

        # Handle None data - return None for Optional types
        if data is None:
            return None

        # Handle primitive types (bool, int, str, etc.) that don't have model_validate
        if response_model in (bool, int, str, float):
            return data

        try:
            # Validate in JSON mode so wire-format values (e.g. string enum
            # members) are accepted. Unknown response keys are ignored to match
            # ref-core Zod object parsing, which strips additive fields by
            # default. The data originates from response.json(), so re-encoding
            # is lossless for JSON-native types.
            # Handle List[Model] types
            origin = get_origin(response_model)
            if origin is list:
                args = get_args(response_model)
                if args and isinstance(data, list):
                    item_model = args[0]
                    return [
                        self._validate_response_json(item_model, item)
                        for item in data
                    ]

            # Handle single model
            if isinstance(data, list):
                return [
                    self._validate_response_json(response_model, item)
                    for item in data
                ]

            return self._validate_response_json(response_model, data)

        except ValidationError as e:
            raise WiilValidationError(
                'Response validation failed',
                details=e.errors()
            )

    def __del__(self):
        """Close the session when the client is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()


class AttrDict(dict):
    """Dictionary wrapper that allows attribute-style access."""

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError as exc:
            raise AttributeError(key) from exc


__all__ = ['HttpClient']
