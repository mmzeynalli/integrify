from enum import Enum


class Code(int, Enum):
    """Bulk SMS tranzaksiyanın status kodları"""

    SUCCESS = 0
    IN_PROCESS_NOT_READY = 1
    DUPLICATE = 2
    BAD_REQUEST = 100
    OPERATION_TYPE_EMPTY = 101
    INVALID_OPERATION = 102
    EMTPY_LOGIN = 103
    EMTPY_PASSWORD = 104  # nosec: B105
    INVALID_AUTH = 105
    EMPTY_TITLE = 106
    INVALID_TITLE = 107
    EMPTY_TASK_ID = 108
    INVALID_TASK_ID = 109
    EMPTY_CONTROL_ID = 110
    EMPTY_SCHEDULED_DATE = 111
    INVALID_SCHEDULED_DATE = 112
    OLD_SCHEDULED_DATE = 113
    EMPTY_ISBULK = 114
    INVALID_ISBULK = 115
    INVALID_BULK_MSG = 116
    INVALID_BODY = 117
    INSUFFICIENT_BALANCE = 118


class SMSStatus(int, Enum):
    """Bulk göndərilmədə hər SMS üçün status kodları"""

    MESSAGE_EXPIRED = 1
    MESSAGE_DELIVERED = 2
    MESSAGE_UNDELIVERED = 3
    MESSAGE_SENT = 4
    SYSTEM_ERROR = 5
    BLACK_LIST = 6
    MESSAGE_IN_QUEUE = 7
    DUPLICATE_MESSAGE = 8
