from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator

from integrify.epoint.schemas.enums import (
    Code,
    TransactionStatus,
    TransactionStatusExtended,
)


class MinimalResponseSchema(BaseModel):
    status: TransactionStatus
    """Success və ya failed əməliyyatının nəticəsi"""

    message: Optional[str] = None
    """Ödənişin icra statusu haqqında mesaj"""


class BaseResponseSchema(MinimalResponseSchema):
    # if success
    transaction: Optional[str] = None
    """EPoint xidmətinin əməliyyat IDsi"""

    bank_transaction: Optional[str] = None
    """Bank ödəniş əməliyyatı IDsi"""

    bank_response: Optional[str] = None
    """Ödəniş icrasının nəticəsi ilə bankın cavabı"""

    operation_code: Optional[str] = None
    """001-kart qeydiyyatı\n100- istifadəçi ödənişi"""

    rrn: Optional[str] = None
    """Retrieval Reference Number - unikal əməliyyat identifikatoru.
    Yalnız uğurlu bir əməliyyat üçün mövcuddur"""

    card_mask: Optional[str] = None
    """Ödəniş səhifəsində göstərilən istifadəçi adı"""

    card_name: Optional[str] = None
    """123456******1234 formatında əks edilən kart maskası"""

    amount: Optional[Decimal] = None
    """Ödəniş məbləği"""


class BaseWithCodeSchema(BaseResponseSchema):
    code: Optional[str] = None
    """Bankın cavab kodu. 3 rəqəmli koddan, xəta/uğur mesajına çevrilir."""

    @field_validator('code', mode='before')
    @classmethod
    def code_to_msg(cls, v: Optional[str] = None):
        return Code[v] if v else None


#################################################################
class RedirectUrlResponseSchema(MinimalResponseSchema):
    # if success
    transaction: Optional[str] = None
    """EPoint xidmətinin əməliyyat IDsi"""

    redirect_url: Optional[str] = None
    """İstifadəçinin kart məlumatlarını daxil etmək üçün yönləndirilməsi lazım olan URL"""


class RedirectUrlWithCardIdResponseSchema(RedirectUrlResponseSchema):
    card_id: Optional[str] = None
    """Ödənişləri yerinə yetirmək üçün istifadə edilməsi
    lazım olan unikal kart identifikatoru"""


class PaymentSchema(BaseWithCodeSchema):
    order_id: str
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: Optional[str] = None
    """Əlavə göndərdiyiniz seçimlər"""


class TransactionStatusResponseSchema(BaseWithCodeSchema):
    status: TransactionStatusExtended  # type: ignore[assignment]
    """Tranzaksiyanın detallı statusu"""

    order_id: Optional[str] = None
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: Optional[str] = None
    """Əlavə göndərdiyiniz seçimlər"""


class SplitPayWithSavedCardResponseSchema(BaseResponseSchema):
    split_amount: Optional[Decimal] = None
    """İkinci istifadəçi üçün ödəniş məbləği."""
