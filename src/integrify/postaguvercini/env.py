import os
from enum import Enum
from typing import Optional

VERSION = 'v1'

POSTA_GUVERCINI_USERNAME: Optional[str] = os.getenv('POSTA_GUVERCINI_USERNAME', '')
POSTA_GUVERCINI_PASSWORD: Optional[str] = os.getenv('POSTA_GUVERCINI_PASSWORD', '')


class API(str, Enum):
    BASE_URL = 'https://www.poctgoyercini.com'

    SEND_SINGLE_SMS = '/api_json/v1/Sms/Send_1_N'
    SEND_MULTIPLE_SMS = '/api_json/v1/Sms/Send_N_N'
    STATUS = '/api_json/v1/Sms/Status'
    CREDIT_BALANCE = '/api_json/v1/Sms/CreditBalance'


__all__ = [
    'VERSION',
    'POSTA_GUVERCINI_USERNAME',
    'POSTA_GUVERCINI_PASSWORD',
    'API',
]
