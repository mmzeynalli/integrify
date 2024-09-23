"""Qeyri-ödəniş sorğular (status və kart yadda saxlama) (sync)"""

from integrify.epoint.schemas.types import (
    EPointRedirectUrlWithCardIdResponseSchema,
    EPointTransactionStatusResponseSchema,
)
from integrify.epoint.sync.base import EPointRequest


class EPointGetTransactionStatusRequest(EPointRequest[EPointTransactionStatusResponseSchema]):
    """Transaksiya statusunu öyrənmək üçün sorğu (sync)

    Example:
        >>> EPointGetTransactionStatusRequest(transaction_id='texxxxxx')()

    Cavab formatı: :class:`EPointTransactionStatusResponseSchema`
    """

    def __init__(self, transaction_id: str):
        """
        Args:
            transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                            Adətən `te` prefiksi ilə olur.
        """
        super().__init__()
        self.verb = 'POST'
        self.path = '/api/1/get-status'
        self.data['transaction'] = transaction_id


class EPointSaveCardRequest(EPointRequest[EPointRedirectUrlWithCardIdResponseSchema]):
    """Ödəniş olmadan kartı yadda saxlamaq sorğusu (sync)

    Example:
        >>> EPointSaveCardRequest()()

    Cavab formatı: :class:`EPointRedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.
    """

    def __init__(self):
        super().__init__()
        self.path = '/api/1/card-registration'
        self.verb = 'POST'
