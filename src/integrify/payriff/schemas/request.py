from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import Field

from integrify.payriff import env
from integrify.payriff.schemas.enums import Currency, Language, Operation
from integrify.payriff.schemas.utils import BaseCamelRequestSchema
from integrify.schemas import PayloadBaseModel


class BaseRequestSchema(PayloadBaseModel, BaseCamelRequestSchema):
    amount: Decimal
    """Ödəniş miqadrı"""
    language: Language = Language.AZ
    """Dil"""
    currency: Currency = Currency.AZN
    """Məzənnə"""
    description: str
    """Təsvir"""
    callback_url: Optional[str] = env.PAYRIFF_CALLBACK_URL
    """Callback URLi"""
    card_save: Optional[bool] = False
    """Kartı yadda saxlamaq istəyirsinizsə `True` dəyərini verin."""
    operation: Operation = Operation.PURCHASE
    """Əməliyyat tipi"""


class CreateOrderRequestSchema(BaseRequestSchema): ...


class GetOrderInfoRequestSchema(PayloadBaseModel):
    URL_PARAM_FIELDS = {'order_id'}
    """URL parametrləri"""
    order_id: UUID
    """Ödənişin ID-si."""


class RefundRequestSchema(PayloadBaseModel):
    amount: Decimal
    """Geri ödəniş miqdarı. Numerik dəyər."""
    order_id: UUID = Field(serialization_alias='orderId')
    """Ödənişin ID-si."""


class CompleteRequestSchema(RefundRequestSchema): ...
