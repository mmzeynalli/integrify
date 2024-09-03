from decimal import Decimal

from pydantic import BaseModel


class PaymentWithSavedCardSchema(BaseModel):
    amount: Decimal
    currency: str
    uuid: str
    saved_card_id: str
