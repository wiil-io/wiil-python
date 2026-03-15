"""Property Configuration resource for managing property listings."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    PropertyCategory,
    CreatePropertyCategory,
    UpdatePropertyCategory,
    PropertyAddress,
    CreatePropertyAddress,
    UpdatePropertyAddress,
    Property,
    CreateProperty,
    UpdateProperty,
)
from wiil.types import PaginatedResult, PaginationRequest


class PropertyConfigResource:
    """Resource class for managing property configurations in the WIIL Platform.

    Provides comprehensive methods for managing property categories, property addresses,
    and property listings. Supports filtering and search operations.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/property-management'

    # =============== Property Category Methods ===============

    def create_category(self, data: CreatePropertyCategory) -> PropertyCategory:
        """Create a new property category.

        Args:
            data: Property category creation data

        Returns:
            The created property category
        """
        return self._http.post(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreatePropertyCategory
        )

    def get_category(self, category_id: str) -> PropertyCategory:
        """Retrieve a property category by ID.

        Args:
            category_id: Property category ID

        Returns:
            The requested property category
        """
        return self._http.get(f'{self._base_path}/categories/{category_id}')

    def list_categories(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[PropertyCategory]:
        """List property categories with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of property categories
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/categories{query_string}')

    def update_category(self, data: UpdatePropertyCategory) -> PropertyCategory:
        """Update a property category.

        Args:
            data: Property category update data (must include id)

        Returns:
            The updated property category
        """
        return self._http.patch(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdatePropertyCategory
        )

    def delete_category(self, category_id: str) -> bool:
        """Delete a property category.

        Args:
            category_id: Property category ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/categories/{category_id}')

    # =============== Property Address Methods ===============

    def create_address(self, data: CreatePropertyAddress) -> PropertyAddress:
        """Create a new property address.

        Args:
            data: Property address creation data

        Returns:
            The created property address
        """
        return self._http.post(
            f'{self._base_path}/addresses',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreatePropertyAddress
        )

    def get_address(self, address_id: str) -> PropertyAddress:
        """Retrieve a property address by ID.

        Args:
            address_id: Property address ID

        Returns:
            The requested property address
        """
        return self._http.get(f'{self._base_path}/addresses/{address_id}')

    def list_addresses(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[PropertyAddress]:
        """List property addresses with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of property addresses
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/addresses{query_string}')

    def update_address(self, data: UpdatePropertyAddress) -> PropertyAddress:
        """Update a property address.

        Args:
            data: Property address update data (must include id)

        Returns:
            The updated property address
        """
        return self._http.patch(
            f'{self._base_path}/addresses',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdatePropertyAddress
        )

    def delete_address(self, address_id: str) -> bool:
        """Delete a property address.

        Args:
            address_id: Property address ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/addresses/{address_id}')

    def verify_address(self, address_id: str) -> PropertyAddress:
        """Verify a property address.

        Args:
            address_id: Property address ID

        Returns:
            The verified property address
        """
        return self._http.post(f'{self._base_path}/addresses/{address_id}/verify', {})

    # =============== Property Methods ===============

    def create(self, data: CreateProperty) -> Property:
        """Create a new property listing.

        Args:
            data: Property creation data

        Returns:
            The created property
        """
        return self._http.post(
            f'{self._base_path}/properties',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProperty
        )

    def get(self, property_id: str) -> Property:
        """Retrieve a property by ID.

        Args:
            property_id: Property ID

        Returns:
            The requested property
        """
        return self._http.get(f'{self._base_path}/properties/{property_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[Property]:
        """List properties with pagination.

        Args:
            params: Pagination parameters
            include_deleted: Include deleted properties

        Returns:
            Paginated list of properties
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size
        if include_deleted is not None:
            query_params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/properties{query_string}')

    def get_by_category(
        self,
        category_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[Property]:
        """Retrieve properties by category.

        Args:
            category_id: Category ID
            params: Pagination parameters

        Returns:
            Paginated list of properties in the category
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(f'{self._base_path}/properties/by-category/{category_id}{query_string}')

    def get_by_address(self, address_id: str) -> Property:
        """Retrieve a property by address ID.

        Args:
            address_id: Address ID

        Returns:
            The property at the specified address
        """
        return self._http.get(f'{self._base_path}/properties/by-address/{address_id}')

    def search(
        self,
        query: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[Property]:
        """Search properties by query string.

        Args:
            query: Search query
            params: Pagination parameters

        Returns:
            Paginated list of matching properties
        """
        query_params: Dict[str, Any] = {'query': query}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        return self._http.get(f'{self._base_path}/properties/search?{urlencode(query_params)}')

    def update(self, data: UpdateProperty) -> Property:
        """Update a property.

        Args:
            data: Property update data (must include id)

        Returns:
            The updated property
        """
        return self._http.patch(
            f'{self._base_path}/properties',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProperty
        )

    def delete(self, property_id: str) -> bool:
        """Delete a property.

        Args:
            property_id: Property ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/properties/{property_id}')


__all__ = ['PropertyConfigResource']
