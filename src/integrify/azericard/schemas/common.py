import random
from datetime import datetime
from decimal import Decimal
from typing import Union

from pydantic import BaseModel, Field, field_validator

from integrify.azericard import env
from integrify.azericard.schemas.enums import TrType


class AzeriCardMinimalDataSchema(BaseModel):
    order: str = Field(min_length=6, max_length=32)
    """Satıcı sifariş ID-si, rəqəmsal. Son 6 rəqəm sistem izi audit nömrəsi kimi istifadə olunur,
    terminal id üçün bir gün ərzində unikal olmalıdır"""

    terminal: str = Field(default=env.AZERICARD_MERCHANT_ID)  # type: ignore[assignment]
    """Bank tərəfindən təyin edilmiş Merchant Terminal ID"""

    trtype: TrType = Field(min_length=1, max_length=2)
    """Tranzaksiya növü = 0 (Pre-Avtorizasiya əməliyyatı),
    Tranzaksiya növü = 1 (Avtorizasiya əməliyyatı)"""

    timestamp: str = Field(default_factory=datetime.now, validate_default=True)  # type: ignore[assignment]
    """GMT-də e-ticarət şlüzünün vaxt damğası: YYYYMMDDHHMMSS"""

    nonce: str = Field(
        default_factory=lambda: f'{random.getrandbits(128):0>16X}',
        min_length=8,
        max_length=32,
    )
    """E-Commerce Gateway qeyri-dəyərlidir. Hexadecimal formatda 8-32
    təsadüfi baytla doldurulacaq. MAC istifadə edildikdə mövcud olacaq."""

    @field_validator('timestamp', mode='before')
    @classmethod
    def validate_timestamp(cls, val: Union[datetime, str, None]) -> str:
        """Input string dəyərdirsə, datetime obyektinə çevirən funksiya"""

        if val is None:
            return datetime.now().strftime('%Y%m%d%H%M%S')

        if isinstance(val, datetime):
            return val.strftime('%Y%m%d%H%M%S')

        return val


class AzeriCardMinimalWithAmountDataSchema(AzeriCardMinimalDataSchema):
    amount: Decimal
    """Sifarişin ümumi məbləği"""

    currency: str = Field(min_length=1, max_length=3)
    """Sifariş valyutası: 3 simvollu valyuta kodu"""
