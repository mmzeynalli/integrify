from clientaz.epoint.schemas.data import PaymentWithSavedCardSchema
from clientaz.epoint.schemas.response import EPointPayWithSavedCardResponseSchema
from clientaz.epoint.sync.base import EPointRequest


class EPointPayWithSavedCardRequest(EPointRequest[EPointPayWithSavedCardResponseSchema]):
    def __init__(self, transaction: PaymentWithSavedCardSchema):
        super().__init__()

        self.path = '/api/1/execute-pay'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': transaction.amount,
                'currency': transaction.currency,
                'order_id': transaction.uuid,
                'card_id': transaction.saved_card_id,
            }
        )
