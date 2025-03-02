from typing import Optional

from integrify.postaguvercini.schemas.utils import BaseSchema


class MinimalResponseSchema(BaseSchema):
    status_code: int
    status_description: str


class CreditBalanceResultSchema(BaseSchema):
    balance: int


class SendSingleSMSResultSchema(BaseSchema):
    message_id: str
    receiver: str
    charge: int


class StatusResultSchema(BaseSchema):
    message_id: str
    receiver: str
    sms_status: str
    sms_status_description: str
    is_final_status: str
    status_time: str
    sms_charge: str


# Response schemas


class SendSMSResponseSchema(MinimalResponseSchema):
    result: Optional[list[SendSingleSMSResultSchema]]


class StatusResponseSchema(MinimalResponseSchema):
    result: Optional[list[StatusResultSchema]]


class CreditBalanceResponseSchema(MinimalResponseSchema):
    result: Optional[CreditBalanceResultSchema]
