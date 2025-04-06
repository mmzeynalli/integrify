from uuid import UUID

from integrify.payriff.schemas.utils import BaseCamelResponseSchema
from integrify.schemas import PayloadBaseModel


class CreateOrderResponseSchema(PayloadBaseModel, BaseCamelResponseSchema):
    order_id: UUID
    """Sifariş ID"""
    payment_url: str
    """Ödəniş URL-i"""
    transaction_id: int
    """Tranzaksiya ID"""
