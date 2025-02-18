import os
from enum import Enum
from typing import Optional

VERSION = '2024.11.22'

LSIM_LOGIN: Optional[str] = os.getenv('LSIM_LOGIN')
LSIM_PASSWORD: Optional[str] = os.getenv('LSIM_PASSWORD')
LSIM_SENDER_NAME: Optional[str] = os.getenv('LSIM_SENDER_NAME')


class API(str, Enum):
    BASE_URL = 'https://apps.lsim.az'

    SEND_SMS_GET = '/quicksms/v1/send'
    SEND_SMS_POST = '/quicksms/v1/smssender'

    CHECK_BALANCE = '/quicksms/v1/balance'

    GET_REPORT_GET = '/quicksms/v1/report'
    GET_REPORT_POST = '/quicksms/v1/smsreporter'
