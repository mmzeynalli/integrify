from datetime import datetime
from decimal import Decimal
from hashlib import md5
from typing import ClassVar, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.alias_generators import to_pascal
from typing_extensions import Self

from integrify.azericard import env
from integrify.azericard.schemas.enums import (
    Action,
    AuthorizationResponseType,
    AuthorizationType,
    TransferStatusCode,
)
from integrify.azericard.utils import TimeStampIn


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

    trtype: Union[AuthorizationType, AuthorizationResponseType] = Field(
        validation_alias='Original transaction TRTYPE'
    )
    """Orijinal əməliyyat TRTYPE"""

    timestamp: TimeStampIn = Field(validation_alias='Timestamp')
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


class TransferDeclineResponseSchema(BaseModel):
    SIGNATURE_FIELDS: ClassVar[list[str]] = [
        'operation_id',
        'srn',
        'amount',
        'cur',
        'status',
        'timestamp',
        'response_code',
        'message',
    ]
    """Signature hesablanılması üçün lazım olan field adları"""

    model_config = ConfigDict(alias_generator=to_pascal)

    operation_id: str
    """Sorğu əməliyyatının ID-si"""

    srn: str = Field(validation_alias='SRN')
    """Unikal əməliyyat nömrəsi"""

    amount: Optional[Decimal] = None
    """Ödəniş məbləği"""

    cur: Optional[str] = None
    """Ödəniş valyutası"""

    status: Optional[str] = None
    """Status Mesajı"""

    timestamp: Optional[TimeStampIn] = None
    """Sorğunun vaxtı"""

    response_code: Union[TransferStatusCode, int]
    """Uğur(suz)luq kodu"""

    message: str
    """Mesaj"""

    signature: str
    """AzeriCard imzası"""

    @model_validator(mode='after')
    def validate_signature(self) -> Self:
        """AzeriCard-dan gələn signature-ni təsdiqləmə funksiyası"""
        assert self.SIGNATURE_FIELDS

        source = ''
        for field in self.SIGNATURE_FIELDS:
            val = getattr(self, field) or ''
            source += str(val)

        with open(env.AZERICARD_KEY_FILE_PATH, encoding='utf-8') as key_file:
            key = key_file.read()

        source += key

        calc_signature = md5(source.encode('utf-8'), usedforsecurity=False).hexdigest()

        assert calc_signature == self.signature, 'Signature does not match!'

        return self


class TransferConfirmResponseSchema(TransferDeclineResponseSchema):
    SIGNATURE_FIELDS: ClassVar[list[str]] = [
        'operation_id',
        'srn',
        'rrn',
        'amount',
        'cur',
        'receiver_pan',
        'status',
        'timestamp',
        'response_code',
        'message',
    ]
    """Signature hesablanılması üçün lazım olan field adları"""

    rrn: str = Field(validation_alias='RRN')
    """Unikal əməliyyat nömrəsi"""

    receiver_pan: str
    """Maskalanmış kart nömrəsi"""
