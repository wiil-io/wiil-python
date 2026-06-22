"""Menu item variants resource for managing item size and option variants."""

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateMenuItemVariant,
    MenuItemVariant,
    UpdateMenuItemVariant,
)
from wiil.types import PaginatedResult

BATCH_LIMIT = 100


class MenuItemVariantsResource:
    """Resource class for menu item variants."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/menu-management/variants"

    def create(self, data: CreateMenuItemVariant) -> MenuItemVariant:
        """Create a new menu item variant."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMenuItemVariant,
            response_model=MenuItemVariant,
        )

    def get(self, variant_id: str) -> MenuItemVariant:
        """Retrieve a menu item variant by ID."""
        return self._http.get(
            f"{self._base_path}/{variant_id}",
            response_model=MenuItemVariant,
        )

    def get_default(self, menu_item_id: str) -> Optional[MenuItemVariant]:
        """Retrieve the default variant for a menu item."""
        return self._http.get(
            f"{self._base_path}/default/{menu_item_id}",
            response_model=MenuItemVariant,
        )

    def update(
        self,
        variant_id: str,
        data: UpdateMenuItemVariant,
    ) -> MenuItemVariant:
        """Update an existing menu item variant."""
        return self._http.patch(
            f"{self._base_path}/{variant_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMenuItemVariant,
            response_model=MenuItemVariant,
        )

    def delete(self, variant_id: str) -> bool:
        """Delete a menu item variant."""
        return self._http.delete(f"{self._base_path}/{variant_id}")

    def create_batch(
        self,
        data: List[Union[CreateMenuItemVariant, Dict[str, Any]]],
    ) -> PaginatedResult[MenuItemVariant]:
        """Create multiple menu item variants in a batch."""
        if len(data) > BATCH_LIMIT:
            raise WiilValidationError(
                f"Batch size exceeds maximum limit of {BATCH_LIMIT}",
                details=[
                    {
                        "path": ["data"],
                        "message": (
                            f"Array length {len(data)} exceeds "
                            f"maximum of {BATCH_LIMIT}"
                        ),
                    }
                ],
            )

        payload = []
        for i, item in enumerate(data):
            try:
                if isinstance(item, dict):
                    validated = CreateMenuItemVariant.model_validate(item)
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
            f"{self._base_path}/batch",
            payload,
            response_model=PaginatedResult[MenuItemVariant],
        )


__all__ = ["MenuItemVariantsResource"]
