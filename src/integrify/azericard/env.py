import os
from enum import Enum
from typing import Literal

from integrify.schemas import Environment

VERSION = '2024.11.6'


AZERICARD_MERCHANT_ID = os.getenv('AZERICARD_MERCHANT_ID', '')
AZERICARD_ENV: str = os.getenv('AZERICARD_ENV', Environment.TEST)


class MPI_API(str, Enum):
    """Endpoint constant-ları"""

    TEST_BASE_URL: Literal['https://testmpi.3dsecure.az'] = 'https://testmpi.3dsecure.az'
    PROD_BASE_URL = ''

    AUTHORIZATION: Literal['/cgi-bin/cgi_link'] = '/cgi-bin/cgi_link'
    SAVE_CARD: Literal['/token/cgi_link'] = '/token/cgi_link'

    @classmethod
    def get_base_url(cls, env: str):
        return cls.PROD_BASE_URL if env == Environment.PROD else cls.TEST_BASE_URL


__all__ = [
    'AZERICARD_MERCHANT_ID',
    'MPI_API',
]
