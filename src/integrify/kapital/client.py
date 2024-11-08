from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.kapital import env
from integrify.kapital.handlers import (
    CreateOrderPayloadHandler,
    OrderInformationPayloadHandler,
)
from integrify.kapital.schemas.response import (
    CreateOrderResponseSchema,
    OrderInformationResponseSchema,
)

__all__ = ['KapitalClientClass']


class KapitalClientClass(APIClient):
    def __init__(self, sync: bool = True):
        super().__init__('Kapital', env.KAPITAL_BASE_URL, None, sync)

        self.add_url('create_order', env.API.CREATE_ORDER, verb='POST')
        self.add_handler('create_order', CreateOrderPayloadHandler)

        self.add_url('order_information', env.API.ORDER_INFORMATION, verb='GET')
        self.add_handler('order_information', OrderInformationPayloadHandler)

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

            Bu sorğunu göndərdikdə, cavab olaraq ödənişin detallarını əldə edə bilərsiniz.

            Args:
                order_id: Ödənişin ID-si.
            """  # noqa: E501


KapitalRequest = KapitalClientClass(sync=True)
KapitalAsyncRequest = KapitalClientClass(sync=False)
