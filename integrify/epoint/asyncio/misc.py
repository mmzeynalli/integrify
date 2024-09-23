"""Qeyri-ödəniş sorğular (status və kart yadda saxlama) (async)"""

from integrify.epoint.asyncio.base import EPointRequest
from integrify.epoint.schemas.types import (
    EPointRedirectUrlWithCardIdResponseSchema,
    EPointTransactionStatusResponseSchema,
)


class EPointGetTransactionStatusRequest(EPointRequest[EPointTransactionStatusResponseSchema]):
    """Transaksiya statusunu öyrənmək üçün sorğu (async)

    Example:
        >>> await EPointGetTransactionStatusRequest(transaction_id='texxxxxx')()

    Cavab formatı: :class:`EPointTransactionStatusResponseSchema`
    """


class EPointSaveCardRequest(EPointRequest[EPointRedirectUrlWithCardIdResponseSchema]):
    """Ödəniş olmadan kartı yadda saxlamaq sorğusu (async)

    Example:
        >>> await EPointSaveCardRequest()()

    Cavab formatı: :class:`EPointRedirectUrlWithCardIdResponseSchema`

    Axın:
        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.
    """
