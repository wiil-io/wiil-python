"""WIIL SDK client for outbound communication and real-time services."""

from urllib.parse import urlparse

from wiil.client.http_client import HttpClient
from wiil.client.types import WiilClientConfig
from wiil.errors import WiilConfigurationError
from wiil.services import MessagingService, OttService, TranslationService


DEFAULT_OTT_BASE_URL = "https://ott.wiil.io"
DEFAULT_API_BASE_URL = "https://api.wiil.io/v1"
DEFAULT_TIMEOUT = 30


class WiilService:
    """WIIL SDK client for outbound communication and real-time services.

    Provides access to messaging (calls, SMS, email), translation sessions,
    and OTT connection services for AI-powered customer interactions.

    Example:
        >>> from wiil import WiilService
        >>>
        >>> service = WiilService(api_key="your-api-key")
        >>>
        >>> # Request an outbound call
        >>> service.messaging.request_call({...})
        >>>
        >>> # Send an SMS
        >>> service.messaging.send_sms({...})
        >>>
        >>> # Send an email
        >>> service.messaging.send_email({...})
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_OTT_BASE_URL,
        api_base_url: str = DEFAULT_API_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self._validate_config(api_key, base_url, api_base_url, timeout)

        self.config = WiilClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )

        self._http = HttpClient(self.config)
        self._api_http = HttpClient(
            WiilClientConfig(
                api_key=api_key,
                base_url=api_base_url,
                timeout=timeout,
            )
        )
        self.translation = TranslationService(self._http)
        self.ott = OttService(self._http)
        self.messaging = MessagingService(self._api_http)

    def get(self, path: str, **kwargs):
        """Make a GET request for service endpoints."""
        return self._http.get(path, **kwargs)

    def post(self, path: str, data, schema=None, **kwargs):
        """Make a POST request for service endpoints."""
        return self._http.post(path, data, schema=schema, **kwargs)

    def put(self, path: str, data, schema=None, **kwargs):
        """Make a PUT request for service endpoints."""
        return self._http.put(path, data, schema=schema, **kwargs)

    def patch(self, path: str, data, schema=None, **kwargs):
        """Make a PATCH request for service endpoints."""
        return self._http.patch(path, data, schema=schema, **kwargs)

    def delete(self, path: str, **kwargs):
        """Make a DELETE request for service endpoints."""
        return self._http.delete(path, **kwargs)

    @staticmethod
    def _validate_config(
        api_key: str,
        base_url: str,
        api_base_url: str,
        timeout: int,
    ) -> None:
        """Validate service configuration."""
        if not api_key:
            raise WiilConfigurationError(
                "API key is required. Please provide a valid API key "
                "in the configuration."
            )

        if not api_key.strip():
            raise WiilConfigurationError(
                "API key cannot be empty. Please provide a valid API key."
            )

        try:
            result = urlparse(base_url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL structure")
        except Exception:
            raise WiilConfigurationError(
                f"Invalid base URL: {base_url}. Please provide a valid URL."
            )

        try:
            result = urlparse(api_base_url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL structure")
        except Exception:
            raise WiilConfigurationError(
                f"Invalid API base URL: {api_base_url}. Please provide a valid URL."
            )

        if timeout <= 0:
            raise WiilConfigurationError(
                "Timeout must be a positive number in seconds."
            )


__all__ = ["WiilService"]
