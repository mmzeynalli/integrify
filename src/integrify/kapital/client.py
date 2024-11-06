from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.kapital import env
from integrify.kapital.handlers import CreateOrderPayloadHandler

from integrify.kapital.schemas.response import CreateOrderResponseSchema

__all__ = ["KapitalClientClass"]


class KapitalClientClass(APIClient):

    def __init__(self, sync: bool = True):
        super().__init__("Kapital", env.KAPITAL_BASE_URL, None, sync)

        self.add_url("create_order", env.API.CREATE_ORDER)
        self.add_handler("create_order", CreateOrderPayloadHandler)

    def add_url(self, route_name, url):
        # TODO: Change this according to the method in future
        return super().add_url(route_name, url, "POST")

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

            Bu sorğunu göndərdikdə cavabda ...

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödənişin məzənnəsi. Mümkün dəyərlər: `["AZN", "USD"]`.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """


KapitalRequest = KapitalClientClass(sync=True)
KapitalAsyncRequest = KapitalClientClass(sync=False)
