from decimal import Decimal

from clientaz.epoint import EPOINT_FAILED_REDIRECT_URL, EPOINT_SUCCESS_REDIRECT_URL
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import (
    EPointMinimalResponseSchema,
    EPointPayoutResponseSchema,
    EPointPayWithSavedCardResponseSchema,
    EPointRedirectResponseSchema,
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


class EPointPayAndSaveCardRequest(EPointRequest[EPointRedirectResponseSchema]):
    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        description: str | None = None,
    ):
        super().__init__()

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

        self.path = '/api/1/card-registration-with-pay'
        self.verb = 'POST'


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
    """
    This request class allows you to request a refund for a specific transaction,
    fully or partially.

    Example:
        >>> EPointRefundRequest(transaction_id='1234567', currency='AZN', amount=100)()
    """

    def __init__(self, transaction_id: str, currency: str, amount: Decimal | None = None):
        """
        Args:
            transaction_id: Unique transaction ID of **EPoint side**. Usually starts with 'te'
            currency: 3 letter currency in which refund should be made
            amount: Optional argument: if not specified, full refund will be issued, otherwise,
                    one can issue partial refund by passing this argument.
        """
        super().__init__()

        self.path = '/api/1/reverse'
        self.verb = 'POST'

        self.data.update({'transaction': transaction_id, 'currency': currency})

        if amount:
            self.data['amount'] = str(amount)
