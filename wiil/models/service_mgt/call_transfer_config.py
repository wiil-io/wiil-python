"""Call transfer configuration schema definitions.

This module contains models for call transfer configurations that enable
AI agents to transfer calls to human operators or other phone numbers.
"""

from typing import List, Literal

from pydantic import ConfigDict, Field
from pydantic import BaseModel as PydanticBaseModel

# Transfer type
TransferType = Literal["blind", "warm"]


class CallTransferConfig(PydanticBaseModel):
    """Call transfer configuration.

    Defines the structure for configuring call transfers in the telephony system.
    Call transfer configurations enable agents to handle escalations and routing scenarios.

    Transfer Types:
        - Blind Transfer: Immediately transfers the call without announcement
        - Warm Transfer: Announces the call to the recipient before connecting

    Use Cases:
        - Sales inquiries → Transfer to sales team
        - Technical support escalation → Transfer to senior technician
        - Billing questions → Transfer to billing department
        - Emergency situations → Transfer to on-call manager

    Attributes:
        transfer_number: Phone number to transfer calls to in E.164 format
        transfer_type: Transfer type ('blind' or 'warm')
        transfer_conditions: Natural language conditions that trigger this transfer

    Example:
        ```python
        transfer = CallTransferConfig(
            transfer_number="+15551234567",
            transfer_type="warm",
            transfer_conditions=[
                "speak to sales",
                "talk to manager",
                "escalate"
            ]
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True,
        use_enum_values=True,
    )

    transfer_number: str = Field(
        ...,
        description="Phone number in E.164 format (e.g., '+15551234567')"
    )
    transfer_type: TransferType = Field(
        "blind",
        description="Transfer type: 'blind' (immediate) or 'warm' (announced)"
    )
    transfer_conditions: List[str] = Field(
        ...,
        description="Natural language conditions that trigger this transfer"
    )
