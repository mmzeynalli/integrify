import os
from enum import Enum
from typing import Literal, Optional

LSIM_LOGIN: Optional[str] = os.getenv('LSIM_LOGIN')
LSIM_PASSWORD: Optional[str] = os.getenv('LSIM_PASSWORD')
LSIM_SENDER_NAME: Optional[str] = os.getenv('LSIM_SENDER_NAME')


class API(str, Enum):
    BASE_URL: Literal['https://apps.lsim.az'] = 'https://apps.lsim.az'

    SEND_SMS_GET: Literal['/quicksms/v1/send'] = '/quicksms/v1/send'
    SEND_SMS_POST: Literal['/quicksms/v1/smssender'] = '/quicksms/v1/smssender'

    CHECK_BALANCE: Literal['/quicksms/v1/balance'] = '/quicksms/v1/balance'

    GET_REPORT_GET: Literal['/quicksms/v1/report'] = '/quicksms/v1/report'
    GET_REPORT_POST: Literal['/quicksms/v1/smsreporter'] = '/quicksms/v1/smsreporter'
