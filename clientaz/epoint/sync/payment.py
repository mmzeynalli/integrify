from decimal import Decimal

from clientaz.epoint import EPOINT_FAILED_REDIRECT_URL, EPOINT_SUCCESS_REDIRECT_URL
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import (
    EPointMinimalResponseSchema,
    EPointPayoutResponseSchema,
    EPointPayWithSavedCardResponseSchema,
    EPointRedirectUrlResponseSchema,
)
from clientaz.epoint.sync.base import EPointRequest


class EPointPaymentRequest(EPointRequest[EPointDecodedCallbackDataSchema]):
    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        description: str | None = None,
        **extra,
    ):
        super().__init__()

        self.path = '/api/1/request'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = EPOINT_SUCCESS_REDIRECT_URL

        if EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = EPOINT_SUCCESS_REDIRECT_URL

        if extra:
            self.data['other_attr'] = extra


class EPointPayWithSavedCardRequest(EPointRequest[EPointPayWithSavedCardResponseSchema]):
    def __init__(self, amount: Decimal, currency: str, transaction_id: str, card_id: str):
        super().__init__()

        self.path = '/api/1/execute-pay'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
                'card_id': card_id,
            }
        )


class EPointPayAndSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        description: str | None = None,
    ):
        super().__init__()

        self.path = '/api/1/card-registration-with-pay'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = EPOINT_SUCCESS_REDIRECT_URL

        if EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = EPOINT_SUCCESS_REDIRECT_URL


class EPointPayoutRequest(EPointRequest[EPointPayoutResponseSchema]):
    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        card_id: str,
        description: str | None = None,
    ):
        super().__init__()

        self.path = '/api/1/refund-request'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
                'card_id': card_id,
            }
        )

        if description:
            self.data['description'] = description


class EPointRefundRequest(EPointRequest[EPointMinimalResponseSchema]):
    def __init__(self, transaction_id: str, currency: str, amount: Decimal | None = None):
        super().__init__()

        self.path = '/api/1/reverse'
        self.verb = 'POST'

        self.data.update({'transaction': transaction_id, 'currency': currency})

        if amount:
            self.data['amount'] = str(amount)
