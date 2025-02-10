from datetime import datetime
from decimal import Decimal
from typing import Union

from pydantic import BaseModel, Field, field_validator

from integrify.azericard.schemas.enums import Action, TrType


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
    def validate_timestamp(cls, val: Union[datetime, str]) -> datetime:
        """İnput string dəyərdirsə, datetime obyektinə çevirən funksiya"""
        if isinstance(val, datetime):
            return val

        return datetime.strptime(val, '%Y%m%d%H%M%S')
