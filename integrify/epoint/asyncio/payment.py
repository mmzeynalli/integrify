"""Ödəmə üçün sorğular (async)"""

from integrify.epoint.asyncio.base import BaseRequest
from integrify.epoint.schemas.types import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
)
from integrify.epoint.sync import payment as sync


class PaymentRequest(
    BaseRequest[RedirectUrlResponseSchema],
    sync.PaymentRequest,
):
    """Ödəniş sorğusu (async)

    Example:
        >>> await PaymentRequest(amount=100, currency='AZN', order_id='12345678',\
        description='Ödəniş')()

    **Cavab formatı**: :class:`RedirectUrlResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
    olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
    APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
    ilə DecodedCallbackDataSchema formatında məlumat gəlir.
    """


class PayWithSavedCardRequest(
    BaseRequest[BaseResponseSchema],
    sync.PayWithSavedCardRequest,
):
    """Yadda saxlanılmış kartla ödəniş sorğusu (async)

    Example:
        >>> await PayWithSavedCardRequest(amount=100, currency='AZN', \
                                            order_id='12345678', card_id='cexxxxxx')()

    Cavab formatı: :class:`BaseResponseSchema`

    Axın:
    -------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq :class:`BaseResponseSchema` formatında
    cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir
    """


class PayAndSaveCardRequest(
    BaseRequest[RedirectUrlWithCardIdResponseSchema],
    sync.PayAndSaveCardRequest,
):
    """Ödəniş və kartı yadda saxlama sorğusu (async)

    Example:
        >>> await PayAndSaveCardRequest(amount=100, currency='AZN', \
                                    order_id='12345678', description='Ödəniş')()

    Cavab formatı: :class:`RedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir. Müştəri həmin URLə
    daxil olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
    APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id` və
    `card_id` ilə :class:`DecodedCallbackDataSchema` formatında məlumat gəlir.
    """


class PayoutRequest(
    BaseRequest[BaseResponseSchema],
    sync.PayoutRequest,
):
    """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu (async)

    Example:
        >>> await PayAndSaveCardRequest(amount=100, currency='AZN', \
                                    order_id='12345678', description='Ödəniş')()


    Cavab sorğu formatı: :class:`BaseResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, əməliyyat Epoint xidməti tərəfindən işləndikdən və bankdan ödəniş
    statusu alındıqdan sonra cavab :class:`BaseResponseSchema` formatında
    qayıdacaqdır.
    """


class RefundRequest(BaseRequest[MinimalResponseSchema], sync.RefundRequest):
    """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu (async)

    Examples:
        >>> await RefundRequest(transaction_id='texxxxxx', currency='AZN')()
        >>> await RefundRequest(transaction_id='texxxxxx', currency='AZN', amount=50)()

    Cavab formatı: :class:`MinimalResponseSchema`

    Axın:
    -----------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
    Heç bir callback sorğusu göndərilmir.
    """
