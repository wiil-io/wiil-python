"""Tests for Provisioning Configurations resource (Translation Chains)."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.service_mgt import (
    CreateTranslationChainConfig,
    UpdateTranslationChainConfig,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProvisioningConfigurationsResource:
    """Test suite for ProvisioningConfigurationsResource (Translation Chains)."""

    def test_create_translation_chain_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new translation chain configuration."""
        mock_response = {
            "id": "trans_123",
            "chainName": "spanish-english-translation",
            "description": "Spanish to English translation chain",
            "sttConfig": {
                "modelId": "model_stt_1",
                "defaultLanguage": "es",
            },
            "processingModelId": "model_proc_1",
            "ttsConfig": {
                "modelId": "model_tts_1",
                "defaultLanguage": "en-US",
                "voiceId": "adam",
            },
            "isTranslation": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        # Mock support model validation calls
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/supports/Deepgram/nova-2",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/supports/OpenAI/gpt-4o-mini",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/support-models/supports/ElevenLabs/eleven_multilingual_v2",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.create(CreateTranslationChainConfig(
            chain_name="spanish-english-translation",
            description="Spanish to English translation chain",
            stt_config={
                "provider_type": "Deepgram",
                "provider_model_id": "nova-2",
                "language_id": "es",
            },
            processing_config={
                "provider_type": "OpenAI",
                "provider_model_id": "gpt-4o-mini",
            },
            tts_config={
                "provider_type": "ElevenLabs",
                "provider_model_id": "eleven_multilingual_v2",
                "language_id": "en-US",
                "voice_id": "adam",
            }
        ))

        assert result.id == "trans_123"
        assert result.chain_name == "spanish-english-translation"

    def test_get_translation_chain_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a translation chain configuration by ID."""
        mock_response = {
            "id": "trans_123",
            "chainName": "spanish-english-translation",
            "description": "Spanish to English translation chain",
            "sttConfig": {
                "modelId": "model_stt_1",
                "defaultLanguage": "es",
            },
            "processingModelId": "model_proc_1",
            "ttsConfig": {
                "modelId": "model_tts_1",
                "defaultLanguage": "en-US",
                "voiceId": "adam",
            },
            "isTranslation": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/trans_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.get("trans_123")

        assert result.id == "trans_123"
        assert result.chain_name == "spanish-english-translation"

    def test_get_translation_chain_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when translation chain configuration not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Translation chain configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.provisioning_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_translation_chain_configuration_by_chain_name(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a translation chain configuration by chain name."""
        mock_response = {
            "id": "trans_123",
            "chainName": "spanish-english-translation",
            "description": "Spanish to English translation chain",
            "sttConfig": {
                "modelId": "model_stt_1",
                "defaultLanguage": "es",
            },
            "processingModelId": "model_proc_1",
            "ttsConfig": {
                "modelId": "model_tts_1",
                "defaultLanguage": "en-US",
                "voiceId": "adam",
            },
            "isTranslation": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/by-chain-name/spanish-english-translation",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.get_by_chain_name("spanish-english-translation")

        assert result.id == "trans_123"
        assert result.chain_name == "spanish-english-translation"

    def test_update_translation_chain_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a translation chain configuration."""
        mock_response = {
            "id": "trans_123",
            "chainName": "spanish-english-translation",
            "description": "Updated translation chain",
            "sttConfig": {
                "modelId": "model_stt_1",
                "defaultLanguage": "es",
            },
            "processingModelId": "model_proc_1",
            "ttsConfig": {
                "modelId": "model_tts_1",
                "defaultLanguage": "en-US",
                "voiceId": "adam",
            },
            "isTranslation": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/provisioning-configurations/trans_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.update(UpdateTranslationChainConfig(
            id="trans_123",
            description="Updated translation chain"
        ))

        assert result.description == "Updated translation chain"
        assert result.updated_at == 1234567891

    def test_delete_translation_chain_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a translation chain configuration."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/provisioning-configurations/trans_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.provisioning_configs.delete("trans_123")

        assert result is True

    def test_delete_translation_chain_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when deleting non-existent translation chain config."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/provisioning-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Translation chain configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.provisioning_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_translation_chain_configurations(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing translation chain configurations with pagination."""
        mock_configs = [
            {
                "id": "trans_1",
                "chainName": "spanish-english",
                "description": "Spanish to English",
                "sttConfig": {
                    "modelId": "model_stt_1",
                    "defaultLanguage": "es",
                },
                "processingModelId": "model_proc_1",
                "ttsConfig": {
                    "modelId": "model_tts_1",
                    "defaultLanguage": "en-US",
                    "voiceId": "adam",
                },
                "isTranslation": True,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "trans_2",
                "chainName": "french-english",
                "description": "French to English",
                "sttConfig": {
                    "modelId": "model_stt_2",
                    "defaultLanguage": "fr",
                },
                "processingModelId": "model_proc_2",
                "ttsConfig": {
                    "modelId": "model_tts_2",
                    "defaultLanguage": "en-US",
                    "voiceId": "rachel",
                },
                "isTranslation": True,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_configs,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 2,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/translations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_translation_chain_configurations_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing translation chain configs with pagination parameters."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 2,
                "pageSize": 50,
                "totalCount": 100,
                "totalPages": 2,
                "hasNextPage": False,
                "hasPreviousPage": True,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/translations?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True

    def test_list_translation_chain_configurations_with_include_deleted(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing translation chain configs including deleted items."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 5,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/translations?includeDeleted=true",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list(include_deleted=True)

        assert result.meta.total_count == 5
