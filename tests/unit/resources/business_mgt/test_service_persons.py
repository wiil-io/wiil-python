"""Tests for Service Persons resource."""

import responses

from wiil import WiilClient
from wiil.types import PaginationRequest

BASE_URL = 'https://api.wiil.io/v1'
API_KEY = 'test-api-key'


class TestServicePersonsResource:
    """Test suite for ServicePersonsResource."""

    @staticmethod
    def _person_payload(person_id: str = 'person_123'):
        return {
            'id': person_id,
            'name': 'Alex Stylist',
            'locationId': 'loc_123',
            'isActive': True,
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_get_by_location(self, client: WiilClient, mock_api, api_response):
        """Test retrieving service persons by location."""
        mock_response = {
            'data': [self._person_payload('person_1')],
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
                f'{BASE_URL}/service-providers/persons/by-location/'
                'loc_123?page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_persons.get_by_location(
            'loc_123',
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].id == 'person_1'
