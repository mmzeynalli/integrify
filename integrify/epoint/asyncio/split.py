"""Bölmə ilə ödəmə sorğuları (async)"""

from integrify.epoint.asyncio.base import Request
from integrify.epoint.schemas.types import (
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
)
from integrify.epoint.sync import split as sync


class SplitPaymentRequest(
    Request[RedirectUrlResponseSchema],
    sync.SplitPaymentRequest,
):
    """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (async)

    Example:
        >>> await SplitPaymentRequest(amount=100, currency='AZN', order_id='123456789',
        split_user_id='epoint_user_id', split_amount=50, description='split payment')()
    """


class SplitPayWithSavedCardRequest(
    Request[SplitPayWithSavedCardResponseSchema],
    sync.SplitPayWithSavedCardRequest,
):
    """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (async)

    Example:
        >>> await SplitPayWithSavedCardRequest(amount=100, currency='AZN',
        order_id='123456789', card_id='cexxxxxx', split_user_id='epoint_user_id',
        split_amount=50, description='split payment')()

    Cavab formatı: :class:`SplitPayWithSavedCardResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """


class SplitPayAndSaveCardRequest(
    Request[RedirectUrlWithCardIdResponseSchema],
    sync.SplitPayAndSaveCardRequest,
):
    """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu (async)

    Example:
        >>> await SplitPayAndSaveCardRequest(amount=100, currency='AZN', order_id='123456789',
            split_user_id='epoint_user_id', split_amount=50, description='split payment')()

    Cavab formatı: :class:`RedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """
