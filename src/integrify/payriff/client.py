from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from integrify.api import APIClient
from integrify.payriff import env
from integrify.payriff.handlers import (
    CompletePayloadHandler,
    CreateOrderPayloadHandler,
    GetOrderInfoPayloadHandler,
    RefundPayloadHandler,
)
from integrify.payriff.schemas.enums import Currency, Language, Operation
from integrify.payriff.schemas.response import (
    BaseResponseSchema,
    CreateOrderResponseSchema,
    GetOrderInfoResponseSchema,
    RefundResponseSchema,
)
from integrify.schemas import APIResponse


class PayriffClientClass(APIClient):
    def __init__(
        self,
        name='Payriff',
        base_url=env.API.BASE_URL,
        default_handler=None,
        sync=True,
        dry=False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url('create_order', env.API.CREATE_ORDER, verb='POST')
        self.add_handler('create_order', CreateOrderPayloadHandler)

        self.add_url('get_order_info', env.API.GET_ORDER, verb='GET')
        self.add_handler('get_order_info', GetOrderInfoPayloadHandler)

        self.add_url('refund', env.API.REFUND, verb='POST')
        self.add_handler('refund', RefundPayloadHandler)

        self.add_url('complete', env.API.COMPLETE, verb='POST')
        self.add_handler('complete', CompletePayloadHandler)

    if TYPE_CHECKING:

        def create_order(
            self,
            amount: Decimal,
            description: str,
            language: Language = Language.AZ,
            currency: Currency = Currency.AZN,
            callback_url: Optional[str] = None,
            card_save: Optional[bool] = False,
            operation: Operation = Operation.PURCHASE,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Ödəniş sorğusu

            **Endpoint** /api/order

            Example:
            ```python
            from integrify.payriff import PayriffClient

            PayriffClient.create_order(
                amount=10.0,
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.payriff.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `payment_url` gəlir. Müştəri həmin URLə daxil olub,
            kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback APIsinə
            ("environment variable"-larına əlavə etdiyiniz `PAYRIFF_CALLBACK_URL` -ə ) sorğu göndərilir.

            Preauth ödəniş üsulunda (`operation='PRE_AUTH'`) müştəri ödəniş edir, məbləğ hesabında bloklanır. Ödəniş siz tərəfindən tamamlanmalı(complete)
            və ya geri qaytarma(pre-reverse) edilməlidir. Ödəniş complete olunan kimi məbləğ hesabınıza köçür.
            Bu üsulu adətən otellər istifadə edir, rezervasiya kimi xidmətləri üçün (Payriff ilə əlaqə zamanı belə məlumat verildi).
            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                description: Ödəniş səbəbi. Maksimal uzunluq: 1000 simvol.
                language: Ödəniş səbəbi dili. Mümkün dəyərlər: `["AZ", "EN", "RU"]`. Default: `AZ`
                currency: Ödəniş valyutası. Default: `AZN`
                callback_url: Callback URL. Default: None
                card_save: Kart saqlanacaqmi? Default: False
                operation: Operation. Default: PURCHASE
            """  # noqa: E501

        def get_order_info(
            self, order_id: UUID
        ) -> APIResponse[BaseResponseSchema[GetOrderInfoResponseSchema]]:
            """Ödəniş barədə ətraflı məlumat əldə etmək üçün sorğu

            **Endpoint** /api/v3/orders/{order_id}

            Example:
            ```python
            from integrify.payriff import PayriffClient

            PayriffClient.get_order_info(order_id='123456')
            ```

            **Cavab formatı: [`BaseResponseSchema[GetOrderInfoResponseSchema]`][integrify.payriff.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödəniş barədə ətraflı məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def refund(
            self,
            order_id: UUID,
            amount: Decimal,
        ) -> APIResponse[RefundResponseSchema]:
            """Geri ödəniş sorğusu

            **Endpoint** /api/v3/refund

            Example:
            ```python
            from integrify.payriff import PayriffClient

            PayriffClient.refund(
                order_id='123456',
                amount=10.0,
            )
            ```

            **Cavab formatı: [`RefundResponseSchema]`][integrify.payriff.schemas.response.RefundResponseSchema]**

            Bu sorğu ilə əvvəlki ödənişi geri ödəmək üçün istifadə edə bilərsiniz.
            Cavab olaraq geri ödənişin detallarını əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
                amount: Geri ödəniş miqdarı. Numerik dəyər.
            """  # noqa: E501

        def complete(
            self,
            order_id: UUID,
            amount: Decimal,
        ):
            """Ödənişin tamamlanması sorğusu

            **Endpoint** /api/v3/complete

            Example:
            ```python
            from integrify.payriff import PayriffClient

            PayriffClient.complete(order_id='123456')
            ```


            Bu sorğunu göndərdikdə, daxil edilən `order_id` və `amount` ilə qeyd edilən ödəniş tamamlanacaq.

            Args:
                order_id: Ödənişin ID-si.
                amount: Ödəniş miqdarı.
            """  # noqa: E501


PayriffClient = PayriffClientClass()

PayriffAsyncClient = PayriffClientClass(sync=False)
