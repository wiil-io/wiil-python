"""Tests for Service Providers resource."""

import responses

from wiil import WiilClient
from wiil.types import PaginationRequest

BASE_URL = 'https://api.wiil.io/v1'
API_KEY = 'test-api-key'


class TestServiceProvidersResource:
    """Test suite for ServiceProvidersResource."""

    @staticmethod
    def _provider_payload(provider_id: str = 'sp_123'):
        return {
            'id': provider_id,
            'serviceId': 'service_123',
            'providerId': 'provider_123',
            'active': True,
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_get_by_service(self, client: WiilClient, mock_api, api_response):
        """Test retrieving providers by service."""
        mock_response = {
            'data': [self._provider_payload('sp_1')],
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
            (
                f'{BASE_URL}/service-providers/bindings/by-service/'
                'service_123?page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_providers.get_by_service(
            'service_123',
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].id == 'sp_1'

    def test_get_by_provider(self, client: WiilClient, mock_api, api_response):
        """Test retrieving providers by provider ID."""
        mock_response = {
            'data': [self._provider_payload('sp_1')],
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
            (
                f'{BASE_URL}/service-providers/bindings/by-provider/'
                'provider_123?page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_providers.get_by_provider(
            'provider_123',
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].id == 'sp_1'
