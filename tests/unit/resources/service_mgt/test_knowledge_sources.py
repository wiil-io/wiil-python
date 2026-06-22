"""Tests for Knowledge Sources resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestKnowledgeSourcesResource:
    """Test suite for KnowledgeSourcesResource."""

    def test_get_knowledge_source(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a knowledge source by ID."""
        mock_response = {
            "id": "source_123",
            "name": "Product Documentation",
            "sourceType": "document",
            "request_success": True,
            "processingStatus": "completed",
            "content": None,
            "prepped_content": None,
            "content_path": None,
            "prepped_content_path": None,
            "original_content_url": "https://docs.example.com",
            "stored_content_url": None,
            "prepped_content_url": None,
            "content_size": None,
            "prepped_content_size": None,
            "storage_tier": "firestore",
            "last_accessed": None,
            "access_count": 0,
            "is_compressed": False,
            "compression_ratio": None,
            "metadata": {},
            "original_content_type": None,
            "content_hash": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/knowledge-sources/source_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.knowledge_sources.get("source_123")

        assert result.id == "source_123"
        assert result.name == "Product Documentation"

    def test_get_knowledge_source_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test API error when knowledge source not found."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/knowledge-sources/invalid_id",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Knowledge source not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.knowledge_sources.get("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == "NOT_FOUND"

    def test_list_knowledge_sources(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing knowledge sources with pagination."""
        mock_sources = [
            {
                "id": "source_1",
                "name": "Product Documentation",
                "sourceType": "document",
                "request_success": True,
                "processingStatus": "completed",
                "content": None,
                "prepped_content": None,
                "content_path": None,
                "prepped_content_path": None,
                "original_content_url": "https://docs.example.com",
                "stored_content_url": None,
                "prepped_content_url": None,
                "content_size": None,
                "prepped_content_size": None,
                "storage_tier": "firestore",
                "last_accessed": None,
                "access_count": 5,
                "is_compressed": False,
                "compression_ratio": None,
                "metadata": {},
                "original_content_type": "application/pdf",
                "content_hash": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "source_2",
                "name": "FAQ Database",
                "sourceType": "url",
                "request_success": True,
                "processingStatus": "completed",
                "content": None,
                "prepped_content": None,
                "content_path": None,
                "prepped_content_path": None,
                "original_content_url": "https://faq.example.com",
                "stored_content_url": None,
                "prepped_content_url": None,
                "content_size": None,
                "prepped_content_size": None,
                "storage_tier": "firestore",
                "last_accessed": None,
                "access_count": 3,
                "is_compressed": False,
                "compression_ratio": None,
                "metadata": {},
                "original_content_type": "text/html",
                "content_hash": None,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_sources,
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
            f"{BASE_URL}/knowledge-sources",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.knowledge_sources.list()

        assert len(result.data) == 2
        assert result.meta.total_count == 2
        assert result.meta.page == 1

    def test_list_knowledge_sources_with_pagination(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing knowledge sources with pagination parameters."""
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
            f"{BASE_URL}/knowledge-sources?page=2&pageSize=50",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.knowledge_sources.list(
            PaginationRequest(page=2, page_size=50)
        )

        assert result.meta.page == 2
        assert result.meta.page_size == 50
        assert result.meta.has_previous_page is True
