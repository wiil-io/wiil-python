"""Tests for Menu Pricing Rules resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateMenuPricingRule,
    MenuPricingRuleCondition,
    UpdateMenuPricingRule,
)
from wiil.models.business_mgt.menu_management.menu_pricing_rule import (
    PricingChannel,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenuPricingRulesResource:
    """Test suite for MenuPricingRulesResource."""

    def _rule(self, rule_id: str = "rule_123") -> dict:
        return {
            "id": rule_id,
            "name": "Happy Hour",
            "discountId": "discount_123",
            "condition": {
                "menuSetId": "set_123",
                "channel": "ALL",
            },
            "displayOrder": 1,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_create(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-pricing-rules",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(self._rule()),
            status=200,
        )

        result = client.menu_pricing_rules.create(
            CreateMenuPricingRule(
                name="Happy Hour",
                discount_id="discount_123",
                condition=MenuPricingRuleCondition(menu_set_id="set_123"),
            )
        )

        assert result.id == "rule_123"

    def test_get_by_menu_set(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [self._rule("rule_1")],
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
            responses.GET,
            (
                f"{BASE_URL}/menu-pricing-rules/by-menu-set/"
                "set_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_pricing_rules.get_by_menu_set(
            "set_123",
            PaginationRequest(page=1, page_size=10),
        )

        assert result.meta.total_count == 1

    def test_get_by_discount(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [self._rule("rule_1")],
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
            responses.GET,
            f"{BASE_URL}/menu-pricing-rules/by-discount/discount_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_pricing_rules.get_by_discount("discount_123")

        assert len(result.data) == 1

    def test_get_active(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [self._rule("rule_1")],
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
            responses.GET,
            (
                f"{BASE_URL}/menu-pricing-rules/active?"
                "effectiveAt=1234567890&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_pricing_rules.get_active(
            timestamp=1234567890,
            params=PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1

    def test_update_delete_and_list(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        updated = self._rule()
        updated["name"] = "Late Night"

        list_response = {
            "data": [updated],
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
            responses.PATCH,
            f"{BASE_URL}/menu-pricing-rules/rule_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(updated),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/menu-pricing-rules/rule_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-pricing-rules?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(list_response),
            status=200,
        )

        updated_rule = client.menu_pricing_rules.update(
            "rule_123",
            UpdateMenuPricingRule(id="rule_123", name="Late Night"),
        )
        deleted = client.menu_pricing_rules.delete("rule_123")
        listed = client.menu_pricing_rules.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert updated_rule.name == "Late Night"
        assert deleted is True
        assert listed.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [self._rule("rule_1")],
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
            f"{BASE_URL}/menu-pricing-rules/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_pricing_rules.create_batch(
            [
                CreateMenuPricingRule(
                    name="Happy Hour",
                    discount_id="discount_123",
                    condition=MenuPricingRuleCondition(
                        menu_set_id="set_123",
                        channel=PricingChannel.ALL,
                    ),
                )
            ]
        )

        assert len(result.data) == 1
