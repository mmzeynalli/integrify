from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.epoint import env
from integrify.epoint.handlers import (
    GetTransactionStatusPayloadHandler,
    PayAndSaveCardPayloadHandler,
    PaymentPayloadHandler,
    PayoutPayloadHandler,
    PayWithSavedCardPayloadHandler,
    RefundPayloadHandler,
    SaveCardPayloadHandler,
    SplitPayAndSaveCardPayloadHandler,
    SplitPayPayloadHandler,
    SplitPayWithSavedCardPayloadHandler,
)
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TransactionStatusResponseSchema,
)

__all__ = ['EPointClientClass']


class EPointClientClass(APIClient):
    """EPoint sorğular üçün baza class"""

    def __init__(self, sync: bool = True):
        super().__init__('EPoint', env.API.BASE_URL, None, sync)

        self.add_url('pay', env.API.PAY)
        self.add_handler('pay', PaymentPayloadHandler)

        self.add_url('get_transaction_status', env.API.GET_STATUS)
        self.add_handler('get_transaction_status', GetTransactionStatusPayloadHandler)

        self.add_url('save_card', env.API.SAVE_CARD)
        self.add_handler('save_card', SaveCardPayloadHandler)

        self.add_url('pay_with_saved_card', env.API.PAY_WITH_SAVED_CARD)
        self.add_handler('pay_with_saved_card', PayWithSavedCardPayloadHandler)

        self.add_url('pay_and_save_card', env.API.PAY_AND_SAVE_CARD)
        self.add_handler('pay_and_save_card', PayAndSaveCardPayloadHandler)

        self.add_url('payout', env.API.PAYOUT)
        self.add_handler('payout', PayoutPayloadHandler)

        self.add_url('refund', env.API.REFUND)
        self.add_handler('refund', RefundPayloadHandler)

        self.add_url('split_pay', env.API.SPLIT_PAY)
        self.add_handler('split_pay', SplitPayPayloadHandler)

        self.add_url('split_pay_with_saved_card', env.API.SPLIT_PAY_WITH_SAVED_CARD)
        self.add_handler('split_pay_with_saved_card', SplitPayWithSavedCardPayloadHandler)

        self.add_url('split_pay_and_save_card', env.API.SPLIT_PAY_AND_SAVE_CARD)
        self.add_handler('split_pay_and_save_card', SplitPayAndSaveCardPayloadHandler)

    def add_url(self, route_name: str, url: str):  # type: ignore[override]
        # All Epoint requests are POST
        return super().add_url(route_name, url, 'POST')

    if TYPE_CHECKING:

        def pay(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[RedirectUrlResponseSchema]:
            """Ödəniş sorğusu

            **Endpoint:** */api/1/request*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
                ```

            **Cavab formatı**: [`RedirectUrlResponseSchema`][integrify.epoint.schemas.response.RedirectUrlResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
            ilə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema]
            formatında məlumat gəlir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
                **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                            geri göndərilir.
            """  # noqa: E501

        def get_transaction_status(
            self,
            transaction_id: str,
        ) -> APIResponse[TransactionStatusResponseSchema]:
            """
            Transaksiya statusunu öyrənmək üçün sorğu

            **Endpoint:** */api/1/get-status*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.get_transaction_status(transaction_id='texxxxxx')
                ```

            Cavab formatı: [`TransactionStatusResponseSchema`][integrify.epoint.schemas.response.TransactionStatusResponseSchema]

            Args:
                transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                                Adətən `te` prefiksi ilə olur.
            """  # noqa: E501

        def save_card(self) -> APIResponse[RedirectUrlWithCardIdResponseSchema]:
            """Ödəniş olmadan kartı yadda saxlamaq sorğusu

            **Endpoint:** */api/1/card-registration*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.save_card()
                ```

            Cavab formatı: [`RedirectUrlWithCardIdResponseSchema`][integrify.epoint.schemas.response.RedirectUrlWithCardIdResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
            Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
            backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
            və eyni `card_id` ilə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema]
            formatında məlumat gəlir.
            """  # noqa: E501

        def pay_with_saved_card(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
        ) -> APIResponse[BaseResponseSchema]:
            """Yadda saxlanılmış kartla ödəniş sorğusu

            **Endpoint:** */api/1/execute-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay_with_saved_card(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx')
                ```

            Cavab formatı: [`BaseResponseSchema`][integrify.epoint.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
            cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
            """  # noqa: E501

        def pay_and_save_card(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Optional[str] = None,
        ) -> APIResponse[RedirectUrlWithCardIdResponseSchema]:
            """Ödəniş və kartı yadda saxlama sorğusu

            **Endpoint:** */api/1/card-registration-with-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay_and_save_card(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
                ```

            Cavab formatı:  [`RedirectUrlWithCardIdResponseSchema`][integrify.epoint.schemas.response.RedirectUrlWithCardIdResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir. Müştəri həmin URLə
            daxil olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id` və
            `card_id` ilə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema]
            formatında məlumat gəlir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def payout(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
            description: Optional[str] = None,
        ) -> APIResponse[BaseResponseSchema]:
            """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu

            **Endpoint:** */api/1/refund-request*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.payout(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx', description='Ödəniş')
                ```

            Cavab sorğu formatı: [`BaseResponseSchema`][integrify.epoint.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, əməliyyat Epoint xidməti tərəfindən işləndikdən və bankdan ödəniş
            statusu alındıqdan sonra cavab `BaseResponseSchema` formatında qayıdacaqdır

            Args:
                amount: Nağdlaşdırmaq miqdarı. Numerik dəyər.
                currency: Nağdlaşdırma məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
                description: Nağdlaşdırmanın təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def refund(
            self,
            transaction_id: str,
            currency: str,
            amount: Optional[Numeric] = None,
        ) -> APIResponse[MinimalResponseSchema]:
            """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu

            **Endpoint:** */api/1/reverse*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                # Full refund
                EPointRequest.refund(transaction_id='texxxxxx', currency='AZN')

                # Partial refund
                EPointRequest.refund(transaction_id='texxxxxx', currency='AZN', amount=50)
                ```

            Cavab formatı: [`MinimalResponseSchema`][integrify.epoint.schemas.response.MinimalResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
            Heç bir callback sorğusu göndərilmir.

            Args:
                transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                                Adətən `te` prefiksi ilə olur.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                amount: Ödəniş məbləği. Məbləğin göndərilməsi yarımçıq geri-qaytarma hesab olunur,
                        əks halda tam geri-qaytarma baş verəcəkdir.
            """  # noqa: E501

        def split_pay(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[RedirectUrlResponseSchema]:
            """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu

            **Endpoint:** */api/1/split-request*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.split_pay(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
                ```

            Cavab formatı: [`RedirectUrlResponseSchema`][integrify.epoint.schemas.response.RedirectUrlResponseSchema]

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

        def split_pay_with_saved_card(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Optional[str] = None,
        ) -> APIResponse[SplitPayWithSavedCardResponseSchema]:
            """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu

            **Endpoint:** */api/1/split-execute-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.split_pay_with_saved_card(amount=100, currency='AZN', order_id='123456789', card_id='cexxxxxx', split_user_id='epoint_user_id', split_amount=50, description='split payment')
                ```

            Cavab formatı: [`SplitPayWithSavedCardResponseSchema`][integrify.epoint.schemas.response.SplitPayWithSavedCardResponseSchema]

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
                split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
                split_amount: Bölünən miqdar. Numerik dəyər
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def split_pay_and_save_card(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Optional[str] = None,
        ) -> APIResponse[RedirectUrlWithCardIdResponseSchema]:
            """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu

            **Endpoint:** */api/1/split-card-registration-with-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.split_pay_and_save_card(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
                ```

            Cavab formatı: [`RedirectUrlWithCardIdResponseSchema`][integrify.epoint.schemas.response.RedirectUrlWithCardIdResponseSchema]

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
                split_amount: Bölünən miqdar. Numerik dəyər
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501


EPointRequest = EPointClientClass(sync=True)
EPointAsyncRequest = EPointClientClass(sync=False)
