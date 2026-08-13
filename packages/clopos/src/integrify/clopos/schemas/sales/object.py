from decimal import Decimal

from integrify.clopos.schemas.common.object import Balance, Media, Timestamp
from integrify.utils import UnsetOrNoneField


class PaymentMethod(Timestamp):
    id: int
    """The unique identifier for the payment method"""

    name: str
    """The name of the payment method (e.g., "Cash", "Card")"""

    customer_required: int
    """Whether a customer must be attached to the transaction (1 for yes, 0 for no)"""

    is_system: int
    """Indicates if it’s a system-default payment method"""

    balance_id: UnsetOrNoneField[int]
    """The ID of the balance associated with the payment method"""

    balance: UnsetOrNoneField[Balance]
    """An object containing details of the associated balance account"""

    service: UnsetOrNoneField[dict]
    """Details of any external service integrated with this payment method"""

    split: UnsetOrNoneField[int]
    """Indicates if this payment method can be used for split payments"""

    status: dict[str, int]
    """Map of venue_id -> 0/1 availability for this method"""


class SaleType(Timestamp):
    id: int
    """The unique identifier for the sale type"""

    name: str
    """The name of the sale type (e.g., "In-store", "Delivery")"""

    system_type: UnsetOrNoneField[str]
    """A system-defined type identifier (e.g., "IN", "DELIVERY")"""

    status: dict[str, int]
    """Map of venue_id -> 0/1 availability for this method"""

    channel: UnsetOrNoneField[str]
    """The channel the sale type belongs to"""

    service_charge_rate: UnsetOrNoneField[Decimal]
    """The service charge rate associated with this sale type"""

    payment_method_id: UnsetOrNoneField[int]
    """The ID of the default payment method for this sale type, if any"""

    position: UnsetOrNoneField[int]
    """The position of the sale type in the list of sale types"""

    payment_method: UnsetOrNoneField[PaymentMethod]
    """An object containing details of the associated payment method"""

    media: UnsetOrNoneField[list[Media]]
    """Media of the sale type"""
