"""Tests for Provisioning Configurations resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProvisioningConfigurationsResource:
    """Test suite for ProvisioningConfigurationsResource."""

    def test_create_provisioning_configuration(self, client: WiilClient, mock_api, api_response):
        """Test creating a new provisioning configuration chain."""
        input_data = {
            "chain_name": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "processing_steps": ["transcription", "analysis", "response"],
        }

        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "processingSteps": ["transcription", "analysis", "response"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.create(**input_data)

        assert result.id == "prov_123"
        assert result.chain_name == "main-processing-chain"

    def test_create_translation_chain(self, client: WiilClient, mock_api, api_response):
        """Test creating a new translation configuration chain."""
        input_data = {
            "chain_name": "translation-chain",
            "description": "Translation chain for multilingual support",
            "source_language": "en",
            "target_languages": ["es", "fr", "de"],
        }

        mock_response = {
            "id": "trans_123",
            "chainName": "translation-chain",
            "description": "Translation chain for multilingual support",
            "sourceLanguage": "en",
            "targetLanguages": ["es", "fr", "de"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.create_translation(**input_data)

        assert result.id == "trans_123"
        assert result.chain_name == "translation-chain"

    def test_get_provisioning_configuration(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a provisioning configuration by ID."""
        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "processingSteps": ["transcription", "analysis", "response"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/prov_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.get("prov_123")

        assert result.id == "prov_123"
        assert result.chain_name == "main-processing-chain"

    def test_get_provisioning_configuration_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when provisioning configuration not found."""
        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Provisioning configuration not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.provisioning_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_provisioning_configuration_by_chain_name(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a provisioning configuration by chain name."""
        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Main processing chain for customer calls",
            "processingSteps": ["transcription", "analysis", "response"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/by-chain-name/main-processing-chain",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.get_by_chain_name("main-processing-chain")

        assert result.id == "prov_123"
        assert result.chain_name == "main-processing-chain"

    def test_update_provisioning_configuration(self, client: WiilClient, mock_api, api_response):
        """Test updating a provisioning configuration."""
        update_data = {
            "id": "prov_123",
            "description": "Updated processing chain",
            "processing_steps": ["transcription", "analysis", "response", "logging"],
        }

        mock_response = {
            "id": "prov_123",
            "chainName": "main-processing-chain",
            "description": "Updated processing chain",
            "processingSteps": ["transcription", "analysis", "response", "logging"],
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.update(**update_data)

        assert result.description == "Updated processing chain"
        assert len(result.processing_steps) == 4

    def test_delete_provisioning_configuration(self, client: WiilClient, mock_api, api_response):
        """Test deleting a provisioning configuration."""
        mock_api.delete(
            f"{BASE_URL}/provisioning-configurations/prov_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.provisioning_configs.delete("prov_123")

        assert result is True

    def test_delete_provisioning_configuration_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when deleting non-existent provisioning configuration."""
        mock_api.delete(
            f"{BASE_URL}/provisioning-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Provisioning configuration not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.provisioning_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_provisioning_configurations(self, client: WiilClient, mock_api, api_response):
        """Test listing all provisioning configurations with pagination."""
        mock_configs = [
            {
                "id": "prov_1",
                "chainName": "chain-1",
                "description": "Chain 1",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "trans_1",
                "chainName": "translation-1",
                "description": "Translation Chain 1",
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

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_provisioning_configurations_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing provisioning configurations with custom pagination parameters."""
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

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list(page=2, page_size=50)

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True

    def test_list_provisioning_configurations_with_include_deleted(self, client: WiilClient, mock_api, api_response):
        """Test listing provisioning configurations including deleted items."""
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

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations?includeDeleted=true",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list(include_deleted=True)

        assert result.meta.total_count == 5

    def test_list_provisioning_chains(self, client: WiilClient, mock_api, api_response):
        """Test listing provisioning configuration chains."""
        mock_configs = [
            {
                "id": "prov_1",
                "chainName": "chain-1",
                "description": "Processing Chain 1",
                "processingSteps": ["transcription", "analysis"],
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "prov_2",
                "chainName": "chain-2",
                "description": "Processing Chain 2",
                "processingSteps": ["transcription"],
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

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/provisioning",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list_provisioning_chains()

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_list_provisioning_chains_with_pagination(self, client: WiilClient, mock_api, api_response):
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

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/provisioning?page=3&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list_provisioning_chains(page=3, page_size=10)

        assert result.meta.page == 3
        assert result.meta.page_size == 10

    def test_list_translation_chains(self, client: WiilClient, mock_api, api_response):
        """Test listing translation configuration chains."""
        mock_configs = [
            {
                "id": "trans_1",
                "chainName": "translation-1",
                "description": "Translation Chain 1",
                "sourceLanguage": "en",
                "targetLanguages": ["es", "fr"],
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "trans_2",
                "chainName": "translation-2",
                "description": "Translation Chain 2",
                "sourceLanguage": "en",
                "targetLanguages": ["de", "it"],
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

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/translations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list_translation_chains()

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_list_translation_chains_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing translation chains with pagination."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 2,
                "pageSize": 25,
                "totalCount": 30,
                "totalPages": 2,
                "hasNextPage": False,
                "hasPreviousPage": True,
            },
        }

        mock_api.get(
            f"{BASE_URL}/provisioning-configurations/translations?page=2&pageSize=25",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.provisioning_configs.list_translation_chains(page=2, page_size=25)

        assert result.meta.page == 2
        assert result.meta.page_size == 25
        assert result.meta.has_previous_page is True
