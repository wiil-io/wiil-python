"""Menu pricing rules resource for menu-specific promotions and discounts."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateMenuPricingRule,
    MenuPricingRule,
    UpdateMenuPricingRule,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class MenuPricingRulesResource:
    """Resource class for menu pricing rules."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/menu-pricing-rules"

    def create(self, data: CreateMenuPricingRule) -> MenuPricingRule:
        """Create a new menu pricing rule."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateMenuPricingRule,
            response_model=MenuPricingRule,
        )

    def get(self, pricing_rule_id: str) -> MenuPricingRule:
        """Retrieve a menu pricing rule by ID."""
        return self._http.get(
            f"{self._base_path}/{pricing_rule_id}",
            response_model=MenuPricingRule,
        )

    def get_by_menu_set(
        self,
        menu_set_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MenuPricingRule]:
        """Retrieve pricing rules for a menu set."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-menu-set/{menu_set_id}{query_string}",
            response_model=PaginatedResult[MenuPricingRule],
        )

    def get_by_discount(
        self,
        discount_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MenuPricingRule]:
        """Retrieve pricing rules by discount ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-discount/{discount_id}{query_string}",
            response_model=PaginatedResult[MenuPricingRule],
        )

    def get_active(
        self,
        timestamp: Optional[int] = None,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MenuPricingRule]:
        """Retrieve active pricing rules, optionally at a timestamp."""
        query_params: Dict[str, Any] = {}
        if timestamp is not None:
            query_params["effectiveAt"] = timestamp
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/active{query_string}",
            response_model=PaginatedResult[MenuPricingRule],
        )

    def update(
        self,
        pricing_rule_id: str,
        data: UpdateMenuPricingRule,
    ) -> MenuPricingRule:
        """Update an existing menu pricing rule."""
        return self._http.patch(
            f"{self._base_path}/{pricing_rule_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateMenuPricingRule,
            response_model=MenuPricingRule,
        )

    def delete(self, pricing_rule_id: str) -> bool:
        """Delete a menu pricing rule."""
        return self._http.delete(f"{self._base_path}/{pricing_rule_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[MenuPricingRule]:
        """List menu pricing rules with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[MenuPricingRule],
        )

    def create_batch(
        self,
        data: List[Union[CreateMenuPricingRule, Dict[str, Any]]],
    ) -> PaginatedResult[MenuPricingRule]:
        """Create multiple pricing rules in a batch."""
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
                    validated = CreateMenuPricingRule.model_validate(item)
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
            response_model=PaginatedResult[MenuPricingRule],
        )


__all__ = ["MenuPricingRulesResource"]
