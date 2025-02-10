import base64
import hashlib
import hmac
import json
from datetime import datetime
from decimal import Decimal
from hashlib import md5
from typing import Any, ClassVar, Literal, Optional, Union

from pydantic import (
    AliasGenerator,
    ConfigDict,
    Field,
    ValidationInfo,
    computed_field,
    field_serializer,
    field_validator,
)
from pydantic.alias_generators import to_pascal
from pydantic_core import PydanticUndefined
from typing_extensions import TypedDict

from integrify.azericard import env
from integrify.azericard.schemas.common import (
    AzeriCardMinimalDataSchema,
    AzeriCardMinimalWithAmountDataSchema,
)
from integrify.azericard.schemas.enums import TrType
from integrify.schemas import PayloadBaseModel


class BaseRequestSchema(PayloadBaseModel):
    PSIGN_FIELDS: ClassVar[list[str]]
    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=str.upper))

    @computed_field
    def p_sign(self) -> Optional[str]:
        """P_SIGN generasiyası"""
        if not self.PSIGN_FIELDS:
            return None  # pragma: no cover

        with open(env.AZERICARD_KEY_FILE_PATH, encoding='utf-8') as key_file:
            key = key_file.read()

        mac_source = self.generate_mac_source()
        return hmac.new(key.encode('utf-8'), mac_source.encode('utf-8'), hashlib.sha256).hexdigest()

    def generate_mac_source(self):
        """P_SIGN üçün MAC source-un yaradılması"""
        source = ''
        for field in self.PSIGN_FIELDS:
            val = getattr(self, field)

            if val:
                source += str(len(str(val))) + str(val)
            else:
                # So far, no case can reach this state
                source += '-'  # pragma: no cover

        return source

    @field_validator('p_sign', mode='before')
    @classmethod
    def set_if_none(cls, v: Any, info: ValidationInfo):
        """If `None` is set, return default value for that field"""
        if (
            info.field_name
            and not cls.model_fields[info.field_name].is_required()
            and cls.model_fields[info.field_name].get_default() is not PydanticUndefined
            and v is None
        ):
            return cls.model_fields[info.field_name].get_default()

        return v


class MobilePhone(TypedDict):
    cc: str
    subscriber: str


class MInfo(TypedDict):
    browserScreenHeight: str
    browserScreenWidth: str
    browserTZ: str
    mobilePhone: MobilePhone


class AuthRequestSchema(BaseRequestSchema, AzeriCardMinimalWithAmountDataSchema):
    PSIGN_FIELDS: ClassVar[list[str]] = [
        'amount',
        'currency',
        'terminal',
        'trtype',
        'timestamp',
        'nonce',
        'merch_url',
    ]

    # Next three fields can be set either through
    # functions or environment, but they MUST be set
    desc: str = Field(default=env.AZERICARD_MERCHANT_NAME, min_length=1, max_length=50)  # type: ignore[assignment]
    merch_name: str = Field(default=env.AZERICARD_MERCHANT_NAME, min_length=1, max_length=50)  # type: ignore[assignment]
    merch_url: str = Field(default=env.AZERICARD_MERCHANT_URL, min_length=1, max_length=250)  # type: ignore[assignment]

    email: Optional[str] = Field(default=env.AZERICARD_MERCHANT_EMAIL, max_length=80)
    country: Optional[str] = Field(None, max_length=2)
    merch_gmt: Optional[str] = Field(None, min_length=1, max_length=5)
    backref: str = Field(default=env.AZERICARD_CALLBACK_URL, min_length=1, max_length=250)  # type: ignore[assignment]
    lang: str = Field(default=env.AZERICARD_INTERFACE_LANG, min_length=2, max_length=2)
    name: Optional[str] = Field(None, min_length=2, max_length=45)
    m_info: Optional[MInfo] = None

    @field_serializer('m_info')
    def serialize_minfo_to_b64(self, m_info: Optional[MInfo]):
        """M_INFO dcit-ini base64 encodelaşdırılması"""
        if not m_info:
            return None

        return base64.b64encode(json.dumps(m_info).encode()).decode()

    @classmethod
    def get_input_fields(cls):
        return [
            'amount',
            'currency',
            'order',
            'desc',
            'trtype',
            'merch_name',
            'merch_url',
            'terminal',
            'email',
            'country',
            'merch_gmt',
            'backref',
            'timestamp',
            'lang',
            'name',
            'm_info',
        ]


