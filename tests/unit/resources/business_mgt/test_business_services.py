"""Tests for Business Services resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    BusinessServiceCatalog,
    CreateBusinessService,
    UpdateBusinessService,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestBusinessServicesResource:
    """Test suite for BusinessServicesResource."""

    @staticmethod
    def _service_payload(service_id: str = 'svc_123'):
        return {
            'id': service_id,
            'name': 'Haircut',
            'description': 'Professional haircut service',
            'duration': 30,
            'basePrice': 25.0,
            'isBookable': True,
            'isActive': True,
            'createdAt': 1234567890,
            'updatedAt': 1234567890,
        }

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new business service."""
        mock_response = self._service_payload()

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/business-services",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.create(CreateBusinessService(
            name="Haircut",
            description="Professional haircut service",
            duration=30,
            is_bookable=True,
            base_price=25.0,
            is_active=True,
        ))

        assert result.id == "svc_123"
        assert result.name == "Haircut"
        assert result.base_price == 25.0

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a business service by ID."""
        mock_response = self._service_payload()

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/business-services/svc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.get("svc_123")

        assert result.id == "svc_123"
        assert result.name == "Haircut"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a business service."""
        mock_response = self._service_payload()
        mock_response['name'] = 'Premium Haircut'
        mock_response['basePrice'] = 35.0
        mock_response['updatedAt'] = 1234567891

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/business-services",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.update(UpdateBusinessService(
            id="svc_123",
            name="Premium Haircut",
            base_price=35.0
        ))

        assert result.name == "Premium Haircut"
        assert result.base_price == 35.0

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a business service."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/business-services/svc_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.business_services.delete("svc_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing business services with pagination."""
        mock_services = [
            self._service_payload('svc_1'),
            self._service_payload('svc_2'),
        ]

        mock_response = {
            "data": mock_services,
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
            f"{BASE_URL}/business-services?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 2
        assert result.meta.total_count == 2

    def test_get_catalog(self, client: WiilClient, mock_api, api_response):
        """Test retrieving service catalog."""
        catalog_payload = [{
            'serviceCategory': {
                'id': 'cat_123',
                'name': 'Hair Services',
                'isActive': True,
                'createdAt': 1234567890,
                'updatedAt': 1234567890,
            },
            'services': [self._service_payload('svc_1')],
        }]

        mock_api.add(
            responses.GET,
            f'{BASE_URL}/business-services/catalog',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(catalog_payload),
            status=200,
        )

        result: BusinessServiceCatalog = client.business_services.get_catalog()

        assert len(result) == 1
        assert result[0].service_category.id == 'cat_123'
        assert len(result[0].services) == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        """Test creating services in batch."""
        mock_response = {
            'data': [self._service_payload('svc_1')],
            'meta': {
                'page': 1,
                'pageSize': 20,
                'totalCount': 1,
                'totalPages': 1,
                'hasNextPage': False,
                'hasPreviousPage': False,
            },
        }

        mock_api.add(
            responses.POST,
            f'{BASE_URL}/business-services/batch',
            headers={'X-Wiil-Api-Key': API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.business_services.create_batch([
            {
                'name': 'Haircut',
                'duration': 30,
                'basePrice': 25.0,
            }
        ])

        assert len(result.data) == 1
        assert result.data[0].id == 'svc_1'

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create service handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/business-services",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Name is required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.business_services.create(
                CreateBusinessService(
                    name="Valid Service",
                )
            )

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get service handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/business-services/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Service not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.business_services.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
