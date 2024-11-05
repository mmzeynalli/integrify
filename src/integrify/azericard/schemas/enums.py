from enum import Enum


class TrType(str, Enum):
    PRE_AUTHORAZATION = '0'
    AUTHORAZATION = '1'
    ACCEPT_REQUEST = '21'
    RETURN_REQUEST = '22'
    CANCEL_REQUEST = '24'


class Action(str, Enum):
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
