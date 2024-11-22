import os
from enum import Enum
from typing import Literal
from warnings import warn

from integrify.schemas import Environment

VERSION = '2024.11.6'


AZERICARD_MERCHANT_ID = os.getenv('AZERICARD_MERCHANT_ID', '')
AZERICARD_KEY_FILE_PATH = os.getenv('AZERICARD_KEY_FILE_PATH', '')
AZERICARD_ENV: str = os.getenv('AZERICARD_ENV', Environment.TEST)
AZERICARD_INTERFACE_LANG = os.getenv('AZERICARD_INTERFACE_LANG', 'az')
AZERICARD_MERCHANT_NAME = os.getenv('AZERICARD_MERCHANT_NAME', None)
AZERICARD_MERCHANT_URL = os.getenv('AZERICARD_MERCHANT_URL', None)

if not AZERICARD_MERCHANT_ID or not AZERICARD_KEY_FILE_PATH:
    warn(
        'AZERICARD_MERCHANT_ID/AZERICARD_KEY_FILE_PATH mühit dəyişənlərinə'
        'dəyər verməsəniz sorğular çalışmayacaq!'
    )


class MPI_API(str, Enum):
    """Endpoint constant-ları"""

    TEST_BASE_URL: Literal['https://testmpi.3dsecure.az'] = 'https://testmpi.3dsecure.az'
    PROD_BASE_URL: Literal['https://mpi.3dsecure.az'] = 'https://mpi.3dsecure.az'
    BASE_URL = PROD_BASE_URL if AZERICARD_ENV == Environment.PROD else TEST_BASE_URL

    AUTHORIZATION: Literal['/cgi-bin/cgi_link'] = '/cgi-bin/cgi_link'
    SAVE_CARD: Literal['/token/cgi_link'] = '/token/cgi_link'


__all__ = [
    'AZERICARD_MERCHANT_ID',
    'MPI_API',
]
