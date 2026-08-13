from typing import Literal

from integrify.api import PayloadBaseModel
from integrify.clopos.schemas.common.request import ByIDRequest, PaginatedDataRequest
from integrify.clopos.schemas.enums import OrderStatus
from integrify.clopos.schemas.orders.object import OrderPayloadIn
from integrify.utils import UnsetField


class GetOrdersRequest(PaginatedDataRequest):
    status: UnsetField[OrderStatus]


class GetOrderByIDRequest(ByIDRequest):
    with_: UnsetField[Literal['receipt:id', 'service_notification_id', 'status']]


class CreateOrderRequest(PayloadBaseModel):
    model_config = {'extra': 'allow'}

    customer_id: int
    """Customer identifier"""

    payload: OrderPayloadIn
    """List of order items"""

    meta: UnsetField[dict]
    """Order meta data"""


class UpdateOrderRequest(ByIDRequest):
    status: OrderStatus
