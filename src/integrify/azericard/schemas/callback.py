from datetime import datetime
from decimal import Decimal
from hashlib import md5
from typing import Optional, Union

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.alias_generators import to_pascal
from typing_extensions import Self

from integrify.azericard import env
from integrify.azericard.schemas.common import AzeriCardMinimalWithAmountDataSchema
from integrify.azericard.schemas.enums import Action, CardStatus
from integrify.azericard.utils import TimeStampIn


class AuthCallbackSchema(AzeriCardMinimalWithAmountDataSchema):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=str.upper))

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


class AuthCallbackWithCardDataSchema(AuthCallbackSchema):
    card: Optional[str]
    """Masklanmış kart nömrəsi"""

    token: Optional[str]
    """Saxlanılacaq kartın TOKEN parametri"""


class TransferCallbackSchema(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=to_pascal))

    operation_id: str = Field(min_length=16, max_length=20, validation_alias='OperationID')
    """AzeriCard tərəfindən verilmiş unikal əməliyyat nömrəsi"""

    srn: str = Field(min_length=1, max_length=12, validation_alias='SRN')
    """Tərəfinizdən unikal əməliyyat nömrəsi"""

    amount: Decimal
    """Müraciətdən gələn məbləğ"""

    cur: str
    """Sorğunun valyutası yalnız 944 (AZN) olmalıdır"""

    card_status: CardStatus
    """Azericard tərəfində istifadəçi kartı statusu"""

    receiver_pan: str = Field(min_length=16, max_length=16, validation_alias='ReceiverPAN')
    """Maskalı kart nömrəsi"""

    status: str
    """Cari tranzaksiya statusu (məsələn, "pending")"""

    timestamp: TimeStampIn
    """Cavab vaxtı"""

    rc: str = Field(validation_alias='Response Code')
    """Cavab kodu"""

    message: str
    """Cavab mesajı"""

    signature: str
    """Hesablanmış dəyər MD5(Bütün sahələr birləşdirilib + Açar)"""

    @field_validator('timestamp', mode='before')
    @classmethod
    def validate_timestamp(cls, val: Union[datetime, str]) -> datetime:
        """Input string dəyərdirsə, datetime obyektinə çevirən funksiya"""
        if isinstance(val, datetime):
            return val

        return datetime.strptime(val, '%Y%m%d%H%M%S')

    @model_validator(mode='after')
    def validate_signature(self) -> Self:
        """AzeriCard-dan gələn signature-ni təsdiqləmə funksiyası"""
        with open(env.AZERICARD_KEY_FILE_PATH, encoding='utf-8') as key_file:
            key = key_file.read()

        calc_signature = md5(
            str(
                self.operation_id
                + self.srn
                + str(self.amount)
                + self.cur
                + self.card_status
                + self.receiver_pan
                + self.status
                + self.timestamp.strftime('%Y%m%d%H%M%S')
                + self.rc
                + self.message
                + key
            ).encode(),
            usedforsecurity=False,
        ).hexdigest()

        assert calc_signature == self.signature, ' Signature does not match!'

        return self
