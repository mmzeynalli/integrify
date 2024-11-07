from typing import ClassVar, Generic, TypeVar, Union

from pydantic import BaseModel, Field, field_validator

ResponseType = TypeVar('ResponseType', bound=BaseModel)


class APIResponse(BaseModel, Generic[ResponseType]):
    """Cavab sorğu base payload tipi. Generic tip-i qeyd etmıəklə
    sorğu cavabını validate edə bilərsiniz.
    """

    ok: bool = Field(validation_alias='is_success')
    """Cavab sorğusunun statusu 400dən kiçikdirsə"""

    status_code: int
    """Cavab sorğusunun status kodu"""

    headers: dict
    """Cavab sorğusunun header-i"""

    body: ResponseType = Field(validation_alias='content')
    """Cavab sorğusunun body-si"""

    @field_validator('body', mode='before')
    def convert_to_dict(cls, v: Union[str, bytes]) -> dict:
        """Binary content-i dict-ə çevirərək, validation-a hazır vəziyyətə gətirir."""
        import json

        return json.loads(v)


class PayloadBaseModel(BaseModel):
    URL_PARAM_FIELDS: ClassVar[set[str]] = set()

    @classmethod
    def from_args(cls, *args, **kwds):
        """Verilən `*args` və `**kwds` (və ya `**kwargs`) parametrlərini birləşdirərək
        Pydantic validasiyası edən funksiya. Positional arqumentlər üçün (`*args`) Pydantic
        modelindəki field-lərin ardıcıllığı və çağırılan funksiyada parametrlərinin ardıcıllığı
        EYNİ OLMALIDIR, əks halda, bu method yararsızdır.
        """
        return cls.model_validate({**{k: v for k, v in zip(cls.model_fields.keys(), args)}, **kwds})
