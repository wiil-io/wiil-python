"""Tests for Product Pricing Rules resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateProductPricingRule,
    ProductPricingRuleCondition,
    UpdateProductPricingRule,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductPricingRulesResource:
    """Test suite for ProductPricingRulesResource."""

    def _rule(self, rule_id: str = "rule_123") -> dict:
        return {
            "id": rule_id,
            "locationId": None,
            "name": "Discount",
            "channelMappings": None,
            "discountId": "disc_123",
            "productSetRevisionId": None,
            "condition": {
                "productSetId": "set_123",
                "daysOfWeek": [],
                "startMinute": None,
                "endMinute": None,
                "customerSegmentIds": None,
                "channel": "ALL",
            },
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
            f"{BASE_URL}/product-pricing-rules",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-pricing-rules/rule_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/product-pricing-rules/by-product-set/"
                "set_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-pricing-rules/by-discount/disc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/product-pricing-rules/active?"
                "effectiveAt=1234567890&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-pricing-rules/rule_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-pricing-rules/rule_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-pricing-rules?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.product_pricing_rules.create(
            CreateProductPricingRule(
                name="Discount",
                discount_id="disc_123",
                condition=ProductPricingRuleCondition(
                    product_set_id="set_123"
                ),
            )
        )
        get_result = client.product_pricing_rules.get("rule_123")
        by_set = client.product_pricing_rules.get_by_product_set(
            "set_123",
            PaginationRequest(page=1, page_size=10),
        )
        by_discount = client.product_pricing_rules.get_by_discount("disc_123")
        active = client.product_pricing_rules.get_active(
            timestamp=1234567890,
            params=PaginationRequest(page=1, page_size=10),
        )
        update_result = client.product_pricing_rules.update(
            "rule_123",
            UpdateProductPricingRule(id="rule_123", name="Discount"),
        )
        delete_result = client.product_pricing_rules.delete("rule_123")
        list_result = client.product_pricing_rules.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "rule_123"
        assert get_result.id == "rule_123"
        assert by_set.meta.total_count == 1
        assert by_discount.meta.total_count == 1
        assert active.meta.total_count == 1
        assert update_result.id == "rule_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1
