"""Bölmə ilə ödəmə sorğuları (async)"""

from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.types import (
    EPointRedirectUrlResponseSchema,
    EPointRedirectUrlWithCardIdResponseSchema,
    EPointSplitPayWithSavedCardResponseSchema,
)
from clientaz.epoint.sync import split as sync


class EPointSplitPaymentRequest(
    EPointRequest[EPointRedirectUrlResponseSchema],
    sync.EPointSplitPaymentRequest,
):
    """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (async)

    Example:
        >>> await EPointSplitPaymentRequest(amount=100, currency='AZN', order_id='123456789',
        split_user_id='epoint_user_id', split_amount=50, description='split payment')()
    """


class EPointSplitPayWithSavedCardRequest(
    EPointRequest[EPointSplitPayWithSavedCardResponseSchema],
    sync.EPointSplitPayWithSavedCardRequest,
):
    """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (async)

    Example:
        >>> await EPointSplitPayWithSavedCardRequest(amount=100, currency='AZN',
        order_id='123456789', card_id='cexxxxxx', split_user_id='epoint_user_id',
        split_amount=50, description='split payment')()

    Cavab formatı: :class:`EPointSplitPayWithSavedCardResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """


class EPointSplitPayAndSaveCardRequest(
    EPointRequest[EPointRedirectUrlWithCardIdResponseSchema],
    sync.EPointSplitPayAndSaveCardRequest,
):
    """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu (async)

    Example:
        >>> await EPointSplitPayAndSaveCardRequest(amount=100, currency='AZN', order_id='123456789',
            split_user_id='epoint_user_id', split_amount=50, description='split payment')()

    Cavab formatı: :class:`EPointRedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """
