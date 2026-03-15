"""Call transfer configuration schema definitions.

Call transfer configurations enable AI agents to transfer calls to human operators or other
phone numbers based on specific conditions or user requests. Supports both blind (immediate)
and warm (announced) transfer types.
"""

from typing import List, Literal

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


# Transfer type
TransferType = Literal["blind", "warm"]


class CallTransferConfig(PydanticBaseModel):
    """Call transfer configuration.

    Defines the structure for configuring call transfers in the telephony system. Call transfer
    configurations are used by Agent Configurations to handle escalations and routing scenarios.
    Multiple transfer configurations can be defined, each with different conditions and destinations.

    Architecture Context:
        - Used By: Agent Configuration (call_transfer_config array)
        - Purpose: Enables agents to escalate or route calls to human operators or specialized teams
        - Transfer Types:
            - Blind Transfer: Immediately transfers the call without announcement
            - Warm Transfer: Announces the call to the recipient before connecting the caller

    Use Cases:
        - Sales inquiries -> Transfer to sales team
        - Technical support escalation -> Transfer to senior technician
        - Billing questions -> Transfer to billing department
        - Emergency situations -> Transfer to on-call manager

    Attributes:
        transfer_number: The phone number to transfer calls to in E.164 format
        transfer_type: Transfer type (blind for immediate, warm for announced)
        transfer_conditions: Array of conditions or phrases that trigger this transfer

    Example:
        ```python
        config = CallTransferConfig(
            transfer_number="+15551234567",
            transfer_type="warm",
            transfer_conditions=["speak to sales", "talk to manager", "escalate"]
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    transfer_number: str = Field(
        ...,
        description="Phone number in E.164 international format to transfer calls to (e.g., '+15551234567' for US numbers, '+442071234567' for UK numbers)"
    )
    transfer_type: TransferType = Field(
        "blind",
        description="Type of call transfer: 'blind' for immediate transfer without announcement (faster), 'warm' for announced transfer where the recipient is informed before connection (professional)"
    )
    transfer_conditions: List[str] = Field(
        ...,
        description="Array of natural language conditions, keywords, or phrases that trigger this call transfer (e.g., 'speak to sales', 'talk to a human', 'escalate to manager')"
    )
