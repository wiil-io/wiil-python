"""Tests for Service Categories resource."""

import responses

from wiil import WiilClient
from wiil.types import PaginationRequest

BASE_URL = 'https://api.wiil.io/v1'
API_KEY = 'test-api-key'


class TestServiceCategoriesResource:
    """Test suite for ServiceCategoriesResource."""

    @staticmethod
    def _category_payload(category_id: str = 'cat_123'):
        return {
            'id': category_id,
            'name': 'Hair Services',
            'description': 'Hair and styling category',
            'isActive': True,
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a category by ID."""
        mock_api.add(
            responses.GET,
            f'{BASE_URL}/service-categories/cat_123',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(self._category_payload()),
            status=200,
        )

        result = client.service_categories.get('cat_123')

        assert result.id == 'cat_123'
        assert result.name == 'Hair Services'

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing categories with pagination."""
        mock_response = {
            'data': [self._category_payload('cat_1')],
            'meta': {
                'page': 1,
                'pageSize': 20,
                'totalCount': 1,
                'totalPages': 1,
                'hasNextPage': False,
                'hasPreviousPage': False,
            },
        }

        mock_api.add(
            responses.GET,
            f'{BASE_URL}/service-categories?page=1&pageSize=10',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_categories.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].id == 'cat_1'
