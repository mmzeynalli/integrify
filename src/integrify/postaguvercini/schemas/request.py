from typing import List, Optional

from pydantic import Field

from integrify.postaguvercini import env
from integrify.postaguvercini.schemas.utils import BaseSchema
from integrify.schemas import PayloadBaseModel


class SendSingleSMSRequestSchema(PayloadBaseModel, BaseSchema):
    message: str
    receivers: List[str]

    # Not required
    send_date: Optional[str] = None
    expire_date: Optional[str] = None
    channel: Optional[str] = None
    originator: Optional[str] = None
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)  # type: ignore[assignment]
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)  # type: ignore[assignment]


class SMSMessage(PayloadBaseModel, BaseSchema):
    receiver: str
    message: str


class SendMultipleSMSRequestSchema(PayloadBaseModel, BaseSchema):
    messages: List[SMSMessage]

    # Not required
    send_date: Optional[str] = None
    expire_date: Optional[str] = None
    channel: Optional[str] = None
    originator: Optional[str] = None
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)  # type: ignore[assignment]
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)  # type: ignore[assignment]


class StatusRequestSchema(PayloadBaseModel, BaseSchema):
    message_ids: List[str]
    # Not required
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)  # type: ignore[assignment]
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)  # type: ignore[assignment]


class CreditBalanceRequestSchema(PayloadBaseModel, BaseSchema):
    # Not required
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)  # type: ignore[assignment]
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)  # type: ignore[assignment]
