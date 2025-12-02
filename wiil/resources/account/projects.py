"""Projects resource for managing project entities.

This module provides the ProjectsResource class for managing projects
in the WIIL Platform API.

Example:
    >>> from wiil import WiilClient
    >>> client = WiilClient(api_key='your-api-key')
    >>> project = client.projects.create(name='Production')
    >>> print(project.id)
"""

from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.account import (
    Project,
    CreateProject,
    UpdateProject,
)
from wiil.types import PaginatedResult


class ProjectsResource:
    """Resource class for managing projects in the WIIL Platform.

    Provides methods for creating, retrieving, updating, deleting, and listing
    projects. Projects are organizational units within an organization that group
    resources, deployments, and configurations. Supports retrieving the default
    project for an organization.

    Example:
        >>> client = WiilClient(api_key='your-api-key')
        >>>
        >>> # Create a new project
        >>> project = client.projects.create(
        ...     name='Production Environment',
        ...     description='Main production deployment',
        ...     compliance=['SOC2', 'HIPAA']
        ... )
        >>>
        >>> # Get a project by ID
        >>> proj = client.projects.get('proj_123')
        >>>
        >>> # Get the default project
        >>> default_proj = client.projects.get_default()
        >>>
        >>> # Update a project
        >>> updated = client.projects.update(
        ...     id='proj_123',
        ...     description='Updated production deployment',
        ...     region_id='us-west-2'
        ... )
        >>>
        >>> # List all projects
        >>> projects = client.projects.list(page=1, page_size=20)
        >>>
        >>> # Delete a project
        >>> client.projects.delete('proj_123')
    """

    def __init__(self, http: HttpClient):
        """Initialize the projects resource.

        Args:
            http: HTTP client for API communication
        """
        self._http = http
        self._base_path = '/projects'

    def create(self, **kwargs: Any) -> Project:
        """Create a new project.

        Args:
            **kwargs: Project data fields (name, description, compliance, etc.)

        Returns:
            The created project

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> project = client.projects.create(
            ...     name='Development Environment',
            ...     description='Development and testing project',
            ...     compliance=['SOC2'],
            ...     metadata={
            ...         'environment': 'development',
            ...         'team': 'engineering'
            ...     }
            ... )
            >>> print('Created project:', project.id)
        """
        data = CreateProject(**kwargs)
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProject
        )

    def get(self, project_id: str) -> Project:
        """Retrieve a project by ID.

        Args:
            project_id: Project ID

        Returns:
            The requested project

        Raises:
            WiilAPIError: When the project is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> project = client.projects.get('proj_123')
            >>> print('Project:', project.name)
            >>> print('Is Default:', project.is_default)
        """
        return self._http.get(f'{self._base_path}/{project_id}')

    def get_default(self) -> Project:
        """Retrieve the default project for the current organization.

        Every organization should have a default project. This method retrieves
        the project marked as default for the authenticated organization.

        Returns:
            The default project

        Raises:
            WiilAPIError: When the default project is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> default_project = client.projects.get_default()
            >>> print('Default Project:', default_project.name)
            >>> print('Project ID:', default_project.id)
        """
        return self._http.get(f'{self._base_path}/default')

    def update(self, **kwargs: Any) -> Project:
        """Update an existing project.

        Args:
            **kwargs: Project update data (must include id)

        Returns:
            The updated project

        Raises:
            WiilValidationError: When input validation fails
            WiilAPIError: When the project is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> updated = client.projects.update(
            ...     id='proj_123',
            ...     name='Production Environment v2',
            ...     description='Updated production deployment',
            ...     metadata={
            ...         'updated_by': 'admin-user',
            ...         'version': '2.0'
            ...     }
            ... )
            >>> print('Updated project:', updated.name)
        """
        data = UpdateProject(**kwargs)
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProject
        )

    def delete(self, project_id: str) -> bool:
        """Delete a project.

        This operation is irreversible. Ensure you have proper authorization
        before deleting a project. All resources associated with the project
        may also be affected.

        Args:
            project_id: Project ID

        Returns:
            True if deletion was successful

        Raises:
            WiilAPIError: When the project is not found or API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> deleted = client.projects.delete('proj_123')
            >>> if deleted:
            ...     print('Project deleted successfully')
        """
        return self._http.delete(f'{self._base_path}/{project_id}')

    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None
    ) -> PaginatedResult[Project]:
        """List projects with optional pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            sort_by: Field to sort by
            sort_direction: Sort direction ('asc' or 'desc')

        Returns:
            Paginated list of projects

        Raises:
            WiilAPIError: When the API returns an error
            WiilNetworkError: When network communication fails

        Example:
            >>> # List first page with default page size
            >>> result = client.projects.list()
            >>>
            >>> # List with custom pagination
            >>> page2 = client.projects.list(
            ...     page=2,
            ...     page_size=50,
            ...     sort_by='name',
            ...     sort_direction='desc'
            ... )
            >>>
            >>> print(f"Found {page2.meta.total_count} projects")
            >>> print(f"Page {page2.meta.page} of {page2.meta.total_pages}")
            >>> for project in page2.data:
            ...     print(f"- {project.name} ({project.id})")
        """
        params: Dict[str, Any] = {}
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['pageSize'] = page_size
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_direction is not None:
            params['sortDirection'] = sort_direction

        query_string = f'?{urlencode(params)}' if params else ''
        return self._http.get(f'{self._base_path}{query_string}')


__all__ = ['ProjectsResource']
