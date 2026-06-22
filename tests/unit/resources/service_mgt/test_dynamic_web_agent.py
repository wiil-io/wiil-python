"""Tests for Dynamic Web Agent resource."""

import responses

from wiil import WiilClient
from wiil.models.service_mgt.dynamic_setup import (
    DynamicWebAgentSetup,
    UpdateDynamicWebAgent,
)
from wiil.models.type_definitions import SupportedProprietor
from wiil.resources.service_mgt.dynamic_web_agent import WebAgentCreateOptions


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestDynamicWebAgentResource:
    """Test suite for DynamicWebAgentResource."""

    def test_create_dynamic_web_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new dynamic web agent."""
        mock_response = {
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "integrationSnippets": [
                '<script src="https://cdn.wiil.io/widget.js"></script>',
                '<div id="wiil-widget" data-agent="agent_123"></div>',
            ],
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/dynamic-setup/web-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_web_agent.create(
            DynamicWebAgentSetup(
                assistant_name="Website Support Agent",
                website_url="https://example.com",
                communication_type="UNIFIED",
                language="en-US",
                capabilities=[]
            ),
            options=WebAgentCreateOptions(
                poll_until_complete=False,
                silent=True
            )
        )

        assert result.success is True
        assert result.agent_configuration_id == "agent_123"
        assert result.instruction_configuration_id == "instr_456"
        assert len(result.integration_snippets) == 2

    def test_create_web_agent_with_voice_type(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a web agent with voice communication type."""
        mock_response = {
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_456",
            "instructionConfigurationId": "instr_789",
            "integrationSnippets": [
                '<script src="https://cdn.wiil.io/voice-widget.js"></script>',
            ],
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
            f"{BASE_URL}/dynamic-setup/web-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_web_agent.create(
            DynamicWebAgentSetup(
                assistant_name="Voice Web Agent",
                website_url="https://example.com",
                communication_type="VOICE",
                language="en-US",
                capabilities=[],
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
            options=WebAgentCreateOptions(
                poll_until_complete=False,
                silent=True
            )
        )

        assert result.success is True
        assert result.agent_configuration_id == "agent_456"

    def test_update_dynamic_web_agent(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a dynamic web agent."""
        mock_response = {
            "processingState": {
                "status": "completed",
                "progressPercentage": 100,
            },
            "success": True,
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "instr_456",
            "integrationSnippets": [
                '<script src="https://cdn.wiil.io/widget.js"></script>',
            ],
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/dynamic-setup/web-agent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.dynamic_web_agent.update(UpdateDynamicWebAgent(
            id="agent_123",
            assistant_name="Updated Website Support Agent",
            website_url="https://new-example.com"
        ))

        assert result.success is True
        assert result.agent_configuration_id == "agent_123"
