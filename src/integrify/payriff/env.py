import os
from enum import Enum
from typing import Optional
from warnings import warn

VERSION = '3'

PAYRIFF_AUTHORIZATION_KEY: str = os.getenv('PAYRIFF_AUTHORIZATION_KEY', '')
PAYRIFF_MERCHANT_ID: str = os.getenv('PAYRIFF_MERCHANT_ID', '')


PAYRIFF_CALLBACK_URL: Optional[str] = os.getenv('PAYRIFF_CALLBACK_URL', '')
PAYRIFF_LOGGER_NAME: str = os.getenv('PAYRIFF_LOGGER_NAME', 'payriff')


if not PAYRIFF_AUTHORIZATION_KEY or not PAYRIFF_MERCHANT_ID:
    warn(
        'set PAYRIFF_AUTHORIZATION_KEY/PAYRIFF_MERCHANT_ID mühit dəyişənlərinə dəyər verməsəniz'
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    """Payriff API constant-ları"""

    BASE_URL = 'https://api.payriff.com'
    CREATE_ORDER = '/api/v3/orders'
    GET_ORDER = '/api/v3/orders/{order_id}'


__all__ = [
    'VERSION',
    'API',
    'PAYRIFF_AUTHORIZATION_KEY',
    'PAYRIFF_MERCHANT_ID',
]
