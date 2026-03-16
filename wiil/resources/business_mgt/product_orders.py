"""Product Orders resource for managing customer product orders."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    ProductOrder,
    CreateProductOrder,
    UpdateProductOrder,
)
from wiil.types import PaginatedResult, PaginationRequest


class ProductOrdersResource:
    """Resource class for managing product orders in the WIIL Platform."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/product-orders'

    def create(self, data: CreateProductOrder) -> ProductOrder:
        """Create a new product order."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductOrder,
            response_model=ProductOrder
        )

    def get(self, order_id: str) -> ProductOrder:
        """Retrieve a product order by ID."""
        return self._http.get(f'{self._base_path}/{order_id}', response_model=ProductOrder)

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ProductOrder]:
        """Retrieve product orders by customer."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-customer/{customer_id}{query_string}',
            response_model=PaginatedResult[ProductOrder]
        )

    def update(self, data: UpdateProductOrder) -> ProductOrder:
        """Update a product order."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductOrder,
            response_model=ProductOrder
        )

    def update_status(self, order_id: str, status: str) -> ProductOrder:
        """Update product order status."""
        return self._http.patch(
            f'{self._base_path}/{order_id}/status',
            {'status': status},
            response_model=ProductOrder
        )

    def cancel(self, order_id: str, reason: Optional[str] = None) -> ProductOrder:
        """Cancel a product order."""
        data: Dict[str, Any] = {}
        if reason is not None:
            data['cancelReason'] = reason
        return self._http.post(
            f'{self._base_path}/{order_id}/cancel',
            data,
            response_model=ProductOrder
        )

    def delete(self, order_id: str) -> bool:
        """Delete a product order."""
        return self._http.delete(f'{self._base_path}/{order_id}')

    def list(self, params: Optional[PaginationRequest] = None) -> PaginatedResult[ProductOrder]:
        """List product orders with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[ProductOrder]
        )


__all__ = ['ProductOrdersResource']
