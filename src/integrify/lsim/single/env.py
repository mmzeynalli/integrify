from enum import Enum

VERSION = '2024.11.22'


class API(str, Enum):
    BASE_URL = 'https://apps.lsim.az'

    SEND_SMS_GET = '/quicksms/v1/send'
    SEND_SMS_POST = '/quicksms/v1/smssender'

    CHECK_BALANCE = '/quicksms/v1/balance'

    GET_REPORT_GET = '/quicksms/v1/report'
    GET_REPORT_POST = '/quicksms/v1/smsreporter'
