"""Tests for Menus resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestMenusResource:
    """Test suite for MenusResource."""

    # =============== Menu Category Tests ===============

    def test_create_category(self, client: WiilClient, mock_api, api_response):
        """Test creating a new menu category."""
        input_data = {
            "name": "Appetizers",
            "description": "Starter dishes",
        }

        mock_response = {
            "id": "cat_123",
            "name": "Appetizers",
            "description": "Starter dishes",
            "displayOrder": 1,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/menu-management/categories",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menus.create_category(**input_data)

        assert result.id == "cat_123"
        assert result.name == "Appetizers"

    def test_get_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a menu category by ID."""
        mock_response = {
            "id": "cat_123",
            "name": "Appetizers",
            "description": "Starter dishes",
            "displayOrder": 1,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/menu-management/categories/cat_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

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
                "isDefault": False,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "cat_2",
                "name": "Main Course",
                "description": None,
                "displayOrder": 2,
                "isDefault": False,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_api.get(
            f"{BASE_URL}/menu-management/categories",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_categories)))

        result = client.menus.list_categories()

        assert len(result) == 2
        assert result[0].name == "Appetizers"

    def test_update_category(self, client: WiilClient, mock_api, api_response):
        """Test updating a menu category."""
        update_data = {
            "id": "cat_123",
            "name": "Updated Appetizers",
            "description": "New description",
        }

        mock_response = {
            "id": "cat_123",
            "name": "Updated Appetizers",
            "description": "New description",
            "displayOrder": 1,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/menu-management/categories",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menus.update_category(**update_data)

        assert result.name == "Updated Appetizers"
        assert result.description == "New description"

    def test_delete_category(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu category."""
        mock_api.delete(
            f"{BASE_URL}/menu-management/categories/cat_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.menus.delete_category("cat_123")

        assert result is True

    # =============== Menu Item Tests ===============

    def test_create_item(self, client: WiilClient, mock_api, api_response):
        """Test creating a new menu item."""
        input_data = {
            "name": "Caesar Salad",
            "category_id": "cat_123",
            "price": 12.99,
            "description": "Fresh romaine lettuce",
        }

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
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/menu-management/items",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menus.create_item(**input_data)

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
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/menu-management/items/item_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

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

        mock_api.get(
            f"{BASE_URL}/menu-management/items?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menus.list_items(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_items_by_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving menu items by category."""
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
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_api.get(
            f"{BASE_URL}/menu-management/items/by-category/cat_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_items)))

        result = client.menus.get_items_by_category("cat_123")

        assert len(result) == 1
        assert result[0].category_id == "cat_123"

    def test_get_popular_items(self, client: WiilClient, mock_api, api_response):
        """Test retrieving popular menu items."""
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
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_api.get(
            f"{BASE_URL}/menu-management/items/popular?limit=5",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_items)))

        result = client.menus.get_popular_items(limit=5)

        assert len(result) == 1
        assert result[0].name == "Caesar Salad"

    def test_update_item(self, client: WiilClient, mock_api, api_response):
        """Test updating a menu item."""
        update_data = {
            "id": "item_123",
            "name": "Updated Caesar Salad",
            "price": 13.99,
        }

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
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/menu-management/items",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menus.update_item(**update_data)

        assert result.name == "Updated Caesar Salad"
        assert result.price == 13.99

    def test_delete_item(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu item."""
        mock_api.delete(
            f"{BASE_URL}/menu-management/items/item_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.menus.delete_item("item_123")

        assert result is True

    # =============== Menu QR Code Tests ===============

    def test_get_qr_codes(self, client: WiilClient, mock_api, api_response):
        """Test retrieving all menu QR codes."""
        mock_qr_codes = [
            {
                "id": "qr_123",
                "menuUrl": "https://menu.example.com/qr_123",
                "qrCodeImage": None,
                "tableNumber": "Table 1",
            },
        ]

        mock_api.get(
            f"{BASE_URL}/menu-management/qr-codes",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_qr_codes)))

        result = client.menus.get_qr_codes()

        assert len(result) == 1
        assert result[0].table_number == "Table 1"

    def test_generate_qr_code(self, client: WiilClient, mock_api, api_response):
        """Test generating a new menu QR code."""
        mock_response = {
            "id": "qr_123",
            "menuUrl": "https://menu.example.com/qr_123",
            "qrCodeImage": None,
            "tableNumber": "Table 1",
        }

        mock_api.post(
            f"{BASE_URL}/menu-management/qr-codes",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.menus.generate_qr_code(name="Table 1 Menu", category_id="cat_123")

        assert result.id == "qr_123"
        assert result.menu_url == "https://menu.example.com/qr_123"

    def test_delete_qr_code(self, client: WiilClient, mock_api, api_response):
        """Test deleting a menu QR code."""
        mock_api.delete(
            f"{BASE_URL}/menu-management/qr-codes/qr_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.menus.delete_qr_code("qr_123")

        assert result is True
