from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.kapital import env
from integrify.kapital.handlers import (
    ClearingOrderPayloadHandler,
    CreateOrderAndSaveCardPayloadHandler,
    CreateOrderPayloadHandler,
    DetailedOrderInformationPayloadHandler,
    FullReverseOrderPayloadHandler,
    OrderInformationPayloadHandler,
    PartialReverseOrderPayloadHandler,
    RefundOrderPayloadHandler,
    SaveCardPayloadHandler,
)
from integrify.kapital.schemas.response import (
    BaseResponseSchema,
    ClearingOrderResponseSchema,
    CreateOrderResponseSchema,
    DetailedOrderInformationResponseSchema,
    FullReverseOrderResponseSchema,
    OrderInformationResponseSchema,
    PartialReverseOrderResponseSchema,
    RefundOrderResponseSchema,
)

__all__ = ['KapitalClientClass']


class KapitalClientClass(APIClient):
    def __init__(self, sync: bool = True):
        super().__init__('Kapital', env.KAPITAL_BASE_URL, None, sync)

        self.add_url('create_order', env.API.CREATE_ORDER, verb='POST')
        self.add_handler('create_order', CreateOrderPayloadHandler)

        self.add_url('order_information', env.API.ORDER_INFORMATION, verb='GET')
        self.add_handler('order_information', OrderInformationPayloadHandler)

        self.add_url('detailed_order_information', env.API.DETAILED_ORDER_INFORMATION, verb='GET')
        self.add_handler('detailed_order_information', DetailedOrderInformationPayloadHandler)

        self.add_url('refund_order', env.API.REFUND_ORDER, verb='POST')
        self.add_handler('refund_order', RefundOrderPayloadHandler)

        self.add_url('save_card', env.API.SAVE_CARD, verb='POST')
        self.add_handler('save_card', SaveCardPayloadHandler)

        self.add_url(
            'create_order_and_save_card',
            env.API.CREATE_ORDER_AND_SAVE_CARD,
            verb='POST',
        )
        self.add_handler('create_order_and_save_card', CreateOrderAndSaveCardPayloadHandler)

        self.add_url('full_reverse_order', env.API.FULL_REVERSE_ORDER, verb='POST')
        self.add_handler('full_reverse_order', FullReverseOrderPayloadHandler)

        self.add_url('clearing_order', env.API.CLEARING_ORDER, verb='POST')
        self.add_handler('clearing_order', ClearingOrderPayloadHandler)

        self.add_url('partial_reverse_order', env.API.PARTIAL_REVERSE_ORDER, verb='POST')
        self.add_handler('partial_reverse_order', PartialReverseOrderPayloadHandler)

    if TYPE_CHECKING:

        def create_order(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Ödəniş sorğusu

            **Kapital** /api/order

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.create_order(
                amount=10.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını detailed_order_information() funksiyandan istifadə edərək əldə edə bilərsiz.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def order_information(
            self, order_id: str
        ) -> APIResponse[BaseResponseSchema[OrderInformationResponseSchema]]:
            """Ödənişin detallarını əldə etmək üçün sorğu

            **Kapital** /api/order/{order_id}

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.order_information(order_id="123456")
            ```

            **Cavab formatı: [`BaseResponseSchema[OrderInformationResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödəniş haqda məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def detailed_order_information(
            self, order_id: str
        ) -> APIResponse[BaseResponseSchema[DetailedOrderInformationResponseSchema]]:
            """Ödənişin detallarını əldə etmək üçün ətraflı sorğu

            **Kapital** /api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.detailed_order_information(order_id="123456")
            ```

            **Cavab formatı: [`BaseResponseSchema[DetailedOrderInformationResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin detallı məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def refund_order(
            self,
            order_id: str,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[RefundOrderResponseSchema]]:
            """Geri ödəniş sorğusu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.refund_order(
                order_id="123456",
                amount=10.0,
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[RefundOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq geri ödənişin detallarını əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
                amount: Geri ödəniş miqdarı. Numerik dəyər.
            """  # noqa: E501

        def save_card(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Kartı saxlamaq üçün ödəniş sorğusu

            **Kapital** /api/order

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.save_card(
                amount=1.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını detailed_order_information() funksiyandan istifadə edərək əldə edə bilərsiz.
            Həmin detallarda storedTokens key-i altındaki tokenləri saxlayaraq, sonrakı ödənişlərdə bu tokenləri
            istifadə edə bilərsiniz.
            """  # noqa: E501

        def create_order_and_save_card(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[CreateOrderResponseSchema]]:
            """Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu

            **Kapital** /api/order

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.pay_and_save_card(
                amount=1.0,
                currency="AZN",
                description="Test payment",
            )
            ```

            **Cavab formatı: [`BaseResponseSchema[CreateOrderResponseSchema]`][integrify.kapital.schemas.response.BaseResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. Ödənişin
            detallarını detailed_order_information() funksiyandan istifadə edərək əldə edə bilərsiz.
            Həmin detallarda storedTokens key-i altındaki tokenləri saxlayaraq, sonrakı ödənişlərdə bu tokenləri
            istifadə edə bilərsiniz.
            """  # noqa: E501

        def full_reverse_order(
            self,
            order_id: str,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[FullReverseOrderResponseSchema]]:
            """Ödənişi ləğv etmək üçün sorğu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.full_reverse_order(order_id="123456")
            ```

            **Cavab formatı: [`BaseResponseSchema[FullReverseOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin ləğv edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani save_card() funksiyası ilə yaradılan ödənişlər üçün istifadə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def clearing_order(
            self,
            order_id: str,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[ClearingOrderResponseSchema]]:
            """Ödənişin təsdiq edilməsi üçün sorğu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.clearing_order(order_id="123456")
            ```

            **Cavab formatı: [`BaseResponseSchema[ClearingOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin təsdiq edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani save_card() funksiyası ilə yaradılan ödənişlər üçün istifadə edə bilərsiniz.
            Preauthorization əməliyyatının ikinci mərhələsi üçün.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def partial_reverse_order(
            self,
            order_id: str,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[BaseResponseSchema[PartialReverseOrderResponseSchema]]:
            """Ödənişin hissəsini ləğv etmək üçün sorğu

            **Kapital** /api/order/{order_id}/exec-tran

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.partial_reverse_order(order_id="123456", amount=5.0)
            ```

            **Cavab formatı: [`BaseResponseSchema[PartialReverseOrderResponseSchema]`](integrify.kapital.schemas.response.BaseResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin ləğv edilməsi haqda məlumat əldə edə bilərsiniz.
            Bu funksiyani clearing_order() funksiyası ilə təsdiq edilmiş ödənişlər üçün istifadə edə bilərsiniz.
            İlkin məbləğdən az olan vəsaitləri qaytarmaq üçün istifadə olunur. Bir dəfə istifadə etmək olar.

            Args:
                order_id: Ödənişin ID-si.
                amount: Ləğv olunacaq miqdar. Numerik dəyər.
            """  # noqa: E501


KapitalRequest = KapitalClientClass(sync=True)
KapitalAsyncRequest = KapitalClientClass(sync=False)
