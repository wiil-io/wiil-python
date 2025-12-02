"""Deployment Channels resource for managing deployment channel entities."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    DeploymentChannel,
    CreateDeploymentChannel,
    DeploymentChannelUpdateRequest,
)
from wiil.types import PaginatedResult


class DeploymentChannelsResource:
    """Resource class for managing deployment channels in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    deployment channels. Deployment channels represent communication endpoints
    (phone numbers, web URLs, etc.) used for AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/deployment-channels'

    def create(self, **kwargs: Any) -> DeploymentChannel:
        """Create a new deployment channel."""
        data = CreateDeploymentChannel(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateDeploymentChannel
        )

    def get(self, channel_id: str) -> DeploymentChannel:
        """Retrieve a deployment channel by ID."""
        return self._http.get(f'{self._base_path}/{channel_id}')

    def get_by_identifier(self, identifier: str, channel_type: str) -> DeploymentChannel:
        """Retrieve a deployment channel by identifier and type.

        Args:
            identifier: Channel identifier (phone number, URL, etc.)
            channel_type: Deployment type (CALLS, SMS, WEB, MOBILE)
        """
        return self._http.get(f'{self._base_path}/by-identifier/{identifier}?type={channel_type}')

    def update(self, **kwargs: Any) -> DeploymentChannel:
        """Update an existing deployment channel."""
        data = DeploymentChannelUpdateRequest(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=DeploymentChannelUpdateRequest
        )

    def delete(self, channel_id: str) -> bool:
        """Delete a deployment channel."""
        return self._http.delete(f'{self._base_path}/{channel_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[DeploymentChannel]:
        """List deployment channels with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def list_by_type(
        self,
        channel_type: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[DeploymentChannel]:
        """List deployment channels by deployment type.

        Args:
            channel_type: Deployment type (CALLS, SMS, WEB, MOBILE)
            page: Page number
            page_size: Number of items per page
        """
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}/by-type/{channel_type}{query_string}')


__all__ = ['DeploymentChannelsResource']
