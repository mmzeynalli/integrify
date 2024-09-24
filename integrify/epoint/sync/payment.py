"""Ödəmə üçün sorğular (sync)"""

from decimal import Decimal
from typing import Optional

from integrify import epoint
from integrify.epoint.schemas.types import (
    EPointBaseResponseSchema,
    EPointMinimalResponseSchema,
    EPointRedirectUrlResponseSchema,
    EPointRedirectUrlWithCardIdResponseSchema,
)
from integrify.epoint.sync.base import EPointRequest

__all__ = ['EPointPaymentRequest', 'EPointPayWithSavedCardRequest', 'EPointPayAndSaveCardRequest']


class EPointPaymentRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    """Ödəniş sorğusu (sync)

    Example:
        >>> EPointPaymentRequest(amount=100, currency='AZN', order_id='12345678',\
            description='Ödəniş')()

    **Cavab formatı**: :class:`EPointRedirectUrlResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
    olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
    APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
    ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
        **extra,
    ):
        """
        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                        geri göndərilir.
        """
        super().__init__()

        self.path = '/api/1/request'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if epoint.EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = epoint.EPOINT_SUCCESS_REDIRECT_URL

        if epoint.EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = epoint.EPOINT_SUCCESS_REDIRECT_URL

        if extra:
            self.data['other_attr'] = extra


class EPointPayWithSavedCardRequest(EPointRequest[EPointBaseResponseSchema]):
    """Yadda saxlanılmış kartla ödəniş sorğusu (sync)

    Example:
        >>> EPointPayWithSavedCardRequest(amount=100, currency='AZN', \
                                            order_id='12345678', card_id='cexxxxxx')()

    Cavab formatı: :class:`EPointBaseResponseSchema`

    Axın:
    -------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq :class:`EPointBaseResponseSchema` formatında
    cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir
    """

    def __init__(self, amount: Decimal, currency: str, order_id: str, card_id: str):
        """
        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
        """
        super().__init__()

        self.path = '/api/1/execute-pay'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
                'card_id': card_id,
            }
        )


class EPointPayAndSaveCardRequest(EPointRequest[EPointRedirectUrlWithCardIdResponseSchema]):
    """Ödəniş və kartı yadda saxlama sorğusu (sync)

    Example:
        >>> EPointPayAndSaveCardRequest(amount=100, currency='AZN', \
                                    order_id='12345678', description='Ödəniş')()

    Cavab formatı: :class:`EPointRedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir. Müştəri həmin URLə
    daxil olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
    APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id` və
    `card_id` ilə :class:`EPointDecodedCallbackDataSchema` formatında məlumat gəlir.
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
    ):
        """
        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """
        super().__init__()

        self.path = '/api/1/card-registration-with-pay'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if epoint.EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = epoint.EPOINT_SUCCESS_REDIRECT_URL

        if epoint.EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = epoint.EPOINT_SUCCESS_REDIRECT_URL


class EPointPayoutRequest(EPointRequest[EPointBaseResponseSchema]):
    """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu (sync)

    Example:
        >>> EPointPayAndSaveCardRequest(amount=100, currency='AZN', \
                                    order_id='12345678', description='Ödəniş')()


    Cavab sorğu formatı: :class:`EPointBaseResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------------
    Bu sorğunu göndərdikdə, əməliyyat Epoint xidməti tərəfindən işləndikdən və bankdan ödəniş
    statusu alındıqdan sonra cavab :class:`EPointBaseResponseSchema` formatında qayıdacaqdır
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        description: Optional[str] = None,
    ):
        super().__init__()

        self.path = '/api/1/refund-request'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
                'card_id': card_id,
            }
        )

        if description:
            self.data['description'] = description


class EPointRefundRequest(EPointRequest[EPointMinimalResponseSchema]):
    """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu (sync)

    Examples:
        >>> EPointRefundRequest(transaction_id='texxxxxx', currency='AZN')()
        >>> EPointRefundRequest(transaction_id='texxxxxx', currency='AZN', amount=50)()

    Cavab formatı: :class:`EPointMinimalResponseSchema`

    Axın:
    -----------------------------------------------------------------
    Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
    Heç bir callback sorğusu göndərilmir.
    """

    def __init__(self, transaction_id: str, currency: str, amount: Optional[Decimal] = None):
        """
        Args:
            transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                            Adətən `te` prefiksi ilə olur.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            amount: Ödəniş məbləği. Məbləğin göndərilməsi yarımçıq geri-qaytarma hesab olunur,
                    əks halda tam geri-qaytarma baş verəcəkdir.
        """
        super().__init__()

        self.path = '/api/1/reverse'
        self.verb = 'POST'

        self.data.update({'transaction': transaction_id, 'currency': currency})

        if amount:
            self.data['amount'] = str(amount)
