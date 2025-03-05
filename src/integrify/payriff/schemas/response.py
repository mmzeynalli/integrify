from datetime import datetime
from decimal import Decimal
from typing import Generic, Optional
from uuid import UUID

from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel

from integrify.payriff.schemas.enums import Currency, Operation, ResultCodes
from integrify.payriff.schemas.utils import BaseSchema
from integrify.schemas import PayloadBaseModel
from integrify.utils import _ResponsePayloadType


class BaseResponseSchema(PayloadBaseModel, BaseSchema, Generic[_ResponsePayloadType]):
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
    payload: _ResponsePayloadType
    """Payload"""


class CreateOrderResponseSchema(PayloadBaseModel, BaseSchema):
    order_id: UUID
    """Sifariş ID"""
    payment_url: str
    """Ödəniş URL-i"""
    transaction_id: int
    """Tranzaksiya ID"""


class GetOrderTransactionResponseSchema(PayloadBaseModel, BaseSchema):
    uuid: UUID
    """Tranzaksiya ID"""
    created_date: datetime
    """Tranzaksiya tarixi"""
    status: str
    """Tranzaksiya statusu"""
    channel: str
    """Kanal"""
    channel_type: str = Field(validation_alias='channelType')
    """Kanal tipi"""
    request_rrn: str = Field(validation_alias='requestRrn')
    response_rrn: str = Field(validation_alias='responseRrn')
    pan: str
    """Kart nömrəsi"""
    payment_way: str = Field(validation_alias='paymentWay')
    """Ödəniş səhifəsi"""

    card_details: 'CardDetails'
    """Kart məlumatları"""


class CardDetails(PayloadBaseModel, BaseSchema):
    masked_pan: str = Field(validation_alias='maskedPan')
    """Maskalanmış kart nömrəsi"""
    brand: str
    """Kart markası"""
    card_holder_name: str = Field(validation_alias='cardHolderName')
    """Kart sahibinin adı"""

class GetOrderInfoResponseSchema(PayloadBaseModel, BaseSchema):
    order_id: UUID = Field(validation_alias='orderId')
    """Sifariş ID"""
    amount: Decimal
    """Ödəniş miqadrı"""
    currency_type: Currency = Field(validation_alias='currencyType')
    """Məzənnə"""
    merchant_name: str
    """Sifarişçinin adı"""
    operation_type: Operation = Field(validation_alias='operationType')
    """Əməliyyat tipi"""
    payment_status: str = Field(validation_alias='paymentStatus')
    """Ödəniş statusu"""
    auto: bool
    """Otomatik ödəniş"""
    created_date: datetime
    """Sifariş tarixi"""
    description: str
    """Sifariş təsviri"""
    transactions: list[GetOrderTransactionResponseSchema]



