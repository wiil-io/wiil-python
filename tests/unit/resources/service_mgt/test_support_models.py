"""Tests for Support Models resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestSupportModelsResource:
    """Test suite for SupportModelsResource."""

    def test_get_support_model(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a support model by ID."""
        mock_response = {
            "modelId": "model_123",
            "name": "GPT-4 Turbo",
            "provider_model_id": "gpt-4-1106-preview",
            "proprietor": "OpenAI",
            "description": "Latest GPT-4 model with improved performance",
            "type": "MULTI_MODE",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": [
                {
                    "languageId": "en-us",
                    "name": "English (United States)",
                    "code": "en-US",
                    "isDefault": True,
                    "isExperimental": False,
                },
            ],
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/model_123",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get("model_123")

        assert result.model_id == "model_123"
        assert result.name == "GPT-4 Turbo"
        assert result.proprietor == "OpenAI"

    def test_get_support_model_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when support model not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response("NOT_FOUND", "Support model not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.support_models.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_list_support_models(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing all support models."""
        mock_models = [
            {
                "modelId": "model_1",
                "name": "GPT-4 Turbo",
                "provider_model_id": "gpt-4-1106-preview",
                "proprietor": "OpenAI",
                "description": "Latest GPT-4 model with improved performance",
                "type": "MULTI_MODE",
                "discontinued": False,
                "supportedVoices": None,
                "supportLanguages": [
                    {
                        "languageId": "en-us",
                        "name": "English (United States)",
                        "code": "en-US",
                        "isDefault": True,
                        "isExperimental": False,
                    },
                ],
            },
            {
                "modelId": "model_2",
                "name": "Claude Sonnet 4",
                "provider_model_id": "claude-sonnet-4",
                "proprietor": "Anthropic",
                "description": "Anthropic Claude Sonnet 4 model",
                "type": "TEXT_PROCESSING",
                "discontinued": False,
                "supportedVoices": None,
                "supportLanguages": [
                    {
                        "languageId": "en-us",
                        "name": "English (United States)",
                        "code": "en-US",
                        "isDefault": True,
                        "isExperimental": False,
                    },
                ],
            },
        ]

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_models),
            status=200,
        )

        result = client.support_models.list()

        assert len(result) == 2
        assert result[0].name == "GPT-4 Turbo"
        assert result[1].name == "Claude Sonnet 4"

    def test_get_default_multi_mode(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default multi-mode model."""
        mock_response = {
            "modelId": "model_multi",
            "name": "GPT-4 Omni",
            "provider_model_id": "gpt-4o",
            "proprietor": "OpenAI",
            "description": "GPT-4 Omni multimodal model",
            "type": "MULTI_MODE",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/multi-mode",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_multi_mode()

        assert result.type == "MULTI_MODE"
        assert result.name == "GPT-4 Omni"

    def test_get_default_sts(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default STS model."""
        mock_response = {
            "modelId": "model_sts",
            "name": "OpenAI STS Model",
            "provider_model_id": "sts-1",
            "proprietor": "OpenAI",
            "description": "OpenAI Speech-to-Speech model",
            "type": "STS",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/sts",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_sts()

        assert result.type == "STS"

    def test_get_default_tts(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default TTS model."""
        mock_response = {
            "modelId": "model_tts",
            "name": "ElevenLabs TTS",
            "provider_model_id": "eleven-multilingual-v2",
            "proprietor": "ElevenLabs",
            "description": "ElevenLabs multilingual TTS model",
            "type": "TTS",
            "discontinued": False,
            "supportedVoices": [
                {
                    "voiceId": "adam",
                    "name": "Adam",
                    "description": "Deep male voice",
                    "gender": "male",
                    "language": "en-US",
                    "isDefault": True,
                },
                {
                    "voiceId": "bella",
                    "name": "Bella",
                    "description": "Warm female voice",
                    "gender": "female",
                    "language": "en-US",
                    "isDefault": False,
                },
            ],
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/tts",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_tts()

        assert result.type == "TTS"
        assert len(result.supported_voices) == 2

    def test_get_default_stt(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default STT model."""
        mock_response = {
            "modelId": "model_stt",
            "name": "Deepgram Nova 2",
            "provider_model_id": "nova-2",
            "proprietor": "Deepgram",
            "description": "Deepgram Nova 2 STT model",
            "type": "STT",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": [
                {
                    "languageId": "en-us",
                    "name": "English (United States)",
                    "code": "en-US",
                    "isDefault": True,
                    "isExperimental": False,
                },
            ],
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/stt",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_stt()

        assert result.type == "STT"
        assert result.proprietor == "Deepgram"

    def test_get_default_transcribe(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default transcription model."""
        mock_response = {
            "modelId": "model_transcribe",
            "name": "Whisper Large V3",
            "provider_model_id": "whisper-large-v3",
            "proprietor": "OpenAI",
            "description": "OpenAI Whisper Large V3 transcription model",
            "type": "TRANSCRIBE",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/transcribe",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_transcribe()

        assert result.type == "TRANSCRIBE"

    def test_get_default_batch(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default batch model."""
        mock_response = {
            "modelId": "model_batch",
            "name": "GPT-4 Turbo Batch",
            "provider_model_id": "gpt-4-turbo-batch",
            "proprietor": "OpenAI",
            "description": "GPT-4 Turbo batch processing model",
            "type": "TEXT_PROCESSING",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/batch",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_batch()

        assert result.model_id == "model_batch"

    def test_get_default_translation_stt(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default translation STT model."""
        mock_response = {
            "modelId": "model_trans_stt",
            "name": "Translation STT Model",
            "provider_model_id": "translation-stt-1",
            "proprietor": "Deepgram",
            "description": "Deepgram translation-optimized STT model",
            "type": "STT",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/translation-stt",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_translation_stt()

        assert result.model_id == "model_trans_stt"

    def test_get_default_translation_tts(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving the default translation TTS model."""
        mock_response = {
            "modelId": "model_trans_tts",
            "name": "Translation TTS Model",
            "provider_model_id": "translation-tts-1",
            "proprietor": "ElevenLabs",
            "description": "ElevenLabs translation-optimized TTS model",
            "type": "TTS",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/defaults/translation-tts",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_default_translation_tts()

        assert result.model_id == "model_trans_tts"

    def test_get_by_type_and_proprietor(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a model by type and proprietor."""
        mock_response = {
            "modelId": "model_123",
            "name": "Claude Sonnet 4",
            "provider_model_id": "claude-sonnet-4",
            "proprietor": "Anthropic",
            "description": "Anthropic Claude Sonnet 4 model",
            "type": "TEXT_PROCESSING",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/lookup/type-proprietor/TEXT_PROCESSING/Anthropic",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_by_type_and_proprietor(
            "TEXT_PROCESSING",
            "Anthropic"
        )

        assert result.proprietor == "Anthropic"

    def test_get_by_proprietor_and_provider_model_id(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a model by proprietor and provider model ID."""
        mock_response = {
            "modelId": "model_123",
            "name": "Gemini 2.0 Flash",
            "provider_model_id": "gemini-2.0-flash-exp",
            "proprietor": "Google",
            "description": "Google Gemini 2.0 Flash model",
            "type": "MULTI_MODE",
            "discontinued": False,
            "supportedVoices": None,
            "supportLanguages": None,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/lookup/proprietor-provider/Google/gemini-2.0-flash-exp",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.support_models.get_by_proprietor_and_provider_model_id(
            "Google",
            "gemini-2.0-flash-exp"
        )

        assert result.provider_model_id == "gemini-2.0-flash-exp"
        assert result.proprietor == "Google"
