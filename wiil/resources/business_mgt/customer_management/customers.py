"""Customers resource for managing customer records.

This module provides the CustomersResource class for managing customers
in the WIIL Platform API.

Example:
    >>> from wiil import WiilClient
    >>> from wiil.models.business_mgt import CreateCustomer
    >>> client = WiilClient(api_key='your-api-key')
    >>> customer = client.customers.create(CreateCustomer(
    ...     first_name='John',
    ...     last_name='Doe',
    ...     email='john.doe@example.com'
    ... ))
"""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, quote

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    Customer,
    CreateCustomer,
    UpdateCustomer,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class CustomersResource:
    """Resource class for managing customers in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    customers. Customers represent individuals or entities that interact with
    the business. Supports searching by phone number, email, or general query.

    Example:
        >>> client = WiilClient(api_key='your-api-key')
        >>>
        >>> # Create a new customer
        >>> customer = client.customers.create(CreateCustomer(
        ...     first_name='John',
        ...     last_name='Doe',
        ...     email='john.doe@example.com',
        ...     phone_number='+1234567890'
        ... ))
        >>>
        >>> # Get a customer by ID
        >>> customer = client.customers.get('cust_123')
        >>>
        >>> # Search customers
        >>> results = client.customers.search('john', PaginationRequest(page=1, page_size=10))
        >>>
        >>> # Get customer by phone
        >>> customer = client.customers.get_by_phone('+1234567890')
        >>>
        >>> # Update a customer
        >>> updated = client.customers.update('cust_123', UpdateCustomer(
        ...     email='john.newemail@example.com'
        ... ))
        >>>
        >>> # List all customers
        >>> customers = client.customers.list(PaginationRequest(page=1, page_size=20))
        >>>
        >>> # Delete a customer
        >>> deleted = client.customers.delete('cust_123')
    """

    def __init__(self, http: HttpClient):
        """Initialize the customers resource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._base_path = '/customers'

    def create(self, data: CreateCustomer) -> Customer:
        """Create a new customer.

        Args:
            data: Customer creation data

        Returns:
            The created customer

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> customer = client.customers.create(CreateCustomer(
            ...     first_name='Jane',
            ...     last_name='Smith',
            ...     email='jane.smith@example.com',
            ...     phone_number='+1987654321',
            ...     metadata={
            ...         'source': 'website',
            ...         'referral_code': 'FRIEND2023'
            ...     }
            ... ))
            >>> print('Created customer:', customer.id)
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateCustomer,
            response_model=Customer
        )

    def get(self, customer_id: str) -> Customer:
        """Retrieve a customer by ID.

        Args:
            customer_id: Customer ID

        Returns:
            The requested customer

        Raises:
            WiilAPIError: When the customer is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> customer = client.customers.get('cust_123')
            >>> print('Customer:', customer.first_name, customer.last_name)
            >>> print('Email:', customer.email)
            >>> print('Phone:', customer.phone_number)
        """
        return self._http.get(f'{self._base_path}/{customer_id}', response_model=Customer)

    def get_by_phone(self, phone_number: str) -> Optional[Customer]:
        """Retrieve a customer by phone number.

        Args:
            phone_number: Customer phone number

        Returns:
            The customer or None if not found

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> customer = client.customers.get_by_phone('+1234567890')
            >>> if customer:
            ...     print('Found customer:', customer.first_name)
            ... else:
            ...     print('No customer found with that phone number')
        """
        return self._http.get(f'{self._base_path}/phone/{quote(phone_number, safe="")}', response_model=Customer)

    def get_by_email(self, email: str) -> Optional[Customer]:
        """Retrieve a customer by email address.

        Args:
            email: Customer email address

        Returns:
            The customer or None if not found

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> customer = client.customers.get_by_email('john@example.com')
            >>> if customer:
            ...     print('Found customer:', customer.id)
        """
        return self._http.get(f'{self._base_path}/email/{quote(email, safe="")}', response_model=Customer)

    def search(
        self,
        query: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[Customer]:
        """Search customers by query string.

        The search query will match against customer names, email, and phone number.

        Args:
            query: Search query string
            params: Pagination parameters

        Returns:
            Paginated search results

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> results = client.customers.search('john', PaginationRequest(
            ...     page=1,
            ...     page_size=20
            ... ))
            >>>
            >>> print(f"Found {results.meta.total_count} customers")
            >>> for customer in results.data:
            ...     print(f"- {customer.first_name} {customer.last_name}")
        """
        query_params: Dict[str, Any] = {'query': query}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        return self._http.get(
            f'{self._base_path}/search?{urlencode(query_params)}',
            response_model=PaginatedResult[Customer]
        )

    def update(self, customer_id: str, data: UpdateCustomer) -> Customer:
        """Update an existing customer.

        Args:
            customer_id: Customer ID
            data: Customer update data

        Returns:
            The updated customer

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When the customer is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> updated = client.customers.update('cust_123', UpdateCustomer(
            ...     email='newemail@example.com',
            ...     phone_number='+1555555555',
            ...     metadata={
            ...         'updated_by': 'admin-user',
            ...         'loyalty_tier': 'gold'
            ...     }
            ... ))
            >>> print('Updated customer:', updated.email)
        """
        return self._http.patch(
            f'{self._base_path}/{customer_id}',
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateCustomer,
            response_model=Customer
        )

    def delete(self, customer_id: str) -> bool:
        """Delete a customer.

        This operation is irreversible. Ensure you have proper authorization
        before deleting a customer. Associated data may be affected.

        Args:
            customer_id: Customer ID

        Returns:
            True if deletion was successful

        Raises:
            WiilAPIError: When the customer is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> deleted = client.customers.delete('cust_123')
            >>> if deleted:
            ...     print('Customer deleted successfully')
        """
        return self._http.delete(f'{self._base_path}/{customer_id}')

    def list(self, params: Optional[PaginationRequest] = None) -> PaginatedResult[Customer]:
        """List customers with optional pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of customers

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> # List first page with default page size
            >>> result = client.customers.list()
            >>>
            >>> # List with custom pagination
            >>> page2 = client.customers.list(PaginationRequest(page=2, page_size=50))
            >>>
            >>> print(f"Found {page2.meta.total_count} customers")
            >>> print(f"Page {page2.meta.page} of {page2.meta.total_pages}")
            >>> for customer in page2.data:
            ...     print(f"- {customer.first_name} {customer.last_name} ({customer.email})")
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[Customer]
        )

    def create_batch(
        self,
        data: List[Union[CreateCustomer, Dict[str, Any]]]
    ) -> PaginatedResult[Customer]:
        """Create multiple customers in a batch.

        Args:
            data: List of customers to create (max 50 items)

        Returns:
            PaginatedResult containing created customers

        Raises:
            WiilValidationError: When batch size exceeds limit or validation fails
        """
        if len(data) > BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': f'Array length {len(data)} exceeds maximum of {BATCH_LIMIT}'
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateCustomer.model_validate(item)
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
            f'{self._base_path}/batch',
            payload,
            response_model=PaginatedResult[Customer]
        )


__all__ = ['CustomersResource']
