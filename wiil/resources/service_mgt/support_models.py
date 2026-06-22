"""Support Models resource for accessing LLM model configurations.

This module provides the SupportModelsResource class for accessing support model
configurations in the WIIL Platform API.

Example:
    >>> from wiil import WiilClient
    >>> client = WiilClient(api_key='your-api-key')
    >>> model = client.support_models.get('gpt-4-turbo')
    >>> print(model.name)
    >>> tts_model = client.support_models.get_default_tts()
"""

from typing import Optional

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt.support_llm import WiilSupportModel
from wiil.types import PaginatedResult


class SupportModelsResource:
    """Resource class for accessing support model configurations in the WIIL Platform.

    This resource provides methods for retrieving LLM model configurations, including
    default models for various capabilities (TTS, STT, multi-mode, etc.) and internal
    lookup methods. The Support Model Registry maintains a curated list of LLM models
    from various providers (OpenAI, Anthropic, etc.) with their capabilities, supported
    languages, and voices. This is a read-only resource.

    Example:
        >>> client = WiilClient(api_key='your-api-key')
        >>>
        >>> # Get a support model by ID
        >>> model = client.support_models.get('USIEJD12345')
        >>> print('Model:', model.name)
        >>> print('Proprietor:', model.proprietor)
        >>>
        >>> # List all support models
        >>> result = client.support_models.list()
        >>> print(f"Found {result.meta.total_count} models")
        >>>
        >>> # Get default TTS model
        >>> tts_model = client.support_models.get_default_tts()
        >>> if tts_model:
        ...     print('Default TTS:', tts_model.name)
    """

    def __init__(self, http: HttpClient):
        """Initialize the support models resource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._base_path = '/support-models'

    def get(self, model_id: str) -> WiilSupportModel:
        """Retrieve a support model by Wiil model ID.

        Args:
            model_id: Wiil unique model identifier (not the provider's model ID)

        Returns:
            The support model configuration

        Raises:
            WiilAPIError: When the model is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> # Get model by Wiil model ID
            >>> model = client.support_models.get('wiil-model-id-123')
            >>> print('Model:', model.name)
            >>> print('Proprietor:', model.proprietor)
            >>> print('Provider Model ID:', model.provider_model_id)
            >>> print('Type:', model.type)
            >>> print('Discontinued:', model.discontinued)
        """
        return self._http.get(f'{self._base_path}/{model_id}', response_model=WiilSupportModel)

    def list(self) -> PaginatedResult[WiilSupportModel]:
        """List all support models in the registry.

        Returns:
            Paginated list of all support models

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> result = client.support_models.list()
            >>> print(f"Found {result.meta.total_count} models")
            >>> for model in result.data:
            ...     print(f"- {model.name} ({model.proprietor})")
        """
        return self._http.get(self._base_path, response_model=PaginatedResult[WiilSupportModel])

    def get_default_multi_mode(self) -> Optional[WiilSupportModel]:
        """Retrieve the default multi-mode model.

        Returns:
            The default multi-mode model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_multi_mode()
            >>> if model:
            ...     print('Default multi-mode model:', model.name)
        """
        return self._http.get(f'{self._base_path}/defaults/multi-mode', response_model=WiilSupportModel)

    def get_default_sts(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Speech-to-Speech model.

        Returns:
            The default STS model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_sts()
            >>> if model:
            ...     print('Default STS model:', model.name)
        """
        return self._http.get(f'{self._base_path}/defaults/sts', response_model=WiilSupportModel)

    def get_default_tts(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Text-to-Speech model.

        Returns:
            The default TTS model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_tts()
            >>> if model:
            ...     print('Default TTS model:', model.name)
            ...     if model.supported_voices:
            ...         print(f"Supported voices: {len(model.supported_voices)}")
        """
        return self._http.get(f'{self._base_path}/defaults/tts', response_model=WiilSupportModel)

    def get_default_stt(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Speech-to-Text model.

        Returns:
            The default STT model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_stt()
            >>> if model:
            ...     print('Default STT model:', model.name)
            ...     if model.support_languages:
            ...         print(f"Supported languages: {len(model.support_languages)}")
        """
        return self._http.get(f'{self._base_path}/defaults/stt', response_model=WiilSupportModel)

    def get_default_transcribe(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Transcription model.

        Returns:
            The default transcription model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_transcribe()
            >>> if model:
            ...     print('Default transcription model:', model.name)
        """
        return self._http.get(f'{self._base_path}/defaults/transcribe', response_model=WiilSupportModel)

    def get_default_batch(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Batch processing model.

        Returns:
            The default batch model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_batch()
            >>> if model:
            ...     print('Default batch model:', model.name)
        """
        return self._http.get(f'{self._base_path}/defaults/batch', response_model=WiilSupportModel)

    def get_default_translation_stt(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Translation Speech-to-Text model.

        Returns:
            The default translation STT model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_translation_stt()
            >>> if model:
            ...     print('Default translation STT model:', model.name)
        """
        return self._http.get(f'{self._base_path}/defaults/translation-stt', response_model=WiilSupportModel)

    def get_default_translation_tts(self) -> Optional[WiilSupportModel]:
        """Retrieve the default Translation Text-to-Speech model.

        Returns:
            The default translation TTS model or None if not configured

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_default_translation_tts()
            >>> if model:
            ...     print('Default translation TTS model:', model.name)
        """
        return self._http.get(f'{self._base_path}/defaults/translation-tts', response_model=WiilSupportModel)

    def get_by_type_and_proprietor(
        self,
        type: str,
        proprietor: str
    ) -> Optional[WiilSupportModel]:
        """Retrieve a model by LLM type and proprietor (internal lookup method).

        Args:
            type: LLM type (e.g., 'TEXT', 'VOICE', 'MULTI_MODE')
            proprietor: Model proprietor (e.g., 'OPENAI', 'ANTHROPIC')

        Returns:
            The matching model or None if not found

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_by_type_and_proprietor('TEXT', 'OPENAI')
            >>> if model:
            ...     print('Found model:', model.name)
        """
        return self._http.get(
            f'{self._base_path}/lookup/type-proprietor/{type}/{proprietor}',
            response_model=WiilSupportModel
        )

    def get_by_proprietor_and_provider_model_id(
        self,
        proprietor: str,
        provider_model_id: str
    ) -> Optional[WiilSupportModel]:
        """Retrieve a model by proprietor and provider model ID (internal lookup method).

        Args:
            proprietor: Model proprietor (e.g., 'OPENAI', 'ANTHROPIC')
            provider_model_id: Provider-specific model identifier (e.g., 'gpt-4-1106-preview')

        Returns:
            The matching model or None if not found

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> model = client.support_models.get_by_proprietor_and_provider_model_id(
            ...     'OPENAI',
            ...     'gpt-4-1106-preview'
            ... )
            >>> if model:
            ...     print('Found model:', model.name)
            ...     print('Wiil Model ID:', model.model_id)
        """
        return self._http.get(
            f'{self._base_path}/lookup/proprietor-provider/{proprietor}/{provider_model_id}',
            response_model=WiilSupportModel
        )

    def is_supported(
        self,
        proprietor: str,
        provider_model_id: str
    ) -> bool:
        """Check if a model is supported by proprietor and provider model ID.

        Args:
            proprietor: Model proprietor (e.g., 'OpenAI', 'Anthropic', 'Deepgram')
            provider_model_id: Provider-specific model identifier (e.g., 'gpt-4-turbo')

        Returns:
            True if the model is supported, False otherwise

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> # Check if a specific model is supported
            >>> is_supported = client.support_models.is_supported('OpenAI', 'gpt-4-turbo')
            >>> if is_supported:
            ...     print('Model is supported')
            >>> else:
            ...     print('Model is not supported')
        """
        return self._http.get(
            f'{self._base_path}/supports/{proprietor}/{provider_model_id}',
            response_model=bool
        )


__all__ = ['SupportModelsResource']
