"""Ödəmə üçün sorğular (async)"""

from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import (
    EPointMinimalResponseSchema,
    EPointPayoutResponseSchema,
    EPointPayWithSavedCardResponseSchema,
    EPointRedirectUrlResponseSchema,
)


class EPointPaymentRequest(EPointRequest[EPointDecodedCallbackDataSchema]): ...


class EPointPayWithSavedCardRequest(EPointRequest[EPointPayWithSavedCardResponseSchema]): ...


class EPointPayAndSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]): ...


class EPointPayoutRequest(EPointRequest[EPointPayoutResponseSchema]): ...


class EPointRefundRequest(EPointRequest[EPointMinimalResponseSchema]):
    """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu (async)

    Examples:
        >>> await EPointRefundRequest(transaction_id='texxxxxx', currency='AZN')()
        >>> await EPointRefundRequest(transaction_id='texxxxxx', currency='AZN', amount=50)()

    Cavab sorğu formatı: EPointMinimalResponseSchema

    Axın:
        Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
        Heç bir callback sorğusu göndərilmir.
    """
