"""Menus resource for managing menu categories and items.

This module provides the MenusResource class for managing menu categories,
menu items, and menu QR codes in the WIIL Platform API.

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
    CreateBusinessMenuItem,
    UpdateBusinessMenuItem,
    MenuQRCode,
)
from wiil.types import PaginatedResult, PaginationRequest

CATEGORY_BATCH_LIMIT = 50
ITEM_BATCH_LIMIT = 100


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
    ) -> List[MenuCategory]:
        """List all menu categories with optional pagination.

        Args:
            params: Optional pagination parameters

        Returns:
            List of menu categories
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/categories{query_string}',
            response_model=List[MenuCategory]
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

    def create_item(self, data: CreateBusinessMenuItem) -> BusinessMenuItem:
        """Create a new menu item.

        Args:
            data: Menu item creation data

        Returns:
            The created menu item
        """
        return self._http.post(
            f'{self._base_path}/items',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessMenuItem,
            response_model=BusinessMenuItem
        )

    def get_item(self, item_id: str) -> BusinessMenuItem:
        """Retrieve a menu item by ID.

        Args:
            item_id: Menu item ID

        Returns:
            The requested menu item
        """
        return self._http.get(
            f'{self._base_path}/items/{item_id}',
            response_model=BusinessMenuItem
        )

    def list_items(
        self,
        params: Optional[PaginationRequest] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[BusinessMenuItem]:
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
            response_model=PaginatedResult[BusinessMenuItem]
        )

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
        return self._http.get(
            f'{self._base_path}/items/by-category/{category_id}{query_string}',
            response_model=List[BusinessMenuItem]
        )

    def get_popular_items(self, limit: Optional[int] = None) -> List[BusinessMenuItem]:
        """Retrieve popular menu items.

        Args:
            limit: Maximum number of items to return

        Returns:
            List of popular menu items
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params['limit'] = limit

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(
            f'{self._base_path}/items/popular{query_string}',
            response_model=List[BusinessMenuItem]
        )

    def update_item(self, data: UpdateBusinessMenuItem) -> BusinessMenuItem:
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
            response_model=BusinessMenuItem
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

    # =============== Menu QR Code Methods ===============

    def get_qr_codes(self) -> List[MenuQRCode]:
        """Retrieve all menu QR codes.

        Returns:
            List of all menu QR codes
        """
        return self._http.get(
            f'{self._base_path}/qr-codes',
            response_model=List[MenuQRCode]
        )

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

        return self._http.post(
            f'{self._base_path}/qr-codes',
            data,
            response_model=MenuQRCode
        )

    def delete_qr_code(self, qr_code_id: str) -> bool:
        """Delete a menu QR code.

        Args:
            qr_code_id: QR code ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/qr-codes/{qr_code_id}')


__all__ = ['MenusResource']
