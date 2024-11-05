from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from integrify.azericard import env
from integrify.azericard.schemas.enums import TrType


class AzeriCardDataSchema(BaseModel):
    amount: Decimal
    """Sifarişin ümumi məbləği"""

    currency: str = Field(min_length=1, max_length=3)
    """Sifariş valyutası: 3 simvollu valyuta kodu"""

    order: str = Field(min_length=6, max_length=32)
    """Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur,
    terminal id üçün bir gün ərzində unikal olmalıdır"""

    terminal: Optional[str] = env.AZERICARD_MERCHANT_ID
    """Bank tərəfindən təyin edilmiş Merchant Terminal ID"""

    trtype: TrType = Field(min_length=1, max_length=1)
    """Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),
    Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)"""

    timestamp: str = Field(min_length=14, max_length=14)
    """GMT-də e-ticarət şlüzünün vaxt damğası:: YYYYMMDDHHMMSS"""

    nonce: str = Field(min_length=1, max_length=64)
    """E-Commerce Gateway qeyri-dəyərlidir. Hexadecimal formatda 8-32
    təsadüfi baytla doldurulacaq. MAC istifadə edildikdə mövcud olacaq."""

    p_sign: str = Field(min_length=1, max_length=256)
    """16-lıq formatda Merchant MAC"""
