import os
from enum import Enum
from typing import Literal
from warnings import warn

from integrify.schemas import Environment

VERSION = '2024.11.6'


AZERICARD_MERCHANT_ID = os.getenv('AZERICARD_MERCHANT_ID', '')
"""Bank tərəfindən təyin edilmiş Merchant Terminal ID"""

AZERICARD_KEY_FILE_PATH = os.getenv('AZERICARD_KEY_FILE_PATH', '')
"""AzeriCard sorğuları üçün açar"""

AZERICARD_ENV: str = os.getenv('AZERICARD_ENV', Environment.TEST)  # pylint: disable=invalid-envvar-default
"""AzeriCard sorğu mühiti (test/prod)"""

AZERICARD_MERCHANT_NAME = os.getenv('AZERICARD_MERCHANT_NAME', None)
"""Satıcının (merchan) adı (kart istifadəçisinin anladığı formada olmalıdır)"""

AZERICARD_MERCHANT_URL = os.getenv('AZERICARD_MERCHANT_URL', None)
"""Satıcının web site URL-ı"""

AZERICARD_CALLBACK_URL = os.getenv('AZERICARD_CALLBACK_URL', None)
"""Avtorizasiya nəticəsinin yerləşdirilməsində(post) istifadə olunan Merchant URL."""

AZERICARD_INTERFACE_LANG = os.getenv('AZERICARD_INTERFACE_LANG', 'az')
"""Dil seçimi (default: az)"""

if not AZERICARD_KEY_FILE_PATH:
    warn('AZERICARD_KEY_FILE_PATH mühit dəyişənlərinə dəyər verməsəniz sorğular çalışmayacaq!')


class MpiAPI(str, Enum):
    """Endpoint constant-ları"""

    TEST_BASE_URL: Literal['https://testmpi.3dsecure.az'] = 'https://testmpi.3dsecure.az'
    PROD_BASE_URL: Literal['https://mpi.3dsecure.az'] = 'https://mpi.3dsecure.az'
    BASE_URL = PROD_BASE_URL if AZERICARD_ENV == Environment.PROD else TEST_BASE_URL

    AUTHORIZATION: Literal['/cgi-bin/cgi_link'] = '/cgi-bin/cgi_link'
    SAVE_CARD: Literal['/token/cgi_link'] = '/token/cgi_link'


class MtAPI(str, Enum):
    """MT Endpoint constant-ları"""

    TEST_BASE_URL: Literal['https://testmt.azericard.com'] = 'https://testmt.azericard.com'
    PROD_BASE_URL: Literal['https://mt.azericard.com'] = 'https://mt.azericard.com'
    BASE_URL = PROD_BASE_URL if AZERICARD_ENV == Environment.PROD else TEST_BASE_URL

    TRANSFER: Literal['/payment/view'] = '/payment/view'
    TRANSFER_CONFIRM: Literal['/api/confirm'] = '/api/confirm'


__all__ = [
    'AZERICARD_MERCHANT_ID',
    'MpiAPI',
]
