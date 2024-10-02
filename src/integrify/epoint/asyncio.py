import base64
import json
from decimal import Decimal
from typing import Any, Coroutine, Optional

from integrify.base import ApiResponse, AsyncApiRequest
from integrify.epoint.helper import generate_signature
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TransactionStatusResponseSchema,
)
from integrify.epoint.sync import EPointRequestClass as SyncEPointRequest

__all__ = ['EPointRequest']


class EPointRequestClass(AsyncApiRequest, SyncEPointRequest):
    """EPoint async sorğular üçün baza class"""

    async def pay(  # type: ignore[override]
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: str | None = None,
        **extra: Any,
    ) -> Coroutine[Any, Any, ApiResponse[RedirectUrlResponseSchema]]:
        """Ödəniş sorğusu (async)

        **Endpoint:** */api/1/request*

        Example:
        ```python
        await EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
        ```

        **Cavab formatı**: `RedirectUrlResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
        olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
        APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
        ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.

        Args:
            amount: Ödəniş miqdarı. Numerik dəyər.
            currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
            order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
            description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                        geri göndərilir.
        """  # noqa: E501
        return await super().pay(amount, currency, order_id, description, **extra)  # type: ignore[misc]

    async def get_transaction_status(
        self,
        transaction_id: str,
    ) -> Coroutine[Any, Any, ApiResponse[TransactionStatusResponseSchema]]:
        """
        Transaksiya statusunu öyrənmək üçün sorğu (async)

        **Endpoint:** */api/1/get-status*

        Example:
        ```python
        await EPointRequest.get_transaction_status(transaction_id='texxxxxx')
        ```

        Cavab formatı: `TransactionStatusResponseSchema`

        Args:
            transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                            Adətən `te` prefiksi ilə olur.
        """
        return await super().get_transaction_status(transaction_id)

    async def save_card(
        self,
    ) -> Coroutine[Any, Any, ApiResponse[RedirectUrlWithCardIdResponseSchema]]:
        """Ödəniş olmadan kartı yadda saxlamaq sorğusu (async)

        **Endpoint:** */api/1/card-registration*

        Example:
        ```python
        await EPointRequest.save_card()
        ```

        Cavab formatı: `RedirectUrlWithCardIdResponseSchema`

        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə `DecodedCallbackDataSchema` formatında məlumat gəlir.
        """
        return await super().save_card()

    async def pay_with_saved_card(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
    ) -> Coroutine[Any, Any, ApiResponse[BaseResponseSchema]]:
        """Yadda saxlanılmış kartla ödəniş sorğusu (async)

        **Endpoint:** */api/1/execute-pay*

        Example:
        ```python
        await EPointRequest.pay_with_saved_card(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx')
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
        return await super().pay_with_saved_card(amount, currency, order_id, card_id)

    async def pay_and_save_card(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        description: Optional[str] = None,
    ) -> Coroutine[Any, Any, ApiResponse[RedirectUrlWithCardIdResponseSchema]]:
        """Ödəniş və kartı yadda saxlama sorğusu (async)

        **Endpoint:** */api/1/card-registration-with-pay*

        Example:
        ```python
        await EPointRequest.pay_and_save_card(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
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
        return await super().pay_and_save_card(amount, currency, order_id, description)

    async def payout(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        description: Optional[str] = None,
    ) -> Coroutine[Any, Any, ApiResponse[BaseResponseSchema]]:
        """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu (async)

        **Endpoint:** */api/1/refund-request*

        Example:
        ```python
        await EPointRequest.payout(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
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
        return await super().payout(amount, currency, order_id, card_id, description)

    async def refund(
        self,
        transaction_id: str,
        currency: str,
        amount: Optional[Decimal] = None,
    ) -> Coroutine[Any, Any, ApiResponse[MinimalResponseSchema]]:
        """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu (async)

        **Endpoint:** */api/1/reverse*

        Examples:
        ```python
        # Full refund
        await EPointRequest.refund(transaction_id='texxxxxx', currency='AZN')

        # Partial refund
        await EPointRequest.refund(transaction_id='texxxxxx', currency='AZN', amount=50)
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
        return await super().refund(transaction_id, currency, amount)

    async def split_pay(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
        **extra: Any,
    ) -> Coroutine[Any, Any, ApiResponse[RedirectUrlResponseSchema]]:
        """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (async)

        **Endpoint:** */api/1/split-request*

        Example:
        ```python
        await EPointRequest.split_pay(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
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
        return await super().split_pay(
            amount,
            currency,
            order_id,
            split_user_id,
            split_amount,
            description,
            **extra,
        )

    async def split_pay_with_saved_card(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        card_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ) -> Coroutine[Any, Any, ApiResponse[SplitPayWithSavedCardResponseSchema]]:
        """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu (async)

        **Endpoint:** */api/1/split-execute-pay*

        Example:
        ```python
        await EPointRequest.split_pay_with_saved_card(amount=100, currency='AZN', order_id='123456789', card_id='cexxxxxx', split_user_id='epoint_user_id', split_amount=50, description='split payment')
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
        return super().split_pay_with_saved_card(
            amount,
            currency,
            order_id,
            card_id,
            split_user_id,
            split_amount,
            description,
        )

    async def split_pay_and_save_card(
        self,
        amount: Decimal,
        currency: str,
        order_id: str,
        split_user_id: str,
        split_amount: Decimal,
        description: Optional[str] = None,
    ) -> Coroutine[Any, Any, ApiResponse[RedirectUrlWithCardIdResponseSchema]]:
        """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu (sync)

        **Endpoint:** */api/1/split-card-registration-with-pay*

        Example:
        ```python
        await EPointRequest.split_pay_and_save_card(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
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
        return super().split_pay_and_save_card(
            amount,
            currency,
            order_id,
            split_user_id,
            split_amount,
            description,
        )

    async def __call__(self, *args, **kwargs):
        b64data = base64.b64encode(json.dumps(self.data).encode()).decode()
        self.body = {
            'data': b64data,
            'signature': generate_signature(b64data),
        }
        return await super().__call__(*args, **kwargs)


EPointRequest = EPointRequestClass()
