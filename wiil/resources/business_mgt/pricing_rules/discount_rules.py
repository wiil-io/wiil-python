"""Discount rules resource for order discount configuration management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateDiscountRule,
    DiscountRule,
    UpdateDiscountRule,
)
from wiil.models.type_definitions.business_definitions import (
    DiscountScope,
    DiscountType,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class DiscountRulesResource:
    """Resource class for managing discount rules."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/discount-rules"

    def create(self, data: CreateDiscountRule) -> DiscountRule:
        """Create a new discount rule."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateDiscountRule,
            response_model=DiscountRule,
        )

    def get(self, rule_id: str) -> DiscountRule:
        """Retrieve a discount rule by ID."""
        return self._http.get(
            f"{self._base_path}/{rule_id}",
            response_model=DiscountRule,
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[DiscountRule]:
        """Retrieve discount rules by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[DiscountRule],
        )

    def get_by_code(self, code: str) -> DiscountRule:
        """Retrieve a discount rule by promo code."""
        return self._http.get(
            f"{self._base_path}/by-code/{code}",
            response_model=DiscountRule,
        )

    def get_by_scope(
        self,
        scope: DiscountScope,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[DiscountRule]:
        """Retrieve discount rules by scope."""
        query_params: Dict[str, Any] = {"scope": scope.value}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-scope?{urlencode(query_params)}",
            response_model=PaginatedResult[DiscountRule],
        )

    def get_by_type(
        self,
        discount_type: DiscountType,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[DiscountRule]:
        """Retrieve discount rules by type."""
        query_params: Dict[str, Any] = {"type": discount_type.value}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-type?{urlencode(query_params)}",
            response_model=PaginatedResult[DiscountRule],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[DiscountRule]:
        """Retrieve active discount rules."""
        query_params: Dict[str, Any] = {"isActive": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/active?{urlencode(query_params)}",
            response_model=PaginatedResult[DiscountRule],
        )

    def get_stackable(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[DiscountRule]:
        """Retrieve stackable discount rules."""
        query_params: Dict[str, Any] = {"isStackable": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/stackable?{urlencode(query_params)}",
            response_model=PaginatedResult[DiscountRule],
        )

    def update(self, data: UpdateDiscountRule) -> DiscountRule:
        """Update an existing discount rule."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateDiscountRule,
            response_model=DiscountRule,
        )

    def delete(self, rule_id: str) -> bool:
        """Delete a discount rule."""
        return self._http.delete(f"{self._base_path}/{rule_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[DiscountRule]:
        """List discount rules with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[DiscountRule],
        )

    def create_batch(
        self,
        data: List[Union[CreateDiscountRule, Dict[str, Any]]],
    ) -> PaginatedResult[DiscountRule]:
        """Create multiple discount rules in one batch call."""
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
                    validated = CreateDiscountRule.model_validate(item)
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
            response_model=PaginatedResult[DiscountRule],
        )


__all__ = ["DiscountRulesResource"]
