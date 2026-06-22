"""Tests for Menu Item Variants resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateMenuItemVariant,
    UpdateMenuItemVariant,
)

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenuItemVariantsResource:
    """Test suite for MenuItemVariantsResource."""

    def _variant(self, variant_id: str = "variant_123") -> dict:
        return {
            "id": variant_id,
            "menuItemId": "item_123",
            "name": "Large",
            "price": 5.99,
            "isAvailable": True,
            "isActive": True,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_create(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-management/variants",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(self._variant()),
            status=200,
        )

        result = client.menu_item_variants.create(
            CreateMenuItemVariant(
                menu_item_id="item_123",
                name="Large",
                price=5.99,
            )
        )

        assert result.id == "variant_123"
        assert result.name == "Large"

    def test_get(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/variants/variant_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(self._variant()),
            status=200,
        )

        result = client.menu_item_variants.get("variant_123")

        assert result.id == "variant_123"

    def test_get_default(self, client: WiilClient, mock_api, api_response):
        response = self._variant("variant_default")
        response["isDefault"] = True

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/variants/default/item_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(response),
            status=200,
        )

        result = client.menu_item_variants.get_default("item_123")

        assert result is not None
        assert result.is_default is True

    def test_update(self, client: WiilClient, mock_api, api_response):
        updated = self._variant()
        updated["name"] = "XL"

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/menu-management/variants/variant_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(updated),
            status=200,
        )

        result = client.menu_item_variants.update(
            "variant_123",
            UpdateMenuItemVariant(id="variant_123", name="XL"),
        )

        assert result.name == "XL"

    def test_delete(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/menu-management/variants/variant_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.menu_item_variants.delete("variant_123")

        assert result is True

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        mock_response = {
            "data": [self._variant("variant_1")],
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
            f"{BASE_URL}/menu-management/variants/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menu_item_variants.create_batch(
            [
                CreateMenuItemVariant(
                    menu_item_id="item_123",
                    name="Large",
                    price=5.99,
                )
            ]
        )

        assert len(result.data) == 1

    def test_get_api_error(
        self,
        client: WiilClient,
        mock_api,
        error_response,
    ):
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/variants/missing",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Variant not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.menu_item_variants.get("missing")

        assert exc_info.value.code == "NOT_FOUND"
