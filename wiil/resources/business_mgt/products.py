"""Products resource for managing product categories and products."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    ProductCategory,
    CreateProductCategory,
    UpdateProductCategory,
    BusinessProduct,
    CreateBusinessProduct,
    UpdateBusinessProduct,
)
from wiil.types import PaginatedResult, PaginationRequest

CATEGORY_BATCH_LIMIT = 50
PRODUCT_BATCH_LIMIT = 100


class ProductsResource:
    """Resource class for managing products in the WIIL Platform."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/product-management'

    # =============== Product Category Methods ===============

    def create_category(self, data: CreateProductCategory) -> ProductCategory:
        """Create a new product category."""
        return self._http.post(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductCategory,
            response_model=ProductCategory
        )

    def get_category(self, category_id: str) -> ProductCategory:
        """Retrieve a product category by ID."""
        return self._http.get(
            f'{self._base_path}/categories/{category_id}',
            response_model=ProductCategory
        )

    def list_categories(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ProductCategory]:
        """List product categories with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/categories{query_string}',
            response_model=PaginatedResult[ProductCategory]
        )

    def update_category(self, data: UpdateProductCategory) -> ProductCategory:
        """Update a product category."""
        return self._http.patch(
            f'{self._base_path}/categories',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductCategory,
            response_model=ProductCategory
        )

    def delete_category(self, category_id: str) -> bool:
        """Delete a product category."""
        return self._http.delete(f'{self._base_path}/categories/{category_id}')

    def create_category_batch(
        self,
        data: List[Union[CreateProductCategory, Dict[str, Any]]]
    ) -> PaginatedResult[ProductCategory]:
        """Create multiple product categories in a batch.

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
                    validated = CreateProductCategory.model_validate(item)
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
            response_model=PaginatedResult[ProductCategory]
        )

    # =============== Product Methods ===============

    def create(self, data: CreateBusinessProduct) -> BusinessProduct:
        """Create a new product."""
        return self._http.post(
            f'{self._base_path}/products',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessProduct,
            response_model=BusinessProduct
        )

    def get(self, product_id: str) -> BusinessProduct:
        """Retrieve a product by ID."""
        return self._http.get(
            f'{self._base_path}/products/{product_id}',
            response_model=BusinessProduct
        )

    def get_by_sku(self, sku: str) -> BusinessProduct:
        """Retrieve a product by SKU."""
        return self._http.get(
            f'{self._base_path}/products/by-sku/{sku}',
            response_model=BusinessProduct
        )

    def get_by_barcode(self, barcode: str) -> BusinessProduct:
        """Retrieve a product by barcode."""
        return self._http.get(
            f'{self._base_path}/products/by-barcode/{barcode}',
            response_model=BusinessProduct
        )

    def list(
        self,
        params: Optional[PaginationRequest] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[BusinessProduct]:
        """List products with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size
        if include_deleted is not None:
            query_params['includeDeleted'] = str(include_deleted).lower()

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/products{query_string}',
            response_model=PaginatedResult[BusinessProduct]
        )

    def get_by_category(
        self,
        category_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[BusinessProduct]:
        """Retrieve products by category."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/products/by-category/{category_id}{query_string}',
            response_model=PaginatedResult[BusinessProduct]
        )

    def search(
        self,
        query: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[BusinessProduct]:
        """Search products by query string."""
        query_params: Dict[str, Any] = {'query': query}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        return self._http.get(
            f'{self._base_path}/products/search?{urlencode(query_params)}',
            response_model=PaginatedResult[BusinessProduct]
        )

    def update(self, data: UpdateBusinessProduct) -> BusinessProduct:
        """Update a product."""
        return self._http.patch(
            f'{self._base_path}/products',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessProduct,
            response_model=BusinessProduct
        )

    def delete(self, product_id: str) -> bool:
        """Delete a product."""
        return self._http.delete(f'{self._base_path}/products/{product_id}')

    def create_batch(
        self,
        data: List[Union[CreateBusinessProduct, Dict[str, Any]]]
    ) -> PaginatedResult[BusinessProduct]:
        """Create multiple products in a batch.

        Args:
            data: List of products to create (max 100 items)

        Returns:
            PaginatedResult containing created products

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
        if len(data) > PRODUCT_BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {PRODUCT_BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': f'Array length {len(data)} exceeds maximum of {PRODUCT_BATCH_LIMIT}'
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateBusinessProduct.model_validate(item)
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
            f'{self._base_path}/products/batch',
            payload,
            response_model=PaginatedResult[BusinessProduct]
        )


__all__ = ['ProductsResource']
