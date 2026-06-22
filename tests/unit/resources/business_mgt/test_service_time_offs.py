"""Tests for Service Time Offs resource."""

import responses

from wiil import WiilClient
from wiil.types import PaginationRequest

BASE_URL = 'https://api.wiil.io/v1'
API_KEY = 'test-api-key'


class TestServiceTimeOffsResource:
    """Test suite for ServiceTimeOffsResource."""

    @staticmethod
    def _time_off_payload(time_off_id: str = 'to_123'):
        return {
            'id': time_off_id,
            'providerId': 'provider_123',
            'type': 'specific',
            'reason': 'Vacation',
            'startDate': 1234567890,
            'endDate': 1234567990,
            'status': 'pending',
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_get_by_provider(self, client: WiilClient, mock_api, api_response):
        """Test retrieving time offs by provider."""
        mock_response = {
            'data': [self._time_off_payload('to_1')],
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
                f'{BASE_URL}/service-providers/time-off/by-provider/'
                'provider_123?page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_time_offs.get_by_provider(
            'provider_123',
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].id == 'to_1'

    def test_approve(self, client: WiilClient, mock_api, api_response):
        """Test approving time off."""
        mock_response = self._time_off_payload()
        mock_response['status'] = 'approved'

        mock_api.add(
            responses.POST,
            f'{BASE_URL}/service-providers/time-off/to_123/approve',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_time_offs.approve('to_123')

        assert result.status == 'approved'
