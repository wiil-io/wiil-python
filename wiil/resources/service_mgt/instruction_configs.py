"""Instruction Configurations resource for managing instruction configuration entities."""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    InstructionConfiguration,
    CreateInstructionConfiguration,
    UpdateInstructionConfiguration,
)
from wiil.types import PaginatedResult


class InstructionConfigurationsResource:
    """Resource class for managing instruction configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    instruction configurations. Instruction configurations define the prompts,
    knowledge sources, and behavior instructions for AI agents.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/instruction-configurations'

    def create(self, **kwargs: Any) -> InstructionConfiguration:
        """Create a new instruction configuration."""
        data = CreateInstructionConfiguration(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateInstructionConfiguration
        )

    def get(self, config_id: str) -> InstructionConfiguration:
        """Retrieve an instruction configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}')

    def update(self, **kwargs: Any) -> InstructionConfiguration:
        """Update an existing instruction configuration."""
        data = UpdateInstructionConfiguration(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateInstructionConfiguration
        )

    def delete(self, config_id: str) -> bool:
        """Delete an instruction configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> PaginatedResult[InstructionConfiguration]:
        """List instruction configurations with pagination."""
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')

    def get_supported_templates(self) -> List[InstructionConfiguration]:
        """Retrieve the list of supported instruction templates.

        Returns:
            Array of supported instruction template configurations

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> templates = client.instruction_configs.get_supported_templates()
            >>> print(f"Found {len(templates)} supported templates")
            >>> for template in templates:
            ...     print(f"- {template.name} ({template.id})")
        """
        return self._http.get(f'{self._base_path}/supported-templates')


__all__ = ['InstructionConfigurationsResource']
