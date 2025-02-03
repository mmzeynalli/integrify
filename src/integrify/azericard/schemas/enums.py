from enum import Enum
from typing import Literal


class TrType(str, Enum):
    PRE_AUTHORAZATION: Literal['0'] = '0'
    AUTHORAZATION: Literal['1'] = '1'
    ACCEPT_REQUEST: Literal['21'] = '21'
    RETURN_REQUEST: Literal['22'] = '22'
    CANCEL_REQUEST: Literal['24'] = '24'
    REQUEST_STATUS: Literal['90'] = '90'

    def __str__(self):
        return self.value


class Action(int, Enum):
    TRANSACTION_SUCCESS: Literal[0] = 0
    """Tranzaksiya uğurla tamamlandı"""

    TRANSACTION_DUPLICATE: Literal[1] = 1
    """Duplikat əməliyyat aşkar edildi"""

    TRANSACTION_CANCELLED: Literal[2] = 2
    """Tranzaksiya rədd edildi"""

    TRANSACTION_PROCESSING_ERROR: Literal[3] = 3
    """Tranzaksiya emal xətası"""

    TRANSACTION_REPEAT_OF_CANCELLED: Literal[6] = 6
    """İmtina edilmiş əməliyyatın təkrarlanması"""

    TRANSACTION_REPEAT_OF_UNAPPROVED: Literal[7] = 7
    """Doğrulama xətası ilə əməliyyatın təkrarlanması"""

    TRANSACTION_REPEAT_OF_UNRESPONDED: Literal[8] = 8
    """Cavab verilmədən dayandırılmış əməliyyatın təkrarlanması"""


class CardStatus(str, Enum):
    ACTIVE: Literal['our_active'] = 'our_active'
    """Kart AzeriCard database-indədir və aktiv statusa malikdir"""

    INACTIVE: Literal['our_inactive'] = 'our_inactive'
    """Kart AzeriCard database-indədir və və qeyri-aktiv statusa malikdir (bloklanmış/müddəti bitmiş və s.)"""  # noqa: E501

    MISSING: Literal['foreign'] = 'foreign'
    """Kart AzeriCard database-ində yoxdur"""
