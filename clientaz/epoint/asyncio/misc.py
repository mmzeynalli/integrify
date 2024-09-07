"""Qeyri-ödəniş sorğular (status və kart yadda saxlama) (async)"""

from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import EPointRedirectUrlResponseSchema


class EPointGetTransactionStatusRequest(EPointRequest[EPointDecodedCallbackDataSchema]):
    """Transaksiya statusunu öyrənmək üçün sorğu (async)

    Example:
        >>> await EPointGetTransactionStatusRequest(transaction_id='texxxxxx')()

    Cavab sorğu formatı: EPointDecodedCallbackDataSchema
    """


class EPointSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    """Ödəniş olmadan kartı yadda saxlamaq sorğusu (async)

    Example:
        >>> await EPointSaveCardRequest()()

    Cavab sorğu formatı: EPointRedirectUrlResponseSchema

    Axın:
        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.
    """
