"""Tests for Product Variant Axes resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateVariantAxis,
    UpdateVariantAxis,
    VariantAxisValue,
)
from wiil.models.type_definitions.business_definitions import VariantAxisType
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductVariantAxesResource:
    """Test suite for ProductVariantAxesResource."""

    def _axis(self, axis_id: str = "axis_123") -> dict:
        return {
            "id": axis_id,
            "name": "Size",
            "type": "text",
            "values": [
                {
                    "id": "size_s",
                    "label": "Small",
                    "swatchColor": None,
                    "imageId": None,
                    "numericValue": None,
                    "sortOrder": 0,
                }
            ],
            "isActive": True,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_crud_and_query(self, client: WiilClient, mock_api, api_response):
        axis = self._axis()
        paged = {
            "data": [axis],
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
            f"{BASE_URL}/product-variant-axes",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(axis),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-variant-axes/axis_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(axis),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-variant-axes/by-name/Size",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(axis),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-variant-axes/axis_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(axis),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-variant-axes/axis_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-variant-axes?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.product_variant_axes.create(
            CreateVariantAxis(
                name="Size",
                type=VariantAxisType.TEXT,
                values=[VariantAxisValue(id="size_s", label="Small")],
            )
        )
        get_result = client.product_variant_axes.get("axis_123")
        by_name = client.product_variant_axes.get_by_name("Size")
        update_result = client.product_variant_axes.update(
            "axis_123",
            UpdateVariantAxis(id="axis_123", name="Size"),
        )
        delete_result = client.product_variant_axes.delete("axis_123")
        list_result = client.product_variant_axes.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "axis_123"
        assert get_result.id == "axis_123"
        assert by_name is not None
        assert update_result.id == "axis_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        paged = {
            "data": [self._axis("axis_1")],
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
            f"{BASE_URL}/product-variant-axes/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.product_variant_axes.create_batch(
            [
                CreateVariantAxis(
                    name="Size",
                    type=VariantAxisType.TEXT,
                    values=[VariantAxisValue(id="size_s", label="Small")],
                )
            ]
        )

        assert len(result.data) == 1
