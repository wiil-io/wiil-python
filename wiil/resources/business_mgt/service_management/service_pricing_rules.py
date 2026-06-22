"""Service pricing rules resource for conditional pricing management."""

from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from pydantic import BaseModel, ValidationError

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import (
    CreateServicePricingRule,
    ServicePricingRule,
    UpdateServicePricingRule,
)
from wiil.types import PaginatedResult, PaginationRequest

BATCH_LIMIT = 50


class ServicePricingRulesResource:
    """Resource class for service pricing rules."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/service-pricing-rules"

    def create(self, data: CreateServicePricingRule) -> ServicePricingRule:
        """Create a new service pricing rule."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateServicePricingRule,
            response_model=ServicePricingRule,
        )

    def get(self, rule_id: str) -> ServicePricingRule:
        """Retrieve a service pricing rule by ID."""
        return self._http.get(
            f"{self._base_path}/{rule_id}",
            response_model=ServicePricingRule,
        )

    def get_by_location(
        self,
        location_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServicePricingRule]:
        """Retrieve service pricing rules by location."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-location/{location_id}{query_string}",
            response_model=PaginatedResult[ServicePricingRule],
        )

    def update(self, data: UpdateServicePricingRule) -> ServicePricingRule:
        """Update an existing service pricing rule."""
        return self._http.patch(
            f"{self._base_path}/{data.id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateServicePricingRule,
            response_model=ServicePricingRule,
        )

    def delete(self, rule_id: str) -> bool:
        """Delete a service pricing rule."""
        return self._http.delete(f"{self._base_path}/{rule_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ServicePricingRule]:
        """List service pricing rules with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ServicePricingRule],
        )

    def create_batch(
        self,
        data: List[Union[CreateServicePricingRule, Dict[str, Any]]],
    ) -> PaginatedResult[ServicePricingRule]:
        """Create multiple service pricing rules in one batch call."""
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
                    validated = CreateServicePricingRule.model_validate(item)
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
            response_model=PaginatedResult[ServicePricingRule],
        )


__all__ = ["ServicePricingRulesResource"]
