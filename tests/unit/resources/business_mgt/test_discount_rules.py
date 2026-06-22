"""Tests for Discount Rules resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import CreateDiscountRule, UpdateDiscountRule
from wiil.models.type_definitions.business_definitions import (
    DiscountScope,
    DiscountType,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestDiscountRulesResource:
    """Test suite for DiscountRulesResource."""

    def _rule(self, rule_id: str = "disc_123") -> dict:
        return {
            "id": rule_id,
            "locationId": None,
            "name": "Summer Sale",
            "code": "SUMMER20",
            "scope": "ORDER",
            "type": "PERCENTAGE",
            "value": 20,
            "currency": "USD",
            "catalogScope": "ALL",
            "externalDiscountId": None,
            "minSubtotal": None,
            "customerSegment": None,
            "firstOrderOnly": False,
            "maxUses": None,
            "maxUsesPerCustomer": None,
            "isStackable": True,
            "priority": 1,
            "effectiveFrom": None,
            "effectiveTo": None,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_crud_and_queries(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        rule = self._rule()
        paged = {
            "data": [rule],
            "meta": {
                "page": 1,
                "pageSize": 10,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/discount-rules",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/discount-rules/disc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/discount-rules/by-location/"
                "loc_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/discount-rules/by-code/SUMMER20",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/discount-rules/by-scope?"
                "scope=ORDER&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/discount-rules/by-type?"
                "type=PERCENTAGE&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/discount-rules/active?"
                "isActive=true&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/discount-rules/stackable?"
                "isStackable=true&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/discount-rules",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/discount-rules/disc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/discount-rules?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.discount_rules.create(
            CreateDiscountRule(
                name="Summer Sale",
                code="SUMMER20",
                scope=DiscountScope.ORDER,
                type=DiscountType.PERCENTAGE,
                value=20,
            )
        )
        get_result = client.discount_rules.get("disc_123")
        by_location = client.discount_rules.get_by_location(
            "loc_123", PaginationRequest(page=1, page_size=10)
        )
        by_code = client.discount_rules.get_by_code("SUMMER20")
        by_scope = client.discount_rules.get_by_scope(
            DiscountScope.ORDER,
            PaginationRequest(page=1, page_size=10),
        )
        by_type = client.discount_rules.get_by_type(
            DiscountType.PERCENTAGE,
            PaginationRequest(page=1, page_size=10),
        )
        active = client.discount_rules.get_active(
            PaginationRequest(page=1, page_size=10)
        )
        stackable = client.discount_rules.get_stackable(
            PaginationRequest(page=1, page_size=10)
        )
        update_result = client.discount_rules.update(
            UpdateDiscountRule(id="disc_123", value=25)
        )
        delete_result = client.discount_rules.delete("disc_123")
        list_result = client.discount_rules.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "disc_123"
        assert get_result.id == "disc_123"
        assert by_location.meta.total_count == 1
        assert by_code.id == "disc_123"
        assert by_scope.meta.total_count == 1
        assert by_type.meta.total_count == 1
        assert active.meta.total_count == 1
        assert stackable.meta.total_count == 1
        assert update_result.id == "disc_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        paged = {
            "data": [self._rule("disc_1")],
            "meta": {
                "page": 1,
                "pageSize": 1,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/discount-rules/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.discount_rules.create_batch(
            [
                CreateDiscountRule(
                    name="Summer Sale",
                    code="SUMMER20",
                    scope=DiscountScope.ORDER,
                    type=DiscountType.PERCENTAGE,
                    value=20,
                )
            ]
        )

        assert len(result.data) == 1
