from typing import Optional

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from integrify.payriff.schemas.enums import ResultCodes
from integrify.schemas import PayloadBaseModel


class BaseResponseSchema(PayloadBaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    code: ResultCodes
    """Cavab kodu"""
    message: str
    """Cavab mesajı"""
    route: str
    """Route"""
    response_id: str
    """Cavab ID"""
    internal_message: Optional[str] = None
    """Daxili mesaj"""
    payload: dict
    """Payload"""


class CreateOrderMinimalResponseSchema(PayloadBaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    order_id: str
    """Sifariş ID"""
    payment_url: str
    """Ödəniş URL-i"""
    transaction_id: int
    """Tranzaksiya ID"""


class CreateOrderResponseSchema(BaseResponseSchema):
    payload: CreateOrderMinimalResponseSchema
