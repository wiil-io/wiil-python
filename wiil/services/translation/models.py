"""Translation service request and response models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SupportLanguage(BaseModel):
    """Supported language descriptor."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    code: str
    name: str = Field(..., min_length=1, max_length=100)
    native_name: str = Field(..., alias="nativeName", min_length=1, max_length=100)


class TranslationRequest(BaseModel):
    """Translation connection configuration request payload."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    initiator_id: str = Field(..., alias="initiatorId")
    participant_id: Optional[str] = Field(None, alias="participantId")
    initiator_language_code: str = Field(..., alias="initiatorLanguageCode")
    participant_language_code: str = Field(..., alias="participantLanguageCode")
    session_id: Optional[str] = Field(None, alias="sessionId")
    provisioning_config_id: Optional[str] = Field(None, alias="provisioningConfigId")


class TranslationConnectionConfig(BaseModel):
    """Translation connection configuration response payload."""

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    sdrtn_id: str = Field(..., alias="sdrtnId")
    channel_identifier: str = Field(..., alias="channelIdentifier")
    initiator_access_id: int = Field(..., alias="initiatorAccessId")
    initiator_token: str = Field(..., alias="initiatorToken")
    participant_access_id: int = Field(..., alias="participantAccessId")
    participant_token: str = Field(..., alias="participantToken")
