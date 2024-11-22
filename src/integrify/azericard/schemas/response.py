from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, field_validator

from integrify.azericard.schemas.common import AzeriCardMinimalDataSchema
from integrify.azericard.schemas.enums import Action, TrType


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=str.upper))


class AuthResponseSchema(BaseResponseSchema, AzeriCardMinimalDataSchema):
    action: Action
    """EGateway fəaliyyət kodu"""

    rc: str = Field(min_length=2, max_length=2)
    """Əməliyyat cavab kodu (ISO-8583 Sahə 39)"""

    approval: Optional[str] = Field(..., min_length=6, max_length=6)
    """Müştəri bankının təsdiq kodu (ISO-8583 Sahə 38). Kart idarəetmə sistemi
    tərəfindən təmin edilmədikdə boş ola bilər."""

    rrn: str = Field(min_length=12, max_length=12)
    """Müştəri bankının axtarış istinad nömrəsi (ISO-8583 Sahə 37)"""

    int_ref: str = Field(min_length=1, max_length=128)
    """Elektron ticarət şlüzünün daxili istinad nömrəsi"""

    p_sign: str = Field(min_length=1, max_length=256)
    """16-lıq formatda Merchant MAC"""


class GetTransactionStatusResponseSchema(BaseModel):
    action: Action = Field(validation_alias='ACTION')
    """Sorğu üçün orijinal əməliyyat"""

    rc: str = Field(validation_alias='Response code')
    """Sorğu üçün orijinal əməliyyat kodu (ISO-8583 Sahə 39)"""

    status_message: str = Field(validation_alias='Transaction Status message')
    """Orijinal əməliyyat statusu mesajı"""

    terminal: str = Field(validation_alias='TERMINAL')
    """Orijinal əməliyyat Terminal ID"""

    card_number: str = Field(validation_alias='Card number')
    """Orijinal əməliyyat maskalı kart nömrəsi"""

    amount: Decimal = Field(validation_alias='Transaction amount')
    """Orijinal əməliyyat məbləği"""

    currency: str = Field(validation_alias='Transaction currency')
    """Orijinal əməliyyat valyutası"""

    date: datetime = Field(validation_alias='Transaction date')
    """Orijinal əməliyyat tarixi"""

    state: str = Field(validation_alias='Transaction state')
    """Orijinal əməliyyat vəziyyəti"""

    order: str = Field(validation_alias='Merchant order id')
    """Orijinal əməliyyat ORDER ID-si"""

    approval: str = Field(validation_alias='Banks approval code')
    """Orijinal əməliyyatın təsdiq kodu"""

    rrn: str = Field(validation_alias='Transaction RRN')
    """Orijinal əməliyyat RRN"""

    int_ref: str = Field(validation_alias='INT_REF')
    """Orijinal əməliyyat INT_REF"""

    trtype: TrType = Field(validation_alias='Original transaction TRTYPE')
    """Orijinal əməliyyat TRTYPE"""

    timestamp: datetime = Field(validation_alias='Timestamp')
    """Sorğunun vaxtı"""

    nonce: str = Field(validation_alias='Nonce')
    """Orijinal əməliyyat Nonce"""

    p_sign: str = Field(validation_alias='P_SIGN')
    """16-lıq formada E-Commerce Gateway MAC (Message Authentication Code).
    MAC istifadə edilərsə mövcud olacaq."""

    @field_validator('timestamp', 'date', mode='before')
    @classmethod
    def validate_timestamp(cls, val: datetime | str) -> datetime:
        if isinstance(val, datetime):
            return val

        return datetime.strptime(val, '%Y%m%d%H%M%S')
