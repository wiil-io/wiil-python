"""Deployment Channels resource for managing deployment channel entities."""

from typing import Any, Dict, Optional
from urllib.parse import quote, urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    DeploymentChannel,
    CreateDeploymentChannel,
    UpdateDeploymentChannel,
)
from wiil.types import PaginatedResult, PaginationRequest


class DeploymentChannelsResource:
    """Resource class for managing deployment channels in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    deployment channels. Deployment channels represent communication endpoints
    (phone numbers, web URLs, etc.) used for AI deployments.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/deployment-channels'

    def create(self, data: CreateDeploymentChannel) -> DeploymentChannel:
        """Create a new deployment channel.

        Args:
            data: Deployment channel creation data

        Returns:
            The created deployment channel
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateDeploymentChannel,
            response_model=DeploymentChannel
        )

    def get(self, channel_id: str) -> DeploymentChannel:
        """Retrieve a deployment channel by ID."""
        return self._http.get(f'{self._base_path}/{channel_id}', response_model=DeploymentChannel)

    def get_by_identifier(self, identifier: str, channel_type: str) -> DeploymentChannel:
        """Retrieve a deployment channel by identifier and type.

        Args:
            identifier: Channel identifier (phone number, URL, etc.)
            channel_type: Deployment type (CALLS, SMS, WEB, MOBILE)

        Returns:
            The deployment channel matching the identifier and type
        """
        encoded_identifier = quote(identifier, safe='')
        return self._http.get(
            f'{self._base_path}/by-identifier/{encoded_identifier}?type={channel_type}',
            response_model=DeploymentChannel
        )

    def update(self, data: UpdateDeploymentChannel) -> DeploymentChannel:
        """Update an existing deployment channel.

        Args:
            data: Deployment channel update data (must include id)

        Returns:
            The updated deployment channel
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateDeploymentChannel,
            response_model=DeploymentChannel
        )

    def delete(self, channel_id: str, delete_phone_config: bool = False) -> bool:
        """Delete a deployment channel.

        Args:
            channel_id: Deployment channel ID
            delete_phone_config: Whether to also delete the associated phone
                configuration (default: False)

        Returns:
            True if deletion was successful
        """
        query_string = '?deletePhoneConfig=true' if delete_phone_config else ''
        return self._http.delete(f'{self._base_path}/{channel_id}{query_string}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DeploymentChannel]:
        """List deployment channels with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of deployment channels
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[DeploymentChannel]
        )

    def list_by_type(
        self,
        channel_type: str,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[DeploymentChannel]:
        """List deployment channels by deployment type.

        Args:
            channel_type: Deployment type (CALLS, SMS, WEB, MOBILE)
            params: Pagination parameters

        Returns:
            Paginated list of deployment channels of the specified type
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}/by-type/{channel_type}{query_string}',
            response_model=PaginatedResult[DeploymentChannel]
        )


__all__ = ['DeploymentChannelsResource']
