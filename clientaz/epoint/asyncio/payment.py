"""Ödəmə üçün sorğular (async)"""

from clientaz.epoint.asyncio.base import EPointRequest
from clientaz.epoint.schemas.types import (
    EPointBaseResponseSchema,
    EPointMinimalResponseSchema,
    EPointRedirectUrlResponseSchema,
    EPointRedirectUrlWithCardIdResponseSchema,
)
from clientaz.epoint.sync import payment as sync


class EPointPaymentRequest(
    EPointRequest[EPointRedirectUrlResponseSchema],
    sync.EPointPaymentRequest,
):
    """Ödəniş sorğusu (async)

    Example:
        >>> await EPointPaymentRequest(amount=100, currency='AZN', order_id='12345678',\
        description='Ödəniş')()

    **Cavab formatı**: :class:`EPointRedirectUrlResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
    olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
    APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
    ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.
    """


class EPointPayWithSavedCardRequest(
    EPointRequest[EPointBaseResponseSchema],
    sync.EPointPayWithSavedCardRequest,
):
    """Yadda saxlanılmış kartla ödəniş sorğusu (async)

    Example:
        >>> await EPointPayWithSavedCardRequest(amount=100, currency='AZN', \
                                            order_id='12345678', card_id='cexxxxxx')()

    Cavab formatı: :class:`EPointBaseResponseSchema`

    Axın:
    -------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq :class:`EPointBaseResponseSchema` formatında
    cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir
    """


class EPointPayAndSaveCardRequest(
    EPointRequest[EPointRedirectUrlWithCardIdResponseSchema],
    sync.EPointPayAndSaveCardRequest,
):
    """Ödəniş və kartı yadda saxlama sorğusu (async)

    Example:
        >>> await EPointPayAndSaveCardRequest(amount=100, currency='AZN', \
                                    order_id='12345678', description='Ödəniş')()

    Cavab formatı: :class:`EPointRedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir. Müştəri həmin URLə
    daxil olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
    APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id` və
    `card_id` ilə :class:`EPointDecodedCallbackDataSchema` formatında məlumat gəlir.
    """


class EPointPayoutRequest(
    EPointRequest[EPointBaseResponseSchema],
    sync.EPointPayoutRequest,
):
    """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu (async)

    Example:
        >>> await EPointPayAndSaveCardRequest(amount=100, currency='AZN', \
                                    order_id='12345678', description='Ödəniş')()


    Cavab sorğu formatı: :class:`EPointBaseResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, əməliyyat Epoint xidməti tərəfindən işləndikdən və bankdan ödəniş
    statusu alındıqdan sonra cavab :class:`EPointBaseResponseSchema` formatında
    qayıdacaqdır.
    """


class EPointRefundRequest(EPointRequest[EPointMinimalResponseSchema], sync.EPointRefundRequest):
    """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu (async)

    Examples:
        >>> await EPointRefundRequest(transaction_id='texxxxxx', currency='AZN')()
        >>> await EPointRefundRequest(transaction_id='texxxxxx', currency='AZN', amount=50)()

    Cavab formatı: :class:`EPointMinimalResponseSchema`

    Axın:
    -----------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
    Heç bir callback sorğusu göndərilmir.
    """
