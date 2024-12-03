import base64
import hashlib
import hmac
import json
from typing import ClassVar, Literal, Optional, Set, TypedDict

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, computed_field, field_serializer

from integrify.azericard import env
from integrify.azericard.schemas.common import (
    AzeriCardMinimalDataSchema,
    AzeriCardMinimalWithAmountDataSchema,
)
from integrify.azericard.schemas.enums import TrType


class BaseRequestSchema(BaseModel):
    PSIGN_FIELDS: ClassVar[Set[str]]
    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=str.upper))

    @computed_field
    def p_sign(self) -> Optional[str]:
        """P_SIGN generasiyası"""
        if not self.PSIGN_FIELDS:
            return None

        with open(env.AZERICARD_KEY_FILE_PATH, encoding='utf-8') as key_file:
            key = key_file.read()

        mac_source = self.generate_mac_source()
        return hmac.new(key.encode('utf-8'), mac_source.encode('utf-8'), hashlib.sha256).hexdigest()

    def generate_mac_source(self):
        """P_SIGN üçün MAC source-un yaradılması"""
        source = ''
        for field in self.PSIGN_FIELDS:
            val = getattr(self, field)
            assert val
            source += str(len(val)) + str(val)

        return source


class MobilePhone(TypedDict):
    cc: str
    subscriber: str


class MInfo(TypedDict):
    browserScreenHeight: str
    browserScreenWidth: str
    browserTZ: str
    mobilePhone: MobilePhone


class AuthRequestSchema(BaseRequestSchema, AzeriCardMinimalWithAmountDataSchema):
    PSIGN_FIELDS: ClassVar[Set[str]] = {
        'amount',
        'currency',
        'terminal',
        'trtype',
        'timestamp',
        'nonce',
        'merch_url',
    }

    # Next three fields can be set either through
    # functions or environment, but they MUST be set
    desc: str = Field(default=env.AZERICARD_MERCHANT_NAME, min_length=1, max_length=50)  # type: ignore[assignment]
    merch_name: str = Field(default=env.AZERICARD_MERCHANT_NAME, min_length=1, max_length=50)  # type: ignore[assignment]
    merch_url: str = Field(default=env.AZERICARD_MERCHANT_URL, min_length=1, max_length=250)  # type: ignore[assignment]

    email: Optional[str] = Field(..., max_length=80)
    country: Optional[str] = Field(..., max_length=2)
    merch_gmt: Optional[str] = Field(..., min_length=1, max_length=5)
    backref: str = Field(min_length=1, max_length=250)
    lang: str = Field(min_length=2, max_length=2)
    name: str = Field(min_length=2, max_length=45)
    m_info: Optional[MInfo] = None

    @field_serializer('m_info')
    def serialize_minfo_to_b64(self, m_info: Optional[MInfo]):
        """M_INFO dcit-ini base64 encodelaşdırılması"""
        if not m_info:
            return None

        return base64.b64encode(json.dumps(m_info).encode()).decode()


class AuthConfirmRequestSchema(BaseRequestSchema, AzeriCardMinimalWithAmountDataSchema):
    PSIGN_FIELDS: ClassVar[Set[str]] = {
        'amount',
        'currency',
        'terminal',
        'trtype',
        'order',
        'rrn',
        'int_ref',
    }

    rrn: str = Field(min_length=12, max_length=12)
    """Müştəri bankının axtarış istinad nömrəsi (ISO-8583 Sahə 37)"""

    int_ref: str = Field(min_length=1, max_length=128)
    """Elektron ticarət şlüzünün daxili istinad nömrəsi"""


class PayAndSaveCardRequestSchema(AuthRequestSchema):
    token_action: Literal['REGISTER']


class PayWithSavedCardRequestSchema(AuthRequestSchema):
    token: str = Field(min_length=28, max_length=28)


class GetTransactionStatusRequestSchema(BaseRequestSchema, AzeriCardMinimalDataSchema):
    PSIGN_FIELDS: ClassVar[Set[str]] = {
        'order',
        'terminal',
        'trtype',
        'timestamp',
        'nonce',
    }
    tran_trtype: TrType = Field(min_length=1, max_length=2)
    trtype: Literal[TrType.REQUEST_STATUS]
