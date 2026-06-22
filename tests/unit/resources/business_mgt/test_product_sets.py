"""Tests for Product Sets resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateProductSet,
    ProductSetItem,
    UpdateProductSet,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductSetsResource:
    """Test suite for ProductSetsResource."""

    def _product_set(self, set_id: str = "set_123") -> dict:
        return {
            "id": set_id,
            "productRevisionId": None,
            "code": "BUNDLE-1",
            "name": "Bundle",
            "description": None,
            "channelMappings": None,
            "targetingMode": "EXPLICIT",
            "pricingMode": "SUM_OF_ITEMS",
            "fixedPrice": None,
            "items": [
                {
                    "productId": "prod_123",
                    "productVariantId": None,
                    "quantity": 1,
                    "isRequired": True,
                    "displayOrder": None,
                }
            ],
            "selector": None,
            "isActive": True,
            "imageUrl": None,
            "imageUrls": None,
            "displayOrder": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_crud_and_queries(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        product_set = self._product_set()
        paged = {
            "data": [product_set],
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
            f"{BASE_URL}/product-sets",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(product_set),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-sets/set_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(product_set),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-sets/code/BUNDLE-1",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(product_set),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-sets/active?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-sets/set_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(product_set),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-sets/set_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-sets?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.product_sets.create(
            CreateProductSet(
                name="Bundle",
                items=[ProductSetItem(product_id="prod_123", quantity=1)],
            )
        )
        get_result = client.product_sets.get("set_123")
        by_code = client.product_sets.get_by_code("BUNDLE-1")
        active = client.product_sets.get_active(
            PaginationRequest(page=1, page_size=10)
        )
        update_result = client.product_sets.update(
            "set_123",
            UpdateProductSet(id="set_123", name="Bundle"),
        )
        delete_result = client.product_sets.delete("set_123")
        list_result = client.product_sets.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "set_123"
        assert get_result.id == "set_123"
        assert by_code is not None
        assert active.meta.total_count == 1
        assert update_result.id == "set_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        paged = {
            "data": [self._product_set("set_1")],
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
            f"{BASE_URL}/product-sets/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.product_sets.create_batch(
            [
                CreateProductSet(
                    name="Bundle",
                    items=[ProductSetItem(product_id="prod_123", quantity=1)],
                )
            ]
        )

        assert len(result.data) == 1
