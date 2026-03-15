"""OTT service for fetching chat and voice connection configurations."""

from typing import Dict, Union
from urllib.parse import quote, urlencode

from pydantic import ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.services.ott.models import (
    GetOttConfigurationRequest,
    OttChatConnectionConfig,
    OttVoiceConnectionConfig,
)


CHAT_CONFIG_PATH = "chat-service-config"
VOICE_CONFIG_PATH = "commission-service-agent"


class OttService:
    """Service class for OTT connection configuration operations."""

    def __init__(self, http: HttpClient):
        self._http = http

    def get_chat_connection_configuration(
        self,
        request: Union[GetOttConfigurationRequest, Dict[str, object]],
    ) -> OttChatConnectionConfig:
        """Fetch chat connection configuration."""
        validated_request = self._validate_request(request)
        path = self._build_config_path(CHAT_CONFIG_PATH, validated_request)

        response = self._http.get(path)
        try:
            return OttChatConnectionConfig.model_validate(response)
        except ValidationError as exc:
            raise WiilValidationError(
                "Invalid OTT chat config response payload.",
                exc.errors(),
            )

    def get_voice_connection_configuration(
        self,
        request: Union[GetOttConfigurationRequest, Dict[str, object]],
    ) -> OttVoiceConnectionConfig:
        """Fetch voice connection configuration."""
        validated_request = self._validate_request(request)
        path = self._build_config_path(VOICE_CONFIG_PATH, validated_request)

        response = self._http.get(path)
        try:
            return OttVoiceConnectionConfig.model_validate(response)
        except ValidationError as exc:
            raise WiilValidationError(
                "Invalid OTT voice config response payload.",
                exc.errors(),
            )

    def _validate_request(
        self,
        request: Union[GetOttConfigurationRequest, Dict[str, object]],
    ) -> GetOttConfigurationRequest:
        try:
            if isinstance(request, GetOttConfigurationRequest):
                return request
            return GetOttConfigurationRequest.model_validate(request)
        except ValidationError as exc:
            raise WiilValidationError(
                "Invalid OTT config request payload.",
                exc.errors(),
            )

    @staticmethod
    def _build_config_path(
        endpoint: str,
        request: GetOttConfigurationRequest,
    ) -> str:
        encoded_config_id = quote(request.config_id, safe="")
        base_path = f"/{endpoint}/{encoded_config_id}"

        query_params = {}
        if request.contact and request.contact.email:
            query_params["email"] = request.contact.email
        if request.contact and request.contact.phone:
            query_params["phone"] = request.contact.phone

        if not query_params:
            return base_path

        return f"{base_path}?{urlencode(query_params)}"
