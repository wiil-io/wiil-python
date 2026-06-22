"""Tests for Modifiers resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateItemModifierBinding,
    CreateModifierGroup,
    CreateModifierGroupOption,
    CreateModifierOption,
    UpdateItemModifierBinding,
    UpdateModifierGroup,
    UpdateModifierOption,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestModifiersResource:
    """Test suite for ModifiersResource."""

    def _option(self, option_id: str = "opt_123") -> dict:
        return {
            "id": option_id,
            "modifierGroupId": "grp_123",
            "name": "Extra Cheese",
            "priceDelta": 1.5,
            "isDefault": False,
            "displayOrder": 1,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def _group(self, group_id: str = "grp_123") -> dict:
        return {
            "id": group_id,
            "name": "Toppings",
            "options": [self._option("opt_1")],
            "minSelection": 0,
            "maxSelection": 3,
            "isRequired": False,
            "displayOrder": 1,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def _binding(self, binding_id: str = "bind_123") -> dict:
        return {
            "id": binding_id,
            "menuItemId": "item_123",
            "modifierGroupId": "grp_123",
            "displayOrder": 1,
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_group_methods(self, client: WiilClient, mock_api, api_response):
        group = self._group()
        paged = {
            "data": [group],
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
            f"{BASE_URL}/modifiers/groups",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(group),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/modifiers/groups/grp_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(group),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/modifiers/groups?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/modifiers/groups/grp_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(group),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/modifiers/groups/grp_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/modifiers/groups/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        created = client.modifiers.create_group(
            CreateModifierGroup(
                name="Toppings",
                options=[CreateModifierGroupOption(name="Extra Cheese")],
            )
        )
        fetched = client.modifiers.get_group("grp_123")
        listed = client.modifiers.list_groups(
            PaginationRequest(page=1, page_size=10)
        )
        updated = client.modifiers.update_group(
            "grp_123",
            UpdateModifierGroup(id="grp_123", name="Sauces"),
        )
        deleted = client.modifiers.delete_group("grp_123")
        batch = client.modifiers.create_group_batch(
            [
                CreateModifierGroup(
                    name="Sauces",
                    options=[CreateModifierGroupOption(name="BBQ")],
                )
            ]
        )

        assert created.id == "grp_123"
        assert fetched.id == "grp_123"
        assert listed.meta.total_count == 1
        assert updated.id == "grp_123"
        assert deleted is True
        assert len(batch.data) == 1

    def test_option_methods(self, client: WiilClient, mock_api, api_response):
        option = self._option()
        paged = {
            "data": [option],
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
            f"{BASE_URL}/modifiers/options",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(option),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/modifiers/options/opt_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(option),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/modifiers/options/by-group/"
                "grp_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/modifiers/options?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/modifiers/options/opt_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(option),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/modifiers/options/opt_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/modifiers/options/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        created = client.modifiers.create_option(
            CreateModifierOption(
                modifier_group_id="grp_123",
                name="Extra Cheese",
            )
        )
        fetched = client.modifiers.get_option("opt_123")
        by_group = client.modifiers.get_options_by_group(
            "grp_123",
            PaginationRequest(page=1, page_size=10),
        )
        listed = client.modifiers.list_options(
            PaginationRequest(page=1, page_size=10)
        )
        updated = client.modifiers.update_option(
            "opt_123",
            UpdateModifierOption(id="opt_123", name="Extra Sauce"),
        )
        deleted = client.modifiers.delete_option("opt_123")
        batch = client.modifiers.create_option_batch(
            [
                CreateModifierOption(
                    modifier_group_id="grp_123",
                    name="Bacon",
                )
            ]
        )

        assert created.id == "opt_123"
        assert fetched.id == "opt_123"
        assert by_group.meta.total_count == 1
        assert listed.meta.total_count == 1
        assert updated.id == "opt_123"
        assert deleted is True
        assert len(batch.data) == 1

    def test_binding_methods(self, client: WiilClient, mock_api, api_response):
        binding = self._binding()
        paged = {
            "data": [binding],
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
            f"{BASE_URL}/modifiers/bindings",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(binding),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/modifiers/bindings/bind_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(binding),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/modifiers/bindings/by-menu-item/"
                "item_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/modifiers/bindings/by-menu-set/"
                "set_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/modifiers/bindings?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/modifiers/bindings/bind_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(binding),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/modifiers/bindings/bind_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/modifiers/bindings/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        created = client.modifiers.create_binding(
            CreateItemModifierBinding(
                menu_item_id="item_123",
                modifier_group_id="grp_123",
            )
        )
        fetched = client.modifiers.get_binding("bind_123")
        by_item = client.modifiers.get_bindings_by_menu_item(
            "item_123",
            PaginationRequest(page=1, page_size=10),
        )
        by_set = client.modifiers.get_bindings_by_menu_set(
            "set_123",
            PaginationRequest(page=1, page_size=10),
        )
        listed = client.modifiers.list_bindings(
            PaginationRequest(page=1, page_size=10)
        )
        updated = client.modifiers.update_binding(
            "bind_123",
            UpdateItemModifierBinding(
                id="bind_123",
                menu_item_id="item_123",
                modifier_group_id="grp_123",
            ),
        )
        deleted = client.modifiers.delete_binding("bind_123")
        batch = client.modifiers.create_binding_batch(
            [
                CreateItemModifierBinding(
                    menu_set_id="set_123",
                    modifier_group_id="grp_123",
                )
            ]
        )

        assert created.id == "bind_123"
        assert fetched.id == "bind_123"
        assert by_item.meta.total_count == 1
        assert by_set.meta.total_count == 1
        assert listed.meta.total_count == 1
        assert updated.id == "bind_123"
        assert deleted is True
        assert len(batch.data) == 1
