"""Tests for Provisioning Configurations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    UpdateProvisioningConfig,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProvisioningConfigurationsResource:
    """Test suite for ProvisioningConfigurationsResource."""

    def test_create_provisioning_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new provisioning configuration chain."""
        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "sttConfig": {
                "modelId": "whisper-v3",
                "defaultLanguage": "en-US",
            },
            "ttsConfig": {
                "modelId": "eleven-labs-v2",
                "voiceId": "adam",
                "defaultLanguage": "en-US",
                "voiceSettings": None,
            },
            "agentConfigurationId": "agent_456",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.create(CreateProvisioningConfig(
            chain_name="main-processing-chain",
            description="Main processing chain for customer calls",
            stt_config={
                "provider_type": "Deepgram",
                "provider_model_id": "nova-2",
                "language_id": "en",
            },
            processing_config={
                "provider_type": "OpenAI",
                "provider_model_id": "gpt-4o-mini",
            },
            tts_config={
                "provider_type": "ElevenLabs",
                "provider_model_id": "eleven_multilingual_v2",
                "language_id": "en",
                "voice_id": "adam",
            }
        ))

        assert result.id == "prov_123"
        assert result.chain_name == "main-processing-chain"


    def test_get_provisioning_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a provisioning configuration by ID."""
        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "sttConfig": {
                "modelId": "whisper-v3",
                "defaultLanguage": "en-US",
            },
            "ttsConfig": {
                "modelId": "eleven-labs-v2",
                "voiceId": "adam",
                "defaultLanguage": "en-US",
                "voiceSettings": None,
            },
            "agentConfigurationId": "agent_456",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/prov_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.get("prov_123")

        assert result.id == "prov_123"
        assert result.chain_name == "main-processing-chain"

    def test_get_provisioning_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when provisioning configuration not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Provisioning configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.provisioning_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_provisioning_configuration_by_chain_name(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a provisioning configuration by chain name."""
        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "sttConfig": {
                "modelId": "whisper-v3",
                "defaultLanguage": "en-US",
            },
            "ttsConfig": {
                "modelId": "eleven-labs-v2",
                "voiceId": "adam",
                "defaultLanguage": "en-US",
                "voiceSettings": None,
            },
            "agentConfigurationId": "agent_456",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/by-chain-name/main-processing-chain",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.get_by_chain_name("main-processing-chain")

        assert result.id == "prov_123"
        assert result.chain_name == "main-processing-chain"

    def test_update_provisioning_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a provisioning configuration."""
        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Updated processing chain",
            "sttConfig": {
                "modelId": "whisper-v3",
                "defaultLanguage": "en-US",
            },
            "ttsConfig": {
                "modelId": "eleven-labs-v2",
                "voiceId": "adam",
                "defaultLanguage": "en-US",
                "voiceSettings": None,
            },
            "agentConfigurationId": "agent_456",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.update(UpdateProvisioningConfig(
            id="prov_123",
            description="Updated processing chain"
        ))

        assert result.description == "Updated processing chain"
        assert result.updated_at == 1234567891

    def test_delete_provisioning_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a provisioning configuration."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/provisioning-configurations/prov_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.provisioning_configs.delete("prov_123")

        assert result is True

    def test_delete_provisioning_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when deleting non-existent provisioning config."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/provisioning-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Provisioning configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.provisioning_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_provisioning_configurations(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing all provisioning configurations with pagination."""
        mock_configs = [
            {
                "id": "prov_1",
                "chainName": "chain-1",
                "description": "Chain 1",
                "sttConfig": {
                    "modelId": "whisper-v3",
                    "defaultLanguage": "en-US",
                },
                "ttsConfig": {
                    "modelId": "eleven-labs-v2",
                    "voiceId": "adam",
                    "defaultLanguage": "en-US",
                    "voiceSettings": None,
                },
                "agentConfigurationId": "agent_001",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "trans_1",
                "chainName": "translation-1",
                "description": "Translation Chain 1",
                "sttConfig": {
                    "modelId": "whisper-v3",
                    "defaultLanguage": "es-ES",
                },
                "ttsConfig": {
                    "modelId": "google-tts-wavenet",
                    "voiceId": "es-neural",
                    "defaultLanguage": "es-ES",
                    "voiceSettings": None,
                },
                "agentConfigurationId": "agent_002",
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
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_provisioning_configurations_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing provisioning configs with pagination parameters."""
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
            f"{BASE_URL}/provisioning-configurations?page=2&pageSize=50",
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

    def test_list_provisioning_configurations_with_include_deleted(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing provisioning configs including deleted items."""
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
            f"{BASE_URL}/provisioning-configurations?includeDeleted=true",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list(include_deleted=True)

        assert result.meta.total_count == 5

    def test_list_provisioning_chains(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing provisioning configuration chains."""
        mock_configs = [
            {
                "id": "prov_1",
                "chainName": "chain-1",
                "description": "Processing Chain 1",
                "sttConfig": {
                    "modelId": "whisper-v3",
                    "defaultLanguage": "en-US",
                },
                "ttsConfig": {
                    "modelId": "eleven-labs-v2",
                    "voiceId": "adam",
                    "defaultLanguage": "en-US",
                    "voiceSettings": None,
                },
                "agentConfigurationId": "agent_001",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "prov_2",
                "chainName": "chain-2",
                "description": "Processing Chain 2",
                "sttConfig": {
                    "modelId": "whisper-v3",
                    "defaultLanguage": "en-US",
                },
                "ttsConfig": {
                    "modelId": "eleven-labs-v2",
                    "voiceId": "rachel",
                    "defaultLanguage": "en-US",
                    "voiceSettings": None,
                },
                "agentConfigurationId": "agent_002",
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
            f"{BASE_URL}/provisioning-configurations/provisioning",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list_provisioning_chains()

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_list_provisioning_chains_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing provisioning chains with pagination."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 3,
                "pageSize": 10,
                "totalCount": 50,
                "totalPages": 5,
                "hasNextPage": True,
                "hasPreviousPage": True,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/provisioning-configurations/provisioning?page=3&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.provisioning_configs.list_provisioning_chains(
            PaginationRequest(page=3, page_size=10)
        )

        assert result.meta.page == 3
        assert result.meta.page_size == 10

