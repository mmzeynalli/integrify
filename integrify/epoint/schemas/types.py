from decimal import Decimal
from typing import Optional
from urllib.parse import parse_qsl

from pydantic import BaseModel, field_validator, model_validator

from integrify.epoint.schemas.parts import (
    EPointCode,
    EPointTransactionStatus,
    EPointTransctionStatusExtended,
)


class EPointMinimalResponseSchema(BaseModel):
    status: EPointTransactionStatus
    """Success və ya failed əməliyyatının nəticəsi"""

    message: Optional[str] = None
    """Ödənişin icra statusu haqqında mesaj"""


class EPointBaseResponseSchema(EPointMinimalResponseSchema):
    # if success
    transaction: Optional[str] = None
    """Epoint xidmətinin əməliyyat IDsi"""

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


class EPointBaseWithCodeSchema(EPointBaseResponseSchema):
    code: Optional[str] = None
    """Bankın cavab kodu. 3 rəqəmli koddan, xəta/uğur mesajına çevrilir."""

    @field_validator('code', mode='before')
    @classmethod
    def code_to_msg(cls, v: Optional[str] = None):
        return EPointCode[v] if v else None


#################################################################
class EPointRedirectUrlResponseSchema(EPointMinimalResponseSchema):
    # if success
    transaction: Optional[str] = None
    """Epoint xidmətinin əməliyyat IDsi"""

    redirect_url: Optional[str] = None
    """İstifadəçinin kart məlumatlarını daxil etmək üçün yönləndirilməsi lazım olan URL"""


class EPointRedirectUrlWithCardIdResponseSchema(EPointRedirectUrlResponseSchema):
    card_id: Optional[str] = None
    """Ödənişləri yerinə yetirmək üçün istifadə edilməsi
    lazım olan unikal kart identifikatoru"""


class EPointPaymentSchema(EPointBaseWithCodeSchema):
    order_id: str
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: Optional[str] = None
    """Əlavə göndərdiyiniz seçimlər"""


class EPointTransactionStatusResponseSchema(EPointBaseWithCodeSchema):
    status: EPointTransctionStatusExtended  # type: ignore[assignment]
    """Tranzaksiyanın detallı statusu"""

    order_id: Optional[str] = None
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: Optional[str] = None
    """Əlavə göndərdiyiniz seçimlər"""


class EPointSplitPayWithSavedCardResponseSchema(EPointBaseResponseSchema):
    split_amount: Optional[Decimal] = None
    """İkinci istifadəçi üçün ödəniş məbləği."""


#########################################################################
class EPointCallbackDataSchema(BaseModel):
    data: str
    signature: str

    @model_validator(mode='before')
    @classmethod
    def convert_str_to_dict(cls, data: bytes) -> dict:
        return dict(parse_qsl(data.decode()))


class EPointDecodedCallbackDataSchema(EPointBaseWithCodeSchema):
    order_id: Optional[str] = None
    """Tətbiqinizdə unikal əməliyyat ID"""

    card_id: Optional[str] = None
    """Ödənişləri yerinə yetirmək üçün istifadə edilməsi
    lazım olan unikal kart identifikatoru"""

    split_amount: Optional[Decimal] = None
    """İkinci istifadəçi üçün ödəniş məbləği."""

    other_attr: Optional[str] = None
    """Əlavə göndərdiyiniz seçimlər"""
