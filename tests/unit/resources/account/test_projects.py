"""Tests for Projects resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError, WiilValidationError
from wiil.models.account import CreateProject, UpdateProject
from wiil.types import PaginationRequest


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProjectsResource:
    """Test suite for ProjectsResource."""

    def test_create_project(self, client: WiilClient, mock_api, api_response):
        """Test creating a new project."""
        input_data = CreateProject(
            name="Production Environment",
            description="Main production deployment",
            is_default=True,
        )

        mock_response = {
            "id": "proj_123",
            "name": "Production Environment",
            "description": "Main production deployment",
            "isDefault": True,
            "serviceStatus": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/projects",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.projects.create(input_data)

        assert result.id == "proj_123"
        assert result.name == "Production Environment"
        assert result.is_default is True

    def test_create_project_validation_error(self, client: WiilClient):
        """Test validation error for invalid input."""
        with pytest.raises(WiilValidationError):
            # Name too short - should fail validation
            CreateProject(name="P", is_default=True)

    def test_get_project(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a project by ID."""
        mock_response = {
            "id": "proj_123",
            "name": "Production Environment",
            "isDefault": True,
            "serviceStatus": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/projects/proj_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.projects.get("proj_123")

        assert result.id == "proj_123"
        assert result.name == "Production Environment"

    def test_get_project_not_found(
        self,
        client: WiilClient,
        mock_api,
        error_response
    ):
        """Test API error when project not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/projects/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Project not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.projects.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_get_default_project(
        self,
        client: WiilClient,
        mock_api,
        api_response
    ):
        """Test retrieving the default project for the organization."""
        mock_response = {
            "id": "proj_default",
            "name": "Default Project",
            "description": "Organization default project",
            "isDefault": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/projects/default",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.projects.get_default()

        assert result.id == "proj_default"
        assert result.name == "Default Project"
        assert result.is_default is True

    def test_update_project(self, client: WiilClient, mock_api, api_response):
        """Test updating a project."""
        update_data = UpdateProject(
            id="proj_123",
            name="Production Environment v2",
            description="Updated production deployment",
        )

        mock_response = {
            "id": "proj_123",
            "name": "Production Environment v2",
            "description": "Updated production deployment",
            "isDefault": True,
            "serviceStatus": "ACTIVE",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/projects",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.projects.update(update_data)

        assert result.name == "Production Environment v2"
        assert result.description == "Updated production deployment"

    def test_delete_project(self, client: WiilClient, mock_api, api_response):
        """Test deleting a project."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/projects/proj_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.projects.delete("proj_123")

        assert result is True

    def test_delete_project_not_found(
        self,
        client: WiilClient,
        mock_api,
        error_response
    ):
        """Test API error when deleting non-existent project."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/projects/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Project not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.projects.delete("invalid_id")

        assert exc_info.value.status_code == 404

    def test_list_projects(self, client: WiilClient, mock_api, api_response):
        """Test listing projects with pagination."""
        mock_projects = [
            {
                "id": "proj_1",
                "name": "Production",
                "isDefault": True,
                "serviceStatus": "ACTIVE",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "proj_2",
                "name": "Development",
                "isDefault": False,
                "serviceStatus": "ACTIVE",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/projects",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.projects.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_projects_with_pagination(
        self,
        client: WiilClient,
        mock_api,
        api_response
    ):
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/projects?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.projects.list(PaginationRequest(page=2, page_size=50))

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
