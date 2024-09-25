"""Qeyri-ödəniş sorğular (status və kart yadda saxlama) (sync)"""

from integrify.epoint.schemas.types import (
    RedirectUrlWithCardIdResponseSchema,
    TransactionStatusResponseSchema,
)
from integrify.epoint.sync.base import Request


class GetTransactionStatusRequest(Request[TransactionStatusResponseSchema]):
    """Transaksiya statusunu öyrənmək üçün sorğu (sync)

    Example:
        >>> GetTransactionStatusRequest(transaction_id='texxxxxx')()

    Cavab formatı: :class:`TransactionStatusResponseSchema`
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


class SaveCardRequest(Request[RedirectUrlWithCardIdResponseSchema]):
    """Ödəniş olmadan kartı yadda saxlamaq sorğusu (sync)

    Example:
        >>> SaveCardRequest()()

    Cavab formatı: :class:`RedirectUrlWithCardIdResponseSchema`

    Axın:
    -----------------------------------------------------------------------------------
        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə DecodedCallbackDataSchema formatında məlumat gəlir.
    """

    def __init__(self):
        super().__init__()
        self.path = '/api/1/card-registration'
        self.verb = 'POST'
