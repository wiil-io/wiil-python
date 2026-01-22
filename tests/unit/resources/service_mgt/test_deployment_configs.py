"""Tests for Deployment Configurations resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestDeploymentConfigurationsResource:
    """Test suite for DeploymentConfigurationsResource."""

    def test_create_deployment_configuration(self, client: WiilClient, mock_api, api_response):
        """Test creating a new deployment configuration."""
        input_data = {
            "name": "Customer Service Deployment",
            "agent_config_id": "agent_123",
            "instruction_config_id": "inst_456",
            "project_id": "proj_789",
        }

        mock_response = {
            "id": "deploy_123",
            "projectId": "proj_789",
            "deploymentChannelId": "channel_999",
            "deploymentName": "Customer Service Deployment",
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "inst_456",
            "deploymentStatus": "PENDING",
            "provisioningType": "DIRECT",
            "provisioningConfigChainId": None,
            "isActive": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/deployment-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.create(**input_data)

        assert result.id == "deploy_123"
        assert result.deployment_name == "Customer Service Deployment"
        assert result.agent_configuration_id == "agent_123"

    def test_create_chain_deployment_configuration(self, client: WiilClient, mock_api, api_response):
        """Test creating a chained deployment configuration."""
        input_data = {
            "name": "Voice Chain Deployment",
            "provisioning_config_chain_id": "chain_123",
            "project_id": "proj_789",
        }

        mock_response = {
            "id": "deploy_456",
            "projectId": "proj_789",
            "deploymentChannelId": "channel_888",
            "deploymentName": "Voice Chain Deployment",
            "agentConfigurationId": "agent_456",
            "instructionConfigurationId": "inst_789",
            "deploymentStatus": "PENDING",
            "provisioningType": "CHAINED",
            "provisioningConfigChainId": "chain_123",
            "isActive": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/deployment-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.create_chain(**input_data)

        assert result.id == "deploy_456"
        assert result.deployment_name == "Voice Chain Deployment"
        assert result.provisioning_config_chain_id == "chain_123"

    def test_get_deployment_configuration(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a deployment configuration by ID."""
        mock_response = {
            "id": "deploy_123",
            "projectId": "proj_789",
            "deploymentChannelId": "channel_999",
            "deploymentName": "Customer Service Deployment",
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "inst_456",
            "deploymentStatus": "ACTIVE",
            "provisioningType": "DIRECT",
            "provisioningConfigChainId": None,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/deployment-configurations/deploy_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.get("deploy_123")

        assert result.id == "deploy_123"
        assert result.deployment_name == "Customer Service Deployment"
        assert result.deployment_status == "ACTIVE"

    def test_get_deployment_configuration_by_channel(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a deployment configuration by channel ID."""
        mock_response = {
            "id": "deploy_123",
            "projectId": "proj_789",
            "deploymentChannelId": "channel_789",
            "deploymentName": "Customer Service Deployment",
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "inst_456",
            "deploymentStatus": "ACTIVE",
            "provisioningType": "DIRECT",
            "provisioningConfigChainId": None,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/deployment-configurations/by-channel/channel_789",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.get_by_channel("channel_789")

        assert result.id == "deploy_123"
        assert result.deployment_channel_id == "channel_789"

    def test_update_deployment_configuration(self, client: WiilClient, mock_api, api_response):
        """Test updating a deployment configuration."""
        update_data = {
            "id": "deploy_123",
            "name": "Updated Deployment Name",
        }

        mock_response = {
            "id": "deploy_123",
            "projectId": "proj_789",
            "deploymentChannelId": "channel_999",
            "deploymentName": "Updated Deployment Name",
            "agentConfigurationId": "agent_123",
            "instructionConfigurationId": "inst_456",
            "deploymentStatus": "ACTIVE",
            "provisioningType": "DIRECT",
            "provisioningConfigChainId": None,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/deployment-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.update(**update_data)

        assert result.deployment_name == "Updated Deployment Name"
        assert result.updated_at == 1234567891

    def test_delete_deployment_configuration(self, client: WiilClient, mock_api, api_response):
        """Test deleting a deployment configuration."""
        mock_api.delete(
            f"{BASE_URL}/deployment-configurations/deploy_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.deployment_configs.delete("deploy_123")

        assert result is True

    def test_list_deployment_configurations(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment configurations with pagination."""
        mock_configs = [
            {
                "id": "deploy_1",
                "projectId": "proj_789",
                "deploymentChannelId": "channel_101",
                "deploymentName": "Deployment 1",
                "agentConfigurationId": "agent_123",
                "instructionConfigurationId": "inst_456",
                "deploymentStatus": "ACTIVE",
                "provisioningType": "DIRECT",
                "provisioningConfigChainId": None,
                "isActive": True,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "deploy_2",
                "projectId": "proj_789",
                "deploymentChannelId": "channel_102",
                "deploymentName": "Deployment 2",
                "agentConfigurationId": "agent_456",
                "instructionConfigurationId": "inst_789",
                "deploymentStatus": "PENDING",
                "provisioningType": "DIRECT",
                "provisioningConfigChainId": None,
                "isActive": False,
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
            f"{BASE_URL}/deployment-configurations",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.data[0].deployment_name == "Deployment 1"
        assert result.data[1].deployment_status == "PENDING"

    def test_list_deployment_configurations_by_project(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment configurations by project ID."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 0,
                "totalPages": 0,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/deployment-configurations/by-project/proj_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.list_by_project("proj_123")

        assert len(result.data) == 0

    def test_list_deployment_configurations_by_agent(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment configurations by agent configuration ID."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 0,
                "totalPages": 0,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/deployment-configurations/by-agent/agent_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.list_by_agent("agent_123")

        assert len(result.data) == 0

    def test_list_deployment_configurations_by_instruction(self, client: WiilClient, mock_api, api_response):
        """Test listing deployment configurations by instruction configuration ID."""
        mock_response = {
            "data": [],
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 0,
                "totalPages": 0,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/deployment-configurations/by-instruction/inst_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.deployment_configs.list_by_instruction("inst_123")

        assert len(result.data) == 0
