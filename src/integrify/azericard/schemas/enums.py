from enum import Enum
from typing import Literal


class TrType(str, Enum):
    PRE_AUTHORAZATION: Literal['0'] = '0'
    AUTHORAZATION: Literal['1'] = '1'
    ACCEPT_REQUEST: Literal['21'] = '21'
    RETURN_REQUEST: Literal['22'] = '22'
    CANCEL_REQUEST: Literal['24'] = '24'
    REQUEST_STATUS: Literal['90'] = '90'


class Action(int, Enum):
    TRANSACTION_SUCCESS = 0
    """Tranzaksiya uğurla tamamlandı"""

    TRANSACTION_DUPLICATE = 1
    """Duplikat əməliyyat aşkar edildi"""

    TRANSACTION_CANCELLED = 2
    """Tranzaksiya rədd edildi"""

    TRANSACTION_PROCESSING_ERROR = 3
    """Tranzaksiya emal xətası"""

    TRANSACTION_REPEAT_OF_CANCELLED = 6
    """İmtina edilmiş əməliyyatın təkrarlanması"""

    TRANSACTION_REPEAT_OF_UNAPPROVED = 7
    """Doğrulama xətası ilə əməliyyatın təkrarlanması"""

    TRANSACTION_REPEAT_OF_UNRESPONDED = 8
    """Cavab verilmədən dayandırılmış əməliyyatın təkrarlanması"""
