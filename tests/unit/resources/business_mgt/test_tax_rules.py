"""Tests for Tax Rules resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import CreateTaxRule, UpdateTaxRule
from wiil.models.type_definitions.business_definitions import (
    TaxRateType,
    TaxScope,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestTaxRulesResource:
    """Test suite for TaxRulesResource."""

    def _rule(self, rule_id: str = "tax_123") -> dict:
        return {
            "id": rule_id,
            "locationId": None,
            "name": "State Tax",
            "scope": "ORDER",
            "rateType": "PERCENTAGE",
            "rateValue": 8.25,
            "currency": "USD",
            "catalogScope": "ALL",
            "externalTaxId": None,
            "isInclusive": False,
            "priority": 1,
            "isCompound": False,
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
            f"{BASE_URL}/tax-rules",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/tax-rules/tax_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/tax-rules/by-location/loc_123?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/tax-rules/by-scope?scope=ORDER&page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/tax-rules/by-rate-type?"
                "rateType=PERCENTAGE&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/tax-rules/active?isActive=true&page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/tax-rules",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(rule),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/tax-rules/tax_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/tax-rules?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.tax_rules.create(
            CreateTaxRule(
                name="State Tax",
                scope=TaxScope.ORDER,
                rate_type=TaxRateType.PERCENTAGE,
                rate_value=8.25,
            )
        )
        get_result = client.tax_rules.get("tax_123")
        by_location = client.tax_rules.get_by_location(
            "loc_123", PaginationRequest(page=1, page_size=10)
        )
        by_scope = client.tax_rules.get_by_scope(
            TaxScope.ORDER,
            PaginationRequest(page=1, page_size=10),
        )
        by_rate_type = client.tax_rules.get_by_rate_type(
            TaxRateType.PERCENTAGE,
            PaginationRequest(page=1, page_size=10),
        )
        active = client.tax_rules.get_active(
            PaginationRequest(page=1, page_size=10)
        )
        update_result = client.tax_rules.update(
            UpdateTaxRule(id="tax_123", rate_value=9.0)
        )
        delete_result = client.tax_rules.delete("tax_123")
        list_result = client.tax_rules.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "tax_123"
        assert get_result.id == "tax_123"
        assert by_location.meta.total_count == 1
        assert by_scope.meta.total_count == 1
        assert by_rate_type.meta.total_count == 1
        assert active.meta.total_count == 1
        assert update_result.id == "tax_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        paged = {
            "data": [self._rule("tax_1")],
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
            f"{BASE_URL}/tax-rules/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.tax_rules.create_batch(
            [
                CreateTaxRule(
                    name="State Tax",
                    scope=TaxScope.ORDER,
                    rate_type=TaxRateType.PERCENTAGE,
                    rate_value=8.25,
                )
            ]
        )

        assert len(result.data) == 1
