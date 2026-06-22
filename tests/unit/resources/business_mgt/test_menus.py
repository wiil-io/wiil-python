"""Tests for Menus resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateMenuCategory,
    UpdateMenuCategory,
    CreateBusinessMenuItem,
    CreateBusinessMenuItemVariant,
    UpdateBusinessMenuItem,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenusResource:
    """Test suite for MenusResource."""

    # =============== Menu Category Tests ===============

    def test_create_category(self, client: WiilClient, mock_api, api_response):
        """Test creating a new menu category."""
        mock_response = {
            "id": "cat_123",
            "name": "Appetizers",
            "description": "Starter dishes",
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.create_category(CreateMenuCategory(
            name="Appetizers",
            description="Starter dishes"
        ))

        assert result.id == "cat_123"
        assert result.name == "Appetizers"

    def test_get_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a menu category by ID."""
        mock_response = {
            "id": "cat_123",
            "name": "Appetizers",
            "description": "Starter dishes",
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/categories/cat_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.get_category("cat_123")

        assert result.id == "cat_123"
        assert result.name == "Appetizers"

    def test_list_categories(self, client: WiilClient, mock_api, api_response):
        """Test listing all menu categories."""
        mock_categories = [
            {
                "id": "cat_1",
                "name": "Appetizers",
                "description": None,
                "displayOrder": 1,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "cat_2",
                "name": "Main Course",
                "description": None,
                "displayOrder": 2,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_categories),
            status=200,
        )

        result = client.menus.list_categories()

        assert len(result) == 2
        assert result[0].name == "Appetizers"

    def test_update_category(self, client: WiilClient, mock_api, api_response):
        """Test updating a menu category."""
        mock_response = {
            "id": "cat_123",
            "name": "Updated Appetizers",
            "description": "New description",
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/menu-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.update_category(UpdateMenuCategory(
            id="cat_123",
            name="Updated Appetizers",
            description="New description"
        ))

        assert result.name == "Updated Appetizers"
        assert result.description == "New description"

    def test_delete_category(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu category."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/menu-management/categories/cat_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.menus.delete_category("cat_123")

        assert result is True

    # =============== Menu Item Tests ===============

    def test_create_item(self, client: WiilClient, mock_api, api_response):
        """Test creating a new menu item."""
        mock_response = {
            "id": "item_123",
            "name": "Caesar Salad",
            "description": "Fresh romaine lettuce",
            "price": 12.99,
            "categoryId": "cat_123",
            "category": None,
            "ingredients": None,
            "allergens": None,
            "nutritionalInfo": None,
            "isAvailable": True,
            "preparationTime": None,
            "isActive": True,
            "displayOrder": None,
            "variants": [
                {
                    "id": "var_1",
                    "menuItemId": "item_123",
                    "name": "Regular",
                    "price": 12.99,
                }
            ],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-management/items",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.create_item(CreateBusinessMenuItem(
            name="Caesar Salad",
            category_id="cat_123",
            price=12.99,
            description="Fresh romaine lettuce",
            variants=[
                CreateBusinessMenuItemVariant(name="Regular", price=12.99)
            ]
        ))

        assert result.id == "item_123"
        assert result.name == "Caesar Salad"
        assert result.price == 12.99

    def test_get_item(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a menu item by ID."""
        mock_response = {
            "id": "item_123",
            "name": "Caesar Salad",
            "description": None,
            "price": 12.99,
            "categoryId": "cat_123",
            "category": None,
            "ingredients": None,
            "allergens": None,
            "nutritionalInfo": None,
            "isAvailable": True,
            "preparationTime": None,
            "isActive": True,
            "displayOrder": None,
            "variants": [
                {
                    "id": "var_1",
                    "menuItemId": "item_123",
                    "name": "Regular",
                    "price": 12.99,
                }
            ],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/items/item_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.get_item("item_123")

        assert result.id == "item_123"
        assert result.name == "Caesar Salad"

    def test_list_items(self, client: WiilClient, mock_api, api_response):
        """Test listing menu items with pagination."""
        mock_items = [
            {
                "id": "item_1",
                "name": "Caesar Salad",
                "description": None,
                "price": 12.99,
                "categoryId": "cat_123",
                "category": None,
                "ingredients": None,
                "allergens": None,
                "nutritionalInfo": None,
                "isAvailable": True,
                "preparationTime": None,
                "isActive": True,
                "displayOrder": None,
                "variants": [
                    {
                        "id": "var_1",
                        "menuItemId": "item_1",
                        "name": "Regular",
                        "price": 12.99,
                    }
                ],
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "item_2",
                "name": "Greek Salad",
                "description": None,
                "price": 10.99,
                "categoryId": "cat_123",
                "category": None,
                "ingredients": None,
                "allergens": None,
                "nutritionalInfo": None,
                "isAvailable": True,
                "preparationTime": None,
                "isActive": True,
                "displayOrder": None,
                "variants": [
                    {
                        "id": "var_2",
                        "menuItemId": "item_2",
                        "name": "Regular",
                        "price": 10.99,
                    }
                ],
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_items,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 2,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/items?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.list_items(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_items_by_category(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving menu items by category."""
        mock_items = {
            "data": [
                {
                    "id": "item_1",
                    "name": "Caesar Salad",
                    "description": None,
                    "price": 12.99,
                    "categoryId": "cat_123",
                    "category": None,
                    "ingredients": None,
                    "allergens": None,
                    "nutritionalInfo": None,
                    "isAvailable": True,
                    "preparationTime": None,
                    "isActive": True,
                    "displayOrder": None,
                    "variants": [
                        {
                            "id": "var_1",
                            "menuItemId": "item_1",
                            "name": "Regular",
                            "price": 12.99,
                        }
                    ],
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                },
            ],
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
                f"{BASE_URL}/menu-management/items/by-category/"
                "cat_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_items),
            status=200,
        )

        result = client.menus.get_items_by_category(
            "cat_123",
            PaginationRequest(page=1, page_size=10),
        )

        assert len(result.data) == 1
        assert result.data[0].category_id == "cat_123"

    def test_get_popular_items(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test retrieving popular menu items."""
        mock_items = {
            "data": [
                {
                    "id": "item_1",
                    "name": "Caesar Salad",
                    "description": None,
                    "price": 12.99,
                    "categoryId": "cat_123",
                    "category": None,
                    "ingredients": None,
                    "allergens": None,
                    "nutritionalInfo": None,
                    "isAvailable": True,
                    "preparationTime": None,
                    "isActive": True,
                    "displayOrder": None,
                    "variants": [
                        {
                            "id": "var_1",
                            "menuItemId": "item_1",
                            "name": "Regular",
                            "price": 12.99,
                        }
                    ],
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                },
            ],
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
                f"{BASE_URL}/menu-management/items/popular?"
                "page=1&pageSize=10&limit=5"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_items),
            status=200,
        )

        result = client.menus.get_popular_items(
            PaginationRequest(page=1, page_size=10),
            limit=5,
        )

        assert len(result.data) == 1
        assert result.data[0].name == "Caesar Salad"

    def test_create_category_batch(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test creating menu categories in batch."""
        mock_response = {
            "data": [
                {
                    "id": "cat_1",
                    "name": "Appetizers",
                    "description": None,
                    "displayOrder": 1,
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                }
            ],
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
            f"{BASE_URL}/menu-management/categories/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.create_category_batch(
            [CreateMenuCategory(name="Appetizers")]
        )

        assert len(result.data) == 1
        assert result.data[0].name == "Appetizers"

    def test_create_item_batch(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test creating menu items in batch."""
        mock_response = {
            "data": [
                {
                    "id": "item_1",
                    "name": "Caesar Salad",
                    "description": None,
                    "price": 12.99,
                    "categoryId": "cat_123",
                    "category": None,
                    "ingredients": None,
                    "allergens": None,
                    "nutritionalInfo": None,
                    "isAvailable": True,
                    "preparationTime": None,
                    "isActive": True,
                    "displayOrder": None,
                    "createdAt": 1234567890,
                    "updatedAt": 1234567890,
                }
            ],
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
            f"{BASE_URL}/menu-management/items/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.create_item_batch(
            [
                CreateBusinessMenuItem(
                    name="Caesar Salad",
                    category_id="cat_123",
                    price=12.99,
                    variants=[
                        CreateBusinessMenuItemVariant(
                            name="Regular", price=12.99
                        )
                    ],
                )
            ]
        )

        assert len(result.data) == 1
        assert result.data[0].name == "Caesar Salad"

    def test_update_item(self, client: WiilClient, mock_api, api_response):
        """Test updating a menu item."""
        mock_response = {
            "id": "item_123",
            "name": "Updated Caesar Salad",
            "description": None,
            "price": 13.99,
            "categoryId": "cat_123",
            "category": None,
            "ingredients": None,
            "allergens": None,
            "nutritionalInfo": None,
            "isAvailable": True,
            "preparationTime": None,
            "isActive": True,
            "displayOrder": None,
            "variants": [
                {
                    "id": "var_1",
                    "menuItemId": "item_123",
                    "name": "Regular",
                    "price": 13.99,
                }
            ],
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/menu-management/items",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.menus.update_item(UpdateBusinessMenuItem(
            id="item_123",
            name="Updated Caesar Salad",
            price=13.99
        ))

        assert result.name == "Updated Caesar Salad"
        assert result.price == 13.99

    def test_delete_item(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu item."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/menu-management/items/item_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.menus.delete_item("item_123")

        assert result is True

    # =============== Error Handling Tests ===============

    def test_create_category_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create category handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/menu-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Name is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.menus.create_category(CreateMenuCategory(name="Appetizers"))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_item_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get item handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/menu-management/items/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Menu item not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.menus.get_item("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
