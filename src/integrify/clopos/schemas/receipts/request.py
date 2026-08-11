from decimal import Decimal

from pydantic import BaseModel

from integrify.clopos.helpers import IsoDateTime
from integrify.clopos.schemas.common.request import ByIDRequest, PaginatedDataRequest
from integrify.clopos.schemas.enums import OrderStatus
from integrify.utils import UnsetField


class PaymentMethodIn(BaseModel):
    id: int
    """The unique identifier for the payment method"""

    name: str
    """The name of the payment method (e.g., "Cash", "Card")"""

    amount: Decimal
    """The amount paid via this payment method"""


class GetReceiptsRequest(PaginatedDataRequest):
    sort_by: UnsetField[str]
    sort_order: UnsetField[int]
    date_from: UnsetField[IsoDateTime]
    date_to: UnsetField[IsoDateTime]


class UpdateClosedReceiptRequest(ByIDRequest):
    order_status: UnsetField[OrderStatus]
    order_number: UnsetField[str]
    fiscal_id: UnsetField[str]
    lock: UnsetField[bool]


class CloseReceiptRequest(ByIDRequest):
    id: int
    cid: str
    payment_methods: list[PaymentMethodIn]
    closed_at: IsoDateTime = ''
