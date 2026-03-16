"""Menu Orders resource for managing customer menu orders."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    MenuOrder,
    CreateMenuOrder,
    UpdateMenuOrder,
)
from wiil.types import PaginatedResult, PaginationRequest


class MenuOrdersResource:
    """Resource class for managing menu orders in the WIIL Platform."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/menu-orders'

    def create(self, data: CreateMenuOrder) -> MenuOrder:
        """Create a new menu order."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMenuOrder,
            response_model=MenuOrder
        )

    def get(self, order_id: str) -> MenuOrder:
        """Retrieve a menu order by ID."""
        return self._http.get(f'{self._base_path}/{order_id}', response_model=MenuOrder)

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[MenuOrder]:
        """Retrieve menu orders by customer."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-customer/{customer_id}{query_string}',
            response_model=PaginatedResult[MenuOrder]
        )

    def update(self, data: UpdateMenuOrder) -> MenuOrder:
        """Update a menu order."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMenuOrder,
            response_model=MenuOrder
        )

    def update_status(self, order_id: str, status: str) -> MenuOrder:
        """Update menu order status."""
        return self._http.patch(
            f'{self._base_path}/{order_id}/status',
            {'status': status},
            response_model=MenuOrder
        )

    def cancel(self, order_id: str, reason: Optional[str] = None) -> MenuOrder:
        """Cancel a menu order."""
        data: Dict[str, Any] = {}
        if reason is not None:
            data['cancelReason'] = reason
        return self._http.post(
            f'{self._base_path}/{order_id}/cancel',
            data,
            response_model=MenuOrder
        )

    def delete(self, order_id: str) -> bool:
        """Delete a menu order."""
        return self._http.delete(f'{self._base_path}/{order_id}')

    def list(self, params: Optional[PaginationRequest] = None) -> PaginatedResult[MenuOrder]:
        """List menu orders with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[MenuOrder]
        )


__all__ = ['MenuOrdersResource']
