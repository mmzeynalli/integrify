from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field

from integrify.kapital import env
from integrify.kapital.schemas.utils import BaseSchema
from integrify.schemas import PayloadBaseModel


class CreateOrderRequestSchema(PayloadBaseModel, BaseSchema):
    amount: Decimal
    currency: str
    description: str
    language: Optional[str] = env.KAPITAL_INTERFACE_LANG
    hpp_redirect_url: Optional[str] = Field(default=env.KAPITAL_REDIRECT_URL)
    type_rid: Optional[str] = Field(default='Order_SMS')
    hpp_cof_capture_purposes: Optional[List[str]] = Field(default=['Cit'])


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
    type_rid: Optional[str] = Field(default='Order_DMS')
    hpp_cof_capture_purposes: Optional[List[str]] = Field(default=['Cit', 'Recurring'])
    aut: Dict[str, str] = Field(default={'purpose': 'AddCard'})


class CreateOrderAndSaveCardRequestSchema(CreateOrderRequestSchema):
    type_rid: Optional[str] = Field(default='Order_SMS')
    aut: Dict[str, str] = Field(default={'purpose': 'AddCard'})


class FullReverseOrderRequestSchema(PayloadBaseModel):
    order_id: str
    phase: str = Field(default='Auth')
    void_kind: str = Field(default='Full', alias='voidKind')

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
    void_kind: str = Field(default='Partial', alias='voidKind')

    URL_PARAM_FIELDS = {'order_id'}
