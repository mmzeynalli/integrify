from typing import TYPE_CHECKING

from integrify.api import APIClient
from integrify.postaguvercini import env
from integrify.postaguvercini.handlers import CreditBalancePayloadHandler
from integrify.postaguvercini.schemas.response import CreditBalanceResponseSchema
from integrify.schemas import APIResponse

__all__ = ['PostaGuverciniClientClass']


class PostaGuverciniClientClass(APIClient):
    """Posta Guvercini sorğular üçün baza class"""

    def __init__(self, sync: bool = True):
        super().__init__('PostaGuvercini', env.API.BASE_URL, None, sync=sync)

        self.add_url('credit_balance', env.API.CREDIT_BALANCE, verb='POST')
        self.add_handler('credit_balance', CreditBalancePayloadHandler)

    if TYPE_CHECKING:

        def credit_balance(self) -> APIResponse[CreditBalanceResponseSchema]:
            """Kredit balans sorğusu

            **Endpoint:** /api_json/v1/Sms/CreditBalance

            Example:
            ```python
            from integrify.postaguvercini import PostaGuverciniRequest

            PostaGuverciniRequest.credit_balance()
            ``

            **Cavab formatı**: [`CreditBalanceResponseSchema`][integrify.postaguvercini.schemas.response.CreditBalanceResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq kredit balans məlumatı gəlir.

            Args:
                None
            """  # noqa: E501


PostaGuverciniRequest = PostaGuverciniClientClass(sync=True)
PostaGuverciniAsyncRequest = PostaGuverciniClientClass(sync=False)
