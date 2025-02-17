import os
from enum import Enum
from typing import Optional
from warnings import warn

from integrify.utils import Environment

VERSION = '2024.10.19'

KAPITAL_ENV: str = os.getenv('KAPITAL_ENV', Environment.TEST.value)
KAPITAL_USERNAME: str = os.getenv('KAPITAL_USERNAME', '')
KAPITAL_PASSWORD: str = os.getenv('KAPITAL_PASSWORD', '')

KAPITAL_INTERFACE_LANG: str = os.getenv('KAPITAL_INTERFACE_LANG', 'az')
KAPITAL_REDIRECT_URL: Optional[str] = os.getenv('KAPITAL_REDIRECT_URL')


if not KAPITAL_USERNAME or not KAPITAL_PASSWORD:
    warn(
        'KAPITAL_USERNAME/KAPITAL_PASSWORD mühit dəyişənlərinə dəyər verməsəniz '
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    TEST_BASE_URL = 'https://txpgtst.kapitalbank.az'
    PROD_BASE_URL = 'https://e-commerce.kapitalbank.az'
    BASE_URL = PROD_BASE_URL if KAPITAL_ENV == Environment.PROD else TEST_BASE_URL

    ORDER = '/api/order'
    GET_ORDER = '/api/order/{order_id}'
    GET_DETAILED_ORDER = (
        '/api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2'
    )
    ORDER_EXECUTION = '/api/order/{order_id}/exec-tran'
    ORDER_LINK_CARD_TOKEN = '/api/order/{order_id}/set-src-token?password={password}'  # nosec: B105
    PROCESS_PAYMENT_WITH_SAVED_CARD = '/api/order/{order_id}/exec-tran?password={password}'


__all__ = [
    'VERSION',
    'KAPITAL_USERNAME',
    'KAPITAL_PASSWORD',
    'KAPITAL_INTERFACE_LANG',
    'KAPITAL_REDIRECT_URL',
    'API',
]
