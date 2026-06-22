"""Tests for Product Axis Bindings resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateProductAxisBinding,
    UpdateProductAxisBinding,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductAxisBindingsResource:
    """Test suite for ProductAxisBindingsResource."""

    def _binding(self, binding_id: str = "bind_123") -> dict:
        return {
            "id": binding_id,
            "productRevisionId": None,
            "productId": "prod_123",
            "axisId": "axis_123",
            "displayOrder": 0,
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
            f"{BASE_URL}/product-management/axis-bindings",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(binding),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/axis-bindings/bind_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(binding),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/product-management/axis-bindings/by-product/"
                "prod_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/product-management/axis-bindings/by-axis/"
                "axis_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-management/axis-bindings/bind_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(binding),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-management/axis-bindings/bind_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/axis-bindings?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.product_axis_bindings.create(
            CreateProductAxisBinding(product_id="prod_123", axis_id="axis_123")
        )
        get_result = client.product_axis_bindings.get("bind_123")
        by_product = client.product_axis_bindings.get_by_product(
            "prod_123",
            PaginationRequest(page=1, page_size=10),
        )
        by_axis = client.product_axis_bindings.get_by_axis(
            "axis_123",
            PaginationRequest(page=1, page_size=10),
        )
        update_result = client.product_axis_bindings.update(
            "bind_123",
            UpdateProductAxisBinding(id="bind_123", display_order=1),
        )
        delete_result = client.product_axis_bindings.delete("bind_123")
        list_result = client.product_axis_bindings.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "bind_123"
        assert get_result.id == "bind_123"
        assert by_product.meta.total_count == 1
        assert by_axis.meta.total_count == 1
        assert update_result.id == "bind_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        paged = {
            "data": [self._binding("bind_1")],
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
            f"{BASE_URL}/product-management/axis-bindings/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.product_axis_bindings.create_batch(
            [
                CreateProductAxisBinding(
                    product_id="prod_123",
                    axis_id="axis_123",
                )
            ]
        )

        assert len(result.data) == 1
