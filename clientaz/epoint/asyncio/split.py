from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.response import (
    EPointRedirectUrlResponseSchema,
    EPointSplitPayWithSavedCardResponseSchema,
)


class EPointSplitPaymentRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    """
    This request class is used to split the bill with another EPoint user (async).

    Example:
        >>> await EPointSplitPaymentRequest(amount=100, currency='AZN', transaction_id='123456789',
                                        split_user_id='epoint_user_id', split_amount=50,
                                        description='split payment')()
    """


class EPointSplitPayWithSavedCardRequest(
    EPointRequest[EPointSplitPayWithSavedCardResponseSchema]
): ...


class EPointSplitPayAndSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]): ...
