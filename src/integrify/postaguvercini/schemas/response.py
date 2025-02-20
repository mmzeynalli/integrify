from typing import List, Optional

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


class SendSingleSMSResponseSchema(MinimalResponseSchema):
    result: Optional[SendSingleSMSResultSchema]


class SendMultipleSMSResponseSchema(MinimalResponseSchema):
    result: Optional[List[SendSingleSMSResultSchema]]


class CreditBalanceResponseSchema(MinimalResponseSchema):
    result: Optional[CreditBalanceResultSchema]
