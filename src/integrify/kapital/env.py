import os
from enum import Enum
from typing import Literal, Optional
from warnings import warn

VERSION = '1.0.3'

KAPITAL_BASE_URL: str = os.getenv('KAPITAL_BASE_URL', '')
KAPITAL_USERNAME: str = os.getenv('KAPITAL_USERNAME', '')
KAPITAL_PASSWORD: str = os.getenv('KAPITAL_PASSWORD', '')

KAPITAL_INTERFACE_LANG: str = os.getenv('KAPITAL_INTERFACE_LANG', 'az')
KAPITAL_REDIRECT_URL: Optional[str] = os.getenv('KAPITAL_REDIRECT_URL')


if not KAPITAL_BASE_URL or not KAPITAL_USERNAME or not KAPITAL_PASSWORD:
    warn(
        'KAPITAL_BASE_URL/KAPITAL_USERNAME/KAPITAL_PASSWORD mühit dəyişənlərinə dəyər verməsəniz '
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    CREATE_ORDER: Literal['/api/order'] = '/api/order'


__all__ = [
    'VERSION',
    'KAPITAL_BASE_URL',
    'KAPITAL_USERNAME',
    'KAPITAL_PASSWORD',
    'KAPITAL_INTERFACE_LANG',
    'KAPITAL_REDIRECT_URL',
    'API',
]
