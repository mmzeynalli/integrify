from decimal import Decimal

from clientaz.epoint import EPOINT_FAILED_REDIRECT_URL, EPOINT_SUCCESS_REDIRECT_URL
from clientaz.epoint.schemas.response import (
    EPointRedirectUrlResponseSchema,
    EPointSplitPayWithSavedCardResponseSchema,
)
from clientaz.epoint.sync.base import EPointRequest


class EPointSplitPaymentRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    """
    This request class is used to split the bill with another EPoint user.

    Example:
        >>> EPointSplitPaymentRequest(amount=100, currency='AZN', transaction_id='123456789',
                                        split_user_id='epoint_user_id', split_amount=50,
                                        description='split payment')
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: str | None = None,
        **extra,
    ):
        """Args:
        amount: Total amount of payment
        currency: 3 letter currency in which refund should be made
        transaction_id: Unique identifier of transaction on server side
        split_user_id: **EPoint** user id for split payment
        split_amount: splitted amount
        description: Optional descriptiton of transaction
        extra: Optional extra data you want to pass to request, which will be returned in callback
        """
        super().__init__()

        self.path = '/api/1/split-request'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
                'split_user': split_user_id,
                'split_amount': split_amount,
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


class EPointSplitPayWithSavedCardRequest(EPointRequest[EPointSplitPayWithSavedCardResponseSchema]):
    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        card_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: str | None = None,
    ):
        super().__init__()

        self.path = '/api/1/split-execute-pay'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
                'card_id': card_id,
                'split_user': split_user_id,
                'split_amount': split_amount,
            }
        )

        # Optional
        if description:
            self.data['description'] = description


class EPointSplitPayAndSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    def __init__(
        self,
        amount: Decimal,
        currency: str,
        transaction_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: str | None = None,
    ):
        super().__init__()

        self.path = '/api/1/split-card-registration-with-pay'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': transaction_id,
                'split_user': split_user_id,
                'split_amount': split_amount,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = EPOINT_SUCCESS_REDIRECT_URL

        if EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = EPOINT_SUCCESS_REDIRECT_URL
