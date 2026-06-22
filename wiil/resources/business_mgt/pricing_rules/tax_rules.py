"""Tax rules resource for order tax configuration management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import CreateTaxRule, TaxRule, UpdateTaxRule
from wiil.models.type_definitions.business_definitions import (
    TaxRateType,
    TaxScope,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class TaxRulesResource:
    """Resource class for managing tax rules."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/tax-rules"

    def create(self, data: CreateTaxRule) -> TaxRule:
        """Create a new tax rule."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTaxRule,
            response_model=TaxRule,
        )

    def get(self, rule_id: str) -> TaxRule:
        """Retrieve a tax rule by ID."""
        return self._http.get(
            f"{self._base_path}/{rule_id}",
            response_model=TaxRule,
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TaxRule]:
        """Retrieve tax rules by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[TaxRule],
        )

    def get_by_scope(
        self,
        scope: TaxScope,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TaxRule]:
        """Retrieve tax rules by scope."""
        query_params: Dict[str, Any] = {"scope": scope.value}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-scope?{urlencode(query_params)}",
            response_model=PaginatedResult[TaxRule],
        )

    def get_by_rate_type(
        self,
        rate_type: TaxRateType,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TaxRule]:
        """Retrieve tax rules by rate type."""
        query_params: Dict[str, Any] = {"rateType": rate_type.value}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/by-rate-type?{urlencode(query_params)}",
            response_model=PaginatedResult[TaxRule],
        )

    def get_active(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TaxRule]:
        """Retrieve active tax rules."""
        query_params: Dict[str, Any] = {"isActive": "true"}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        return self._http.get(
            f"{self._base_path}/active?{urlencode(query_params)}",
            response_model=PaginatedResult[TaxRule],
        )

    def update(self, data: UpdateTaxRule) -> TaxRule:
        """Update an existing tax rule."""
        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateTaxRule,
            response_model=TaxRule,
        )

    def delete(self, rule_id: str) -> bool:
        """Delete a tax rule."""
        return self._http.delete(f"{self._base_path}/{rule_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[TaxRule]:
        """List tax rules with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[TaxRule],
        )

    def create_batch(
        self,
        data: List[Union[CreateTaxRule, Dict[str, Any]]],
    ) -> PaginatedResult[TaxRule]:
        """Create multiple tax rules in one batch call."""
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
                    validated = CreateTaxRule.model_validate(item)
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
            response_model=PaginatedResult[TaxRule],
        )


__all__ = ["TaxRulesResource"]
