"""Tests for Dynamic Phone Agent resource."""

import responses

from wiil import WiilClient
from wiil.models.service_mgt.dynamic_setup import (
    DynamicPhoneAgentSetup,
    UpdateDynamicPhoneAgent,
)
from wiil.models.type_definitions import SupportedProprietor
from wiil.resources.service_mgt.dynamic_phone_agent import PhoneAgentCreateOptions


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestDynamicPhoneAgentResource:
    """Test suite for DynamicPhoneAgentResource."""

    def test_create_dynamic_phone_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new dynamic phone agent."""
        mock_response = {
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "phoneNumber": "+15551234567",
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/dynamic-setup/phone-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.create(
            DynamicPhoneAgentSetup(
                assistant_name="Customer Service Agent",
                language="en-US",
                capabilities=[],
                phone_configuration_id="phone_config_123"
            ),
            options=PhoneAgentCreateOptions(
                poll_until_complete=False,
                silent=True
            )
        )

        assert result.success is True
        assert result.agent_configuration_id == "agent_123"
        assert result.instruction_configuration_id == "instr_456"
        assert result.phone_number == "+15551234567"

    def test_create_phone_agent_with_stt_tts(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a phone agent with STT and TTS configurations."""
        mock_response = {
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_456",
            "instructionConfigurationId": "instr_789",
            "phoneNumber": "+15559876543",
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
            f"{BASE_URL}/support-models/supports/ElevenLabs/eleven_turbo_v2",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/dynamic-setup/phone-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_phone_agent.create(
            DynamicPhoneAgentSetup(
                assistant_name="Voice Agent",
                language="en-US",
                capabilities=[],
                phone_configuration_id="phone_config_123",
                stt_configuration={
                    "provider_type": SupportedProprietor.DEEPGRAM,
                    "provider_model_id": "nova-2",
                    "language_id": "en-US",
                },
                tts_configuration={
                    "provider_type": SupportedProprietor.ELEVENLABS,
                    "provider_model_id": "eleven_turbo_v2",
                    "language_id": "en-US",
                    "voice_id": "voice_rachel",
                }
            ),
            options=PhoneAgentCreateOptions(
                poll_until_complete=False,
                silent=True
            )
        )

        assert result.success is True
        assert result.agent_configuration_id == "agent_456"
        assert result.phone_number == "+15559876543"

    def test_update_dynamic_phone_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a dynamic phone agent."""
        mock_response = {
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "phoneNumber": "+15551234567",
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/dynamic-setup/phone-agent",
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
