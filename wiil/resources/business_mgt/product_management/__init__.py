"""Product management business resource classes."""

from .product_axis_bindings import ProductAxisBindingsResource
from .product_orders import ProductOrdersResource
from .product_pricing_rules import ProductPricingRulesResource
from .product_sets import ProductSetsResource
from .product_variant_axes import ProductVariantAxesResource
from .product_variants import ProductVariantsResource
from .products import ProductsResource

__all__ = [
    "ProductsResource",
    "ProductOrdersResource",
    "ProductVariantsResource",
    "ProductVariantAxesResource",
    "ProductAxisBindingsResource",
    "ProductSetsResource",
    "ProductPricingRulesResource",
]
