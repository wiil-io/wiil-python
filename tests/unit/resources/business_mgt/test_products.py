"""Tests for Products resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreateProductCategory,
    UpdateProductCategory,
    CreateBusinessProduct,
    CreateBusinessProductVariant,
    UpdateBusinessProduct,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductsResource:
    """Test suite for ProductsResource."""

    # =============== Product Category Tests ===============

    def test_create_category(self, client: WiilClient, mock_api, api_response):
        """Test creating a new product category."""
        mock_response = {
            "id": "cat_123",
            "name": "Electronics",
            "description": "Electronic devices",
            "displayOrder": None,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/product-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.create_category(CreateProductCategory(
            name="Electronics",
            description="Electronic devices"
        ))

        assert result.id == "cat_123"
        assert result.name == "Electronics"

    def test_get_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product category by ID."""
        mock_response = {
            "id": "cat_123",
            "name": "Electronics",
            "description": "Electronic devices",
            "displayOrder": None,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/categories/cat_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.get_category("cat_123")

        assert result.id == "cat_123"
        assert result.name == "Electronics"

    def test_list_categories(self, client: WiilClient, mock_api, api_response):
        """Test listing product categories with pagination."""
        mock_categories = [
            {
                "id": "cat_1",
                "name": "Electronics",
                "description": None,
                "displayOrder": 1,
                "isDefault": False,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "cat_2",
                "name": "Clothing",
                "description": None,
                "displayOrder": 2,
                "isDefault": False,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/categories?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.list_categories(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_update_category(self, client: WiilClient, mock_api, api_response):
        """Test updating a product category."""
        mock_response = {
            "id": "cat_123",
            "name": "Updated Electronics",
            "description": "New description",
            "displayOrder": None,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.update_category(UpdateProductCategory(
            id="cat_123",
            name="Updated Electronics",
            description="New description"
        ))

        assert result.name == "Updated Electronics"
        assert result.description == "New description"

    def test_delete_category(self, client: WiilClient, mock_api, api_response):
        """Test deleting a product category."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-management/categories/cat_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.products.delete_category("cat_123")

        assert result is True

    # =============== Product Tests ===============

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new product."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "description": "Ergonomic wireless mouse",
            "price": 29.99,
            "sku": "WM-001",
            "barcode": None,
            "categoryId": "cat_123",
            "category": None,
            "brand": None,
            "trackInventory": False,
            "stockQuantity": None,
            "lowStockThreshold": None,
            "weight": None,
            "dimensions": None,
            "isActive": True,
            "displayOrder": None,
            "variants": [
                {
                    "id": "var_1",
                    "productId": "prod_123",
                    "axisValues": {"color": "black"},
                    "stockStatus": "in_stock",
                }
            ],
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/product-management/products",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.create(CreateBusinessProduct(
            name="Wireless Mouse",
            category_id="cat_123",
            sku="WM-001",
            price=29.99,
            description="Ergonomic wireless mouse",
            variants=[
                CreateBusinessProductVariant(axis_values={"color": "black"})
            ]
        ))

        assert result.id == "prod_123"
        assert result.name == "Wireless Mouse"
        assert result.sku == "WM-001"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product by ID."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "description": None,
            "price": 29.99,
            "sku": "WM-001",
            "barcode": None,
            "categoryId": "cat_123",
            "category": None,
            "brand": None,
            "trackInventory": False,
            "stockQuantity": None,
            "lowStockThreshold": None,
            "weight": None,
            "dimensions": None,
            "isActive": True,
            "displayOrder": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/products/prod_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.get("prod_123")

        assert result.id == "prod_123"
        assert result.name == "Wireless Mouse"

    def test_get_by_sku(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product by SKU."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "description": None,
            "price": 29.99,
            "sku": "WM-001",
            "barcode": None,
            "categoryId": "cat_123",
            "category": None,
            "brand": None,
            "trackInventory": False,
            "stockQuantity": None,
            "lowStockThreshold": None,
            "weight": None,
            "dimensions": None,
            "isActive": True,
            "displayOrder": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/products/by-sku/WM-001",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.get_by_sku("WM-001")

        assert result.sku == "WM-001"
        assert result.name == "Wireless Mouse"

    def test_get_by_barcode(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a product by barcode."""
        mock_response = {
            "id": "prod_123",
            "name": "Wireless Mouse",
            "description": None,
            "price": 29.99,
            "sku": None,
            "barcode": "1234567890123",
            "categoryId": "cat_123",
            "category": None,
            "brand": None,
            "trackInventory": False,
            "stockQuantity": None,
            "lowStockThreshold": None,
            "weight": None,
            "dimensions": None,
            "isActive": True,
            "displayOrder": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/products/by-barcode/1234567890123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.get_by_barcode("1234567890123")

        assert result.barcode == "1234567890123"
        assert result.name == "Wireless Mouse"

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing products with pagination."""
        mock_products = [
            {
                "id": "prod_1",
                "name": "Wireless Mouse",
                "description": None,
                "price": 29.99,
                "sku": "WM-001",
                "barcode": None,
                "categoryId": "cat_123",
                "category": None,
                "brand": None,
                "trackInventory": False,
                "stockQuantity": None,
                "lowStockThreshold": None,
                "weight": None,
                "dimensions": None,
                "isActive": True,
                "displayOrder": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
            {
                "id": "prod_2",
                "name": "Keyboard",
                "description": None,
                "price": 49.99,
                "sku": "KB-001",
                "barcode": None,
                "categoryId": "cat_123",
                "category": None,
                "brand": None,
                "trackInventory": False,
                "stockQuantity": None,
                "lowStockThreshold": None,
                "weight": None,
                "dimensions": None,
                "isActive": True,
                "displayOrder": None,
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

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/products?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.list(PaginationRequest(page=1, page_size=10))

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_by_category(self, client: WiilClient, mock_api, api_response):
        """Test retrieving products by category."""
        mock_products = [
            {
                "id": "prod_1",
                "name": "Wireless Mouse",
                "description": None,
                "price": 29.99,
                "sku": "WM-001",
                "barcode": None,
                "categoryId": "cat_123",
                "category": None,
                "brand": None,
                "trackInventory": False,
                "stockQuantity": None,
                "lowStockThreshold": None,
                "weight": None,
                "dimensions": None,
                "isActive": True,
                "displayOrder": None,
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

        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/product-management/products/by-category/"
                "cat_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.get_by_category(
            "cat_123",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].category_id == "cat_123"

    def test_search(self, client: WiilClient, mock_api, api_response):
        """Test searching products by query."""
        mock_products = [
            {
                "id": "prod_1",
                "name": "Wireless Mouse",
                "description": None,
                "price": 29.99,
                "sku": "WM-001",
                "barcode": None,
                "categoryId": "cat_123",
                "category": None,
                "brand": None,
                "trackInventory": False,
                "stockQuantity": None,
                "lowStockThreshold": None,
                "weight": None,
                "dimensions": None,
                "isActive": True,
                "displayOrder": None,
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

        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/product-management/products/search?"
                "query=mouse&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.search(
            "mouse",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].name == "Wireless Mouse"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a product."""
        mock_response = {
            "id": "prod_123",
            "name": "Updated Wireless Mouse",
            "description": None,
            "price": 34.99,
            "sku": "WM-001",
            "barcode": None,
            "categoryId": "cat_123",
            "category": None,
            "brand": None,
            "trackInventory": False,
            "stockQuantity": None,
            "lowStockThreshold": None,
            "weight": None,
            "dimensions": None,
            "isActive": True,
            "displayOrder": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-management/products",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.update(UpdateBusinessProduct(
            id="prod_123",
            name="Updated Wireless Mouse",
            price=34.99
        ))

        assert result.name == "Updated Wireless Mouse"
        assert result.price == 34.99

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a product."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-management/products/prod_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.products.delete("prod_123")

        assert result is True

    def test_create_category_batch(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        """Test creating product categories in batch."""
        mock_response = {
            "data": [
                {
                    "id": "cat_1",
                    "name": "Electronics",
                    "description": None,
                    "displayOrder": 1,
                    "isDefault": False,
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
            f"{BASE_URL}/product-management/categories/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.create_category_batch(
            [CreateProductCategory(name="Electronics")]
        )

        assert len(result.data) == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        """Test creating products in batch."""
        mock_response = {
            "data": [
                {
                    "id": "prod_1",
                    "name": "Wireless Mouse",
                    "description": None,
                    "price": 29.99,
                    "sku": "WM-001",
                    "barcode": None,
                    "categoryId": "cat_123",
                    "category": None,
                    "brand": None,
                    "trackInventory": False,
                    "stockQuantity": None,
                    "lowStockThreshold": None,
                    "weight": None,
                    "dimensions": None,
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
            f"{BASE_URL}/product-management/products/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.products.create_batch(
            [
                CreateBusinessProduct(
                    name="Wireless Mouse",
                    category_id="cat_123",
                    sku="WM-001",
                    price=29.99,
                    variants=[
                        CreateBusinessProductVariant(
                            axis_values={"color": "black"}
                        )
                    ],
                )
            ]
        )

        assert len(result.data) == 1

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create product handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/product-management/products",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Price is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.products.create(CreateBusinessProduct(
                name="Test Product",
                price=0,
                variants=[
                    CreateBusinessProductVariant(axis_values={"color": "black"})
                ]
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get product handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/products/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Product not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.products.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
