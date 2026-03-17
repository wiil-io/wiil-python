"""Tests for Property Configuration resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreatePropertyCategory,
    UpdatePropertyCategory,
    CreatePropertyAddress,
    UpdatePropertyAddress,
    CreateProperty,
    UpdateProperty,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestPropertyConfigResource:
    """Test suite for PropertyConfigResource."""

    # =============== Property Category Tests ===============

    def test_create_category(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new property category."""
        mock_response = {
            "id": "cat_123",
            "name": "Luxury Homes",
            "description": "High-end residential properties",
            "propertyType": "residential",
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.create_category(CreatePropertyCategory(
            name="Luxury Homes",
            description="High-end residential properties",
            property_type="residential",
            display_order=1
        ))

        assert result.id == "cat_123"
        assert result.name == "Luxury Homes"

    def test_get_category(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a property category by ID."""
        mock_response = {
            "id": "cat_123",
            "name": "Luxury Homes",
            "description": "High-end residential properties",
            "propertyType": "residential",
            "displayOrder": 1,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-management/categories/cat_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.get_category("cat_123")

        assert result.id == "cat_123"
        assert result.property_type == "residential"

    def test_list_categories(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing property categories with pagination."""
        mock_categories = [
            {
                "id": "cat_1",
                "name": "Luxury Homes",
                "description": "High-end properties",
                "propertyType": "residential",
                "displayOrder": 1,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_categories,
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
            f"{BASE_URL}/property-management/categories?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.list_categories(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.meta.total_count == 1

    def test_update_category(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a property category."""
        mock_response = {
            "id": "cat_123",
            "name": "Premium Homes",
            "description": "Updated description",
            "propertyType": "residential",
            "displayOrder": 2,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/property-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.update_category(UpdatePropertyCategory(
            id="cat_123",
            name="Premium Homes",
            description="Updated description"
        ))

        assert result.name == "Premium Homes"
        assert result.description == "Updated description"

    def test_delete_category(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a property category."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/property-management/categories/cat_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.property_config.delete_category("cat_123")

        assert result is True

    # =============== Property Address Tests ===============

    def test_create_address(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new property address."""
        mock_response = {
            "id": "addr_123",
            "street": "123 Main St",
            "unit": "Suite 100",
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94102",
            "country": "USA",
            "coordinates": None,
            "neighborhood": "Downtown",
            "district": None,
            "isVerified": False,
            "verifiedAt": None,
            "primaryUserAccountId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-management/addresses",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.create_address(CreatePropertyAddress(
            street="123 Main St",
            unit="Suite 100",
            city="San Francisco",
            state="CA",
            postal_code="94102",
            country="USA",
            neighborhood="Downtown"
        ))

        assert result.id == "addr_123"
        assert result.street == "123 Main St"

    def test_get_address(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a property address by ID."""
        mock_response = {
            "id": "addr_123",
            "street": "123 Main St",
            "unit": None,
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94102",
            "country": "USA",
            "coordinates": None,
            "neighborhood": None,
            "district": None,
            "isVerified": True,
            "verifiedAt": 1234567890,
            "primaryUserAccountId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-management/addresses/addr_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.get_address("addr_123")

        assert result.id == "addr_123"
        assert result.is_verified is True

    def test_list_addresses(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing property addresses with pagination."""
        mock_addresses = [
            {
                "id": "addr_1",
                "street": "123 Main St",
                "unit": None,
                "city": "San Francisco",
                "state": "CA",
                "postalCode": "94102",
                "country": "USA",
                "coordinates": None,
                "neighborhood": None,
                "district": None,
                "isVerified": False,
                "verifiedAt": None,
                "primaryUserAccountId": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_addresses,
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
            f"{BASE_URL}/property-management/addresses?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.list_addresses(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.meta.total_count == 1

    def test_update_address(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a property address."""
        mock_response = {
            "id": "addr_123",
            "street": "456 Oak Ave",
            "unit": "Unit A",
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94103",
            "country": "USA",
            "coordinates": None,
            "neighborhood": "Mission",
            "district": None,
            "isVerified": False,
            "verifiedAt": None,
            "primaryUserAccountId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/property-management/addresses",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.update_address(UpdatePropertyAddress(
            id="addr_123",
            street="456 Oak Ave",
            unit="Unit A",
            neighborhood="Mission"
        ))

        assert result.street == "456 Oak Ave"
        assert result.neighborhood == "Mission"

    def test_delete_address(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a property address."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/property-management/addresses/addr_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.property_config.delete_address("addr_123")

        assert result is True

    def test_verify_address(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test verifying a property address."""
        mock_response = {
            "id": "addr_123",
            "street": "123 Main St",
            "unit": None,
            "city": "San Francisco",
            "state": "CA",
            "postalCode": "94102",
            "country": "USA",
            "coordinates": None,
            "neighborhood": None,
            "district": None,
            "isVerified": True,
            "verifiedAt": 1234567891,
            "primaryUserAccountId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-management/addresses/addr_123/verify",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.verify_address("addr_123")

        assert result.is_verified is True
        assert result.verified_at == 1234567891

    # =============== Property Tests ===============

    def test_create_property(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test creating a new property."""
        mock_response = {
            "id": "prop_123",
            "categoryId": "cat_123",
            "category": None,
            "title": "Beautiful 3BR Home",
            "description": "Spacious family home",
            "propertyType": "residential",
            "propertySubType": "house",
            "addressId": "addr_123",
            "address": None,
            "listingType": "sale",
            "listingStatus": "active",
            "salePrice": 450000,
            "salePriceCurrency": "USD",
            "rentalPrice": None,
            "rentalPeriod": None,
            "rentalPriceCurrency": "USD",
            "priceNegotiable": True,
            "features": None,
            "condition": "excellent",
            "furnished": False,
            "images": [],
            "virtualTourUrl": None,
            "videoUrl": None,
            "availableFrom": None,
            "availableTo": None,
            "isActive": True,
            "isFeatured": False,
            "isVerified": False,
            "externalId": None,
            "mlsNumber": "MLS12345",
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-management/properties",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.create(CreateProperty(
            category_id="cat_123",
            title="Beautiful 3BR Home",
            description="Spacious family home",
            property_type="residential",
            property_sub_type="house",
            address_id="addr_123",
            listing_type="sale",
            listing_status="active",
            sale_price=450000,
            price_negotiable=True,
            condition="excellent",
            mls_number="MLS12345"
        ))

        assert result.id == "prop_123"
        assert result.title == "Beautiful 3BR Home"

    def test_get_property(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a property by ID."""
        mock_response = {
            "id": "prop_123",
            "categoryId": "cat_123",
            "category": None,
            "title": "Beautiful 3BR Home",
            "description": "Spacious family home",
            "propertyType": "residential",
            "propertySubType": "house",
            "addressId": "addr_123",
            "address": None,
            "listingType": "sale",
            "listingStatus": "active",
            "salePrice": 450000,
            "salePriceCurrency": "USD",
            "rentalPrice": None,
            "rentalPeriod": None,
            "rentalPriceCurrency": "USD",
            "priceNegotiable": False,
            "features": None,
            "condition": None,
            "furnished": False,
            "images": [],
            "virtualTourUrl": None,
            "videoUrl": None,
            "availableFrom": None,
            "availableTo": None,
            "isActive": True,
            "isFeatured": False,
            "isVerified": False,
            "externalId": None,
            "mlsNumber": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-management/properties/prop_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.get("prop_123")

        assert result.id == "prop_123"
        assert result.listing_status == "active"

    def test_list_properties(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test listing properties with pagination."""
        mock_properties = [
            {
                "id": "prop_1",
                "categoryId": "cat_123",
                "category": None,
                "title": "Beautiful 3BR Home",
                "description": None,
                "propertyType": "residential",
                "propertySubType": "house",
                "addressId": "addr_123",
                "address": None,
                "listingType": "sale",
                "listingStatus": "active",
                "salePrice": 450000,
                "salePriceCurrency": "USD",
                "rentalPrice": None,
                "rentalPeriod": None,
                "rentalPriceCurrency": "USD",
                "priceNegotiable": False,
                "features": None,
                "condition": None,
                "furnished": False,
                "images": [],
                "virtualTourUrl": None,
                "videoUrl": None,
                "availableFrom": None,
                "availableTo": None,
                "isActive": True,
                "isFeatured": False,
                "isVerified": False,
                "externalId": None,
                "mlsNumber": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_properties,
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
            f"{BASE_URL}/property-management/properties?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.meta.total_count == 1

    def test_get_properties_by_category(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving properties by category."""
        mock_properties = [
            {
                "id": "prop_1",
                "categoryId": "cat_123",
                "category": None,
                "title": "Luxury Home",
                "description": None,
                "propertyType": "residential",
                "propertySubType": "house",
                "addressId": "addr_123",
                "address": None,
                "listingType": "sale",
                "listingStatus": "active",
                "salePrice": 1000000,
                "salePriceCurrency": "USD",
                "rentalPrice": None,
                "rentalPeriod": None,
                "rentalPriceCurrency": "USD",
                "priceNegotiable": False,
                "features": None,
                "condition": None,
                "furnished": False,
                "images": [],
                "virtualTourUrl": None,
                "videoUrl": None,
                "availableFrom": None,
                "availableTo": None,
                "isActive": True,
                "isFeatured": True,
                "isVerified": False,
                "externalId": None,
                "mlsNumber": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_properties,
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
            f"{BASE_URL}/property-management/properties/by-category/cat_123?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.get_by_category(
            "cat_123",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].category_id == "cat_123"

    def test_get_property_by_address(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving a property by address ID."""
        mock_response = {
            "id": "prop_123",
            "categoryId": "cat_123",
            "category": None,
            "title": "Beautiful 3BR Home",
            "description": None,
            "propertyType": "residential",
            "propertySubType": "house",
            "addressId": "addr_123",
            "address": None,
            "listingType": "sale",
            "listingStatus": "active",
            "salePrice": 450000,
            "salePriceCurrency": "USD",
            "rentalPrice": None,
            "rentalPeriod": None,
            "rentalPriceCurrency": "USD",
            "priceNegotiable": False,
            "features": None,
            "condition": None,
            "furnished": False,
            "images": [],
            "virtualTourUrl": None,
            "videoUrl": None,
            "availableFrom": None,
            "availableTo": None,
            "isActive": True,
            "isFeatured": False,
            "isVerified": False,
            "externalId": None,
            "mlsNumber": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-management/properties/by-address/addr_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.get_by_address("addr_123")

        assert result.id == "prop_123"
        assert result.address_id == "addr_123"

    def test_search_properties(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test searching properties."""
        mock_properties = [
            {
                "id": "prop_1",
                "categoryId": "cat_123",
                "category": None,
                "title": "Downtown Condo",
                "description": "Modern downtown living",
                "propertyType": "residential",
                "propertySubType": "condo",
                "addressId": "addr_123",
                "address": None,
                "listingType": "sale",
                "listingStatus": "active",
                "salePrice": 300000,
                "salePriceCurrency": "USD",
                "rentalPrice": None,
                "rentalPeriod": None,
                "rentalPriceCurrency": "USD",
                "priceNegotiable": False,
                "features": None,
                "condition": None,
                "furnished": False,
                "images": [],
                "virtualTourUrl": None,
                "videoUrl": None,
                "availableFrom": None,
                "availableTo": None,
                "isActive": True,
                "isFeatured": False,
                "isVerified": False,
                "externalId": None,
                "mlsNumber": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_properties,
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
            f"{BASE_URL}/property-management/properties/search?query=downtown&page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.search(
            "downtown",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert "Downtown" in result.data[0].title

    def test_update_property(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating a property."""
        mock_response = {
            "id": "prop_123",
            "categoryId": "cat_123",
            "category": None,
            "title": "Updated 3BR Home",
            "description": "Updated description",
            "propertyType": "residential",
            "propertySubType": "house",
            "addressId": "addr_123",
            "address": None,
            "listingType": "sale",
            "listingStatus": "under_offer",
            "salePrice": 475000,
            "salePriceCurrency": "USD",
            "rentalPrice": None,
            "rentalPeriod": None,
            "rentalPriceCurrency": "USD",
            "priceNegotiable": False,
            "features": None,
            "condition": None,
            "furnished": False,
            "images": [],
            "virtualTourUrl": None,
            "videoUrl": None,
            "availableFrom": None,
            "availableTo": None,
            "isActive": True,
            "isFeatured": True,
            "isVerified": False,
            "externalId": None,
            "mlsNumber": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/property-management/properties",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_config.update(UpdateProperty(
            id="prop_123",
            title="Updated 3BR Home",
            sale_price=475000,
            listing_status="active",
            is_featured=True
        ))

        assert result.title == "Updated 3BR Home"
        assert result.sale_price == 475000
        assert result.is_featured is True

    def test_delete_property(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test deleting a property."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/property-management/properties/prop_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.property_config.delete("prop_123")

        assert result is True

    # =============== Error Handling Tests ===============

    def test_create_category_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create category handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-management/categories",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Name required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.property_config.create_category(CreatePropertyCategory(
                name="Residential",
                property_type="residential"
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_category_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get category handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-management/categories/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Category not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.property_config.get_category("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"

    def test_get_property_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get property handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-management/properties/nonexistent",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=error_response("NOT_FOUND", "Property not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.property_config.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
