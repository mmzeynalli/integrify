import base64
import json
from typing import NamedTuple, Optional

from pydantic import AliasGenerator, ConfigDict, Field, field_serializer

from integrify.azericard.schemas.common import AzeriCardDataSchema


class MobilePhone(NamedTuple):
    cc: str
    subscriber: str


class MInfo(NamedTuple):
    browserScreenHeight: str
    browserScreenWidth: str
    browserTZ: str
    mobilePhone: MobilePhone


class AuthRequestSchema(AzeriCardDataSchema):
    model_config = ConfigDict(alias_generator=AliasGenerator(serialization_alias=str.upper))

    desc: str = Field(min_length=1, max_length=50)
    merch_name: str = Field(min_length=1, max_length=50)
    merch_url: str = Field(min_length=1, max_length=250)
    email: Optional[str] = Field(..., max_length=80)
    country: Optional[str] = Field(..., max_length=2)
    merch_gmt: Optional[str] = Field(..., min_length=1, max_length=5)
    backref: str = Field(min_length=1, max_length=250)
    lang: str = Field(min_length=2, max_length=2)
    name: str = Field(min_length=2, max_length=45)
    m_info: Optional[MInfo] = None

    @field_serializer('m_info')
    def serialize_minfo_to_b64(self, m_info: Optional[MInfo]):
        if not m_info:
            return None

        return base64.b64encode(json.dumps(m_info._asdict()).encode()).decode()
