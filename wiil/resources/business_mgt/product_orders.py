"""Product Orders resource for managing customer product orders."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    ProductOrder,
    CreateProductOrder,
    UpdateProductOrder,
)
from wiil.types import PaginatedResult


class ProductOrdersResource:
    """Resource class for managing product orders in the WIIL Platform."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/product-orders'

    def create(self, **kwargs: Any) -> ProductOrder:
        """Create a new product order."""
        data = CreateProductOrder(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductOrder
        )

    def get(self, order_id: str) -> ProductOrder:
        """Retrieve a product order by ID."""
        return self._http.get(f'{self._base_path}/{order_id}')

    def get_by_customer(
        self,
        customer_id: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ProductOrder]:
        """Retrieve product orders by customer."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-customer/{customer_id}{query_string}')

    def update(self, **kwargs: Any) -> ProductOrder:
        """Update a product order."""
        data = UpdateProductOrder(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductOrder
        )

    def update_status(self, order_id: str, status: str) -> ProductOrder:
        """Update product order status."""
        return self._http.patch(
            f'{self._base_path}/{order_id}/status',
            {'status': status}
        )

    def cancel(self, order_id: str, reason: Optional[str] = None) -> ProductOrder:
        """Cancel a product order."""
        data: Dict[str, Any] = {}
        if reason is not None:
            data['reason'] = reason
        return self._http.post(f'{self._base_path}/{order_id}/cancel', data)

    def delete(self, order_id: str) -> bool:
        """Delete a product order."""
        return self._http.delete(f'{self._base_path}/{order_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[ProductOrder]:
        """List product orders with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['ProductOrdersResource']
