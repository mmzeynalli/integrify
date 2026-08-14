from integrify.postaguvercini import env
from integrify.postaguvercini.schemas.enums import ChannelType
from integrify.postaguvercini.schemas.utils import BaseSchema
from integrify.postaguvercini.types import DateTime
from integrify.schemas import PayloadBaseModel
from pydantic import Field
from typing_extensions import TypedDict


class SendSingleSMSRequestSchema(PayloadBaseModel, BaseSchema):
    message: str
    receivers: list[str]

    # Not required
    send_date: DateTime
    expire_date: DateTime
    channel: ChannelType = ChannelType.OTP
    originator: str | None = None
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)


class SMSMessage(TypedDict):
    receiver: str
    message: str


class SendMultipleSMSRequestSchema(PayloadBaseModel, BaseSchema):
    messages: list[SMSMessage]

    # Not required
    send_date: DateTime
    expire_date: DateTime
    channel: ChannelType = ChannelType.OTP
    originator: str | None = None
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)


class StatusRequestSchema(PayloadBaseModel, BaseSchema):
    message_ids: list[str]
    # Not required
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)


class CreditBalanceRequestSchema(PayloadBaseModel, BaseSchema):
    # Not required
    username: str = Field(env.POSTA_GUVERCINI_USERNAME, validate_default=True)
    password: str = Field(env.POSTA_GUVERCINI_PASSWORD, validate_default=True)
