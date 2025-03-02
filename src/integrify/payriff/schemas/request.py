from decimal import Decimal
from typing import Optional

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from integrify.payriff import env
from integrify.payriff.schemas.enums import Currency, Language, Operation
from integrify.schemas import PayloadBaseModel


class BaseRequestSchema(PayloadBaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    amount: Decimal
    """Ödəniş miqadrı"""
    language: Language
    """Dil"""
    currency: Currency
    """Məzənnə"""
    description: str
    """Təsvir"""
    callback_url: Optional[str] = env.PAYRIFF_CALLBACK_URL
    """Callback URLi"""
    card_save: Optional[bool] = False
    """Kartı yadda saxlamaq istəyirsinizsə `True` dəyərini verin."""
    operation: Operation
    """Əməliyyat tipi"""


class CreateOrderRequestSchema(BaseRequestSchema): ...
