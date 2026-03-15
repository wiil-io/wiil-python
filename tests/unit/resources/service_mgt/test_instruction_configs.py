"""Tests for Instruction Configurations resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.service_mgt import (
    CreateInstructionConfiguration,
    UpdateInstructionConfiguration,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestInstructionConfigurationsResource:
    """Test suite for InstructionConfigurationsResource."""

    def test_create_instruction_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new instruction configuration."""
        mock_response = {
            "id": "instruction_123",
            "instructionName": "customer-support-agent",
            "role": "Customer Support Specialist",
            "introductionMessage": "Hello! How can I help you today?",
            "instructions": "You are a helpful customer support agent.",
            "guardrails": "Never share sensitive customer data. Always be polite.",
            "requiredSkills": None,
            "validationRules": None,
            "serviceId": None,
            "supportedServices": [],
            "tools": None,
            "isTemplate": False,
            "isPrimary": False,
            "metadata": None,
            "knowledgeSourceIds": ["source_1", "source_2"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/instruction-configurations",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.instruction_configs.create(CreateInstructionConfiguration(
            instruction_name="customer-support-agent",
            role="Customer Support Specialist",
            introduction_message="Hello! How can I help you today?",
            instructions="You are a helpful customer support agent.",
            guardrails="Never share sensitive customer data. Always be polite.",
            knowledge_source_ids=["source_1", "source_2"]
        ))

        assert result.id == "instruction_123"
        assert result.instruction_name == "customer-support-agent"

    def test_get_instruction_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving an instruction configuration by ID."""
        mock_response = {
            "id": "instruction_123",
            "instructionName": "customer-support-agent",
            "role": "Customer Support Specialist",
            "introductionMessage": "Hello! How can I help you today?",
            "instructions": "You are a helpful customer support agent.",
            "guardrails": "Never share sensitive customer data.",
            "requiredSkills": None,
            "validationRules": None,
            "serviceId": None,
            "supportedServices": [],
            "tools": None,
            "isTemplate": False,
            "isPrimary": False,
            "metadata": None,
            "knowledgeSourceIds": ["source_1", "source_2"],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/instruction-configurations/instruction_123",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.instruction_configs.get("instruction_123")

        assert result.id == "instruction_123"
        assert result.instruction_name == "customer-support-agent"

    def test_get_instruction_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when instruction configuration not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/instruction-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response(
                "NOT_FOUND", "Instruction configuration not found"
            ),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.instruction_configs.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_update_instruction_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating an instruction configuration."""
        mock_response = {
            "id": "instruction_123",
            "instructionName": "customer-support-agent",
            "role": "Senior Customer Support Specialist",
            "introductionMessage": "Hello! How can I help you today?",
            "instructions": "You are an updated support agent.",
            "guardrails": "Never share sensitive customer data.",
            "requiredSkills": None,
            "validationRules": None,
            "serviceId": None,
            "supportedServices": [],
            "tools": None,
            "isTemplate": False,
            "isPrimary": False,
            "metadata": None,
            "knowledgeSourceIds": ["source_1"],
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/instruction-configurations",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.instruction_configs.update(UpdateInstructionConfiguration(
            id="instruction_123",
            role="Senior Customer Support Specialist",
            instructions="You are an updated support agent."
        ))

        assert result.role == "Senior Customer Support Specialist"
        assert result.instructions == "You are an updated support agent."

    def test_delete_instruction_configuration(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting an instruction configuration."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/instruction-configurations/instruction_123",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.instruction_configs.delete("instruction_123")

        assert result is True

    def test_delete_instruction_configuration_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when deleting non-existent instruction."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/instruction-configurations/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response(
                "NOT_FOUND", "Instruction configuration not found"
            ),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.instruction_configs.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_instruction_configurations(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing instruction configurations with pagination."""
        mock_configs = [
            {
                "id": "instruction_1",
                "instructionName": "sales-agent",
                "role": "Sales Representative",
                "introductionMessage": "Hi! I can help you today.",
                "instructions": "Prompt 1",
                "guardrails": "Always be honest.",
                "requiredSkills": None,
                "validationRules": None,
                "serviceId": None,
                "supportedServices": [],
                "tools": None,
                "isTemplate": False,
                "isPrimary": False,
                "metadata": None,
                "knowledgeSourceIds": [],
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "instruction_2",
                "instructionName": "support-agent",
                "role": "Support Specialist",
                "introductionMessage": "Hello! How can I assist?",
                "instructions": "Prompt 2",
                "guardrails": "Be helpful.",
                "requiredSkills": None,
                "validationRules": None,
                "serviceId": None,
                "supportedServices": [],
                "tools": None,
                "isTemplate": False,
                "isPrimary": False,
                "metadata": None,
                "knowledgeSourceIds": [],
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
            f"{BASE_URL}/instruction-configurations",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.instruction_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_instruction_configurations_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing instructions with custom pagination parameters."""
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
            f"{BASE_URL}/instruction-configurations?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.instruction_configs.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
