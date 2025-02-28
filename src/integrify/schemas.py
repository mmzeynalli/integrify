import json
from typing import Any, ClassVar, Generic, TypedDict, Union

from pydantic import BaseModel, Field, field_validator

from integrify.utils import _ResponseT


class APIResponse(BaseModel, Generic[_ResponseT]):
    """Cavab sorğu base payload tipi. Generic tip-i qeyd etmıəklə
    sorğu cavabını validate edə bilərsiniz.
    """

    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: _ResponseT = Field(validation_alias='content')
    """Cavab sorğusunun body-si"""

    @field_validator('body', mode='before')
    @classmethod
    def convert_to_dict(cls, v: Union[str, bytes]):
        """Binary content-i dict-ə çevirərək, validation-a hazır vəziyyətə gətirir."""
        return json.loads(v)


class DryResponse(TypedDict):
    """Dry-run sorğularının `return` tipi"""

    url: str
    """Sorğu göndəriləcək url"""

    verb: str
    """Sorğu metodu (GET, POST və s.)"""

    headers: dict[str, str]
    """Sorğu header-ləri"""

    data: dict[str, Any]
    """Sorğu data-sı (body-si)"""

    request_args: dict[str, Any]
    """httpx.request funksiyasına ötürülən parametrlər"""


class PayloadBaseModel(BaseModel):
    URL_PARAM_FIELDS: ClassVar[set[str]] = set()

    @classmethod
    def from_args(cls, *args, **kwds):
        """Verilən `*args` və `**kwds` (və ya `**kwargs`) parametrlərini birləşdirərək
        Pydantic validasiyası edən funksiya. Positional arqumentlər üçün (`*args`) Pydantic
        modelindəki field-lərin ardıcıllığı və çağırılan funksiyada parametrlərinin ardıcıllığı
        EYNİ OLMALIDIR, əks halda, bu method yararsızdır.
        """
        return cls.model_validate({**dict(zip(cls.model_fields.keys(), args)), **kwds})
