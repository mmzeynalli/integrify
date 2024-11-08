from typing import List, Optional

from pydantic import Field

from integrify.kapital import env
from integrify.schemas import PayloadBaseModel


class CreateOrderRequestSchema(PayloadBaseModel):
    # TODO: Update to decimal
    amount: str
    currency: str
    description: str
    language: Optional[str] = env.KAPITAL_INTERFACE_LANG
    hppRedirectUrl: Optional[str] = Field(default=env.KAPITAL_REDIRECT_URL)
    typeRid: Optional[str] = Field(default='Order_SMS')
    hppCofCapturePurposes: Optional[List[str]] = Field(default=['Cit'])


class RefundOrderRequestSchema(PayloadBaseModel):
    # TODO: Update to decimal
    amount: str
    phase: str = Field(default='Single')
    type: str = Field(default='Refund')
