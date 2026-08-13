import json
from typing import Any, ClassVar, Generic, Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import TypedDict

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
        """Binary content-i dict-ə çevirərək, validation-a hazır vəziyyətə gətirir.

        Cavab JSON deyilsə (məs., gateway xətası zamanı HTML səhifə və ya boş body),
        `json.loads` xətası atmaq əvəzinə boş dict qaytarılır ki, sorğu axını crash olmasın.
        Bu halda, status kodu və `ok` field-ləri vasitəsilə xətanı öyrənmək olar.
        """
        if isinstance(v, (bytes, bytearray, str)):
            if not v:
                return {}

            try:
                return json.loads(v)
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
                return {}

        return v


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
    def get_input_fields(cls) -> list[str]:
        """Modelin field-lərinin listini almaq"""
        return list(cls.model_fields.keys())

    @classmethod
    def from_args(cls, *args, **kwds):
        """Verilən `*args` və `**kwds` (və ya `**kwargs`) parametrlərini birləşdirərək
        Pydantic validasiyası edən funksiya. Positional arqumentlər üçün (`*args`) Pydantic
        modelindəki field-lərin ardıcıllığı və çağırılan funksiyada parametrlərinin ardıcıllığı
        EYNİ OLMALIDIR, əks halda, bu method yararsızdır.
        """
        fields = cls.get_input_fields()

        if len(args) > len(fields):
            raise TypeError(
                f'{cls.__name__}.from_args() got {len(args)} positional arguments '
                f'but only {len(fields)} are expected'
            )

        positional = dict(zip(fields, args))

        # Eyni field həm positional, həm keyword kimi verilibsə, xəta qaldırırıq
        duplicates = positional.keys() & kwds.keys()
        if duplicates:
            raise TypeError(
                f'{cls.__name__}.from_args() got multiple values for '
                f'argument(s): {", ".join(sorted(duplicates))}'
            )

        return cls.model_validate({**positional, **kwds})
