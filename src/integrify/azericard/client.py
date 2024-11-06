from typing import TYPE_CHECKING, Any, Optional
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, APIResponse
from integrify.azericard import env

__all__ = ['AzeriCardClientClass']


class AzeriCardClientClass(APIClient):
    """AzeriCard sorğular üçün baza class"""

    def __init__(self, sync: bool = True):
        super().__init__('AzeriCard', None, None, sync)

        self.add_url(
            'authorize',
            env.MPI_API.AUTHORIZATION,
            'POST',
            base_url=env.MPI_API.get_base_url(env.AZERICARD_ENV),
        )

    if TYPE_CHECKING:

        def authorize(
            self,
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Optional[str] = None,
            **extra: Any,
        ) -> APIResponse:
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


AzeriCardRequest = AzeriCardClientClass(sync=True)
AzeriCardAsyncRequest = AzeriCardClientClass(sync=False)
