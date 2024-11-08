from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.kapital import env
from integrify.kapital.handlers import (
    CreateOrderPayloadHandler,
    DetailedOrderInformationPayloadHandler,
    OrderInformationPayloadHandler,
    RefundOrderPayloadHandler,
)
from integrify.kapital.schemas.response import (
    CreateOrderResponseSchema,
    DetailedOrderInformationResponseSchema,
    OrderInformationResponseSchema,
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

    if TYPE_CHECKING:

        def create_order(
            self,
            amount: Numeric,
            currency: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse[CreateOrderResponseSchema]:
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

            **Cavab formatı: [`CreateOrderResponseSchema`][integrify.kapital.schemas.response.CreateOrderResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə "{callback_url}/?ID={id}&STATUS={status}" formatında sorğusu göndərilir. ID-dən istifadə edərək
            ödənişin detallarını əldə edə bilərsiniz.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        def order_information(self, order_id: str) -> APIResponse[OrderInformationResponseSchema]:
            """Ödənişin detallarını əldə etmək üçün sorğu

            **Kapital** /api/order/{order_id}

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.order_information(order_id="123456")
            ```

            **Cavab formatı: [`OrderInformationResponseSchema`][integrify.kapital.schemas.response.OrderInformationResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödəniş haqda məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def detailed_order_information(
            self, order_id: str
        ) -> APIResponse[DetailedOrderInformationResponseSchema]:
            """Ödənişin detallarını əldə etmək üçün ətraflı sorğu

            **Kapital** /api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2

            Example:
            ```python
            from integrify.kapital import KapitalRequest

            KapitalRequest.detailed_order_information(order_id="123456")
            ```

            **Cavab formatı: [`DetailedOrderInformationResponseSchema`][integrify.kapital.schemas.response.DetailedOrderInformationResponseSchema]**

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin detallı məlumat əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501

        def refund_order(
            self,
            order_id: str,
            amount: Numeric,
            **extra: Any,
        ) -> APIResponse[RefundOrderResponseSchema]:
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

            **Cavab formatı: [`RefundOrderResponseSchema`](integrify.kapital.schemas.response.RefundOrderResponseSchema)**

            Bu sorğunu göndərdikdə, cavab olaraq geri ödənişin detallarını əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
                amount: Geri ödəniş miqdarı. Numerik dəyər.
            """  # noqa: E501


KapitalRequest = KapitalClientClass(sync=True)
KapitalAsyncRequest = KapitalClientClass(sync=False)
