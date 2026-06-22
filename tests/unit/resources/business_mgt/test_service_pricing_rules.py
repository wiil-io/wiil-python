"""Tests for Service Pricing Rules resource."""

import responses

from wiil import WiilClient
from wiil.types import PaginationRequest

BASE_URL = 'https://api.wiil.io/v1'
API_KEY = 'test-api-key'


class TestServicePricingRulesResource:
    """Test suite for ServicePricingRulesResource."""

    @staticmethod
    def _rule_payload(rule_id: str = 'rule_123'):
        return {
            'id': rule_id,
            'name': 'Weekday Special',
            'isActive': True,
            'priority': 1,
            'condition': {
                'allServices': True,
                'daysOfWeek': [],
            },
            'action': {
                'adjustmentType': 'PERCENTAGE',
                'adjustmentValue': 10,
            },
            'applyLevel': 'ORDER',
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_get_by_location(self, client: WiilClient, mock_api, api_response):
        """Test retrieving pricing rules by location."""
        mock_response = {
            'data': [self._rule_payload('rule_1')],
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
                f'{BASE_URL}/service-pricing-rules/by-location/'
                'loc_123?page=1&pageSize=10'
            ),
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.service_pricing_rules.get_by_location(
            'loc_123',
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].id == 'rule_1'
