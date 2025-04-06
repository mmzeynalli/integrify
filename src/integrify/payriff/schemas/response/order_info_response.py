from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from integrify.payriff.schemas.enums import Currency, Operation
from integrify.payriff.schemas.utils import BaseCamelResponseSchema
from integrify.schemas import PayloadBaseModel


class GetOrderInfoResponseSchema(PayloadBaseModel, BaseCamelResponseSchema):
    order_id: UUID
    """Sifariş ID"""
    amount: Decimal
    """Ödəniş miqadrı"""
    currency_type: Currency
    """Məzənnə"""
    merchant_name: str
    """Sifarişçinin adı"""
    operation_type: Operation
    """Əməliyyat tipi"""
    payment_status: str
    """Ödəniş statusu"""
    auto: bool
    """Otomatik ödəniş"""
    created_date: datetime
    """Sifariş tarixi"""
    description: str
    """Sifariş təsviri"""
    transactions: Optional[list['GetOrderTransactionResponseSchema']] = None
    """Tranzaksiyalar"""


class GetOrderTransactionResponseSchema(BaseCamelResponseSchema):
    uuid: UUID
    """Tranzaksiya ID"""
    created_date: datetime
    """Tranzaksiya tarixi"""
    status: str
    """Tranzaksiya statusu"""
    channel: str
    """Tranzaksiya kanalı(bank)"""
    channel_type: Optional[str] = None
    """Kanal tipi"""
    request_rrn: str
    response_rrn: str
    pan: str
    """Kart nömrəsi"""
    payment_way: str
    """Ödəniş səhifəsi"""
    card_details: 'CardDetails'
    """Kart məlumatları"""
    merchant_category: Optional[str] = None
    """Sifarişçi kateqoriyası"""
    installment: Optional['Installment'] = None
    """Taksit məlumatları"""


class CardDetails(BaseCamelResponseSchema):
    masked_pan: str
    """Maskalanmış kart nömrəsi"""
    brand: str
    """Kart markası"""
    card_holder_name: str
    """Kart sahibinin adı"""


class Installment(BaseCamelResponseSchema):
    type: Optional[str] = None
    period: Optional[str] = None
