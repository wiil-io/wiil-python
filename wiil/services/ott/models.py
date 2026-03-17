"""OTT service request and response models."""

from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


class OttContactInfo(BaseModel):
    """Contact information for OTT configuration requests.

    At least one of email or phone must be provided.
    """

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)

    @model_validator(mode='after')
    def check_email_or_phone(self) -> 'OttContactInfo':
        """Validate that at least one contact method is provided."""
        if not self.email and not self.phone:
            raise ValueError('Either email or phone must be provided')
        return self


class GetOttConfigurationRequest(BaseModel):
    """Request payload for fetching OTT connection configuration."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    config_id: str = Field(..., alias="configId")
    contact: Optional[OttContactInfo] = None


class OttChatConnectionConfig(BaseModel):
    """Chat connection configuration returned from the API."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    connection_url: str
    channel_token: str
    channel_identifier: str


class OttVoiceConnectionConfig(BaseModel):
    """Voice connection configuration returned from the API."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    sdrtn_id: str
    channel_identifier: str
    channel_token: str
    platform_user_id: Union[str, int]
