from typing import Generic, Optional

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from integrify.payriff.schemas.enums import ResultCodes
from integrify.payriff.schemas.utils import BaseSchema, _ResponsePayloadT
from integrify.schemas import PayloadBaseModel


class BaseResponseSchema(PayloadBaseModel, BaseSchema, Generic[_ResponsePayloadT]):
    model_config = ConfigDict(alias_generator=to_camel)

    code: ResultCodes
    """Cavab kodu"""
    message: str
    """Cavab mesajı"""
    route: str
    """Route"""
    response_id: str
    """Cavab ID"""
    internal_message: Optional[str] = None
    """Daxili mesaj"""
    payload: _ResponsePayloadT
    """Payload"""
