from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from integrify.api import APIClient
from integrify.payriff import env
from integrify.payriff.handlers import CreateOrderPayloadHandler
from integrify.payriff.schemas.enums import Currency, Language, Operation
from integrify.payriff.schemas.response import CreateOrderResponseSchema
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
        ) -> APIResponse[CreateOrderResponseSchema]:
            """Test docs"""


PayriffClient = PayriffClientClass()
PayriffAsyncClient = PayriffClientClass(sync=False)
