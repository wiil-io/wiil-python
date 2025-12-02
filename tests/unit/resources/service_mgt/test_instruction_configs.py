"""Tests for Instruction Configurations resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestInstructionConfigurationsResource:
    """Test suite for InstructionConfigurationsResource."""

    def test_create_instruction_configuration(self, client: WiilClient, mock_api, api_response):
        """Test creating a new instruction configuration."""
        input_data = {
            "name": "Customer Support Instructions",
            "description": "Instructions for customer support agent",
            "system_prompt": "You are a helpful customer support agent.",
            "knowledge_sources": ["source_1", "source_2"],
        }

        mock_response = {
            "id": "instruction_123",
            "name": "Customer Support Instructions",
            "description": "Instructions for customer support agent",
            "systemPrompt": "You are a helpful customer support agent.",
            "knowledgeSources": ["source_1", "source_2"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/instruction-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.instruction_configs.create(**input_data)

        assert result.id == "instruction_123"
        assert result.name == "Customer Support Instructions"

    def test_get_instruction_configuration(self, client: WiilClient, mock_api, api_response):
        """Test retrieving an instruction configuration by ID."""
        mock_response = {
            "id": "instruction_123",
            "name": "Customer Support Instructions",
            "systemPrompt": "You are a helpful customer support agent.",
            "knowledgeSources": ["source_1", "source_2"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/instruction-configurations/instruction_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.instruction_configs.get("instruction_123")

        assert result.id == "instruction_123"
        assert result.name == "Customer Support Instructions"

    def test_get_instruction_configuration_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when instruction configuration not found."""
        mock_api.get(
            f"{BASE_URL}/instruction-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Instruction configuration not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.instruction_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_update_instruction_configuration(self, client: WiilClient, mock_api, api_response):
        """Test updating an instruction configuration."""
        update_data = {
            "id": "instruction_123",
            "name": "Updated Instructions",
            "description": "Updated description",
            "system_prompt": "You are an updated support agent.",
        }

        mock_response = {
            "id": "instruction_123",
            "name": "Updated Instructions",
            "description": "Updated description",
            "systemPrompt": "You are an updated support agent.",
            "knowledgeSources": ["source_1"],
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/instruction-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.instruction_configs.update(**update_data)

        assert result.name == "Updated Instructions"
        assert result.description == "Updated description"

    def test_delete_instruction_configuration(self, client: WiilClient, mock_api, api_response):
        """Test deleting an instruction configuration."""
        mock_api.delete(
            f"{BASE_URL}/instruction-configurations/instruction_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.instruction_configs.delete("instruction_123")

        assert result is True

    def test_delete_instruction_configuration_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when deleting non-existent instruction configuration."""
        mock_api.delete(
            f"{BASE_URL}/instruction-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Instruction configuration not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.instruction_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_instruction_configurations(self, client: WiilClient, mock_api, api_response):
        """Test listing instruction configurations with pagination."""
        mock_configs = [
            {
                "id": "instruction_1",
                "name": "Instruction 1",
                "systemPrompt": "Prompt 1",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "instruction_2",
                "name": "Instruction 2",
                "systemPrompt": "Prompt 2",
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
            f"{BASE_URL}/instruction-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.instruction_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_instruction_configurations_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing instruction configurations with custom pagination parameters."""
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
            f"{BASE_URL}/instruction-configurations?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.instruction_configs.list(page=2, page_size=50)

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
