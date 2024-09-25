"""Qeyri-ödəniş sorğular (status və kart yadda saxlama) (async)"""

from integrify.epoint.asyncio.base import BaseRequest
from integrify.epoint.schemas.types import (
    RedirectUrlWithCardIdResponseSchema,
    TransactionStatusResponseSchema,
)


class GetTransactionStatusRequest(BaseRequest[TransactionStatusResponseSchema]):
    """Transaksiya statusunu öyrənmək üçün sorğu (async)

    Example:
        >>> await GetTransactionStatusRequest(transaction_id='texxxxxx')()

    Cavab formatı: :class:`TransactionStatusResponseSchema`
    """


class SaveCardRequest(BaseRequest[RedirectUrlWithCardIdResponseSchema]):
    """Ödəniş olmadan kartı yadda saxlamaq sorğusu (async)

    Example:
        >>> await SaveCardRequest()()

    Cavab formatı: :class:`RedirectUrlWithCardIdResponseSchema`

    Axın:
        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə DecodedCallbackDataSchema formatında məlumat gəlir.
    """
