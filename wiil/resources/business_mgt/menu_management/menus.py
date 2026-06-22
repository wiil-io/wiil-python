"""Menus resource for managing menu categories and items.

This module provides the MenusResource class for managing menu categories,
and menu items in the WIIL Platform API.

Example:
    >>> from wiil import WiilClient
    >>> from wiil.models.business_mgt import CreateMenuCategory, CreateBusinessMenuItem
    >>> client = WiilClient(api_key='your-api-key')
    >>> category = client.menus.create_category(CreateMenuCategory(name='Appetizers'))
    >>> item = client.menus.create_item(CreateBusinessMenuItem(name='Caesar Salad', category_id=category.id))
"""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    MenuCategory,
    CreateMenuCategory,
    UpdateMenuCategory,
    BusinessMenuItem,
    MenuItemCatalog,
    CreateBusinessMenuItem,
    UpdateBusinessMenuItem,
)
from wiil.types import PaginatedResult, PaginationRequest

CATEGORY_BATCH_LIMIT = 50
ITEM_BATCH_LIMIT = 100


class MenusResource:
    """Resource class for managing menus in the WIIL Platform.

    Provides comprehensive methods for managing menu categories, menu items,
    and batch operations with filtering support.
    """

    def __init__(self, http: HttpClient):
        """Initialize the menus resource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._base_path = '/menu-management'

    # =============== Menu Category Methods ===============

    def create_category(self, data: CreateMenuCategory) -> MenuCategory:
        """Create a new menu category.

        Args:
            data: Menu category creation data

        Returns:
            The created menu category

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails
        """
        return self._http.post(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMenuCategory,
            response_model=MenuCategory
        )

    def get_category(self, category_id: str) -> MenuCategory:
        """Retrieve a menu category by ID.

        Args:
            category_id: Menu category ID

        Returns:
            The requested menu category
        """
        return self._http.get(
            f'{self._base_path}/categories/{category_id}',
            response_model=MenuCategory
        )

    def list_categories(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[MenuCategory]:
        """List all menu categories with optional pagination.

        Args:
            params: Optional pagination parameters

        Returns:
            Paginated list of menu categories
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/categories{query_string}',
            response_model=PaginatedResult[MenuCategory]
        )

    def update_category(self, data: UpdateMenuCategory) -> MenuCategory:
        """Update a menu category.

        Args:
            data: Menu category update data (must include id)

        Returns:
            The updated menu category
        """
        return self._http.patch(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMenuCategory,
            response_model=MenuCategory
        )

    def set_category_display_order(
        self,
        category_id: str,
        display_order: int
    ) -> MenuCategory:
        """Set the display order for a menu category.

        Args:
            category_id: Menu category ID
            display_order: New display order position

        Returns:
            The updated menu category
        """
        return self._http.patch(
            f'{self._base_path}/categories/{category_id}/display-order',
            {'displayOrder': display_order},
            response_model=MenuCategory
        )

    def reorder_items(self, category_id: str, item_ids: List[str]) -> bool:
        """Reorder menu items within a category.

        Args:
            category_id: Category ID
            item_ids: Ordered list of menu item IDs

        Returns:
            True if the reorder was successful
        """
        return self._http.post(
            f'{self._base_path}/categories/{category_id}/reorder-items',
            {'itemIds': item_ids}
        )

    def delete_category(self, category_id: str) -> bool:
        """Delete a menu category.

        Args:
            category_id: Menu category ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/categories/{category_id}')

    def create_category_batch(
        self,
        data: List[Union[CreateMenuCategory, Dict[str, Any]]]
    ) -> PaginatedResult[MenuCategory]:
        """Create multiple menu categories in a batch.

        Args:
            data: List of categories to create (max 50 items)

        Returns:
            PaginatedResult containing created categories

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
        if len(data) > CATEGORY_BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {CATEGORY_BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': f'Array length {len(data)} exceeds maximum of {CATEGORY_BATCH_LIMIT}'
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateMenuCategory.model_validate(item)
                    payload.append(validated.model_dump(by_alias=True, exclude_none=True))
                elif isinstance(item, BaseModel):
                    payload.append(item.model_dump(by_alias=True, exclude_none=True))
                else:
                    raise WiilValidationError(
                        f'Invalid item type at index {i}',
                        details=[{
                            'path': ['data', i],
                            'message': 'Expected dict or Pydantic model'
                        }]
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f'Validation failed for item at index {i}',
                    details=e.errors()
                )

        return self._http.post(
            f'{self._base_path}/categories/batch',
            payload,
            response_model=PaginatedResult[MenuCategory]
        )

    # =============== Menu Item Methods ===============

    def create_item(self, data: CreateBusinessMenuItem) -> MenuItemCatalog:
        """Create a new menu item.

        Args:
            data: Menu item creation data

        Returns:
            The created menu item catalog entry
        """
        return self._http.post(
            f'{self._base_path}/items',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessMenuItem,
            response_model=MenuItemCatalog
        )

    def get_item(self, item_id: str) -> MenuItemCatalog:
        """Retrieve a menu item by ID.

        Args:
            item_id: Menu item ID

        Returns:
            The requested menu item
        """
        return self._http.get(
            f'{self._base_path}/items/{item_id}',
            response_model=MenuItemCatalog
        )

    def list_items(
        self,
        params: Optional[PaginationRequest] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[MenuItemCatalog]:
        """List menu items with pagination.

        Args:
            params: Pagination parameters
            include_deleted: Include deleted items

        Returns:
            Paginated list of menu items
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size
        if include_deleted is not None:
            query_params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/items{query_string}',
            response_model=PaginatedResult[MenuItemCatalog]
        )

    def get_items_by_category(
        self,
        category_id: str,
        params: Optional[PaginationRequest] = None,
        include_unavailable: Optional[bool] = None
    ) -> PaginatedResult[MenuItemCatalog]:
        """Retrieve menu items by category.

        Args:
            category_id: Category ID
            include_unavailable: Include unavailable items

        Returns:
            List of menu items in the category
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size
        if include_unavailable is not None:
            query_params['includeUnavailable'] = str(
                include_unavailable
            ).lower()

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/items/by-category/{category_id}{query_string}',
            response_model=PaginatedResult[MenuItemCatalog]
        )

    def get_popular_items(
        self,
        params: Optional[PaginationRequest] = None,
        limit: Optional[int] = None
    ) -> PaginatedResult[MenuItemCatalog]:
        """Retrieve popular menu items.

        Args:
            limit: Maximum number of items to return

        Returns:
            List of popular menu items
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size
        if limit is not None:
            query_params['limit'] = limit

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/items/popular{query_string}',
            response_model=PaginatedResult[MenuItemCatalog]
        )

    def update_item(self, data: UpdateBusinessMenuItem) -> MenuItemCatalog:
        """Update a menu item.

        Args:
            data: Menu item update data (must include id)

        Returns:
            The updated menu item
        """
        return self._http.patch(
            f'{self._base_path}/items',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessMenuItem,
            response_model=MenuItemCatalog
        )

    def toggle_item_active(self, item_id: str) -> MenuItemCatalog:
        """Toggle the active status of a menu item.

        Args:
            item_id: Menu item ID

        Returns:
            The updated menu item
        """
        return self._http.patch(
            f'{self._base_path}/items/{item_id}/toggle-active',
            {},
            response_model=MenuItemCatalog
        )

    def toggle_item_availability(self, item_id: str) -> MenuItemCatalog:
        """Toggle the availability status of a menu item.

        Args:
            item_id: Menu item ID

        Returns:
            The updated menu item
        """
        return self._http.patch(
            f'{self._base_path}/items/{item_id}/toggle-availability',
            {},
            response_model=MenuItemCatalog
        )

    def set_item_display_order(
        self,
        item_id: str,
        display_order: int
    ) -> MenuItemCatalog:
        """Set the display order for a menu item.

        Args:
            item_id: Menu item ID
            display_order: New display order position

        Returns:
            The updated menu item
        """
        return self._http.patch(
            f'{self._base_path}/items/{item_id}/display-order',
            {'displayOrder': display_order},
            response_model=MenuItemCatalog
        )

    def update_items_availability_bulk(
        self,
        item_ids: List[str],
        is_available: bool
    ) -> Any:
        """Update availability for multiple menu items in bulk.

        Args:
            item_ids: List of menu item IDs to update
            is_available: Availability flag to apply to all listed items

        Returns:
            Bulk update result (e.g. count of updated items)
        """
        return self._http.patch(
            f'{self._base_path}/items/availability/bulk',
            {'itemIds': item_ids, 'isAvailable': is_available}
        )

    def delete_item(self, item_id: str) -> bool:
        """Delete a menu item.

        Args:
            item_id: Menu item ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/items/{item_id}')

    def create_item_batch(
        self,
        data: List[Union[CreateBusinessMenuItem, Dict[str, Any]]]
    ) -> PaginatedResult[BusinessMenuItem]:
        """Create multiple menu items in a batch.

        Args:
            data: List of menu items to create (max 100 items)

        Returns:
            PaginatedResult containing created menu items

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
        if len(data) > ITEM_BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {ITEM_BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': f'Array length {len(data)} exceeds maximum of {ITEM_BATCH_LIMIT}'
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateBusinessMenuItem.model_validate(item)
                    payload.append(validated.model_dump(by_alias=True, exclude_none=True))
                elif isinstance(item, BaseModel):
                    payload.append(item.model_dump(by_alias=True, exclude_none=True))
                else:
                    raise WiilValidationError(
                        f'Invalid item type at index {i}',
                        details=[{
                            'path': ['data', i],
                            'message': 'Expected dict or Pydantic model'
                        }]
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f'Validation failed for item at index {i}',
                    details=e.errors()
                )

        return self._http.post(
            f'{self._base_path}/items/batch',
            payload,
            response_model=PaginatedResult[BusinessMenuItem]
        )


__all__ = ['MenusResource']
