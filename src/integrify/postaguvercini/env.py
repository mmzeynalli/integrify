import os
from enum import Enum
from warnings import warn

VERSION = 'v1'

POSTA_GUVERCINI_USERNAME: str = os.getenv('POSTA_GUVERCINI_USERNAME', '')
POSTA_GUVERCINI_PASSWORD: str = os.getenv('POSTA_GUVERCINI_PASSWORD', '')


if not POSTA_GUVERCINI_USERNAME or not POSTA_GUVERCINI_PASSWORD:
    warn(
        'POSTA_GUVERCINI_USERNAME/POSTA_GUVERCINI_PASSWORD mühit dəyişənlərinə dəyər verməsəniz '
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    BASE_URL = 'https://www.poctgoyercini.com'

    CREDIT_BALANCE = '/api_json/v1/Sms/CreditBalance'


__all__ = [
    'VERSION',
    'POSTA_GUVERCINI_USERNAME',
    'POSTA_GUVERCINI_PASSWORD',
    'API',
]
