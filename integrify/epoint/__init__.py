"""
Dokumentasiyalar:

AZ: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20az.pdf
EN: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf
RU: https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20ru.pdf
"""

import os
from typing import Optional
from warnings import warn

from dotenv import load_dotenv

load_dotenv()

VERSION = '1.0.3'

EPOINT_PUBLIC_KEY: str = os.getenv('EPOINT_PUBLIC_KEY', '')
EPOINT_PRIVATE_KEY: str = os.getenv('EPOINT_PRIVATE_KEY', '')

EPOINT_INTERFACE_LANG: str = os.getenv('EPOINT_INTERFACE_LANG', 'az')
EPOINT_SUCCESS_REDIRECT_URL: Optional[str] = os.getenv('EPOINT_SUCCESS_REDIRECT_URL')
EPOINT_FAILED_REDIRECT_URL: Optional[str] = os.getenv('EPOINT_FAILED_REDIRECT_URL')
EPOINT_LOGGER_NAME: str = os.getenv('EPOINT_LOGGER_NAME', 'epoint')


if not EPOINT_PUBLIC_KEY or not EPOINT_PRIVATE_KEY:
    warn(
        'EPOINT_PUBLIC_KEY/EPOINT_PRIVATE_KEY mühit dəyişənlərinə dəyər verməsəniz'
        'sorğular çalışmayacaq!'
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
