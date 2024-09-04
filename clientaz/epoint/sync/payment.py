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
    EPointRefundRequest is a class used to send a refund request via the EPoint API.

    This class allows you to request a refund for a specific transaction,
    including the currency used in the transaction and optionally the amount to be refunded.

    Usage:
    ```python
    >>> EPointRefundRequest(transaction_id='1234567',currency='AZN',amount=100)() :
    ```


    **Parameters:**

    * **transaction_id** - *(str)* The unique ID of the transaction to be refunded
    * **currency** - *(str)* The currency to be refunded (for example, 'USD', 'AZN').
    * **amount** - *(Decimal | None)* The amount to be refunded. If not specified,
    a full refund is made.

    **Methods:**
    * __init__: Creates an instance of the EPointRefundRequest class, prepares the necessary data,
    and configures the refund request.
    * __call__: Sends the configured refund request to
    the EPoint API and processes the response from the API.
    """

    def __init__(self, transaction_id: str, currency: str, amount: Decimal | None):
        super().__init__()

        self.path = '/api/1/reverse'
        self.verb = 'POST'

        self.data.update({'transaction': transaction_id, 'currency': currency})

        if amount:
            self.data['amount'] = str(amount)
