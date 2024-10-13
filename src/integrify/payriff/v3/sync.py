from integrify.base import SyncApiRequest
from integrify.payriff import env

__all__ = ['PayriffRequest']


class PayriffRequest(SyncApiRequest):
    """Payriff sorğular üçün baza class (v2)"""

    def __init__(self):
        super().__init__('Payriff', env.PAYRIFF_LOGGER_NAME)

        self.base_url = 'https://api.payriff.com/api/v3/'
        self.headers['Authorization'] = env.PAYRIFF_AUTHORIZATION_KEY
        self.body_data: dict = {}
