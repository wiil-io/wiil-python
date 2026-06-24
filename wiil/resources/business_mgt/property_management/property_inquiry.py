"""Property Inquiry resource for managing property leads and inquiries."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    PropertyInquiry,
    CreatePropertyInquiry,
    UpdatePropertyInquiry,
    UpdatePropertyInquiryStatus,
    ServiceSlotQueryResponse,
)
from wiil.types import PaginatedResult, PaginationRequest


class PropertyInquiryResource:
    """Resource class for managing property inquiries in the WIIL Platform.

    Provides methods for creating, retrieving, updating, and managing
    property inquiries. Supports filtering by property and customer.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/property-inquiries'

    def create(self, data: CreatePropertyInquiry) -> PropertyInquiry:
        """Create a new property inquiry.

        Args:
            data: Property inquiry creation data

        Returns:
            The created property inquiry
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreatePropertyInquiry,
            response_model=PropertyInquiry
        )

    def get_viewing_slots(
        self,
        property_id: str,
        local_date: str
    ) -> ServiceSlotQueryResponse:
        """Get available viewing slots for a property on a specific date.

        Args:
            property_id: Property ID to get viewing slots for
            local_date: Business local date in YYYY-MM-DD format

        Returns:
            Available viewing slots with UTC timestamps
        """
        return self._http.get(
            f'{self._base_path}/viewing-slots/{property_id}?localDate={local_date}',
            response_model=ServiceSlotQueryResponse
        )

    def get(self, inquiry_id: str) -> PropertyInquiry:
        """Retrieve a property inquiry by ID.

        Args:
            inquiry_id: Property inquiry ID

        Returns:
            The requested property inquiry
        """
        return self._http.get(
            f'{self._base_path}/{inquiry_id}',
            response_model=PropertyInquiry
        )

    def get_by_property(
        self,
        property_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[PropertyInquiry]:
        """Retrieve property inquiries by property ID.

        Args:
            property_id: Property ID
            params: Pagination parameters

        Returns:
            Paginated list of property inquiries for the property
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-property/{property_id}{query_string}',
            response_model=PaginatedResult[PropertyInquiry]
        )

    def get_by_customer(
        self,
        customer_id: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[PropertyInquiry]:
        """Retrieve property inquiries by customer ID.

        Args:
            customer_id: Customer ID
            params: Pagination parameters

        Returns:
            Paginated list of property inquiries from the customer
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-customer/{customer_id}{query_string}',
            response_model=PaginatedResult[PropertyInquiry]
        )

    def update(self, data: UpdatePropertyInquiry) -> PropertyInquiry:
        """Update a property inquiry.

        Args:
            data: Property inquiry update data (must include id)

        Returns:
            The updated property inquiry
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdatePropertyInquiry,
            response_model=PropertyInquiry
        )

    def update_status(
        self,
        inquiry_id: str,
        data: UpdatePropertyInquiryStatus
    ) -> PropertyInquiry:
        """Update property inquiry status.

        Args:
            inquiry_id: Property inquiry ID
            data: Status update data

        Returns:
            The updated property inquiry
        """
        return self._http.patch(
            f'{self._base_path}/{inquiry_id}/status',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdatePropertyInquiryStatus,
            response_model=PropertyInquiry
        )

    def delete(self, inquiry_id: str) -> bool:
        """Delete a property inquiry.

        Args:
            inquiry_id: Property inquiry ID

        Returns:
            True if deletion was successful
        """
        return self._http.delete(f'{self._base_path}/{inquiry_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[PropertyInquiry]:
        """List property inquiries with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of property inquiries
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[PropertyInquiry]
        )


__all__ = ['PropertyInquiryResource']
