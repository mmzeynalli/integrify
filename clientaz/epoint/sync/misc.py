"""Qeyri-ödəniş sorğular (status və kart yadda saxlama) (sync)"""

from clientaz.epoint.schemas.request import EPointDecodedCallbackDataSchema
from clientaz.epoint.schemas.response import EPointRedirectUrlResponseSchema
from clientaz.epoint.sync.base import EPointRequest


class EPointGetTransactionStatusRequest(EPointRequest[EPointDecodedCallbackDataSchema]):
    """Transaksiya statusunu öyrənmək üçün sorğu (sync)

    Example:
        >>> EPointGetTransactionStatusRequest(transaction_id='texxxxxx')()

    Cavab sorğu formatı: EPointDecodedCallbackDataSchema
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


class EPointSaveCardRequest(EPointRequest[EPointRedirectUrlResponseSchema]):
    """Ödəniş olmadan kartı yadda saxlamaq sorğusu (sync)

    Example:
        >>> EPointSaveCardRequest()()

    Cavab sorğu formatı: EPointRedirectUrlResponseSchema

    Axın:
        Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
        Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
        backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
        və eyni `card_id` ilə EPointDecodedCallbackDataSchema formatında məlumat gəlir.
    """

    def __init__(self):
        super().__init__()
        self.path = '/api/1/card-registration'
        self.verb = 'POST'
