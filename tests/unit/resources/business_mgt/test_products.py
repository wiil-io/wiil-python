"""Tests for Products resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductsResource:
    """Test suite for ProductsResource."""

    # =============== Product Category Tests ===============

    def test_create_category(self, client: WiilClient, mock_api, api_response):
        """Test creating a new product category."""
        input_data = {
            "name": "Electronics",
            "description": "Electronic devices",
        }

        mock_response = {
            "id": "cat_123",
            "name": "Electronics",
            "description": "Electronic devices",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/product-management/categories",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.create_category(**input_data)

        assert result.id == "cat_123"
        assert result.name == "Electronics"

    def test_get_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product category by ID."""
        mock_response = {
            "id": "cat_123",
            "name": "Electronics",
            "description": "Electronic devices",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/product-management/categories/cat_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.get_category("cat_123")

        assert result.id == "cat_123"
        assert result.name == "Electronics"

    def test_list_categories(self, client: WiilClient, mock_api, api_response):
        """Test listing product categories with pagination."""
        mock_categories = [
            {
                "id": "cat_1",
                "name": "Electronics",
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "cat_2",
                "name": "Clothing",
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_categories,
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
            f"{BASE_URL}/product-management/categories?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.list_categories(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_update_category(self, client: WiilClient, mock_api, api_response):
        """Test updating a product category."""
        update_data = {
            "id": "cat_123",
            "name": "Updated Electronics",
            "description": "New description",
        }

        mock_response = {
            "id": "cat_123",
            "name": "Updated Electronics",
            "description": "New description",
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/product-management/categories",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.update_category(**update_data)

        assert result.name == "Updated Electronics"
        assert result.description == "New description"

    def test_delete_category(self, client: WiilClient, mock_api, api_response):
        """Test deleting a product category."""
        mock_api.delete(
            f"{BASE_URL}/product-management/categories/cat_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.products.delete_category("cat_123")

        assert result is True

    # =============== Product Tests ===============

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new product."""
        input_data = {
            "name": "Wireless Mouse",
            "category_id": "cat_123",
            "sku": "WM-001",
            "price": 29.99,
            "description": "Ergonomic wireless mouse",
        }

        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "categoryId": "cat_123",
            "sku": "WM-001",
            "price": 29.99,
            "description": "Ergonomic wireless mouse",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.post(
            f"{BASE_URL}/product-management/products",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.create(**input_data)

        assert result.id == "prod_123"
        assert result.name == "Wireless Mouse"
        assert result.sku == "WM-001"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product by ID."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "categoryId": "cat_123",
            "sku": "WM-001",
            "price": 29.99,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/product-management/products/prod_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.get("prod_123")

        assert result.id == "prod_123"
        assert result.name == "Wireless Mouse"

    def test_get_by_sku(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product by SKU."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "sku": "WM-001",
            "price": 29.99,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/product-management/products/by-sku/WM-001",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.get_by_sku("WM-001")

        assert result.sku == "WM-001"
        assert result.name == "Wireless Mouse"

    def test_get_by_barcode(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product by barcode."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "barcode": "1234567890123",
            "price": 29.99,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.get(
            f"{BASE_URL}/product-management/products/by-barcode/1234567890123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.get_by_barcode("1234567890123")

        assert result.barcode == "1234567890123"
        assert result.name == "Wireless Mouse"

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing products with pagination."""
        mock_products = [
            {
                "id": "prod_1",
                "name": "Wireless Mouse",
                "sku": "WM-001",
                "price": 29.99,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "prod_2",
                "name": "Keyboard",
                "sku": "KB-001",
                "price": 49.99,
                "createdAt": 1234567891,
                "updatedAt": 1234567891,
            },
        ]

        mock_response = {
            "data": mock_products,
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
            f"{BASE_URL}/product-management/products?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.list(page=1, page_size=10)

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving products by category."""
        mock_products = [
            {
                "id": "prod_1",
                "name": "Wireless Mouse",
                "categoryId": "cat_123",
                "sku": "WM-001",
                "price": 29.99,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_products,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/product-management/products/by-category/cat_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.get_by_category("cat_123", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].category_id == "cat_123"

    def test_search(self, client: WiilClient, mock_api, api_response):
        """Test searching products by query."""
        mock_products = [
            {
                "id": "prod_1",
                "name": "Wireless Mouse",
                "sku": "WM-001",
                "price": 29.99,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_products,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.get(
            f"{BASE_URL}/product-management/products/search?query=mouse&page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.search("mouse", page=1, page_size=10)

        assert len(result.data) == 1
        assert result.data[0].name == "Wireless Mouse"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a product."""
        update_data = {
            "id": "prod_123",
            "name": "Updated Wireless Mouse",
            "price": 34.99,
        }

        mock_response = {
            "id": "prod_123",
            "name": "Updated Wireless Mouse",
            "price": 34.99,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.patch(
            f"{BASE_URL}/product-management/products",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(mock_response)))

        result = client.products.update(**update_data)

        assert result.name == "Updated Wireless Mouse"
        assert result.price == 34.99

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a product."""
        mock_api.delete(
            f"{BASE_URL}/product-management/products/prod_123",
            headers={"X-WIIL-API-Key": API_KEY}
        ).mock(return_value=Response(200, json=api_response(True)))

        result = client.products.delete("prod_123")

        assert result is True
