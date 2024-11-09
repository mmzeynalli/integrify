from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field

from integrify.kapital import env
from integrify.schemas import PayloadBaseModel


class CreateOrderRequestSchema(PayloadBaseModel):
    amount: Decimal
    currency: str
    description: str
    language: Optional[str] = env.KAPITAL_INTERFACE_LANG
    hppRedirectUrl: Optional[str] = Field(default=env.KAPITAL_REDIRECT_URL)
    typeRid: Optional[str] = Field(default='Order_SMS')
    hppCofCapturePurposes: Optional[List[str]] = Field(default=['Cit'])


class OrderInformationRequestSchema(PayloadBaseModel):
    order_id: str

    URL_PARAM_FIELDS = {'order_id'}


class RefundOrderRequestSchema(PayloadBaseModel):
    order_id: str
    amount: Decimal
    phase: str = Field(default='Single')
    type: str = Field(default='Refund')

    URL_PARAM_FIELDS = {'order_id'}


class SaveCardRequestSchema(CreateOrderRequestSchema):
    typeRid: Optional[str] = Field(default='Order_DMS')
    hppCofCapturePurposes: Optional[List[str]] = Field(default=['Cit', 'Recurring'])
    aut: Dict[str, str] = Field(default={'purpose': 'AddCard'})


class CreateOrderAndSaveCardRequestSchema(CreateOrderRequestSchema):
    typeRid: Optional[str] = Field(default='Order_SMS')
    aut: Dict[str, str] = Field(default={'purpose': 'AddCard'})


class FullReverseOrderRequestSchema(PayloadBaseModel):
    order_id: str
    phase: str = Field(default='Auth')
    voidKind: str = Field(default='Full')

    URL_PARAM_FIELDS = {'order_id'}


class ClearingOrderRequestSchema(PayloadBaseModel):
    order_id: str
    amount: Decimal
    phase: str = Field(default='Clearing')

    URL_PARAM_FIELDS = {'order_id'}


class PartialReverseOrderRequestSchema(PayloadBaseModel):
    order_id: str
    amount: Decimal
    phase: str = Field(default='Single')
    voidKind: str = Field(default='Partial')

    URL_PARAM_FIELDS = {'order_id'}
