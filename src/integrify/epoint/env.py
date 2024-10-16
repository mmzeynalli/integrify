import os
from enum import Enum
from typing import Literal, Optional
from warnings import warn

VERSION = '1.0.3'

EPOINT_PUBLIC_KEY: str = os.getenv('EPOINT_PUBLIC_KEY', '')
EPOINT_PRIVATE_KEY: str = os.getenv('EPOINT_PRIVATE_KEY', '')

EPOINT_INTERFACE_LANG: str = os.getenv('EPOINT_INTERFACE_LANG', 'az')
EPOINT_SUCCESS_REDIRECT_URL: Optional[str] = os.getenv('EPOINT_SUCCESS_REDIRECT_URL')
EPOINT_FAILED_REDIRECT_URL: Optional[str] = os.getenv('EPOINT_FAILED_REDIRECT_URL')
EPOINT_LOGGER_NAME: str = os.getenv('EPOINT_LOGGER_NAME', 'epoint')


if not EPOINT_PUBLIC_KEY or not EPOINT_PRIVATE_KEY:
    warn(
        'EPOINT_PUBLIC_KEY/EPOINT_PRIVATE_KEY mühit dəyişənlərinə dəyər verməsəniz '
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    PAY: Literal['/api/1/request'] = '/api/1/request'
    GET_STATUS: Literal['/api/1/get-status'] = '/api/1/get-status'
    SAVE_CARD: Literal['/api/1/card-registration'] = '/api/1/card-registration'
    PAY_WITH_SAVED_CARD: Literal['/api/1/execute-pay'] = '/api/1/execute-pay'
    PAY_AND_SAVE_CARD: Literal['/api/1/card-registration-with-pay'] = (
        '/api/1/card-registration-with-pay'
    )
    PAYOUT: Literal['/api/1/refund-request'] = '/api/1/refund-request'
    REFUND: Literal['/api/1/reverse'] = '/api/1/reverse'
    SPLIT_PAY: Literal['/api/1/split-request'] = '/api/1/split-request'
    SPLIT_PAY_WITH_SAVED_CARD: Literal['/api/1/split-execute-pay'] = '/api/1/split-execute-pay'
    SPLIT_PAY_AND_SAVE_CARD: Literal['/api/1/split-card-registration-with-pay'] = (
        '/api/1/split-card-registration-with-pay'
    )


__all__ = [
    'VERSION',
    'EPOINT_PUBLIC_KEY',
    'EPOINT_PRIVATE_KEY',
    'EPOINT_INTERFACE_LANG',
    'EPOINT_SUCCESS_REDIRECT_URL',
    'EPOINT_FAILED_REDIRECT_URL',
    'EPOINT_LOGGER_NAME',
]
