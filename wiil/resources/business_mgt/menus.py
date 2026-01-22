"""Menus resource for managing menu categories and items.

This module provides the MenusResource class for managing menu categories,
menu items, and menu QR codes in the WIIL Platform API.

Example:
    >>> from wiil import WiilClient
    >>> client = WiilClient(api_key='your-api-key')
    >>> category = client.menus.create_category(name='Appetizers')
    >>> item = client.menus.create_item(name='Caesar Salad', category_id=category.id)
"""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    MenuCategory,
    CreateMenuCategory,
    UpdateMenuCategory,
    BusinessMenuItem,
    CreateBusinessMenuItem,
    UpdateBusinessMenuItem,
    MenuQRCode,
)
from wiil.types import PaginatedResult


class MenusResource:
    """Resource class for managing menus in the WIIL Platform.

    Provides comprehensive methods for managing menu categories, menu items,
    and menu QR codes. Supports batch operations and filtering.
    """

    def __init__(self, http: HttpClient):
        """Initialize the menus resource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._base_path = '/menu-management'

    # =============== Menu Category Methods ===============

    def create_category(self, **kwargs: Any) -> MenuCategory:
        """Create a new menu category.

        Args:
            **kwargs: Menu category data fields

        Returns:
            The created menu category

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails
        """
        data = CreateMenuCategory(**kwargs)
        return self._http.post(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMenuCategory
        )

    def get_category(self, category_id: str) -> MenuCategory:
        """Retrieve a menu category by ID.

        Args:
            category_id: Menu category ID

        Returns:
            The requested menu category
        """
        return self._http.get(f'{self._base_path}/categories/{category_id}')

    def list_categories(self) -> List[MenuCategory]:
        """List all menu categories.

        Returns:
            List of all menu categories
        """
        return self._http.get(f'{self._base_path}/categories')

    def update_category(self, **kwargs: Any) -> MenuCategory:
        """Update a menu category.

        Args:
            **kwargs: Menu category update data (must include id)

        Returns:
            The updated menu category
        """
        data = UpdateMenuCategory(**kwargs)
        return self._http.patch(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMenuCategory
        )

    def delete_category(self, category_id: str) -> bool:
        """Delete a menu category.

        Args:
            category_id: Menu category ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/categories/{category_id}')

    # =============== Menu Item Methods ===============

    def create_item(self, **kwargs: Any) -> BusinessMenuItem:
        """Create a new menu item.

        Args:
            **kwargs: Menu item data fields

        Returns:
            The created menu item
        """
        data = CreateBusinessMenuItem(**kwargs)
        return self._http.post(
            f'{self._base_path}/items',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessMenuItem
        )

    def get_item(self, item_id: str) -> BusinessMenuItem:
        """Retrieve a menu item by ID.

        Args:
            item_id: Menu item ID

        Returns:
            The requested menu item
        """
        return self._http.get(f'{self._base_path}/items/{item_id}')

    def list_items(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[BusinessMenuItem]:
        """List menu items with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            include_deleted: Include deleted items

        Returns:
            Paginated list of menu items
        """
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if include_deleted is not None:
            params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/items{query_string}')

    def get_items_by_category(
        self,
        category_id: str,
        include_unavailable: Optional[bool] = None
    ) -> List[BusinessMenuItem]:
        """Retrieve menu items by category.

        Args:
            category_id: Category ID
            include_unavailable: Include unavailable items

        Returns:
            List of menu items in the category
        """
        params: Dict[str, Any] = {}
        if include_unavailable is not None:
            params['includeUnavailable'] = str(include_unavailable).lower()

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/items/by-category/{category_id}{query_string}')

    def get_popular_items(self, pageSize: Optional[int] = None) -> List[BusinessMenuItem]:
        """Retrieve popular menu items.

        Args:
            pageSize: Maximum number of items to return

        Returns:
            List of popular menu items
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/items/popular{query_string}')

    def update_item(self, **kwargs: Any) -> BusinessMenuItem:
        """Update a menu item.

        Args:
            **kwargs: Menu item update data (must include id)

        Returns:
            The updated menu item
        """
        data = UpdateBusinessMenuItem(**kwargs)
        return self._http.patch(
            f'{self._base_path}/items',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessMenuItem
        )

    def delete_item(self, item_id: str) -> bool:
        """Delete a menu item.

        Args:
            item_id: Menu item ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/items/{item_id}')

    # =============== Menu QR Code Methods ===============

    def get_qr_codes(self) -> List[MenuQRCode]:
        """Retrieve all menu QR codes.

        Returns:
            List of all menu QR codes
        """
        return self._http.get(f'{self._base_path}/qr-codes')

    def generate_qr_code(
        self,
        name: Optional[str] = None,
        category_id: Optional[str] = None
    ) -> MenuQRCode:
        """Generate a new menu QR code.

        Args:
            name: Optional name for the QR code
            category_id: Optional category ID for category-specific QR code

        Returns:
            The generated QR code
        """
        data: Dict[str, Any] = {}
        if name is not None:
            data['name'] = name
        if category_id is not None:
            data['categoryId'] = category_id

        return self._http.post(f'{self._base_path}/qr-codes', data)

    def delete_qr_code(self, qr_code_id: str) -> bool:
        """Delete a menu QR code.

        Args:
            qr_code_id: QR code ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/qr-codes/{qr_code_id}')


__all__ = ['MenusResource']
