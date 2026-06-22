"""Instruction Configurations resource for managing instruction configuration entities."""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.service_mgt import (
    InstructionConfiguration,
    CreateInstructionConfiguration,
    UpdateInstructionConfiguration,
)
from wiil.types import PaginatedResult, PaginationRequest


class InstructionConfigurationsResource:
    """Resource class for managing instruction configurations in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    instruction configurations. Instruction configurations define the prompts,
    knowledge sources, and behavior instructions for AI agents.
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/instruction-configurations'

    def create(self, data: CreateInstructionConfiguration) -> InstructionConfiguration:
        """Create a new instruction configuration.

        Args:
            data: Instruction configuration creation data

        Returns:
            The created instruction configuration
        """
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateInstructionConfiguration,
            response_model=InstructionConfiguration
        )

    def get(self, config_id: str) -> InstructionConfiguration:
        """Retrieve an instruction configuration by ID."""
        return self._http.get(f'{self._base_path}/{config_id}', response_model=InstructionConfiguration)

    def update(self, data: UpdateInstructionConfiguration) -> InstructionConfiguration:
        """Update an existing instruction configuration.

        Args:
            data: Instruction configuration update data (must include id)

        Returns:
            The updated instruction configuration
        """
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateInstructionConfiguration,
            response_model=InstructionConfiguration
        )

    def delete(self, config_id: str) -> bool:
        """Delete an instruction configuration."""
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[InstructionConfiguration]:
        """List instruction configurations with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of instruction configurations
        """
        query_params: Dict[str, Any] = {}
        if params:
            query_params['page'] = params.page
            query_params['pageSize'] = params.page_size

        query_string = f'?{urlencode(query_params)}' if query_params else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[InstructionConfiguration]
        )

    def add_knowledge_sources(
        self,
        config_id: str,
        knowledge_source_ids: List[str]
    ) -> InstructionConfiguration:
        """Attach knowledge sources to an instruction configuration.

        Args:
            config_id: Instruction configuration ID
            knowledge_source_ids: Knowledge source IDs to attach

        Returns:
            The updated instruction configuration
        """
        return self._http.post(
            f'{self._base_path}/{config_id}/knowledge-sources',
            {'knowledgeSourceIds': knowledge_source_ids},
            response_model=InstructionConfiguration
        )

    def remove_knowledge_sources(
        self,
        config_id: str,
        knowledge_source_ids: List[str]
    ) -> InstructionConfiguration:
        """Detach knowledge sources from an instruction configuration.

        Args:
            config_id: Instruction configuration ID
            knowledge_source_ids: Knowledge source IDs to detach

        Returns:
            The updated instruction configuration
        """
        return self._http.delete(
            f'{self._base_path}/{config_id}/knowledge-sources',
            response_model=InstructionConfiguration,
            json={'knowledgeSourceIds': knowledge_source_ids}
        )

    def get_supported_templates(self) -> List[InstructionConfiguration]:
        """Retrieve the list of supported instruction templates.

        Returns:
            List of supported instruction template configurations
        """
        return self._http.get(
            f'{self._base_path}/supported-templates',
            response_model=List[InstructionConfiguration]
        )


__all__ = ['InstructionConfigurationsResource']
