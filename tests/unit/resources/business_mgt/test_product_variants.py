"""Tests for Product Variants resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import CreateProductVariant, UpdateProductVariant

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestProductVariantsResource:
    """Test suite for ProductVariantsResource."""

    def _variant(self, variant_id: str = "var_123") -> dict:
        return {
            "id": variant_id,
            "productId": "prod_123",
            "axisValues": {"size": "M"},
            "sku": "SKU-001",
            "barcode": None,
            "partNumber": None,
            "globalTradeItemNumber": None,
            "price": 19.99,
            "cost": None,
            "compareAtPrice": None,
            "stockQuantity": 10,
            "lowStockThreshold": 2,
            "unitDefinitionId": None,
            "inventoryUnit": None,
            "weight": None,
            "dimensions": None,
            "imageId": None,
            "imageIds": None,
            "channelMappings": None,
            "isActive": True,
            "isDefault": False,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_crud(self, client: WiilClient, mock_api, api_response):
        created = self._variant()
        updated = self._variant()
        updated["sku"] = "SKU-002"

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/product-management/variants",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(created),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/variants/var_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(created),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/product-management/variants/var_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(updated),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/product-management/variants/var_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        create_result = client.product_variants.create(
            CreateProductVariant(
                product_id="prod_123",
                axis_values={"size": "M"},
            )
        )
        get_result = client.product_variants.get("var_123")
        update_result = client.product_variants.update(
            "var_123",
            UpdateProductVariant(id="var_123", sku="SKU-002"),
        )
        delete_result = client.product_variants.delete("var_123")

        assert create_result.id == "var_123"
        assert get_result.id == "var_123"
        assert update_result.sku == "SKU-002"
        assert delete_result is True

    def test_query_methods(self, client: WiilClient, mock_api, api_response):
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/variants/by-sku/SKU-001",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(self._variant()),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/product-management/variants/default/prod_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(self._variant("var_default")),
            status=200,
        )

        by_sku = client.product_variants.get_by_sku("SKU-001")
        default_variant = client.product_variants.get_default("prod_123")

        assert by_sku is not None
        assert default_variant is not None

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        paged = {
            "data": [self._variant("var_1")],
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
            f"{BASE_URL}/product-management/variants/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.product_variants.create_batch(
            [
                CreateProductVariant(
                    product_id="prod_123",
                    axis_values={"size": "M"},
                )
            ]
        )

        assert len(result.data) == 1
