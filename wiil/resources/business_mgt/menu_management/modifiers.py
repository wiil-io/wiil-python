"""Modifiers resource for groups, options, and item bindings."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateItemModifierBinding,
    CreateModifierGroup,
    CreateModifierOption,
    ItemModifierBinding,
    ModifierGroup,
    ModifierOption,
    UpdateItemModifierBinding,
    UpdateModifierGroup,
    UpdateModifierOption,
)
from wiil.types import PaginatedResult, PaginationRequest

GROUP_BATCH_LIMIT = 50
OPTION_BATCH_LIMIT = 100
BINDING_BATCH_LIMIT = 100


class ModifiersResource:
    """Resource class for managing modifier groups, options, and bindings."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/modifiers"

    def create_group(self, data: CreateModifierGroup) -> ModifierGroup:
        """Create a new modifier group."""
        return self._http.post(
            f"{self._base_path}/groups",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateModifierGroup,
            response_model=ModifierGroup,
        )

    def get_group(self, group_id: str) -> ModifierGroup:
        """Retrieve a modifier group by ID."""
        return self._http.get(
            f"{self._base_path}/groups/{group_id}",
            response_model=ModifierGroup,
        )

    def list_groups(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ModifierGroup]:
        """List modifier groups with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/groups{query_string}",
            response_model=PaginatedResult[ModifierGroup],
        )

    def update_group(
        self,
        group_id: str,
        data: UpdateModifierGroup,
    ) -> ModifierGroup:
        """Update a modifier group."""
        return self._http.patch(
            f"{self._base_path}/groups/{group_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateModifierGroup,
            response_model=ModifierGroup,
        )

    def delete_group(self, group_id: str) -> bool:
        """Delete a modifier group."""
        return self._http.delete(f"{self._base_path}/groups/{group_id}")

    def create_group_batch(
        self,
        data: List[Union[CreateModifierGroup, Dict[str, Any]]],
    ) -> PaginatedResult[ModifierGroup]:
        """Create multiple modifier groups in one batch."""
        if len(data) > GROUP_BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {GROUP_BATCH_LIMIT}",
                details=[
                    {
                        "path": ["data"],
                        "message": (
                            f"Array length {len(data)} exceeds "
                            f"maximum of {GROUP_BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateModifierGroup.model_validate(item)
                    payload.append(
                        validated.model_dump(by_alias=True, exclude_none=True)
                    )
                elif isinstance(item, BaseModel):
                    payload.append(
                        item.model_dump(by_alias=True, exclude_none=True)
                    )
                else:
                    raise WiilValidationError(
                        f"Invalid item type at index {i}",
                        details=[
                            {
                                "path": ["data", i],
                                "message": "Expected dict or Pydantic model",
                            }
                        ],
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f"Validation failed for item at index {i}",
                    details=e.errors(),
                )

        return self._http.post(
            f"{self._base_path}/groups/batch",
            payload,
            response_model=PaginatedResult[ModifierGroup],
        )

    def create_option(self, data: CreateModifierOption) -> ModifierOption:
        """Create a new modifier option."""
        return self._http.post(
            f"{self._base_path}/options",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateModifierOption,
            response_model=ModifierOption,
        )

    def get_option(self, option_id: str) -> ModifierOption:
        """Retrieve a modifier option by ID."""
        return self._http.get(
            f"{self._base_path}/options/{option_id}",
            response_model=ModifierOption,
        )

    def get_options_by_group(
        self,
        modifier_group_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ModifierOption]:
        """Retrieve modifier options for a modifier group."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/options/by-group/"
            f"{modifier_group_id}{query_string}",
            response_model=PaginatedResult[ModifierOption],
        )

    def list_options(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ModifierOption]:
        """List modifier options with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/options{query_string}",
            response_model=PaginatedResult[ModifierOption],
        )

    def update_option(
        self,
        option_id: str,
        data: UpdateModifierOption,
    ) -> ModifierOption:
        """Update a modifier option."""
        return self._http.patch(
            f"{self._base_path}/options/{option_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateModifierOption,
            response_model=ModifierOption,
        )

    def delete_option(self, option_id: str) -> bool:
        """Delete a modifier option."""
        return self._http.delete(f"{self._base_path}/options/{option_id}")

    def create_option_batch(
        self,
        data: List[Union[CreateModifierOption, Dict[str, Any]]],
    ) -> PaginatedResult[ModifierOption]:
        """Create multiple modifier options in one batch."""
        if len(data) > OPTION_BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {OPTION_BATCH_LIMIT}",
                details=[
                    {
                        "path": ["data"],
                        "message": (
                            f"Array length {len(data)} exceeds "
                            f"maximum of {OPTION_BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateModifierOption.model_validate(item)
                    payload.append(
                        validated.model_dump(by_alias=True, exclude_none=True)
                    )
                elif isinstance(item, BaseModel):
                    payload.append(
                        item.model_dump(by_alias=True, exclude_none=True)
                    )
                else:
                    raise WiilValidationError(
                        f"Invalid item type at index {i}",
                        details=[
                            {
                                "path": ["data", i],
                                "message": "Expected dict or Pydantic model",
                            }
                        ],
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f"Validation failed for item at index {i}",
                    details=e.errors(),
                )

        return self._http.post(
            f"{self._base_path}/options/batch",
            payload,
            response_model=PaginatedResult[ModifierOption],
        )

    def create_binding(
        self,
        data: CreateItemModifierBinding,
    ) -> ItemModifierBinding:
        """Create a new item modifier binding."""
        return self._http.post(
            f"{self._base_path}/bindings",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateItemModifierBinding,
            response_model=ItemModifierBinding,
        )

    def get_binding(self, binding_id: str) -> ItemModifierBinding:
        """Retrieve an item modifier binding by ID."""
        return self._http.get(
            f"{self._base_path}/bindings/{binding_id}",
            response_model=ItemModifierBinding,
        )

    def get_bindings_by_menu_item(
        self,
        menu_item_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ItemModifierBinding]:
        """Retrieve bindings by menu item ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/bindings/by-menu-item/"
            f"{menu_item_id}{query_string}",
            response_model=PaginatedResult[ItemModifierBinding],
        )

    def get_bindings_by_menu_set(
        self,
        menu_set_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ItemModifierBinding]:
        """Retrieve bindings by menu set ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/bindings/by-menu-set/"
            f"{menu_set_id}{query_string}",
            response_model=PaginatedResult[ItemModifierBinding],
        )

    def list_bindings(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ItemModifierBinding]:
        """List item modifier bindings with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/bindings{query_string}",
            response_model=PaginatedResult[ItemModifierBinding],
        )

    def update_binding(
        self,
        binding_id: str,
        data: UpdateItemModifierBinding,
    ) -> ItemModifierBinding:
        """Update an item modifier binding."""
        return self._http.patch(
            f"{self._base_path}/bindings/{binding_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateItemModifierBinding,
            response_model=ItemModifierBinding,
        )

    def delete_binding(self, binding_id: str) -> bool:
        """Delete an item modifier binding."""
        return self._http.delete(f"{self._base_path}/bindings/{binding_id}")

    def create_binding_batch(
        self,
        data: List[Union[CreateItemModifierBinding, Dict[str, Any]]],
    ) -> PaginatedResult[ItemModifierBinding]:
        """Create multiple item modifier bindings in one batch."""
        if len(data) > BINDING_BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {BINDING_BATCH_LIMIT}",
                details=[
                    {
                        "path": ["data"],
                        "message": (
                            f"Array length {len(data)} exceeds "
                            f"maximum of {BINDING_BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateItemModifierBinding.model_validate(item)
                    payload.append(
                        validated.model_dump(by_alias=True, exclude_none=True)
                    )
                elif isinstance(item, BaseModel):
                    payload.append(
                        item.model_dump(by_alias=True, exclude_none=True)
                    )
                else:
                    raise WiilValidationError(
                        f"Invalid item type at index {i}",
                        details=[
                            {
                                "path": ["data", i],
                                "message": "Expected dict or Pydantic model",
                            }
                        ],
                    )
            except ValidationError as e:
                raise WiilValidationError(
                    f"Validation failed for item at index {i}",
                    details=e.errors(),
                )

        return self._http.post(
            f"{self._base_path}/bindings/batch",
            payload,
            response_model=PaginatedResult[ItemModifierBinding],
        )


__all__ = ["ModifiersResource"]
