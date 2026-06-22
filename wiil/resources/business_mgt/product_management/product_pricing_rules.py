"""Product pricing rules resource for promotions and discount logic."""

from typing import Any, Dict, Optional
from urllib.parse import urlencode

from wiil.client.http_client import HttpClient
from wiil.models.business_mgt import (
    CreateProductPricingRule,
    ProductPricingRule,
    UpdateProductPricingRule,
)
from wiil.types import PaginatedResult, PaginationRequest


class ProductPricingRulesResource:
    """Resource class for product pricing rules."""

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = "/product-pricing-rules"

    def create(self, data: CreateProductPricingRule) -> ProductPricingRule:
        """Create a new product pricing rule."""
        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProductPricingRule,
            response_model=ProductPricingRule,
        )

    def get(self, pricing_rule_id: str) -> ProductPricingRule:
        """Retrieve a product pricing rule by ID."""
        return self._http.get(
            f"{self._base_path}/{pricing_rule_id}",
            response_model=ProductPricingRule,
        )

    def get_by_product_set(
        self,
        product_set_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductPricingRule]:
        """Retrieve pricing rules by product set ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-product-set/{product_set_id}"
            f"{query_string}",
            response_model=PaginatedResult[ProductPricingRule],
        )

    def get_by_discount(
        self,
        discount_id: str,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductPricingRule]:
        """Retrieve pricing rules by discount ID."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}/by-discount/{discount_id}{query_string}",
            response_model=PaginatedResult[ProductPricingRule],
        )

    def get_active(
        self,
        timestamp: Optional[int] = None,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductPricingRule]:
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
            response_model=PaginatedResult[ProductPricingRule],
        )

    def update(
        self,
        pricing_rule_id: str,
        data: UpdateProductPricingRule,
    ) -> ProductPricingRule:
        """Update an existing product pricing rule."""
        return self._http.patch(
            f"{self._base_path}/{pricing_rule_id}",
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProductPricingRule,
            response_model=ProductPricingRule,
        )

    def delete(self, pricing_rule_id: str) -> bool:
        """Delete a product pricing rule."""
        return self._http.delete(f"{self._base_path}/{pricing_rule_id}")

    def list(
        self,
        params: Optional[PaginationRequest] = None,
    ) -> PaginatedResult[ProductPricingRule]:
        """List product pricing rules with pagination."""
        query_params: Dict[str, Any] = {}
        if params:
            query_params["page"] = params.page
            query_params["pageSize"] = params.page_size

        query_string = f"?{urlencode(query_params)}" if query_params else ""
        return self._http.get(
            f"{self._base_path}{query_string}",
            response_model=PaginatedResult[ProductPricingRule],
        )


__all__ = ["ProductPricingRulesResource"]
