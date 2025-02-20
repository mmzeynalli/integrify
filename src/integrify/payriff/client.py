from integrify.api import APIClient
from integrify.payriff import env


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

        self.add_url('orders', env.API.CREATE_ORDER, verb='POST')
        # self.add_handler('orders', CreateOrderPayloadHandler)

    # if TYPE_CHECKING:


PayriffClient = PayriffClientClass()
PayriffAsyncClient = PayriffClientClass(sync=False)
