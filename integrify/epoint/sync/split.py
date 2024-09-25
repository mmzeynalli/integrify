"""Bölmə ilə ödəmə sorğuları (sync)"""

from decimal import Decimal
from typing import Optional

from integrify.epoint import EPOINT_FAILED_REDIRECT_URL, EPOINT_SUCCESS_REDIRECT_URL
from integrify.epoint.schemas.types import (
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
)
from integrify.epoint.sync.base import Request


class SplitPaymentRequest(Request[RedirectUrlResponseSchema]):
    """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (sync)

    Example:
        >>> SplitPaymentRequest(amount=100, currency='AZN', order_id='123456789',
                                                split_user_id='epoint_user_id', split_amount=50,
                                                description='split payment')()

    Cavab formatı: :class:`RedirectUrlResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
        **extra,
    ):
        """
        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
            split_amount: Bölünən miqdar. Numerik dəyər
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                        geri göndərilir.
        """

        super().__init__()

        self.path = '/api/1/split-request'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
                'split_user': split_user_id,
                'split_amount': split_amount,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = EPOINT_SUCCESS_REDIRECT_URL

        if EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = EPOINT_SUCCESS_REDIRECT_URL

        if extra:
            self.data['other_attr'] = extra


class SplitPayWithSavedCardRequest(Request[SplitPayWithSavedCardResponseSchema]):
    """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (sync)

    Example:
        >>> SplitPayWithSavedCardRequest(amount=100, currency='AZN', order_id='123456789',
                                        card_id='cexxxxxx', split_user_id='epoint_user_id',
                                        split_amount=50, description='split payment')()

    Cavab formatı: :class:`SplitPayWithSavedCardResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ):
        """
        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
            split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
            split_amount: Bölünən miqdar. Numerik dəyər
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                        geri göndərilir.
        """
        super().__init__()

        self.path = '/api/1/split-execute-pay'
        self.verb = 'POST'

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
                'card_id': card_id,
                'split_user': split_user_id,
                'split_amount': split_amount,
            }
        )

        # Optional
        if description:
            self.data['description'] = description


class SplitPayAndSaveCardRequest(Request[RedirectUrlWithCardIdResponseSchema]):
    """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu (sync)

    Example:
        >>> SplitPayAndSaveCardRequest(amount=100, currency='AZN', order_id='123456789',
                                                split_user_id='epoint_user_id', split_amount=50,
                                                description='split payment')()

    Cavab formatı: :class:`RedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
    """

    def __init__(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ):
        """
        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
            split_amount: Bölünən miqdar. Numerik dəyər
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """
        super().__init__()

        self.path = '/api/1/split-card-registration-with-pay'
        self.verb = 'POST'

        # Required data
        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
                'split_user': split_user_id,
                'split_amount': split_amount,
            }
        )

        # Optional
        if description:
            self.data['description'] = description

        if EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = EPOINT_SUCCESS_REDIRECT_URL

        if EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = EPOINT_SUCCESS_REDIRECT_URL
