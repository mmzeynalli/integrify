import base64
import json
from functools import cache
from typing import ClassVar, Literal

import rsa
from integrify.azericard import env
from integrify.azericard.schemas.common import (
    AzeriCardMinimalDataSchema,
    AzeriCardMinimalWithAmountDataSchema,
)
from integrify.azericard.schemas.enums import (
    AuthorizationMiscType,
    AuthorizationResponseType,
    AuthorizationType,
)
from integrify.schemas import PayloadBaseModel
from pydantic import (
    AliasGenerator,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
)
from typing_extensions import TypedDict


@cache
def _load_private_key(key_file_path: str) -> rsa.PrivateKey:
    """RSA private key-i fayldan oxuyub cache-ləyən funksiya.

    Əvvəllər hər sorğuda fayl oxunub parse olunurdu; indi eyni fayl yolu üçün bir dəfə
    oxunur. Nəticə eynidir (deterministik), lakin hər sorğuda disk I/O aradan qalxır.
    """
    with open(key_file_path, 'rb') as key_file:
        return rsa.PrivateKey.load_pkcs1(key_file.read())


class BaseRequestSchema(PayloadBaseModel):
    SIGNATURE_FIELDS: ClassVar[list[str]]
    """P_SIGN hesablanılması üçün lazım olan field adları"""

    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=str.upper))

    @computed_field
    def p_sign(self) -> str | None:
        """P_SIGN generasiyası"""
        if not self.SIGNATURE_FIELDS:
            return None  # pragma: no cover

        private_key = _load_private_key(env.AZERICARD_KEY_FILE_PATH)

        mac_source = self.generate_mac_source().encode('utf-8')
        return rsa.sign(mac_source, private_key, 'SHA-256').hex()

    def generate_mac_source(self):
        """P_SIGN üçün MAC source-un yaradılması"""
        source = ''
        for field in self.SIGNATURE_FIELDS:
            val = getattr(self, field)

            if val:
                source += str(len(str(val))) + str(val)
            else:
                # So far, no case can reach this state
                source += '-'  # pragma: no cover

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
    SIGNATURE_FIELDS: ClassVar[list[str]] = [
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
    desc: str = Field(default=env.AZERICARD_MERCHANT_NAME, min_length=1, max_length=50)
    merch_name: str = Field(default=env.AZERICARD_MERCHANT_NAME, min_length=1, max_length=50)
    merch_url: str = Field(default=env.AZERICARD_MERCHANT_URL, min_length=1, max_length=250)

    email: str | None = Field(default=env.AZERICARD_MERCHANT_EMAIL, max_length=80)
    country: str | None = Field(None, max_length=2)
    merch_gmt: str | None = Field(None, min_length=1, max_length=5)
    backref: str = Field(default=env.AZERICARD_CALLBACK_URL, min_length=1, max_length=250)
    lang: str = Field(default=env.AZERICARD_INTERFACE_LANG, min_length=2, max_length=2)
    name: str | None = Field(None, min_length=2, max_length=45)
    m_info: MInfo | None = None

    @field_serializer('m_info')
    def serialize_minfo_to_b64(self, m_info: MInfo | None):
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
    SIGNATURE_FIELDS: ClassVar[list[str]] = [
        'order',
        'amount',
        'currency',
        'terminal',
        'trtype',
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
            'order',
            'amount',
            'currency',
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
    SIGNATURE_FIELDS: ClassVar[list[str]] = [
        'order',
        'terminal',
        'trtype',
        'timestamp',
        'nonce',
    ]
    tran_trtype: AuthorizationType | AuthorizationResponseType = Field(
        min_length=1,
        max_length=2,
    )
    trtype: Literal[AuthorizationMiscType.REQUEST_STATUS] = AuthorizationMiscType.REQUEST_STATUS

    @classmethod
    def get_input_fields(cls):
        return ['tran_trtype', 'order', 'terminal', 'timestamp']
