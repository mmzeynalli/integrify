from decimal import Decimal

from integrify.kapitalbank import env
from integrify.kapitalbank.schemas.utils import BaseSchema
from integrify.schemas import PayloadBaseModel
from pydantic import Field


class CreateOrderRequestSchema(PayloadBaseModel, BaseSchema):
    amount: Decimal
    currency: str
    description: str
    language: str | None = env.KAPITAL_INTERFACE_LANG
    hpp_redirect_url: str | None = Field(default=env.KAPITAL_REDIRECT_URL)
    type_rid: str | None = Field(default='Order_SMS')
    hpp_cof_capture_purposes: list[str] | None = Field(default=['Cit'])


class OrderInformationRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id'}

    order_id: int


class RefundOrderRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id'}

    order_id: int
    amount: Decimal
    phase: str = Field(default='Single')
    type: str = Field(default='Refund')


class SaveCardRequestSchema(CreateOrderRequestSchema):
    type_rid: str | None = Field(default='Order_DMS')
    hpp_cof_capture_purposes: list[str] | None = Field(default=['Cit', 'Recurring'])
    aut: dict[str, str] = Field(default={'purpose': 'AddCard'})


class PayAndSaveCardRequestSchema(CreateOrderRequestSchema):
    type_rid: str | None = Field(default='Order_SMS')
    aut: dict[str, str] = Field(default={'purpose': 'AddCard'})


class FullReverseOrderRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id'}

    order_id: int
    phase: str = Field(default='Auth')
    void_kind: str = Field(default='Full', serialization_alias='voidKind')


class ClearingOrderRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id'}

    order_id: int
    amount: Decimal
    phase: str = Field(default='Clearing')


class PartialReverseOrderRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id'}

    order_id: int
    amount: Decimal
    phase: str = Field(default='Single')
    void_kind: str = Field(default='Partial', serialization_alias='voidKind')


class OrderWithSavedCardRequestSchema(CreateOrderRequestSchema):
    type_rid: str | None = Field(default='Order_REC')
    hpp_redirect_url: None = None
    hpp_cof_capture_purposes: None = None


class LinkCardTokenRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id', 'password'}

    token: int
    order_id: int
    password: str


class ProcessPaymentWithSavedCardRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id', 'password'}

    amount: Decimal
    order_id: int
    password: str
    phase: str | None = Field(default='Single')
    conditions: dict[str, str] | None = Field(default={'cofUsage': 'Cit'})
