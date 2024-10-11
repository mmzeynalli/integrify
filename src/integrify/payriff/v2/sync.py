from typing import Any

from integrify.base import SyncApiRequest
from integrify.payriff import env

__all__ = ['PayriffRequest']


class PayriffRequest(SyncApiRequest):
    """Payriff sorğular üçün baza class (v2)"""

    def __init__(self):
        super().__init__('Payriff', env.PAYRIFF_LOGGER_NAME)

        self.base_url = 'https://api.payriff.com/api/v2/'
        self.headers['Authorization'] = env.PAYRIFF_AUTHORIZATION_KEY
        self.body_data: dict = {}

    def __call__(self, *args: Any, **kwds: Any):
        if self.body_data:
            self.body = {'body': self.body_data, 'merchant': env.PAYRIFF_MERCHANT_ID}

        return super().__call__(*args, **kwds)
