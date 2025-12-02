"""Tests for Projects resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProjectsResource:
    """Test suite for ProjectsResource."""

    def test_create_project(self, client: WiilClient, mock_api, api_response):
        """Test creating a new project."""
        input_data = {
            "name": "Production Environment",
            "description": "Main production deployment",
            "compliance": ["SOC2", "HIPAA"],
        }

        mock_response = {
            "id": "proj_123",
            "name": "Production Environment",
            "description": "Main production deployment",
            "compliance": ["SOC2", "HIPAA"],
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/projects",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.create(**input_data)

        assert result.id == "proj_123"
        assert result.name == "Production Environment"
        assert result.description == "Main production deployment"
        assert result.compliance == ["SOC2", "HIPAA"]
        assert result.is_default is False

    def test_get_project(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a project by ID."""
        mock_response = {
            "id": "proj_123",
            "name": "Production Environment",
            "description": "Main production deployment",
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/projects/proj_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.get("proj_123")

        assert result.id == "proj_123"
        assert result.name == "Production Environment"
        assert result.is_default is False

    def test_get_project_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when project not found."""
        mock_api.get(
            f"{BASE_URL}/projects/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Project not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.projects.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_default_project(self, client: WiilClient, mock_api, api_response):
        """Test retrieving the default project for the organization."""
        mock_response = {
            "id": "proj_default",
            "name": "Default Project",
            "description": "Organization default project",
            "isDefault": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/projects/default",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.get_default()

        assert result.id == "proj_default"
        assert result.name == "Default Project"
        assert result.is_default is True

    def test_update_project(self, client: WiilClient, mock_api, api_response):
        """Test updating a project."""
        update_data = {
            "id": "proj_123",
            "name": "Production Environment v2",
            "description": "Updated production deployment",
        }

        mock_response = {
            "id": "proj_123",
            "name": "Production Environment v2",
            "description": "Updated production deployment",
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/projects",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.update(**update_data)

        assert result.name == "Production Environment v2"
        assert result.description == "Updated production deployment"

    def test_delete_project(self, client: WiilClient, mock_api, api_response):
        """Test deleting a project."""
        mock_api.delete(
            f"{BASE_URL}/projects/proj_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.projects.delete("proj_123")

        assert result is True

    def test_delete_project_not_found(self, client: WiilClient, mock_api, error_response):
        """Test API error when deleting non-existent project."""
        mock_api.delete(
            f"{BASE_URL}/projects/invalid_id",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Project not found")
        ))

        with pytest.raises(WiilAPIError) as exc_info:
            client.projects.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_projects(self, client: WiilClient, mock_api, api_response):
        """Test listing projects with pagination."""
        mock_projects = [
            {
                "id": "proj_1",
                "name": "Project 1",
                "description": "First project",
                "isDefault": True,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "proj_2",
                "name": "Project 2",
                "description": "Second project",
                "isDefault": False,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_projects,
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
            f"{BASE_URL}/projects",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1
        assert result.data[0].is_default is True
        assert result.data[1].is_default is False

    def test_list_projects_with_pagination(self, client: WiilClient, mock_api, api_response):
        """Test listing projects with custom pagination parameters."""
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
            f"{BASE_URL}/projects?page=2&pageSize=50",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.list(page=2, page_size=50)

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True

    def test_list_projects_with_sorting(self, client: WiilClient, mock_api, api_response):
        """Test listing projects with sorting parameters."""
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
            f"{BASE_URL}/projects?sortBy=name&sortDirection=desc",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.projects.list(sort_by="name", sort_direction="desc")

        assert result.meta.page == 1
        assert result.meta.total_count == 0
