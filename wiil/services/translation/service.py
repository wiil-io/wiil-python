"""Translation service operations."""

from typing import Dict, Union

from pydantic import ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.services.translation.models import (
    TranslationConnectionConfig,
    TranslationRequest,
)


TRANSLATION_CONNECTION_RESOURCE_PATH = "/translation/provision"


class TranslationService:
    """Service class for translation connection workflows."""

    def __init__(self, http: HttpClient):
        self._http = http

    def create_connection_config(
        self,
        request: Union[TranslationRequest, Dict[str, object]],
    ) -> TranslationConnectionConfig:
        """Create a translation connection configuration."""
        try:
            validated_request = (
                request
                if isinstance(request, TranslationRequest)
                else TranslationRequest.model_validate(request)
            )
        except ValidationError as exc:
            raise WiilValidationError(
                "Invalid translation request payload.",
                exc.errors(),
            )

        response = self._http.post(
            TRANSLATION_CONNECTION_RESOURCE_PATH,
            validated_request.model_dump(by_alias=True, exclude_none=True),
            schema=TranslationRequest,
        )

        try:
            return TranslationConnectionConfig.model_validate(response)
        except ValidationError as exc:
            raise WiilValidationError(
                "Response validation failed for translation connection configuration.",
                exc.errors(),
            )
