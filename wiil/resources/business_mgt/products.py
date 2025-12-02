"""Products resource for managing product categories and products."""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    ProductCategory,
    CreateProductCategory,
    UpdateProductCategory,
    BusinessProduct,
    CreateBusinessProduct,
    UpdateBusinessProduct,
)
from wiil.types import PaginatedResult


class ProductsResource:
    """Resource class for managing products in the WIIL Platform."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/product-management'

    # =============== Product Category Methods ===============

    def create_category(self, **kwargs: Any) -> ProductCategory:
        """Create a new product category."""
        data = CreateProductCategory(**kwargs)
        return self._http.post(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductCategory
        )

    def get_category(self, category_id: str) -> ProductCategory:
        """Retrieve a product category by ID."""
        return self._http.get(f'{self._base_path}/categories/{category_id}')

    def list_categories(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ProductCategory]:
        """List product categories with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/categories{query_string}')

    def update_category(self, **kwargs: Any) -> ProductCategory:
        """Update a product category."""
        data = UpdateProductCategory(**kwargs)
        return self._http.patch(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductCategory
        )

    def delete_category(self, category_id: str) -> bool:
        """Delete a product category."""
        return self._http.delete(f'{self._base_path}/categories/{category_id}')

    # =============== Product Methods ===============

    def create(self, **kwargs: Any) -> BusinessProduct:
        """Create a new product."""
        data = CreateBusinessProduct(**kwargs)
        return self._http.post(
            f'{self._base_path}/products',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessProduct
        )

    def get(self, product_id: str) -> BusinessProduct:
        """Retrieve a product by ID."""
        return self._http.get(f'{self._base_path}/products/{product_id}')

    def get_by_sku(self, sku: str) -> BusinessProduct:
        """Retrieve a product by SKU."""
        return self._http.get(f'{self._base_path}/products/by-sku/{sku}')

    def get_by_barcode(self, barcode: str) -> BusinessProduct:
        """Retrieve a product by barcode."""
        return self._http.get(f'{self._base_path}/products/by-barcode/{barcode}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[BusinessProduct]:
        """List products with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if include_deleted is not None:
            params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/products{query_string}')

    def get_by_category(
        self,
        category_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[BusinessProduct]:
        """Retrieve products by category."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/products/by-category/{category_id}{query_string}')

    def search(
        self,
        query: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[BusinessProduct]:
        """Search products by query string."""
        params: Dict[str, Any] = {'query': query}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        return self._http.get(f'{self._base_path}/products/search?{urlencode(params)}')

    def update(self, **kwargs: Any) -> BusinessProduct:
        """Update a product."""
        data = UpdateBusinessProduct(**kwargs)
        return self._http.patch(
            f'{self._base_path}/products',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessProduct
        )

    def delete(self, product_id: str) -> bool:
        """Delete a product."""
        return self._http.delete(f'{self._base_path}/products/{product_id}')


__all__ = ['ProductsResource']
