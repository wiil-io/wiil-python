"""Tests for Menu Sets resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateMenuSet,
    MenuSetItem,
    UpdateMenuSet,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenuSetsResource:
    """Test suite for MenuSetsResource."""

    def _menu_set(self, set_id: str = "set_123") -> dict:
        return {
            "id": set_id,
            "name": "Lunch Combo",
            "targetingMode": "EXPLICIT",
            "pricingMode": "SUM_OF_ITEMS",
            "items": [
                {
                    "menuItemId": "item_1",
                    "menuItemVariantId": "variant_1",
                    "quantity": 1,
                    "isRequired": True,
                }
            ],
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_create_get_by_code_and_get(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        response = self._menu_set()

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-sets",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(response),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-sets/code/LUNCH",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(response),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-sets/set_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(response),
            status=200,
        )

        created = client.menu_sets.create(
            CreateMenuSet(
                name="Lunch Combo",
                items=[
                    MenuSetItem(
                        menu_item_id="item_1",
                        menu_item_variant_id="variant_1",
                        quantity=1,
                    )
                ],
            )
        )
        by_code = client.menu_sets.get_by_code("LUNCH")
        fetched = client.menu_sets.get("set_123")

        assert created.id == "set_123"
        assert by_code is not None
        assert fetched.name == "Lunch Combo"

    def test_get_active_and_list(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        mock_response = {
            "data": [self._menu_set("set_1")],
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
            f"{BASE_URL}/menu-sets/active?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-sets?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        active = client.menu_sets.get_active(
            PaginationRequest(page=1, page_size=10)
        )
        listed = client.menu_sets.list(PaginationRequest(page=1, page_size=10))

        assert active.meta.total_count == 1
        assert listed.meta.total_count == 1

    def test_update_delete_and_create_batch(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        updated = self._menu_set()
        updated["name"] = "Dinner Combo"

        batch_response = {
            "data": [updated],
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
            responses.PATCH,
            f"{BASE_URL}/menu-sets/set_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(updated),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/menu-sets/set_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-sets/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(batch_response),
            status=200,
        )

        updated_set = client.menu_sets.update(
            "set_123",
            UpdateMenuSet(id="set_123", name="Dinner Combo"),
        )
        deleted = client.menu_sets.delete("set_123")
        batch = client.menu_sets.create_batch(
            [
                CreateMenuSet(
                    name="Dinner Combo",
                    items=[
                        MenuSetItem(
                            menu_item_id="item_1",
                            menu_item_variant_id="variant_1",
                            quantity=1,
                        )
                    ],
                )
            ]
        )

        assert updated_set.name == "Dinner Combo"
        assert deleted is True
        assert len(batch.data) == 1
