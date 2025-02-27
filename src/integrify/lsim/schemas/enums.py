from enum import Enum


class Code(int, Enum):
    """`error_code` field-inin dəyərləri."""

    IN_QUEUE = 100
    DELIVERED = 101
    UNDELIVERED = 102
    EXPIRED = 103
    REJECTED = 104
    CANCELLED = 105
    ERROR = 106
    UNKNOWN = 107
    SENT = 108
    BLACK_LISTED = 109

    INVALID_KEY = -100
    TOO_LONG_TEXT = -101
    WRONG_NUMBER_FORMAT = -102
    INVALID_SENDER_NAME = -103
    INSUFFICIENT_BALANCE = -104
    NUMBER_IN_BLACK_LIST = -105
    INVALID_TRANSACTION_ID = -106
    IP_ADDRESS_NOT_ALLOWED = -107
    INVALID_HASH = -108
    NO_HOST = -109
    REPORTING_LIMIT_EXCEEDED = -110

    INTERNAL_ERROR = -500


class BulkCode(str, Enum):
    """Bulk SMS status kodları"""

    SUCCESS = '000'
    IN_PROCESS_NOT_READY = '001'
    DUPLICATE = '002'
    BAD_REQUEST = '100'
    OPERATION_TYPE_EMPTY = '101'
    INVALID_OPERATION = '102'
    EMTPY_LOGIN = '103'
    EMTPY_PASSWORD = '104'  # nosec: B105
    INVALID_AUTH = '105'
    EMPTY_TITLE = '106'
    INVALID_TITLE = '107'
    EMPTY_TASK_ID = '108'
    INVALID_TASK_ID = '109'
    EMPTY_CONTROL_ID = '110'
    EMPTY_SCHEDULED_DATE = '111'
    INVALID_SCHEDULED_DATE = '112'
    OLD_SCHEDULED_DATE = '113'
    EMPTY_ISBULK = '114'
    INVALID_ISBULK = '115'
    INVALID_BULK_MSG = '116'
    INVALID_BODY = '117'
    INSUFFICIENT_BALANCE = '118'
