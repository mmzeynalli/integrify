from decimal import Decimal

from integrify.epoint.schemas.enums import Code, TransactionStatus, TransactionStatusExtended
from pydantic import BaseModel, field_validator


class MinimalResponseSchema(BaseModel):
    status: TransactionStatus
    """Success və ya failed əməliyyatının nəticəsi"""

    message: str | None = None
    """Ödənişin icra statusu haqqında mesaj"""


class BaseResponseSchema(MinimalResponseSchema):
    # if success
    transaction: str | None = None
    """EPoint xidmətinin əməliyyat IDsi"""

    bank_transaction: str | None = None
    """Bank ödəniş əməliyyatı IDsi"""

    bank_response: str | None = None
    """Ödəniş icrasının nəticəsi ilə bankın cavabı"""

    operation_code: str | None = None
    """001-kart qeydiyyatı\n100- istifadəçi ödənişi"""

    rrn: str | None = None
    """Retrieval Reference Number - unikal əməliyyat identifikatoru.
    Yalnız uğurlu bir əməliyyat üçün mövcuddur"""

    card_mask: str | None = None
    """Ödəniş səhifəsində göstərilən istifadəçi adı"""

    card_name: str | None = None
    """123456******1234 formatında əks edilən kart maskası"""

    amount: Decimal | None = None
    """Ödəniş məbləği"""


class BaseWithCodeSchema(BaseResponseSchema):
    code: str | None = None
    """Bankın 3 rəqəmli cavab kodu."""

    @field_validator('code', mode='before')
    @classmethod
    def code_to_msg(cls, v: str | None = None) -> str | None:
        """3 rəqəmli koddan, xəta/uğur mesajına çevrilir.

        Kod `Code` lüğətində yoxdursa (bank yeni/naməlum kod qaytara bilər),
        `KeyError` atmaq əvəzinə orijinal kod qaytarılır ki, cavab parse-i crash olmasın.
        """
        if not v:
            return None

        return Code.get(v, v)


#################################################################
class RedirectUrlResponseSchema(MinimalResponseSchema):
    # if success
    transaction: str | None = None
    """EPoint xidmətinin əməliyyat IDsi"""

    redirect_url: str | None = None
    """İstifadəçinin kart məlumatlarını daxil etmək üçün yönləndirilməsi lazım olan URL"""


class RedirectUrlWithCardIdResponseSchema(RedirectUrlResponseSchema):
    card_id: str | None = None
    """Ödənişləri yerinə yetirmək üçün istifadə edilməsi
    lazım olan unikal kart identifikatoru"""


class PaymentSchema(BaseWithCodeSchema):
    order_id: str
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: str | None = None
    """Əlavə göndərdiyiniz seçimlər"""


class TransactionStatusResponseSchema(BaseWithCodeSchema):
    status: TransactionStatusExtended
    """Tranzaksiyanın detallı statusu"""

    order_id: str | None = None
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: str | None = None
    """Əlavə göndərdiyiniz seçimlər"""


class SplitPayWithSavedCardResponseSchema(BaseResponseSchema):
    split_amount: Decimal | None = None
    """İkinci istifadəçi üçün ödəniş məbləği."""
