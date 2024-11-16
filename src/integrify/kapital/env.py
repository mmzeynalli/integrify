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
    ORDER_INFORMATION: Literal['/api/order/{order_id}'] = '/api/order/{order_id}'
    DETAILED_ORDER_INFORMATION: Literal[
        '/api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2'  # noqa E501
    ] = '/api/order/{order_id}?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2'  # noqa E501
    REFUND_ORDER: Literal['/api/order/{order_id}/exec-tran'] = '/api/order/{order_id}/exec-tran'
    SAVE_CARD: Literal['/api/order'] = '/api/order'
    CREATE_ORDER_AND_SAVE_CARD: Literal['/api/order'] = '/api/order'
    FULL_REVERSE_ORDER: Literal['/api/order/{order_id}/exec-tran'] = (
        '/api/order/{order_id}/exec-tran'
    )
    CLEARING_ORDER: Literal['/api/order/{order_id}/exec-tran'] = '/api/order/{order_id}/exec-tran'
    PARTIAL_REVERSE_ORDER: Literal['/api/order/{order_id}/exec-tran'] = (
        '/api/order/{order_id}/exec-tran'
    )
    CREATE_ORDER_FOR_PAY_WITH_SAVED_CARD: Literal['/api/order'] = '/api/order'
    SET_SRC_TOKEN: Literal['/api/order/{order_id}/set-src-token?password={password}'] = (
        '/api/order/{order_id}/set-src-token?password={password}'
    )
    EXEC_PAY_WITH_SAVED_CARD: Literal['/api/order/{order_id}/exec-tran?password={password}'] = (
        '/api/order/{order_id}/exec-tran?password={password}'
    )


__all__ = [
    'VERSION',
    'KAPITAL_BASE_URL',
    'KAPITAL_USERNAME',
    'KAPITAL_PASSWORD',
    'KAPITAL_INTERFACE_LANG',
    'KAPITAL_REDIRECT_URL',
    'API',
]
