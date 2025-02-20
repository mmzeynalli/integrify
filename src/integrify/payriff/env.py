import os
from enum import Enum
from typing import Optional
from warnings import warn

VERSION = '3'

PAYRIFF_AUTHORIZATION_KEY: str = os.getenv('PAYRIFF_AUTHORIZATION_KEY', '')
PAYRIFF_MERCHANT_ID: str = os.getenv('PAYRIFF_MERCHANT_ID', '')

PAYRIFF_SUCCESS_REDIRECT_URL: Optional[str] = os.getenv('PAYRIFF_SUCCESS_REDIRECT_URL')
PAYRIFF_FAILED_REDIRECT_URL: Optional[str] = os.getenv('PAYRIFF_FAILED_REDIRECT_URL')
PAYRIFF_CANCELED_REDIRECT_URL: Optional[str] = os.getenv('PAYRIFF_CANCELED_REDIRECT_URL')

PAYRIFF_LOGGER_NAME: str = os.getenv('PAYRIFF_LOGGER_NAME', 'payriff')


if not PAYRIFF_AUTHORIZATION_KEY or not PAYRIFF_MERCHANT_ID:
    warn(
        'set PAYRIFF_AUTHORIZATION_KEY/PAYRIFF_MERCHANT_ID mühit dəyişənlərinə dəyər verməsəniz'
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    """Payriff API constant-ları"""

    BASE_URL: str = 'https://api.payriff.com'
    CREATE_ORDER: str = '/api/v3/orders'


__all__ = [
    'VERSION',
    'API',
    'PAYRIFF_AUTHORIZATION_KEY',
    'PAYRIFF_MERCHANT_ID',
    'PAYRIFF_SUCCESS_REDIRECT_URL',
    'PAYRIFF_FAILED_REDIRECT_URL',
    'PAYRIFF_CANCELED_REDIRECT_URL',
]
