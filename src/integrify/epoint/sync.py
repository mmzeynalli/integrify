import base64
import json
from decimal import Decimal
from typing import Any, Optional

from integrify.base import ApiResponse, SyncApiRequest, send_request
from integrify.epoint import env
from integrify.epoint.helper import generate_signature
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TransactionStatusResponseSchema,
)

__all__ = ['EPointRequest']


class EPointRequestClass(SyncApiRequest):
    """EPoint sorğular üçün baza class"""

    def __init__(self):
        super().__init__('EPoint', env.EPOINT_LOGGER_NAME)
        self.base_url = 'https://epoint.az'
        self.data = {
            'public_key': env.EPOINT_PUBLIC_KEY,
            'language': env.EPOINT_INTERFACE_LANG,
        }

    @send_request
    def pay(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
        **extra: Any,
    ) -> ApiResponse[RedirectUrlResponseSchema]:
        """Ödəniş sorğusu (sync)

        **Endpoint:** */api/1/request*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
            ```

        **Cavab formatı**: `RedirectUrlResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
        olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
        APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
        ilə `DecodedCallbackDataSchema` formatında məlumat gəlir.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                        geri göndərilir.
        """  # noqa: E501
        self.path = env.API.PAY
        self.verb = 'POST'
        self.resp_model = RedirectUrlResponseSchema

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

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if extra:
            self.data['other_attr'] = extra

    @send_request
    def get_transaction_status(  # type: ignore[return]
        self,
        transaction_id: str,
    ) -> ApiResponse[TransactionStatusResponseSchema]:
        """
        Transaksiya statusunu öyrənmək üçün sorğu (sync)

        **Endpoint:** */api/1/get-status*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.get_transaction_status(transaction_id='texxxxxx')
            ```

        Cavab formatı: `TransactionStatusResponseSchema`

        Args:
            transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                            Adətən `te` prefiksi ilə olur.
        """
        self.verb = 'POST'
        self.path = env.API.GET_STATUS
        self.data['transaction'] = transaction_id
        self.resp_model = TransactionStatusResponseSchema

    @send_request
    def save_card(self) -> ApiResponse[RedirectUrlWithCardIdResponseSchema]:  # type: ignore[return]
        """Ödəniş olmadan kartı yadda saxlamaq sorğusu (sync)

        **Endpoint:** */api/1/card-registration*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.save_card()
            ```

        Cavab formatı: `RedirectUrlWithCardIdResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə `DecodedCallbackDataSchema` formatında məlumat gəlir.
        """
        self.path = env.API.CARD_REGISTRATION
        self.verb = 'POST'
        self.resp_model = RedirectUrlWithCardIdResponseSchema

    @send_request
    def pay_with_saved_card(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
    ) -> ApiResponse[BaseResponseSchema]:
        """Yadda saxlanılmış kartla ödəniş sorğusu (sync)

        **Endpoint:** */api/1/execute-pay*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.pay_with_saved_card(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx')
            ```

        Cavab formatı: `BaseResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
        cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
        """  # noqa: E501
        self.path = env.API.PAY_WITH_CARD
        self.verb = 'POST'
        self.resp_model = BaseResponseSchema

        self.data.update(
            {
                'amount': amount,
                'currency': currency,
                'order_id': order_id,
                'card_id': card_id,
            }
        )

    @send_request
    def pay_and_save_card(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
    ) -> ApiResponse[RedirectUrlWithCardIdResponseSchema]:
        """Ödəniş və kartı yadda saxlama sorğusu (sync)

        **Endpoint:** */api/1/card-registration-with-pay*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.pay_and_save_card(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
            ```

        Cavab formatı: `RedirectUrlWithCardIdResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir. Müştəri həmin URLə
        daxil olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
        APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id` və
        `card_id` ilə `DecodedCallbackDataSchema` formatında məlumat gəlir.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """  # noqa: E501
        self.path = env.API.PAY_AND_SAVE_CARD
        self.verb = 'POST'
        self.resp_model = RedirectUrlWithCardIdResponseSchema

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

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = env.EPOINT_SUCCESS_REDIRECT_URL

    @send_request
    def payout(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        description: Optional[str] = None,
    ) -> ApiResponse[BaseResponseSchema]:
        """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu (sync)

        **Endpoint:** */api/1/refund-request*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.payout(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
            ```

        Cavab sorğu formatı: `BaseResponseSchema`

        Bu sorğunu göndərdikdə, əməliyyat Epoint xidməti tərəfindən işləndikdən və bankdan ödəniş
        statusu alındıqdan sonra cavab `BaseResponseSchema` formatında qayıdacaqdır

        Args:
            amount: Nağdlaşdırmaq miqdarı. Numerik dəyər.
            currency: Nağdlaşdırma məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
            description: Nağdlaşdırmanın təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """  # noqa: E501
        self.path = env.API.PAYOUT
        self.verb = 'POST'
        self.resp_model = BaseResponseSchema

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

    @send_request
    def refund(  # type: ignore[return]
        self,
        transaction_id: str,
        currency: str,
        amount: Optional[Decimal] = None,
    ) -> ApiResponse[MinimalResponseSchema]:
        """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu (sync)

        **Endpoint:** */api/1/reverse*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            # Full refund
            EPointRequest.refund(transaction_id='texxxxxx', currency='AZN')

            # Partial refund
            EPointRequest.refund(transaction_id='texxxxxx', currency='AZN', amount=50)
            ```

        Cavab formatı: `MinimalResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
        Heç bir callback sorğusu göndərilmir.

        Args:
            transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                            Adətən `te` prefiksi ilə olur.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            amount: Ödəniş məbləği. Məbləğin göndərilməsi yarımçıq geri-qaytarma hesab olunur,
                    əks halda tam geri-qaytarma baş verəcəkdir.
        """
        self.path = env.API.REFUND
        self.verb = 'POST'
        self.resp_model = MinimalResponseSchema

        self.data.update({'transaction': transaction_id, 'currency': currency})

        if amount:
            self.data['amount'] = str(amount)

    @send_request
    def split_pay(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
        **extra: Any,
    ) -> ApiResponse[RedirectUrlResponseSchema]:
        """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (sync)

        **Endpoint:** */api/1/split-request*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.split_pay(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
            ```

        Cavab formatı: `RedirectUrlResponseSchema`

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
            split_amount: Bölünən miqdar. Numerik dəyər
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                        geri göndərilir.
        """  # noqa: E501
        self.path = env.API.SPLIT_PAY
        self.verb = 'POST'
        self.resp_model = RedirectUrlResponseSchema

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

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if extra:
            self.data['other_attr'] = extra

    @send_request
    def split_pay_with_saved_card(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ) -> ApiResponse[SplitPayWithSavedCardResponseSchema]:
        """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (sync)

        **Endpoint:** */api/1/split-execute-pay*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.split_pay_with_saved_card(amount=100, currency='AZN', order_id='123456789', card_id='cexxxxxx', split_user_id='epoint_user_id', split_amount=50, description='split payment')
            ```

        Cavab formatı: `SplitPayWithSavedCardResponseSchema`

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
            split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
            split_amount: Bölünən miqdar. Numerik dəyər
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """  # noqa: E501
        self.path = env.API.SPLIT_PAY_WITH_SAVED_CARD
        self.verb = 'POST'
        self.resp_model = SplitPayWithSavedCardResponseSchema

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

    @send_request
    def split_pay_and_save_card(  # type: ignore[return]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ) -> ApiResponse[RedirectUrlWithCardIdResponseSchema]:
        """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu (sync)

        **Endpoint:** */api/1/split-card-registration-with-pay*

        Example:
            ```python
            from integrify.epoint import EPointRequest

            EPointRequest.split_pay_and_save_card(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
            ```

        Cavab formatı: `RedirectUrlWithCardIdResponseSchema`

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
            split_amount: Bölünən miqdar. Numerik dəyər
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
        """  # noqa: E501
        self.path = env.API.SPLIT_PAY_AND_SAVE_CARD
        self.verb = 'POST'
        self.resp_model = RedirectUrlWithCardIdResponseSchema

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

        if env.EPOINT_SUCCESS_REDIRECT_URL:
            self.data['success_redirect_url'] = env.EPOINT_SUCCESS_REDIRECT_URL

        if env.EPOINT_FAILED_REDIRECT_URL:
            self.data['error_redirect__url'] = env.EPOINT_SUCCESS_REDIRECT_URL

    def __call__(self, *args, **kwargs):
        b64data = base64.b64encode(json.dumps(self.data).encode()).decode()
        self.body = {
            'data': b64data,
            'signature': generate_signature(b64data),
        }
        return super().__call__(*args, **kwargs)


EPointRequest = EPointRequestClass()
