"""Payriff üçün sorğular

Test kard məlumatları:

5239151747183468
11/24
292
"""

import os
from typing import Optional
from warnings import warn

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
