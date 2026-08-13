from decimal import Decimal
from hashlib import md5
from typing import ClassVar

from pydantic import AliasGenerator, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_pascal

from integrify.azericard import env
from integrify.azericard.utils import TimeStampOut
from integrify.schemas import PayloadBaseModel


class BaseTransferRequestSchema(PayloadBaseModel):
    SIGNATURE_FIELDS: ClassVar[list[str]]
    """Signature hesablanılması üçün lazım olan field adları"""

    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=to_pascal))

    merchant: str = Field(min_length=1, max_length=16)
    """Şirkət adı"""

    srn: str = Field(min_length=1, max_length=12, serialization_alias='SRN')
    """Tərəfinizdən unikal əməliyyat nömrəsi"""

    amount: Decimal
    """Ödəniş məbləği"""

    cur: str = Field(min_length=3, max_length=3)
    """Ödəniş valyutasının 3 rəqəmli kodu (AZN - 944)"""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def signature(self) -> str:
        """Yaradılmış data üçün signature generasiyası"""
        assert self.SIGNATURE_FIELDS

        with open(env.AZERICARD_KEY_FILE_PATH, encoding='utf-8') as key_file:
            key = key_file.read().replace('\n', '')

        source = ''
        for field in self.SIGNATURE_FIELDS:
            source += str(getattr(self, field))

        source += key

        return md5(source.encode('utf-8'), usedforsecurity=False).hexdigest()


class TransferStartRequestSchema(BaseTransferRequestSchema):
    SIGNATURE_FIELDS: ClassVar[list[str]] = [
        'merchant',
        'srn',
        'amount',
        'cur',
        'receiver_credentials',
        'redirect_link',
    ]

    receiver_credentials: str = Field(max_length=151)
    """İstifadəçinin tam adı"""

    redirect_link: str = Field(max_length=12)
    """Əməliyyatın sonunda müştərini yönləndirmək istədiyiniz keçid"""


class TransferConfirmDeclineRequestSchema(BaseTransferRequestSchema):
    SIGNATURE_FIELDS: ClassVar[list[str]] = ['merchant', 'srn', 'amount', 'cur', 'timestamp']

    timestamp: TimeStampOut
