from typing import List, Optional

from integrify.postaguvercini.schemas.utils import BaseSchema
from integrify.schemas import PayloadBaseModel


class CreditBalanceRequestSchema(PayloadBaseModel, BaseSchema): ...


class SendSingleSMSRequestSchema(PayloadBaseModel, BaseSchema):
    message: str
    receivers: List[str]
    send_date: Optional[str] = None
    expire_date: Optional[str] = None
    channel: Optional[str] = None
    originator: Optional[str] = None


class SMSMessage(PayloadBaseModel, BaseSchema):
    receiver: str
    message: str


class SendMultipleSMSRequestSchema(PayloadBaseModel, BaseSchema):
    messages: List[SMSMessage]
    send_date: Optional[str] = None
    expire_date: Optional[str] = None
    channel: Optional[str] = None
    originator: Optional[str] = None
