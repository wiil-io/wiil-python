"""Tests for Agent Configurations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.service_mgt import (
    CreateAgentConfiguration,
    UpdateAgentConfiguration,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestAgentConfigurationsResource:
    """Test suite for AgentConfigurationsResource."""

    def test_create_agent_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new agent configuration."""
        mock_response = {
            "id": "agent_123",
            "modelId": "YUSI21217J1",
            "name": "Customer Service Agent",
            "defaultFunctionState": "multi_mode",
            "usesWiilSupportModel": True,
            "requiredModelConfig": None,
            "instructionConfigurationId": "inst_789",
            "assistantType": "general",
            "call_transfer_config": [],
            "metadata": None,
            "model": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/agent-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.agent_configs.create(CreateAgentConfiguration(
            name="Customer Service Agent",
            model_id="YUSI21217J1",
            instruction_configuration_id="inst_789",
        ))

        assert result.id == "agent_123"
        assert result.name == "Customer Service Agent"
        assert result.model_id == "YUSI21217J1"

    def test_get_agent_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving an agent configuration by ID."""
        mock_response = {
            "id": "agent_123",
            "modelId": "YUSI21217J1",
            "name": "Customer Service Agent",
            "defaultFunctionState": "multi_mode",
            "usesWiilSupportModel": True,
            "requiredModelConfig": None,
            "instructionConfigurationId": "inst_789",
            "assistantType": "general",
            "call_transfer_config": [],
            "metadata": None,
            "model": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/agent-configurations/agent_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.agent_configs.get("agent_123")

        assert result.id == "agent_123"
        assert result.name == "Customer Service Agent"
        assert result.model_id == "YUSI21217J1"
        assert result.instruction_configuration_id == "inst_789"

    def test_get_agent_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when agent configuration not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/agent-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Agent configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.agent_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_update_agent_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating an agent configuration."""
        mock_response = {
            "id": "agent_123",
            "modelId": "YUSI21217J1",
            "name": "Updated Agent Name",
            "defaultFunctionState": "multi_mode",
            "usesWiilSupportModel": True,
            "requiredModelConfig": None,
            "instructionConfigurationId": "inst_789",
            "assistantType": "general",
            "call_transfer_config": [],
            "metadata": {"description": "Updated description"},
            "model": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/agent-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.agent_configs.update(UpdateAgentConfiguration(
            id="agent_123",
            name="Updated Agent Name"
        ))

        assert result.name == "Updated Agent Name"
        assert result.updated_at == 1234567891

    def test_delete_agent_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting an agent configuration."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/agent-configurations/agent_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.agent_configs.delete("agent_123")

        assert result is True

    def test_delete_agent_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when deleting non-existent agent configuration."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/agent-configurations/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Agent configuration not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.agent_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_agent_configurations(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing agent configurations with pagination."""
        mock_configs = [
            {
                "id": "agent_1",
                "modelId": "YUSI21217J1",
                "name": "Agent 1",
                "defaultFunctionState": "multi_mode",
                "usesWiilSupportModel": True,
                "requiredModelConfig": None,
                "instructionConfigurationId": "inst_101",
                "assistantType": "general",
                "call_transfer_config": [],
                "metadata": None,
                "model": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "agent_2",
                "modelId": "YUSI21217J2",
                "name": "Agent 2",
                "defaultFunctionState": "text",
                "usesWiilSupportModel": True,
                "requiredModelConfig": None,
                "instructionConfigurationId": "inst_102",
                "assistantType": "phone",
                "call_transfer_config": [],
                "metadata": None,
                "model": None,
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
            f"{BASE_URL}/agent-configurations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.agent_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1
        assert result.data[0].name == "Agent 1"
        assert result.data[1].assistant_type == "phone"

    def test_list_agent_configurations_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing agent configurations with custom pagination parameters."""
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
            f"{BASE_URL}/agent-configurations?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.agent_configs.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
