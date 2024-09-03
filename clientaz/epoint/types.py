from decimal import Decimal
from typing import Protocol


class PaymentTransactionWithCardData(Protocol):
    amount: Decimal
    currency: str
    id: str
    card_id: str
