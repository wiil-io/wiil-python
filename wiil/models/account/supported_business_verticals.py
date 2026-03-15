"""Supported Business Vertical IDs.

This file contains only the business vertical IDs extracted from
business-verticals-definitions.ts for use in validation and type checking.

This module mirrors src/core/account/supported-business-verticals.ts
"""

from typing import List, Literal

SUPPORTED_BUSINESS_VERTICALS: List[str] = [
    "healthcare",
    "health-wellness",
    "retail",
    "finance",
    "real-estate",
    "technology",
    "education",
    "legal",
    "automotive",
    "hospitality",
    "professional",
    "others",
]

SupportedBusinessVerticalId = Literal[
    "healthcare",
    "health-wellness",
    "retail",
    "finance",
    "real-estate",
    "technology",
    "education",
    "legal",
    "automotive",
    "hospitality",
    "professional",
    "others",
]