class AuthConfirmRequestSchema(BaseRequestSchema, AzeriCardMinimalWithAmountDataSchema):
    PSIGN_FIELDS: ClassVar[list[str]] = [
        'amount',
        'currency',
        'terminal',
        'trtype',
        'order',
        'rrn',
        'int_ref',
    ]

    rrn: str = Field(min_length=12, max_length=12)
    """Müştəri bankının axtarış istinad nömrəsi (ISO-8583 Sahə 37)"""

    int_ref: str = Field(min_length=1, max_length=128)
    """Elektron ticarət şlüzünün daxili istinad nömrəsi"""

    @classmethod
    def get_input_fields(cls):
        return [
            'amount',
            'currency',
            'order',
            'rrn',
            'int_ref',
            'trtype',
            'terminal',
            'timestamp',
        ]


class AuthAndSaveCardRequestSchema(AuthRequestSchema):
    token_action: Literal['REGISTER'] = 'REGISTER'


class AuthWithSavedCardRequestSchema(AuthRequestSchema):
    token: str = Field(min_length=28, max_length=28)

    @classmethod
    def get_input_fields(cls):
        return [
            'amount',
            'currency',
            'order',
            'desc',
            'trtype',
            'token',
            'merch_name',
            'merch_url',
            'terminal',
            'email',
            'country',
            'merch_gmt',
            'backref',
            'timestamp',
            'lang',
            'name',
            'm_info',
        ]


class GetTransactionStatusRequestSchema(BaseRequestSchema, AzeriCardMinimalDataSchema):
    PSIGN_FIELDS: ClassVar[list[str]] = [
        'order',
        'terminal',
        'trtype',
        'timestamp',
        'nonce',
    ]
    tran_trtype: TrType = Field(min_length=1, max_length=2)
    trtype: Literal[TrType.REQUEST_STATUS] = TrType.REQUEST_STATUS

    @classmethod
    def get_input_fields(cls):
        return ['tran_trtype', 'order', 'terminal', 'timestamp']


class BaseTransferRequestSchema(PayloadBaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=to_pascal))

    merchant: str = Field(min_length=1, max_length=16)
    """Şirkət adı"""

    srn: str = Field(min_length=1, max_length=12)
    """Tərəfinizdən unikal əməliyyat nömrəsi"""

    amount: Decimal
    """Ödəniş məbləği"""

    cur: str = Field(min_length=3, max_length=3)
    """Ödəniş valyutasının 3 rəqəmli kodu (AZN - 944)"""


class StartTransferRequestSchema(BaseTransferRequestSchema):
    receiver_credentials: str = Field(max_length=151)
    """İstifadəçinin tam adı"""

    redirect_link: str = Field(max_length=12)
    """Əməliyyatın sonunda müştərini yönləndirmək istədiyiniz keçid"""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def signature(self) -> str:
        """Yaradılmış data üçün signature generasiyası"""
        with open(env.AZERICARD_KEY_FILE_PATH, encoding='utf-8') as key_file:
            key = key_file.read()

        return md5(
            str(
                self.merchant
                + self.srn
                + str(self.amount)
                + self.cur
                + self.receiver_credentials
                + self.redirect_link
                + key
            ).encode('utf-8')
        ).hexdigest()


class ConfirmTransferRequestSchema(BaseTransferRequestSchema):
    timestamp: str = Field(default_factory=datetime.now, validate_default=True)  # type: ignore[assignment]

    @field_validator('timestamp', mode='before')
    @classmethod
    def format_timestamp(cls, timestamp: Union[datetime, str]) -> str:
        """Serialize etdikdə timestamp-i AzeriCard formatına salan funksiya"""

        if isinstance(timestamp, datetime):
            return timestamp.strftime('%Y%m%d%H%M%S')

        return timestamp
