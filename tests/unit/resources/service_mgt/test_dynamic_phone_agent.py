"""Tests for Dynamic Phone Agent resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.service_mgt.dynamic_setup import (
    DynamicPhoneAgentSetup,
    UpdateDynamicPhoneAgent,
)
from wiil.types import PaginationRequest


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestDynamicPhoneAgentResource:
    """Test suite for DynamicPhoneAgentResource."""

    def test_create_dynamic_phone_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new dynamic phone agent."""
        mock_response = {
            "id": "setup_123",
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "phoneNumber": "+15551234567",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/dynamic-phone-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.create(DynamicPhoneAgentSetup(
            assistant_name="Customer Service Agent",
            language="en-US",
            capabilities=[],
            phone_configuration_id="phone_config_123"
        ))

        assert result.success is True
        assert result.agent_configuration_id == "agent_123"
        assert result.instruction_configuration_id == "instr_456"
        assert result.phone_number == "+15551234567"

    def test_create_phone_agent_with_stt_tts(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a phone agent with STT and TTS configurations."""
        mock_response = {
            "id": "setup_456",
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_456",
            "instructionConfigurationId": "instr_789",
            "phoneNumber": "+15559876543",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/dynamic-phone-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.create(DynamicPhoneAgentSetup(
            assistant_name="Voice Agent",
            language="en-US",
            capabilities=[],
            phone_configuration_id="phone_config_123",
            stt_configuration={
                "provider_type": "Deepgram",
                "provider_model_id": "nova-2",
                "language_id": "en-US",
            },
            tts_configuration={
                "provider_type": "ElevenLabs",
                "provider_model_id": "eleven_turbo_v2",
                "language_id": "en-US",
                "voice_id": "voice_rachel",
            }
        ))

        assert result.success is True
        assert result.agent_configuration_id == "agent_456"
        assert result.phone_number == "+15559876543"

    def test_get_dynamic_phone_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a dynamic phone agent by ID."""
        mock_response = {
            "id": "setup_123",
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "phoneNumber": "+15551234567",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/dynamic-phone-agent/setup_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.get("setup_123")

        assert result.id == "setup_123"
        assert result.success is True
        assert result.phone_number == "+15551234567"

    def test_get_dynamic_phone_agent_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when dynamic phone agent not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/dynamic-phone-agent/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Dynamic phone agent not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.dynamic_phone_agent.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_update_dynamic_phone_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a dynamic phone agent."""
        mock_response = {
            "id": "setup_123",
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "phoneNumber": "+15551234567",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/dynamic-phone-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.update(UpdateDynamicPhoneAgent(
            id="agent_123",
            assistant_name="Updated Customer Service Agent",
            language="es-MX"
        ))

        assert result.success is True
        assert result.agent_configuration_id == "agent_123"

    def test_delete_dynamic_phone_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a dynamic phone agent."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/dynamic-phone-agent/setup_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.dynamic_phone_agent.delete("setup_123")

        assert result is True

    def test_delete_dynamic_phone_agent_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when deleting non-existent phone agent."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/dynamic-phone-agent/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Dynamic phone agent not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.dynamic_phone_agent.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_dynamic_phone_agents(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing dynamic phone agents."""
        mock_agents = [
            {
                "id": "setup_1",
                "processingState": {
                    "status": "completed",
                    "progressPercentage": 100,
                },
                "success": True,
                "agentConfigurationId": "agent_1",
                "instructionConfigurationId": "instr_1",
                "phoneNumber": "+15551111111",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "setup_2",
                "processingState": {
                    "status": "completed",
                    "progressPercentage": 100,
                },
                "success": True,
                "agentConfigurationId": "agent_2",
                "instructionConfigurationId": "instr_2",
                "phoneNumber": "+15552222222",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_agents,
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
            f"{BASE_URL}/dynamic-phone-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_dynamic_phone_agents_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing dynamic phone agents with pagination."""
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
            f"{BASE_URL}/dynamic-phone-agent?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
