from enum import Enum
from typing import Literal


class Code(int, Enum):
    IN_QUEUE: Literal[100] = 100
    DELIVERED: Literal[101] = 101
    UNDELIVERED: Literal[102] = 102
    EXPIRED: Literal[103] = 103
    REJECTED: Literal[104] = 104
    CANCELLED: Literal[105] = 105
    ERROR: Literal[106] = 106
    UNKNOWN: Literal[107] = 107
    SENT: Literal[108] = 108
    BLACK_LISTED: Literal[109] = 109

    INVALID_KEY: Literal[-100] = -100
    TOO_LONG_TEXT: Literal[-101] = -101
    WRONG_NUMBER_FORMAT: Literal[-102] = -102
    INVALID_SENDER_NAME: Literal[-103] = -103
    INSUFFICIENT_BALANCE: Literal[-104] = -104
    NUMBER_IN_BLACK_LIST: Literal[-105] = -105
    INVALID_TRANSACTION_ID: Literal[-106] = -106
    IP_ADDRESS_NOT_ALLOWED: Literal[-107] = -107
    INVALID_HASH: Literal[-108] = -108
    NO_HOST: Literal[-109] = -109
    REPORTING_LIMIT_EXCEEDED: Literal[-110] = -110

    INTERNAL_ERROR: Literal[-500] = -500
