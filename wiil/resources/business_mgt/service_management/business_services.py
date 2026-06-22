"""Business Services resource for managing business service configurations."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    BusinessServiceCatalog,
    BusinessServiceConfig,
    CreateBusinessService,
    UpdateBusinessService,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class BusinessServicesResource:
    """Resource class for managing business services in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting,
    and listing business services. Business services represent
    the services offered by a business within an organization
    (e.g., haircut, massage, consultation).
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/business-services'

    def create(self, data: CreateBusinessService) -> BusinessServiceConfig:
        """Create a new business service."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateBusinessService,
            response_model=BusinessServiceConfig
        )

    def get(self, service_id: str) -> BusinessServiceConfig:
        """Retrieve a business service by ID."""
        return self._http.get(
            f'{self._base_path}/{service_id}',
            response_model=BusinessServiceConfig,
        )

    def update(self, data: UpdateBusinessService) -> BusinessServiceConfig:
        """Update an existing business service."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateBusinessService,
            response_model=BusinessServiceConfig
        )

    def delete(self, service_id: str) -> bool:
        """Delete a business service."""
        return self._http.delete(f'{self._base_path}/{service_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[BusinessServiceConfig]:
        """List business services with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[BusinessServiceConfig]
        )

    def get_catalog(self) -> BusinessServiceCatalog:
        """Retrieve the full business service catalog by category."""
        return self._http.get(
            f'{self._base_path}/catalog',
            response_model=BusinessServiceCatalog,
        )

    def create_batch(
        self,
        data: List[Union[CreateBusinessService, Dict[str, Any]]]
    ) -> PaginatedResult[BusinessServiceConfig]:
        """Create multiple business services in a batch.

        Args:
            data: List of business services to create (max 50 items)

        Returns:
            PaginatedResult containing created business services

        Raises:
            WiilValidationError: When batch size exceeds limit
                or validation fails
        """
        if len(data) > BATCH_LIMIT:
            raise WiilValidationError(
                f'Batch size exceeds maximum limit of {BATCH_LIMIT}',
                details=[{
                    'path': ['data'],
                    'message': (
                        f'Array length {len(data)} exceeds '
                        f'maximum of {BATCH_LIMIT}'
                    ),
                }]
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateBusinessService.model_validate(item)
                    payload.append(
                        validated.model_dump(
                            by_alias=True,
                            exclude_none=True,
                        )
                    )
                elif isinstance(item, BaseModel):
                    payload.append(
                        item.model_dump(
                            by_alias=True,
                            exclude_none=True,
                        )
                    )
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
            response_model=PaginatedResult[BusinessServiceConfig]
        )


__all__ = ['BusinessServicesResource']
